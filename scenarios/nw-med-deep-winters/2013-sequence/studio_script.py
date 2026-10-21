"""
Exp - NW Med deep convection 2013 MODIS 8-day sequence

Port of review/new-projects/exp-nw-med-convection-2013-modis-via-load-stac-best-scenes.py
to plain load_collection (titiler-openeo#473): same composites, labels and layer order.
That load_stac version is not built.

Bottom-reaching convection in the NW Mediterranean, winter 2013 (the year of Houpert et al. 2016,
JGR Oceans, doi:10.1002/2016JC011857, section 4.2.3, Table 4 and Fig. 8g), followed 8 days at a time
from the first low-chl patch to the end of the spring bloom: the horizontal expansion and retreat of
the convection area, then the bloom that starts at its edges and fills it.
Replaces the 2-layer project "Exp - NW Med convection 2013 MODIS via load_stac" (10-17 Feb, 7-14 Apr).

LION: >= 1000 m from 27 Jan to 23 Mar 2013 (bottom, ~2300 m, on many days); Houpert Table 4: end of
the main mixing 28/02/13, second mixing event 13/03/13-17/03/13, end 21/03/13.
Every Aqua composite of 25 Jan-14 Apr 2013 is 92-99 % clear (17-24 Jan: 62 %, left out); 1-8 May: 95 %.
Mayot et al. (2017): bloom at the periphery ~2 March, in the centre ~3 April, maximum 7-9 April.

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
Invalid sea pixels (cloud, cloud edge) are half-transparent light grey, so cloud gaps do not read
as the dark-purple core over the dark satellite basemap. Ocean mask: only pixels that the MODIS
state QA (sur_refl_state_500m bits 3-5, MOD09 User Guide v6.1, Table 13) flags as shallow,
moderate or deep ocean are drawn; land, coastline and inland-water pixels are transparent.
Clear % below = MODIS state-QA clear ocean in the box 2.5-8.5E 40.5-44N (review/scenes/data,
collections-v2/scout/raw/modis_rev and collections-v2/scout/data: the same scan).
LION = mixed-layer depth at the LION mooring (42.04N 4.69E; SEANOE 10.17882/44411; our analysis,
workflow/lion_mld_v2.txt).
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
            properties={"id": condition("starts_with", "MYD09A1")},  # Aqua; see the docstring
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


LEGEND = " (chl proxy, uncalibrated: purple < 0.15, blue < 0.25, red > 2; grey = cloud; land transparent)"

OPEN_ON = 0
LAYERS = [
    ("2013-01-25", "25 Jan-1 Feb 2013: mixing deepens (LION >= 1000 m from 27 Jan), patch appears (97 % clear)"),
    ("2013-02-02", "2-9 Feb 2013: the patch expands (95 % clear)"),
    ("2013-02-10", "10-17 Feb 2013: largest < 0.15 core (93 % clear)"),
    ("2013-02-18", "18-25 Feb 2013: the week of Houpert et al. 2016 Fig. 8g / Table 4 (98 % clear)"),
    ("2013-02-26", "26 Feb-5 Mar 2013: largest < 0.25 envelope, end of the main mixing (93 % clear)"),
    ("2013-03-06", "6-13 Mar 2013: between mixing events, bloom at the patch edges (92 % clear)"),
    ("2013-03-14", "14-21 Mar 2013: second mixing event (13-17 Mar) re-forms the patch (99 % clear)"),
    ("2013-03-22", "22-29 Mar 2013: restratified, bloom starts around the patch (92 % clear)"),
    ("2013-03-30", "30 Mar-6 Apr 2013: bloom onset in the patch (97 % clear)"),
    ("2013-04-07", "7-14 Apr 2013: bloom maximum (99 % clear)"),
    ("2013-05-01", "1-8 May 2013: decline (95 % clear)"),
]
for i, (start, name) in enumerate(LAYERS):
    chl_layer(start, name + (LEGEND if i == OPEN_ON else ""))


# Studio draws every visible layer, later ones on top, at opacity 0.8, 0.7, 0.6, ...: open on ONE layer
# and tick the others one at a time (hidden layers fetch no tiles until ticked).
for i, g in enumerate(map_graphs):
    g["visible"] = i == OPEN_ON
