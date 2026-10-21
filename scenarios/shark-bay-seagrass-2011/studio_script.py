"""
Exp - Shark Bay seagrass loss 2011 heatwave Landsat

Shark Bay, a World Heritage Area in Western Australia, holds vast seagrass meadows and the largest carbon stock reported for a seagrass ecosystem. In the summer of 2010-11 a marine heatwave along the Western Australian coast brought summer seawater 2-5 C warmer than average, and across the World Heritage Area about 1,310 km2 of dense seagrass was lost: the largest loss recorded after a single event. On the shallow banks, seagrass looks dark and bare sand looks bright, so Landsat can show where the meadows thinned.

Four layers (open one at a time):
1. 12 May 2010, before (Landsat 5): dark patches on the turquoise banks = dense seagrass meadows; the long dark fingers are channels (deeper water); bright turquoise = sand; deep water is black.
2. 4 Mar 2011, during the heatwave (Landsat 7): water temperature minus the mean of three cloud-free days of late summer 2000 and 2002 (23 Feb to 11 Mar), same satellite, same time of day. Red = warmer, one colour step per 1 C; white = within 0.5 C of that mean. Thin empty lines are gaps in the 2011 image (Landsat 7's scan-line corrector failed in 2003).
3. 10 Jul 2014, after (Landsat 8): many of the dark banks of 2010 are lighter, most clearly on the Faure Sill between its channels.
4. 2010 to 2014, change in green brightness over water: brown = brighter in 2014 (seagrass thinned or lost, or shallower or clearer water), teal = darker, white = unchanged. The Faure Sill banks are the place to look; the brown rings along the shores of Hamelin Pool are most likely a lower water level in 2014.

Layer 4 compares two different satellites on two days with different tides and water clarity: it shows where to look, it is not a seagrass map.

Method, sources and caveats: openeo-studio-scenarios, scenarios/shark-bay-seagrass-2011/README.md

Landsat data courtesy of the U.S. Geological Survey, via Microsoft Planetary Computer.
"""


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


def landsat(platform, start, end, bands):
    """One overpass of one Landsat satellite (all its scenes between start and end, UTC), as one time step.
    The platform filter keeps the other Landsat satellites out if a window is widened."""
    cube = DataCube(
        graph=PGNode(
            "load_collection",
            id="landsat-c2-l2",
            spatial_extent=bounding_box,
            temporal_extent=[start, end],
            bands=bands,
            properties={"platform": condition("eq", platform)},
        )
    )
    return cube.process("apply_pixel_selection", pixel_selection="first", data=cube)


REFLECTANCE_MAX = 0.15  # sand banks stay below it; land saturates
NO_DATA = -0.19999  # DN 0 after the backend's scale/offset is exactly -0.2; DN 1 is -0.1999725


def no_data(data):
    """DN 0 (no data) in the blue band; the three bands share one footprint."""
    return array_create([data[2] < NO_DATA])


def true_colour(platform, start, end, name):
    """Red, green, blue surface reflectance, 0 to REFLECTANCE_MAX stretched to 0-255."""
    cube = landsat(platform, start, end, ["red", "green", "blue"])
    hide = cube.apply_dimension(dimension="bands", process=no_data)
    rgb = cube.mask(hide).apply(lambda x: clip(x, 0, REFLECTANCE_MAX))
    rgb = rgb.linear_scale_range(input_min=0, input_max=REFLECTANCE_MAX, output_min=0, output_max=255).apply("trunc")
    add_graph_to_map(rgb.save_result("PNG"), name)


WATER_NIR = 0.05  # near-infrared reflectance below this = water; land, cloud and dry sand are brighter


def lwir(data):
    """The `lwir` band alone (the backend already returns it in kelvin)."""
    return array_create([data[0]])


def not_water(data):
    return array_create([data[1] >= WATER_NIR])


def water_temperature(start, end):
    """Landsat 7 surface temperature (`lwir` = ST_B6, kelvin) of one overpass, over water only."""
    cube = landsat("landsat-7", start, end, ["lwir", "nir08"])
    t = cube.apply_dimension(dimension="bands", process=lwir).rename_labels(dimension="bands", target=["t"])
    return t.mask(cube.apply_dimension(dimension="bands", process=not_water))


