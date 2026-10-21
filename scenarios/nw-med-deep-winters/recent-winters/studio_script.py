"""
Exp - NW Med recent winters 2019-2026 vs 2013 and 2018 MODIS patch

Port of review/new-projects/exp-nw-med-convection-between-winters-modis.py
to plain load_collection (titiler-openeo#473): same composites, labels and layer order.
That load_stac version is not built.
For 2005-2012 see "Exp - NW Med deep winters 2005-2018 compared MODIS patch".

One MODIS-Aqua 8-day composite per winter, at that winter's largest (or clearest) low-chl extent, so
the convection area can be compared between years with one sensor and one algorithm. Ordered from the
strongest to the weakest winter. Class = LION mooring Dec-Mar maximum mixed-layer depth across criteria
(workflow/lion_mld_v2.txt) and the in-region low-chl area (41.3-43.2N, 3-7E; review/checks/patch_series.txt).
- bottom-reaching: 2013 (LION ~2300 m)
- deep: 2018 (LION 1500-1750 m)
- moderate: 2019, 2021, 2022, 2023 (LION ~500-1090 m at 0.03-0.05 degC or with the Houpert criterion;
  2021 only once the QC-flagged 194 m and 472 m sensors are masked), each with a satellite low-chl patch
- weak: 2025, 2026 (LION 400-600 m, the 2014-2017 range), no or marginal patch
- none: 2024, 2020 (LION <= 300-350 m)
Picks: the composite with the largest in-region low-chl area of January-March when it is clear enough
(2013, 2018, 2022, 2021, 2026); 2019 2-9 Feb (99 % clear) instead of 25 Jan (80 %, speckled core);
2023 10-17 Feb (99 % clear, 5 % of the core QA-flagged) instead of 26 Feb (88 %, 24 % flagged); for the
no-patch winters the clearest composite near the LION maximum (2024 10-17 Feb rather than 26 Feb-5 Mar,
whose ~2,400 km2 low-chl area lies offshore at ~41.6N 6.0E). Items 2024-03-05..2025-06-10 have an empty
`platform` on MPC (2025 here): selecting Aqua by item id is unaffected.
Areas depend on the grid and the method (up to ~20 % for one year, more between years), so they are not
written into the layer names.

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


# chl proxy class edges (uncalibrated, see above) and one colour per class: the same in every project.
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
# Invalid pixels (-1) in half-transparent grey. Not yet rendered on the backend: if the colour map
# rejects it, delete this line (invalid pixels are then transparent, as in the deployed projects).
RATIO_COLORMAP = RATIO_COLORMAP + [[[-1.5, -0.5], [200, 200, 200, 140]]]


def chl_layer(start, name):
    """One MODIS-Aqua 8-day composite (the one whose first day is `start`), as chl proxy classes."""
    cube = aqua(start)
    cube = cube.process("apply_pixel_selection", pixel_selection="first", data=cube)  # 1 time step
    ratio = cube.apply_dimension(dimension="spectral", process=blue_green_ratio)
    colored = ratio.process("colormap", data=ratio, colormap=RATIO_COLORMAP)
    add_graph_to_map(colored.save_result("PNG"), name)


LEGEND = " (chl proxy, uncalibrated: purple < 0.15, blue < 0.25, red > 2; grey = cloud/land)"

OPEN_ON = 0
LAYERS = [
    ("2013-02-26", "2013 (bottom-reaching, LION ~2300 m), 26 Feb-5 Mar: largest envelope (93 % clear)"),
    ("2018-02-26", "2018 (deep, LION 1500-1750 m), 26 Feb-5 Mar: largest patch (80 % clear)"),
    ("2019-02-02", "2019 (moderate, LION ~500-1090 m), 2-9 Feb (99 % clear)"),
    ("2023-02-10", "2023 (moderate, LION ~600-850 m), 10-17 Feb (99 % clear)"),
    ("2022-02-26", "2022 (moderate, LION ~500-700 m), 26 Feb-5 Mar (100 % clear)"),
    ("2021-01-25", "2021 (moderate, LION ~650-820 m), 25 Jan-1 Feb: small patch (95 % clear)"),
    ("2026-03-06", "2026 (weak, LION ~450-600 m), 6-13 Mar: marginal patch (87 % clear)"),
    ("2025-02-02", "2025 (weak, LION ~400-500 m), 2-9 Feb: no patch (100 % clear)"),
    ("2024-02-10", "2024 (no convection, LION <= 300 m), 10-17 Feb (99 % clear)"),
    ("2020-02-18", "2020 (no convection, LION <= 300 m), 18-25 Feb (100 % clear)"),
]
for i, (start, name) in enumerate(LAYERS):
    chl_layer(start, name + (LEGEND if i == OPEN_ON else ""))


# Studio draws every visible layer, later ones on top, at opacity 0.8, 0.7, 0.6, ...: open on ONE layer
# and tick the others one at a time (hidden layers fetch no tiles until ticked).
for i, g in enumerate(map_graphs):
    g["visible"] = i == OPEN_ON
