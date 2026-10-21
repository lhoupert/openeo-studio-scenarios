"""
Exp - NW Med deep winters 2005-2018 low-chl weeks MODIS

In winters with deep convection, cold northerly winds mix the Gulf of Lion from the surface down to 1000 m or more, often to the seafloor. The mixing carries the surface algae (phytoplankton) down into the dark, so from space the mixed area looks like a patch of very low chlorophyll.

This map counts, for each spot of sea, in how many of seven 8-day satellite images (25 Jan-21 Mar) it was clear and inside that patch. One layer per winter with known deep convection (2005, 2006, 2009-2013 and 2018), plus 2007, a winter without it; the same dates and colours for every winter. The map opens on 2013; open one layer at a time.

How to read the colours: dark purple = 5-7 weeks in the patch (the heart of the mixed area); purple = 4; blues = 1-3 (light blue = 1); no colour = never seen in the patch, or land.

Read with care: a cloudy week counts as "not in the patch", so cloudy winters (2018) look smaller. The count mixes how large and how long-lived the patch was: in 2011 the sea mixed early and the patch had broken up by mid-February.

Method, sources and caveats: openeo-studio-scenarios, scenarios/nw-med-deep-winters/low-chl-weeks/README.md

MODIS-Aqua surface reflectance (MYD09A1 v6.1, NASA LP DAAC), via Microsoft Planetary Computer.
"""
import math
from datetime import date, timedelta

OC3M = (0.2424, -2.7423, 1.8017, 0.0015, -1.2280)


def ratio_for_chl(chl):
    """469/555 ratio that OC3M maps to `chl`. OC3M decreases with the ratio."""
    lo, hi = -1.0, 1.5
    for _ in range(60):
        x = (lo + hi) / 2
        if sum(a * x**i for i, a in enumerate(OC3M)) > math.log10(chl):
            lo = x
        else:
            hi = x
    return 10**x


def condition(process_id, value):
    """A load_collection property filter: `<property> <process_id> value`."""
    return {
        "process_graph": {
            "f": {
                "process_id": process_id,
                "arguments": {"x": {"from_parameter": "value"}, "y": value},
                "result": True,
            }
        }
    }


def aqua(first_start, last_start=None):
    """MODIS-Aqua 8-day composites whose first day is first_start ... last_start, one time step each.
    The search returns items that overlap the interval, end included: ending one day after the first
    day of the last composite keeps the next composite (8 days later) out."""
    end = date.fromisoformat(last_start or first_start) + timedelta(days=1)
    return DataCube(
        graph=PGNode(
            "load_collection",
            id="modis-09A1-061",
            spatial_extent=bounding_box,
            temporal_extent=[first_start, end.isoformat()],
            bands=["sur_refl_b02", "sur_refl_b03", "sur_refl_b04"],
            properties={"id": condition("starts_with", "MYD09A1")},  # Aqua only: see the README
        )
    )


def blue_green_ratio(data):
    nir, blue, green = data[0], data[1], data[2]  # sur_refl_b02, b03, b04
    water = and_(and_(blue > 0, green > 0), and_(nir < green * 0.5, nir > green * -0.5))
    return array_create([if_(water, blue / green, -1.0)])


LOW = ratio_for_chl(0.25)  # 469/555 ratio above which the proxy is < 0.25
# Number of low-chl weeks per pixel; 0 matches no class, so it is transparent.
WEEKS_COLORMAP = [
    [[0.5, 1.5], [198, 219, 239, 255]],
    [[1.5, 2.5], [107, 174, 214, 255]],
    [[2.5, 3.5], [33, 113, 181, 255]],
    [[3.5, 4.5], [84, 39, 143, 255]],
    [[4.5, 7.5], [63, 0, 112, 255]],
]


def low_chl_weeks(year, name):
    """For each pixel, how many of the 7 Aqua composites starting 25 Jan ... 14 Mar (13 Mar in a leap
    year) saw it clear AND in the < 0.25 proxy class."""
    ratio = aqua(f"{year}-01-25", f"{year}-03-14").apply_dimension(dimension="spectral", process=blue_green_ratio)
    low = ratio.mask(ratio < LOW)  # cloud and land (-1) and chl >= 0.25 -> no-data
    weeks = low.process("apply_pixel_selection", pixel_selection="count", data=low)  # unmasked views per pixel
    colored = weeks.process("colormap", data=weeks, colormap=WEEKS_COLORMAP)
    add_graph_to_map(colored.save_result("PNG"), name)


LEGEND = " (weeks in the low-chlorophyll patch, of 7: light blue 1 ... dark purple 5-7)"

OPEN_ON = 7
LAYERS = [
    (2005, "2005 (deep convection), 25 Jan-21 Mar"),
    (2006, "2006 (deep convection), 25 Jan-21 Mar"),
    (2007, "2007 (no deep convection), 25 Jan-21 Mar"),
    (2009, "2009 (mixed to the seafloor), 25 Jan-21 Mar"),
    (2010, "2010 (mixed to the seafloor), 25 Jan-21 Mar"),
    (2011, "2011 (mixed to the seafloor a month early), 25 Jan-21 Mar"),
    (2012, "2012 (mixed to the seafloor), 25 Jan-20 Mar"),
    (2013, "2013 (mixed to the seafloor), 25 Jan-21 Mar"),
    (2018, "2018 (deep, smaller area), 25 Jan-21 Mar: cloudy weeks lower the count"),
]
for i, (year, name) in enumerate(LAYERS):
    low_chl_weeks(year, name + (LEGEND if i == OPEN_ON else ""))


# Studio draws every visible layer, later ones on top, at opacity 0.8, 0.7, 0.6, ...: open on ONE layer
# and tick the others one at a time (hidden layers fetch no tiles until ticked).
for i, g in enumerate(map_graphs):
    g["visible"] = i == OPEN_ON
