"""
Exp - NW Med deep convection 2013 MODIS 8-day sequence

In some winters, cold, dry northerly winds (Mistral, Tramontane) cool the Gulf of Lion so much that the surface water becomes denser than the water below it and sinks: the sea mixes from the surface down to 1000 m or more, sometimes to the seafloor. This is open-ocean deep convection.

The mixing carries the microscopic algae of the surface (phytoplankton) down into the dark, so from space the mixed area looks like a patch of very low chlorophyll. When the wind drops and the surface warms, the algae bloom on the nutrients that the mixing brought up: first around the edges of the patch, then inside it.

Winter 2013 was one of the strongest on record: the sea mixed down to the seafloor (about 2300 m) in mid-February. Eleven satellite images, each the clearest view of 8 days, follow it from the first patch to the end of the spring bloom (open one layer at a time):
1. 25 Jan-1 Feb: the patch appears as the mixing deepens.
2. 2-9 Feb: the patch grows.
3. 10-17 Feb: the largest dark-purple core.
4. 18-25 Feb: the week of the reference study (Houpert et al. 2016).
5. 26 Feb-5 Mar: the patch at its widest; the main mixing ends on 28 Feb.
6. 6-13 Mar: the patch shrinks and the bloom starts at its edges.
7. 14-21 Mar: a second mixing event (13-17 Mar) brings the patch back.
8. 22-29 Mar: the mixing is over; the bloom grows around the patch.
9. 30 Mar-6 Apr: the bloom reaches the centre of the patch.
10. 7-14 Apr: the bloom at its peak.
11. 1-8 May: the bloom fades.

How to read the colours: purple and dark blue = very little chlorophyll (the mixed patch); green and yellow = more; orange and red = the bloom (near the coast, also murky river water). Grey = cloud; land is transparent. The colours come from the colour of the sea and are an uncalibrated index: compare weeks and winters with each other, not with measured chlorophyll.

Method, sources and caveats: openeo-studio-scenarios, scenarios/nw-med-deep-winters/2013-sequence/README.md

MODIS-Aqua surface reflectance (MYD09A1 v6.1, NASA LP DAAC), via Microsoft Planetary Computer.
"""
import math
from datetime import date, timedelta

from openeo.processes import eq, floor, gte, mod, or_

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
    reflectance = DataCube(
        graph=PGNode(
            "load_collection",
            id="modis-09A1-061",
            spatial_extent=bounding_box,
            temporal_extent=[first_start, end.isoformat()],
            bands=["sur_refl_b02", "sur_refl_b03", "sur_refl_b04"],
            properties={"id": condition("starts_with", "MYD09A1")},  # Aqua only: see the README
        )
    )
    # Ocean mask: the state QA band of the same items, read by load_stac at native resolution and
    # warped onto the tile grid (nearest). Not read by load_collection: at z <= 7 a tile-size read
    # comes from the COG overviews, which are smoothed and garble the land/water bits.
    state = DataCube(
        graph=PGNode(
            "load_stac",
            url="https://planetarycomputer.microsoft.com/api/stac/v1/collections/modis-09A1-061",
            spatial_extent=bounding_box,
            temporal_extent=[first_start, end.isoformat()],
            bands=["sur_refl_state_500m"],
            properties={"id": condition("starts_with", "MYD09A1")},
        )
    )
    return reflectance.merge_cubes(state.resample_cube_spatial(target=reflectance, method="near"))


LAND = -9.0  # land, coastline, inland water: in no colour class, so transparent


def blue_green_ratio(data):
    nir, blue, green, state = data[0], data[1], data[2], data[3]  # sur_refl_b02, b03, b04, state QA
    water = and_(and_(blue > 0, green > 0), and_(nir < green * 0.5, nir > green * -0.5))
    land_water = mod(floor(state / 8), 8)  # bits 3-5: 0 shallow, 6 moderate, 7 deep ocean
    ocean = or_(eq(land_water, 0), gte(land_water, 6))
    return array_create([if_(ocean, if_(water, blue / green, -1.0), LAND)])


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
# Invalid sea pixels (-1) in half-transparent grey (renders on production). LAND (-9) is in no
# interval, so land is transparent.
RATIO_COLORMAP = RATIO_COLORMAP + [[[-1.5, -0.5], [200, 200, 200, 140]]]


def chl_layer(start, name):
    """One MODIS-Aqua 8-day composite (the one whose first day is `start`), as chl proxy classes."""
    cube = aqua(start)
    cube = cube.process("apply_pixel_selection", pixel_selection="first", data=cube)  # 1 time step
    ratio = cube.apply_dimension(dimension="spectral", process=blue_green_ratio)
    colored = ratio.process("colormap", data=ratio, colormap=RATIO_COLORMAP)
    add_graph_to_map(colored.save_result("PNG"), name)


LEGEND = " (purple = least chlorophyll, red = most; grey = cloud)"

OPEN_ON = 0
LAYERS = [
    ("2013-01-25", "25 Jan-1 Feb 2013: the patch appears as the mixing deepens"),
    ("2013-02-02", "2-9 Feb 2013: the patch grows"),
    ("2013-02-10", "10-17 Feb 2013: the largest dark-purple core"),
    ("2013-02-18", "18-25 Feb 2013: the week of the reference study (Houpert et al. 2016)"),
    ("2013-02-26", "26 Feb-5 Mar 2013: the patch at its widest; the main mixing ends on 28 Feb"),
    ("2013-03-06", "6-13 Mar 2013: the patch shrinks and the bloom starts at its edges"),
    ("2013-03-14", "14-21 Mar 2013: a second mixing event (13-17 Mar) brings the patch back"),
    ("2013-03-22", "22-29 Mar 2013: the mixing is over; the bloom grows around the patch"),
    ("2013-03-30", "30 Mar-6 Apr 2013: the bloom reaches the centre of the patch"),
    ("2013-04-07", "7-14 Apr 2013: the bloom at its peak"),
    ("2013-05-01", "1-8 May 2013: the bloom fades"),
]
for i, (start, name) in enumerate(LAYERS):
    chl_layer(start, name + (LEGEND if i == OPEN_ON else ""))


# Studio draws every visible layer, later ones on top, at opacity 0.8, 0.7, 0.6, ...: open on ONE layer
# and tick the others one at a time (hidden layers fetch no tiles until ticked).
for i, g in enumerate(map_graphs):
    g["visible"] = i == OPEN_ON
