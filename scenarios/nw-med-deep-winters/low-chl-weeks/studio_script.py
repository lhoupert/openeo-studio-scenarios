"""
Exp - NW Med deep winters 2005-2018 low-chl weeks MODIS

Where, and for how long, the low-chl convection patch held in each deep winter: for every pixel, the
number of the 7 MODIS-Aqua 8-day composites starting 25 Jan ... 14 Mar (13 Mar in the leap year 2012;
together they cover 25 Jan-21 Mar) in which the pixel was clear AND in the < 0.25 class of the chl
proxy. Same window and classes for every winter, so the footprints compare between winters; 2007 is
the contrast winter without deep convection. Opens on 2013.
Multi-composite layer (new with titiler-openeo#473): ONE load_collection over the window keeps one time
step per composite; mask() turns cloud, land and chl >= 0.25 into no-data; apply_pixel_selection
"count" then counts the remaining views per pixel (collections-v2/scout/backend.md, idiom 3).
Read with care:
- a cloudy week counts as not low, so cloud gaps lower the count (Feb 2018 composites: 80-89 % clear);
- the count mixes extent and duration: 2011 mixed early (bottom at LION 27 Jan, Table 4 of Houpert et
  al. 2016) and bloomed in early March, 2005 kept its patch to mid-March;
- 0 weeks (never low, never clear, or land) is transparent.
Up to 14 items per map tile (7 composites x tiles h18v04/h18v05; the code default item limit is 20):
tiles are slower than in the single-composite projects. If a layer fails with ItemsLimitExceeded,
shorten the window (e.g. "-02-02" to "-03-06").

Data: MODIS-Aqua 8-day surface reflectance (modis-09A1-061, 500 m cloud-optimized GeoTIFFs), read with
plain load_collection: since sentinel-hub/titiler-openeo#473 (deployed on openeo.mpc.ds.io on
20 Oct 2026) items with "datetime": null are keyed by their start_datetime.
- temporal_extent = [first day of the composite, that day + 1]: the STAC search returns every item that
  overlaps the interval, end included, so [start, start + 8 days] would return two composites.
- The composite's tiles h18v04 (40-50N) and h18v05 (30-40N) are mosaicked into one time step, so the
  39.5-40N strip has data (the load_stac projects stop at 40N).
- Aqua only, selected by item id (id starts_with "MYD09A1"), never by platform: MPC items of
  5 Mar 2024-10 Jun 2025 have platform "". Terra is not mixed in: over this sea its proxy gives 2-4x
  larger low-chl areas than Aqua (collections-v2/scout/collections.md, "Terra vs Aqua").
- If production rejects the id filter, delete the `properties=` line: Aqua sorts before Terra in each
  time step and fills every pixel, so the map is unchanged (collections-v2/scout/backend.md, idiom 1).

chl proxy, UNCALIBRATED: the OC3M polynomial (O'Reilly et al., 2000) on the 469/555 nm surface-
reflectance ratio. Against Sentinel-3 OLCI chl-OC4ME (4 MODIS 8-day vs OLCI pairs, Feb 2022 and
Feb 2023) it reads 1.2-1.4x high, so its "< 0.15 / < 0.25" classes cover far less than the classes of
Houpert et al. (2016, Table 4; MODIS-Aqua L3 chl). Read the colours as proxy classes, comparable
between these layers and between winters (same sensor, same algorithm, same edges), not as mg m-3.
Clear water: NIR < 0.5 * green AND NIR > -0.5 * green. The second test drops over-corrected cloud-edge
pixels (NIR/green -0.8 to -2.9) that the MODIS state QA flags and that otherwise land in the
dark-purple class; it also drops 15-29 % of the QA-clear core pixels.
Invalid pixels (cloud, cloud edge, land) are half-transparent light grey, so cloud gaps do not read
as the dark-purple core over the dark satellite basemap (land turns grey too).
Clear % below = MODIS state-QA clear ocean in the box 2.5-8.5E 40.5-44N (review/scenes/data,
collections-v2/scout/raw/modis_rev and collections-v2/scout/data: the same scan).
LION = mixed-layer depth at the LION mooring (42.04N 4.69E; SEANOE 10.17882/44411; our analysis,
workflow/lion_mld_v2.txt).
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
            properties={"id": condition("starts_with", "MYD09A1")},  # Aqua; see the docstring
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


LEGEND = " (weeks clear and in the < 0.25 chl proxy class, of 7: light blue 1 ... dark purple 5-7; none = transparent)"

OPEN_ON = 7
LAYERS = [
    (2005, "2005 (deep): low-chl weeks, 25 Jan-21 Mar"),
    (2006, "2006 (deep): low-chl weeks, 25 Jan-21 Mar"),
    (2007, "2007 (contrast, no deep convection): low-chl weeks, 25 Jan-21 Mar"),
    (2009, "2009 (bottom-reaching): low-chl weeks, 25 Jan-21 Mar"),
    (2010, "2010 (bottom-reaching): low-chl weeks, 25 Jan-21 Mar"),
    (2011, "2011 (bottom-reaching): low-chl weeks, 25 Jan-21 Mar"),
    (2012, "2012 (bottom-reaching): low-chl weeks, 25 Jan-20 Mar"),
    (2013, "2013 (bottom-reaching): low-chl weeks, 25 Jan-21 Mar"),
    (2018, "2018 (deep, moderate extent): low-chl weeks, 25 Jan-21 Mar"),
]
for i, (year, name) in enumerate(LAYERS):
    low_chl_weeks(year, name + (LEGEND if i == OPEN_ON else ""))


# Studio draws every visible layer, later ones on top, at opacity 0.8, 0.7, 0.6, ...: open on ONE layer
# and tick the others one at a time (hidden layers fetch no tiles until ticked).
for i, g in enumerate(map_graphs):
    g["visible"] = i == OPEN_ON
