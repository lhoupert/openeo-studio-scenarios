"""
Exp - Larsen B 2022 fast-ice breakout and glacier retreat

For eleven years (2011-2022), sea ice frozen to the coast ("fast ice") filled the northern Larsen B embayment, on the east coast of the Antarctic Peninsula. It held back the glaciers that flow into it, and their ice tongues grew up to 16 km beyond their 2011 fronts. In late January 2022 a strong ocean swell reached the coast through a near-ice-free corridor in the north-western Weddell Sea, where sea ice was at a 12-year low. The fast ice broke out; the study of the event links the breakout to that swell. The glacier tongues broke up next. Within months three glaciers had more than doubled their speed and retreated by 11 to 25 km, calving floating and grounded ice; only grounded ice above flotation adds to sea level (no amount is given here).

Four layers (open one at a time):
1. 18 Jan 2022, true colour: before. White fast ice fills the embayment, fed by glaciers from the mountains to the west; black = open sea east of its edge.
2. 23 Jan-16 Feb 2022, radar change: red = ice there on 23 Jan, gone by 4 Feb; yellow-green = still there on 4 Feb, gone by 16 Feb. These two colours mark only part of the breakout, most clearly the large red area in the south; ice that stayed is a pale, many-coloured speckle. Black wedges inside the red = cracks open on 23 Jan. The red north-east corner is open sea (wind); colours on land and glaciers come from melting and refreezing snow, not motion.
3. 10 Feb 2022, true colour: two weeks into the breakout. Open water and floes in the east and south; the glacier tongues and the ice in front of them still hold in the west.
4. 13 Jan 2023, true colour: a year later. Open water now reaches far into the inlets where the glacier tongues were.

The ice edges and glacier fronts are read from the images, not measured. Dark, blurry patches on the ice in layers 1 and 3 are cloud shadows, not open water.

Method, sources and caveats: openeo-studio-scenarios, scenarios/larsen-b-2022/README.md

Contains modified Copernicus Sentinel data 2022-2023, via Microsoft Planetary Computer.
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
    """HH sigma0 (dB) of the Sentinel-1A IW pass of `day`, relative orbit 38, ~08:02 UTC (its 2 slices mosaicked).

    In 2021-2022 the catalogue spells `platform` "SENTINEL-1A" (upper case), so the pass is selected by
    relative orbit and mode instead.
    """
    cube = DataCube(
        graph=PGNode(
            "load_collection",
            id="sentinel-1-grd",
            spatial_extent=bounding_box,
            temporal_extent=[f"{day}T07:57:00Z", f"{day}T08:07:00Z"],
            bands=["hh"],
            properties={"sar:instrument_mode": condition("eq", "IW"), "sat:relative_orbit": condition("eq", 38)},
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


# L2A reflectances of snow and ice here reach above 1 (p90 1.15 on 18 Jan in our test renders): a 0-1
# stretch turned a quarter of the 18 Jan pixels pure white and hid the texture of the fast ice.
REFLECTANCE = (0.0, 1.25)


def no_data(data):
    """DN 0 after the backend's scale/offset: exactly -0.1 (real reflectances are above -0.0999).

    Before processing baseline 04.00 (the 18 Jan 2022 pass) there is no offset: DN 0 gives 0.0 and is not
    masked; in our renders that pass still shows no black fill, even zoomed out (see README).
    """
    return array_create([data[2] < -0.09995])


def true_colour(start, end, name):
    """One Sentinel-2 L2A overpass (all its tiles between start and end, UTC), reflectance 0-1.25."""
    lo, hi = REFLECTANCE
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
    rgb = cube.mask(hide).apply(lambda x: clip(x, lo, hi))
    rgb = rgb.linear_scale_range(input_min=lo, input_max=hi, output_min=0, output_max=255).apply("trunc")
    add_graph_to_map(rgb.save_result("PNG"), name)


OPEN_ON = 0
true_colour("2022-01-18T13:15:00Z", "2022-01-18T13:25:00Z",
            "18 Jan 2022, true colour: before, white fast ice fills the embayment"
            " (black = open water, east of its edge)")
radar_change(["2022-01-23", "2022-02-04", "2022-02-16"],
             "23 Jan-16 Feb 2022, radar change: red = ice gone by 4 Feb, yellow-green = by 16 Feb"
             " (part of the breakout only); pale speckle = ice that stayed;"
             " NE corner = open sea; land colours = snow")
true_colour("2022-02-10T13:25:00Z", "2022-02-10T13:35:00Z",
            "10 Feb 2022, true colour: two weeks into the breakout, open water (black) and floes in the"
            " east and south, glacier tongues still in the west")
true_colour("2023-01-13T13:15:00Z", "2023-01-13T13:25:00Z",
            "13 Jan 2023, true colour: a year later, open water reaches far into the inlets"
            " where the glacier tongues were")

# Studio draws every visible layer, later ones on top and semi-transparent (80 %, 70 %, ...), so two
# ticked layers blend: open on ONE layer and untick it before ticking the next (hidden layers fetch no
# tiles until ticked).
for i, g in enumerate(map_graphs):
    g["visible"] = i == OPEN_ON
