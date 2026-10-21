"""
Exp - NW Med recent winters 2019-2026 vs 2013 and 2018 MODIS patch

In winters with deep convection, cold northerly winds mix the Gulf of Lion from the surface down to 1000 m or more. The mixing carries the surface algae (phytoplankton) down into the dark, so from space the mixed area looks like a patch of very low chlorophyll. Since 2014 the winter mixing has mostly stayed much shallower.

One satellite image per winter (8 days combined, little cloud), near the time the patch was largest, or the clearest week when there was none: 2013 and 2018 for reference, then 2019-2026, roughly from the strongest winter to the weakest. Each label gives the deepest mixing estimated from the LION mooring, in the middle of the gulf. The map opens on 2013; open one layer at a time.

What to look for: a large patch in 2013, a smaller one in 2018, patches of varying size in the moderate winters (2019, 2021-2023), and almost none around the mooring in 2020 and 2024-2026. The patch shows where the sea mixed, not how deep.

How to read the colours: purple and dark blue = very little chlorophyll (the mixed patch); lighter blue, green and yellow = more; orange and red = much more (near the coast, also murky river water). Grey = no reliable value: cloud, land, and some specks inside the patch. The colours are an uncalibrated index from the colour of the sea: compare winters with each other, not with measured chlorophyll.

Method, sources and caveats: openeo-studio-scenarios, scenarios/nw-med-deep-winters/recent-winters/README.md

MODIS-Aqua surface reflectance (MYD09A1 v6.1, NASA LP DAAC), via Microsoft Planetary Computer. LION mooring data: SEANOE, doi:10.17882/44411.
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


LEGEND = " (purple = least chlorophyll, red = most; grey = no reliable value: cloud, land)"

OPEN_ON = 0
LAYERS = [
    ("2013-02-26", "2013 (mixed to the seafloor, ~2300 m), 26 Feb-5 Mar"),
    ("2018-02-26", "2018 (deep, 1500-1750 m), 26 Feb-5 Mar: cloud hides the eastern part"),
    ("2019-02-02", "2019 (moderate, ~500-1090 m), 2-9 Feb"),
    ("2023-02-10", "2023 (moderate, ~450-850 m), 10-17 Feb"),
    ("2022-02-26", "2022 (moderate, ~350-700 m), 26 Feb-5 Mar"),
    ("2021-01-25", "2021 (moderate, ~650-820 m), 25 Jan-1 Feb: small patch"),
    ("2026-03-06", "2026 (weak, ~450-600 m), 6-13 Mar: no patch at the mooring (the purple streaks further south are likely image artefacts)"),
    ("2025-02-02", "2025 (weak, ~400-500 m), 2-9 Feb: no patch"),
    ("2024-02-10", "2024 (no convection, <= 300 m), 10-17 Feb: no patch"),
    ("2020-02-18", "2020 (no convection, <= 300 m), 18-25 Feb: no patch"),
]
for i, (start, name) in enumerate(LAYERS):
    chl_layer(start, name + (LEGEND if i == OPEN_ON else ""))


# Studio draws every visible layer, later ones on top, at opacity 0.8, 0.7, 0.6, ...: open on ONE layer
# and tick the others one at a time (hidden layers fetch no tiles until ticked).
for i, g in enumerate(map_graphs):
    g["visible"] = i == OPEN_ON
