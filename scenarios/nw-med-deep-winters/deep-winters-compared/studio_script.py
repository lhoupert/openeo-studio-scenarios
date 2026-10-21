"""
Exp - NW Med deep winters 2005-2018 compared MODIS patch

In winters with deep convection, cold northerly winds mix the Gulf of Lion from the surface down to 1000 m or more, often to the seafloor. The mixing carries the surface algae (phytoplankton) down into the dark, so from space the mixed area looks like a patch of very low chlorophyll.

This project compares that patch across every winter with known deep convection that the MODIS-Aqua satellite has seen (2005, 2006, 2009-2013 and 2018), plus 2007, a winter without deep convection. One satellite image per winter (the clearest view of 8 days), taken when the patch was largest, with the same colours everywhere. The map opens on 2013; open one layer at a time.

What to look for: the patch is widest in 2005, 2006 and 2013, and absent in 2007. In 2018 the mixing was deep but covered a smaller area, and cloud hides the eastern part of the patch.

How to read the colours: purple and dark blue = very little chlorophyll (the mixed patch); green and yellow = more; orange and red = much more (near the coast, also murky river water). Grey = cloud or land. The colours are an uncalibrated index from the colour of the sea: compare winters with each other, not with measured chlorophyll.

Method, sources and caveats: openeo-studio-scenarios, scenarios/nw-med-deep-winters/deep-winters-compared/README.md

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


# chl proxy class edges (uncalibrated, see the README) and one colour per class: the same in every project.
CHL_EDGES = [0.15, 0.25, 0.35, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 5.0]
COLORS = [
    [64, 0, 112, 255],  # < 0.15
    [33, 102, 172, 255],  # 0.15-0.25
    [67, 162, 202, 255],
    [102, 194, 164, 255],
    [171, 221, 164, 255],
    [230, 245, 152, 255],
    [254, 224, 139, 255],
    [253, 174, 97, 255],
    [244, 109, 67, 255],
    [215, 48, 39, 255],
    [165, 0, 38, 255],  # > 5
]

# The colour map works on the ratio: low chl is a high ratio.
RATIO_EDGES = [1e6] + [ratio_for_chl(c) for c in CHL_EDGES] + [0.0]
RATIO_COLORMAP = [[[RATIO_EDGES[i + 1], RATIO_EDGES[i]], color] for i, color in enumerate(COLORS)]
# Invalid pixels (-1: cloud, cloud edge and land) in half-transparent grey.
RATIO_COLORMAP = RATIO_COLORMAP + [[[-1.5, -0.5], [200, 200, 200, 140]]]


def chl_layer(start, name):
    """One MODIS-Aqua 8-day composite (the one whose first day is `start`), as chl proxy classes."""
    cube = aqua(start)
    cube = cube.process("apply_pixel_selection", pixel_selection="first", data=cube)  # 1 time step
    ratio = cube.apply_dimension(dimension="spectral", process=blue_green_ratio)
    colored = ratio.process("colormap", data=ratio, colormap=RATIO_COLORMAP)
    add_graph_to_map(colored.save_result("PNG"), name)


LEGEND = " (purple = least chlorophyll, red = most; grey = cloud or land)"

OPEN_ON = 7
LAYERS = [
    ("2005-03-06", "2005 (deep convection), 6-13 Mar"),
    ("2006-02-26", "2006 (deep convection), 26 Feb-5 Mar"),
    ("2007-02-18", "2007 (no deep convection), 18-25 Feb: no patch"),
    ("2009-02-18", "2009 (mixed to the seafloor), 18-25 Feb"),
    ("2010-02-18", "2010 (mixed to the seafloor), 18-25 Feb"),
    ("2011-02-02", "2011 (mixed to the seafloor a month early), 2-9 Feb"),
    ("2012-02-18", "2012 (mixed to the seafloor), 18-25 Feb"),
    ("2013-02-18", "2013 (mixed to the seafloor), 18-25 Feb: the week of the reference study"),
    ("2018-02-26", "2018 (deep, smaller area), 26 Feb-5 Mar: cloud hides the eastern part"),
]
for i, (start, name) in enumerate(LAYERS):
    chl_layer(start, name + (LEGEND if i == OPEN_ON else ""))


# Studio draws every visible layer, later ones on top, at opacity 0.8, 0.7, 0.6, ...: open on ONE layer
# and tick the others one at a time (hidden layers fetch no tiles until ticked).
for i, g in enumerate(map_graphs):
    g["visible"] = i == OPEN_ON
