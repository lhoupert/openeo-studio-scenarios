"""
Exp - NW Med deep winters 2005-2018 compared MODIS patch

The low-chl convection patch of every winter with known deep convection that MODIS-Aqua saw (2005,
2006, 2009-2013, 2018), plus the contrast winter 2007: one 8-day composite per winter, one sensor, one
algorithm and the same class edges, so the horizontal extent can be compared between winters (in the
spirit of Houpert et al. 2016, JGR Oceans, doi:10.1002/2016JC011857, section 4.2.3 and Table 4).
Layers in time order; opens on 2013 (the week of Houpert et al. 2016 Fig. 8g, "18-25 Feb. 2013", p. 8154).
The per-winter 8-day sequences are in the projects "Exp - NW Med deep convection <year> MODIS 8-day sequence".

Pick per winter: the clearest composite (>= 80 % QA-clear) at the largest proxy < 0.25 area of the main
mixing; for 2013 the paper's own week. Not picked: 2012 10-17 Feb (largest area but 82 % clear, and a
LION 469/555 of 6.86, a likely residual-cloud or glint spike) and 2010 6-13 Mar (the second mixing event,
84 % clear). Our scan: collections-v2/scout/raw/modis_rev, review/scenes/data, collections-v2/scout/data.

Published evidence (exact text, page):
- 2005, 2006: Smith et al. 2008, Ocean Sci. 4, abstract, p. 133: "Subsequently, new deep water was
  formed in March of 2005 and 2006".
- 2009-2013: Houpert et al. 2016, Table 4, p. 8151, row "Mixed Layer reaches the bottom": 12 Feb 2009,
  10 Feb 2010, 27 Jan 2011, 10 Feb 2012, 13 Feb 2013; areas of low surface chl-a < 0.15 / < 0.25 mg m-3
  (km2): 16,350 / 34,162 (2009), 13,006 / 29,180 (2010), 15,790 / 24,111 (2011), 17,863 / 41,616 (2012),
  23,583 / 56,351 (2013).
- 2018: Margirier et al. 2020, Sci Rep 10:20923, p. 6: "triggered convection down to at least 1800 m
  depth"; p. 7: "Globcolor and ESA-CCI-OC-v4.2 8-day products respectively gave maximum surface areas
  of 13,400 km 2 and 10,400 km 2 , about half of the surface reported by Houpert et al.14 or Testor
  et al.15 for strong convective years."
- 2007 (contrast): Houpert et al. 2016, p. 8155: "The area of intense dilution (<0.15 mg.m−3) is not
  present in 2007 and 2008", with gliders that "recorded a maximal mixed layer of 400 m depth
  [Testor et al., 2007]."
The proxy under-sizes Table 4 (our comparison: < 0.25 areas 1.35-1.9x smaller, < 0.15 areas 1.7-18x
smaller; our box is also smaller than the paper's domain): compare the winters with each other, not
with the published km2.

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

OPEN_ON = 7
LAYERS = [
    ("2005-03-06", "2005"),
    ("2006-02-26", "2006 (deep, no mooring), 26 Feb-5 Mar: largest envelope of the winter (94 % clear)"),
    ("2007-02-18", "2007 (contrast: no deep convection, gliders <= 400 m), 18-25 Feb: no patch (96 % clear)"),
    ("2009-02-18", "2009 (bottom at LION 12 Feb), 18-25 Feb: largest envelope, main mixing ends 26 Feb (99 % clear)"),
    ("2010-02-18", "2010 (bottom at LION 10 Feb), 18-25 Feb: main mixing ends 20 Feb (92 % clear)"),
    ("2011-02-02", "2011 (bottom at LION 27 Jan), 2-9 Feb: largest envelope, main mixing ends 5 Feb (100 % clear)"),
    ("2012-02-18", "2012 (bottom at LION 10 Feb), 18-25 Feb: main mixing ends 23 Feb (99 % clear)"),
    ("2013-02-18", "2013 (bottom at LION 13 Feb), 18-25 Feb: the week of Houpert et al. 2016 Fig. 8g (98 % clear)"),
    ("2018-02-26", "2018 (deep, LION 1500-1750 m), 26 Feb-5 Mar: largest patch (80 % clear)"),
]
for i, (start, name) in enumerate(LAYERS):
    chl_layer(start, name + (LEGEND if i == OPEN_ON else ""))


# Studio draws every visible layer, later ones on top, at opacity 0.8, 0.7, 0.6, ...: open on ONE layer
# and tick the others one at a time (hidden layers fetch no tiles until ticked).
for i, g in enumerate(map_graphs):
    g["visible"] = i == OPEN_ON