# Temperature difference in 1 C classes centred on 0: blue = colder, white = within 0.5 C, red = warmer.
# Beyond +/-5.5 C: no colour (0.1 % of the water at the opening view; a guard against edge artifacts).
ANOMALY_EDGES = [-5.5, -3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
ANOMALY_COLORS = [
    [5, 48, 97], [33, 102, 172], [67, 147, 195], [146, 197, 222], [247, 247, 247],
    [253, 219, 199], [244, 165, 130], [214, 96, 77], [178, 24, 43], [103, 0, 31],
]
ANOMALY_COLORMAP = [[[ANOMALY_EDGES[i], ANOMALY_EDGES[i + 1]], c + [255]] for i, c in enumerate(ANOMALY_COLORS)]


def temperature_difference(day, reference_days, name):
    """Water temperature of `day` minus the mean of `reference_days`; each is a (start, end) overpass window.
    A pixel missing on any of the days (gap, land, cloud) stays empty: merge_cubes keeps the masks."""
    t = water_temperature(*day)
    refs = [water_temperature(*d) for d in reference_days]
    mean = refs[0]
    for r in refs[1:]:
        mean = mean.merge_cubes(r, overlap_resolver=lambda x, y: x + y)
    mean = mean.apply(lambda v: v / len(refs))
    diff = t.merge_cubes(mean, overlap_resolver=lambda x, y: x - y)
    colored = diff.process("colormap", data=diff, colormap=ANOMALY_COLORMAP)
    add_graph_to_map(colored.save_result("PNG"), name)


# Green reflectance, 2014 minus 2010: teal = darker, white = within 0.005, brown = brighter.
CHANGE_EDGES = [-1, -0.03, -0.02, -0.01, -0.005, 0.005, 0.01, 0.02, 0.03, 1]
CHANGE_COLORS = [
    [1, 102, 94], [53, 151, 143], [128, 205, 193], [199, 234, 229], [245, 245, 245],
    [246, 232, 195], [223, 194, 125], [191, 129, 45], [140, 81, 10],
]
CHANGE_COLORMAP = [[[CHANGE_EDGES[i], CHANGE_EDGES[i + 1]], c + [255]] for i, c in enumerate(CHANGE_COLORS)]


def green_change(data):
    """Green after - green before where both dates are water with data, -99 elsewhere (no colour)."""
    g0, n0, g1, n1 = data[0], data[1], data[2], data[3]
    water = and_(and_(n0 < WATER_NIR, n1 < WATER_NIR), and_(g0 > NO_DATA, g1 > NO_DATA))
    return array_create([if_(water, g1 - g0, -99)])


def green_brightness_change(before, after, name):
    """`before`, `after` = (platform, start, end) of one overpass each."""
    cubes = [
        landsat(*when, ["green", "nir08"]).rename_labels(dimension="bands", target=[f"green{i}", f"nir{i}"])
        for i, when in enumerate([before, after])
    ]
    diff = cubes[0].merge_cubes(cubes[1]).apply_dimension(dimension="bands", process=green_change)
    colored = diff.process("colormap", data=diff, colormap=CHANGE_COLORMAP)
    add_graph_to_map(colored.save_result("PNG"), name)


# Both optical dates come from the same orbit track (path 115), which covers the whole box.
BEFORE = ("landsat-5", "2010-05-12T02:10:00Z", "2010-05-12T02:16:00Z")
AFTER = ("landsat-8", "2014-07-10T02:19:00Z", "2014-07-10T02:25:00Z")
# Heat layer: Landsat 7, path 115, about 10:16 local time. The 2011 image has the scan-line gaps of Landsat 7
# (since May 2003), so the references are the cloud-free path-115 passes from before that, within 9 days of the
# date and 5 minutes of its time (26 Feb 2003 is left out: cloud over the gulfs that the NIR mask misses).
# Each window holds rows 076-079 only: rows 071-073 have no lwir band.
HEATWAVE = ("2011-03-04T02:14:57Z", "2011-03-04T02:16:32Z")
REFERENCES = [
    ("2000-03-05T02:14:01Z", "2000-03-05T02:15:36Z"),
    ("2002-02-23T02:10:18Z", "2002-02-23T02:11:54Z"),
    ("2002-03-11T02:10:20Z", "2002-03-11T02:11:55Z"),
]

OPEN_ON = 0
true_colour(*BEFORE,
            "12 May 2010, before (Landsat 5): dark patches on the turquoise banks = dense seagrass meadows")
temperature_difference(HEATWAVE, REFERENCES,
                       "4 Mar 2011, heatwave (Landsat 7): water temperature minus the mean of 3 late-summer days"
                       " of 2000 and 2002 (red = warmer, 1 C per colour step; thin empty lines = image gaps)")
true_colour(*AFTER,
            "10 Jul 2014, after (Landsat 8): many dark banks of 2010 are lighter (Faure Sill)")
green_brightness_change(BEFORE, AFTER,
                        "2010 to 2014, green brightness over water: brown = brighter in 2014 (seagrass loss,"
                        " or shallower or clearer water), teal = darker, white = unchanged")

# Studio draws every visible layer, later ones on top and semi-transparent (80 %, 70 %, ...), so two
# ticked layers blend: open on ONE layer and untick it before ticking the next (hidden layers fetch no
# tiles until ticked).
for i, g in enumerate(map_graphs):
    g["visible"] = i == OPEN_ON
