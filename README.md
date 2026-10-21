# openEO Studio scenarios

Worked examples for [openEO Studio](https://studio.mpc.ds.io) on Microsoft Planetary Computer
(backend: titiler-openeo at <https://openeo.mpc.ds.io>). Each scenario tells one Earth-observation story
in 3-4 map layers, each layer showing something different, with every method backed by peer-reviewed
references. The Studio project carries a short description; the scenario README here has the details.

| Scenario | Story | Layers | Studio project |
|---|---|---|---|
| [ulysse-oil-spill-2018](scenarios/ulysse-oil-spill-2018/) | Oil spill after the Ulysse / CSL Virginia collision off Cap Corse, Oct 2018 | Sentinel-1 radar (x3, one grey scale) | [open](https://studio.mpc.ds.io/editor/exp-ulysse-csl-virginia-oil-spill-oct-2018-sentinel-1-radar) |
| [north-water-polynya-2026](scenarios/north-water-polynya-2026/) | The North Water polynya and its ice arch, Mar-Jun 2026 | Sentinel-1 radar change, Landsat 9 temperature, Sentinel-2 true colour (x2) | [open](https://studio.mpc.ds.io/editor/exp-north-water-polynya-2026-sentinel-1-radar) |
| [nw-med-deep-winters](scenarios/nw-med-deep-winters/) | Winter deep convection in the Gulf of Lion and the bloom that follows, 2005-2026 | MODIS-Aqua 8-day chlorophyll proxy, four projects of 9-11 layers | [2013](https://studio.mpc.ds.io/editor/exp-nw-med-deep-convection-2013-modis-8-day-sequence), [compared](https://studio.mpc.ds.io/editor/exp-nw-med-deep-winters-2005-2018-compared-modis-patch), [weeks](https://studio.mpc.ds.io/editor/exp-nw-med-deep-winters-2005-2018-low-chl-weeks-modis), [recent](https://studio.mpc.ds.io/editor/exp-nw-med-recent-winters-2019-2026-vs-2013-and-2018-modis-patch) |

## What is in a scenario

- `README.md`: the story, how to read each layer, how it is made, the published method behind it,
  limits, data and references.
- `studio_script.py`: the Python code of the Studio project. Studio wraps it with its own loader, which
  defines `DataCube`, `PGNode`, `bounding_box`, `add_graph_to_map`, `map_graphs` and a few openEO
  processes. Each `add_graph_to_map(...)` call is one map layer; the last block sets the layer the map
  opens on.
- `seed.js`: the same script and editor settings as a snippet for the browser console (made with
  `tools/make_js.py`).
- `run_config.json`: the editor settings (collection, bands, time, bounding box) used for local tests.
- `presenter-notes.md`: a 2-3 minute script for presenting the scenario (opening layer, what to show and
  say at each step).
- `figures/`: the layers rendered tile by tile.

A scenario told with several Studio projects (`nw-med-deep-winters`) has one subfolder per project, each with
its own `studio_script.py`, `seed.js`, `run_config.json` and `README.md`; the shared story, method and
references, the presenter notes and the figures sit in the scenario folder.

## Create or update a Studio project

1. Open <https://studio.mpc.ds.io>, log in and check "My projects": Save stores the project under the
   kebab-case title, so a new title creates a project and the same title overwrites one without warning.
2. Either paste `studio_script.py` into the editor and set the editor's collection, time and bounding box
   from `run_config.json`, or paste `seed.js` in the browser console of the Studio tab and open
   <https://studio.mpc.ds.io/editor>.
3. Click Save **without panning or zooming the map first**: the map view at Save becomes the project's
   saved bounding box (its opening view and the extent of shared links).
4. Check the tiles (browser developer tools, Network, filter `/tiles/`): 200 = rendered, 404 = no data
   there (outside a satellite swath), anything else = read the response body.
5. Use one Studio tab at a time: tabs share the editor's map services and can wipe each other's tiles.

To regenerate a seed after editing a script:

```sh
python tools/make_js.py scenarios/<name>/studio_script.py "<Studio title>" <collection> <start> <end> W,S,E,N <band> [<band> ...] > scenarios/<name>/seed.js
```

The arguments for each scenario are its title and the values in its `run_config.json`.

## Backend notes (titiler-openeo, commit c9b6ee3, October 2026)

- Each layer is computed tile by tile (256 x 256 px tiles, from tile zoom 6, which Studio reaches at map
  zoom 4.5); hidden layers fetch nothing until ticked, and visible layers stack at decreasing opacity
  (0.8, 0.7, ...), so open one at a time.
- Sentinel-1 GRD: `sar_backscatter` supports `beta0`, `sigma0-ellipsoid` and `gamma0-ellipsoid` only
  (always pass `coefficient`); noise removal clamps the darkest pixels to 0, so floor the values before
  `log`. Filter on `platform` and `sar:instrument_mode` and use a time window of the pass time +/- 5 min to
  get exactly one pass.
- Sentinel-1 RTC (`sentinel-1-rtc`) is terrain-corrected gamma0 in linear power; Planetary Computer
  documents it as account-only, but anonymous access works at the time of writing.
- Tiles along the seam between two Sentinel-1 GRD slices can come back blank when zoomed in: the STAC
  search uses the tile bounds only, and the catalogue footprints stop short of the data.
- Sentinel-2 files on Planetary Computer often carry no no-data flag: mask the value that no-data takes
  after the backend's scale and offset (exactly -0.1).

## Credits and licences

Copernicus Sentinel data (modified), Landsat data courtesy of the U.S. Geological Survey, MODIS data from
NASA LP DAAC, and Sentinel-1 RTC processing by Catalyst (CC BY 4.0), all via Microsoft Planetary Computer;
LION mooring data from SEANOE. See each scenario for details. Developed with AI assistance (Claude Code).
