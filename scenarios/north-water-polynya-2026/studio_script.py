"""
Exp - North Water polynya 2026 Sentinel-1 radar

The North Water, between Ellesmere Island (Canada) and Greenland, is the largest polynya of the Arctic: an area that stays open or covered by thin ice in the middle of the winter sea ice. In most winters, ice coming from the north jams in the strait and forms an "ice arch". South of it, wind and currents keep pushing the ice away. The arch breaks up in early summer.

Four layers of 2026 (open one at a time):
1. 22 Mar-15 Apr, radar change: grey = unchanged: ice that did not move (jammed north of the arch) and land; colours = the polynya, where the surface keeps changing.
2. 9 Apr, surface temperature: the polynya is the warm tongue south of the arch; blue = cold, thick ice and land (sunlit slopes on land also show warm colours).
3. 9 May, true colour: the arch is still there; black = open water or very thin ice.
4. 25 Jun, true colour: the arch has broken up.

The arch's 2026 timing is read from satellite images, not from ice charts.

Method, sources and caveats: openeo-studio-scenarios, scenarios/north-water-polynya-2026/README.md

Contains modified Copernicus Sentinel data 2026, via Microsoft Planetary Computer. Landsat data courtesy of the U.S. Geological Survey.
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


HH_DB = (-24.0, -4.0)


def hh_db(day):
    """HH sigma0 (dB) of the Sentinel-1A EW pass of `day`, ~12:09 UTC (its slices mosaicked)."""
    cube = DataCube(
        graph=PGNode(
            "load_collection",
            id="sentinel-1-grd",
            spatial_extent=bounding_box,
            temporal_extent=[f"{day}T12:05:00Z", f"{day}T12:15:00Z"],
            bands=["hh"],
            properties={"sar:instrument_mode": condition("eq", "EW"), "platform": condition("eq", "sentinel-1a")},
        )
    )
    cube = cube.process("sar_backscatter", data=cube, coefficient="sigma0-ellipsoid", noise_removal=True)
    cube = cube.process("apply_pixel_selection", pixel_selection="first", data=cube)
    return cube.apply(lambda x: clip(x, 1e-4, 100).log(10) * 10)


def radar_change(days, name):
    """Red, green, blue = HH of three passes of the same orbit, each stretched to 0-255."""
    lo, hi = HH_DB
    passes = [hh_db(day).rename_labels(dimension="bands", target=[f"pass{i}"]) for i, day in enumerate(days)]
    rgb = passes[0].merge_cubes(passes[1]).merge_cubes(passes[2])
    rgb = rgb.apply(lambda x: linear_scale_range(clip(x, lo, hi), lo, hi, 0, 255)).apply("trunc")
    add_graph_to_map(rgb.save_result("PNG"), name)


def thermal(data):
    """Surface temperature (K) -> blue (below -23 C), purple (-17 C), red (-13 C), orange (-5 C), yellow (-2 C)."""
    t = data[0]
    return array_create([
        linear_scale_range(clip(t, 245, 263), 245, 263, 0, 255),
        linear_scale_range(clip(t, 258, 272), 258, 272, 0, 255),
        linear_scale_range(clip(t, 250, 262), 250, 262, 255, 0),
    ])


def surface_temperature(start, end, name):
    """One Landsat 8/9 overpass (all its scenes between start and end, UTC), ST_B10 in kelvin."""
    cube = DataCube(
        graph=PGNode(
            "load_collection",
            id="landsat-c2-l2",
            spatial_extent=bounding_box,
            temporal_extent=[start, end],
            bands=["lwir11"],
        )
    )
    cube = cube.process("apply_pixel_selection", pixel_selection="first", data=cube)
    rgb = cube.apply_dimension(dimension="bands", process=thermal).apply("trunc")
    add_graph_to_map(rgb.save_result("PNG"), name)


def no_data(data):
    """DN 0 after the backend's scale/offset: exactly -0.1 (real reflectances are above -0.0999)."""
    return array_create([data[2] < -0.09995])


def true_colour(start, end, name):
    """One Sentinel-2 L2A overpass (all its tiles between start and end, UTC), reflectance 0-1."""
    cube = DataCube(
        graph=PGNode(
            "load_collection",
            id="sentinel-2-l2a",
            spatial_extent=bounding_box,
            temporal_extent=[start, end],
            bands=["B04", "B03", "B02"],
        )
    )
    cube = cube.process("apply_pixel_selection", pixel_selection="first", data=cube)
    hide = cube.apply_dimension(dimension="spectral", process=no_data)
    rgb = cube.mask(hide).apply(lambda x: clip(x, 0, 1))
    rgb = rgb.linear_scale_range(input_min=0, input_max=1, output_min=0, output_max=255).apply("trunc")
    add_graph_to_map(rgb.save_result("PNG"), name)


OPEN_ON = 2
radar_change(["2026-03-22", "2026-04-03", "2026-04-15"],
             "22 Mar-15 Apr 2026, radar change: grey = unchanged: ice that did not move (north of the arch)"
             " and land, colour = the polynya, where the surface keeps changing")
surface_temperature("2026-04-09T18:00:00Z", "2026-04-09T18:06:00Z",
                    "9 Apr 2026, surface temperature: yellow = open water, orange to purple at sea = thin new ice,"
                    " blue = thick ice and land")
true_colour("2026-05-09T18:15:00Z", "2026-05-09T18:25:00Z",
            "9 May 2026, true colour: the ice arch, with the dark polynya south of it"
            " (open water or very thin ice)")
true_colour("2026-06-25T18:15:00Z", "2026-06-25T18:25:00Z",
            "25 Jun 2026, true colour: the arch has broken up")

# Studio draws every visible layer, later ones on top and semi-transparent (80 %, 70 %, ...), so two
# ticked layers blend: open on ONE layer and untick it before ticking the next (hidden layers fetch no
# tiles until ticked).
for i, g in enumerate(map_graphs):
    g["visible"] = i == OPEN_ON
