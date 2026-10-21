# NW Mediterranean deep winters: open-ocean convection in the Gulf of Lion

Four Studio projects show, from 8-day MODIS-Aqua images, the patch of very low chlorophyll that marks the
area of deep winter mixing in the Gulf of Lion (down to 1000 m or more in strong winters), and the spring
bloom that follows. They
share one method and one colour scale, so weeks and winters can be compared.

| Project | What it shows | Layers | Opens on | Studio |
|---|---|---|---|---|
| [2013-sequence](2013-sequence/) | One winter, 8 days at a time: the patch appears, grows, shrinks, comes back, then the bloom fills it | 11 composites, 25 Jan-8 May 2013 | 25 Jan-1 Feb | [open](https://studio.mpc.ds.io/editor/exp-nw-med-deep-convection-2013-modis-8-day-sequence) |
| [deep-winters-compared](deep-winters-compared/) | The patch at its largest in every deep winter MODIS-Aqua has seen (2005-2018), and in 2007, a winter without deep convection | 9, one per winter | 2013 | [open](https://studio.mpc.ds.io/editor/exp-nw-med-deep-winters-2005-2018-compared-modis-patch) |
| [low-chl-weeks](low-chl-weeks/) | For the same winters, how many weeks each spot of sea stayed in the patch (25 Jan-21 Mar) | 9, one per winter | 2013 | [open](https://studio.mpc.ds.io/editor/exp-nw-med-deep-winters-2005-2018-low-chl-weeks-modis) |
| [recent-winters](recent-winters/) | 2019-2026 against 2013 and 2018: weaker winters, smaller or no patches | 10, one per winter | 2013 | [open](https://studio.mpc.ds.io/editor/exp-nw-med-recent-winters-2019-2026-vs-2013-and-2018-modis-patch) |

Each project folder has its `studio_script.py` (the code of the Studio project), `seed.js` (seeds the
Studio editor with it), `run_config.json` (the editor settings) and a `README.md` with the layer-by-layer
details. Figures are in [figures/](figures/).

> **Presenting this scenario?** Follow the [presenter notes](presenter-notes.md): which projects and layers
> to open, and what to say at each step (3-4 minutes).

## The story

**Deep convection.** The Gulf of Lion is one of the few places in the world ocean where the sea regularly
mixes from the surface down to the deep in winter (MEDOC Group 1970; Marshall & Schott 1999). Cold, dry
northerly winds (Mistral and Tramontane) cool the sea surface and evaporate water from it, so the surface
water becomes denser. Over the centre of the gulf, where the cyclonic circulation brings dense water close to
the surface, it becomes denser than the water below it and sinks. The mixed layer then deepens from about
100 m to 1000 m or more within weeks, and in strong winters to the seafloor (about 2300 m at the LION
mooring, 42.04N 4.68E; Houpert et al. 2016). This forms Western Mediterranean Deep Water. The main mixing
ends in February; in every deep winter of 2009-2013 a short second event followed in March (Houpert et al.
2016, Table 4).

**Why it shows from space.** The mixing spreads the phytoplankton of the surface over hundreds of metres
and takes most of it below the depth that light reaches, so the surface chlorophyll of the mixed area drops
to very low values: a patch of "intense dilution" that ocean-colour satellites see (Houpert et al. 2016,
p. 8155: "A criterion of surface chl-a < 0.15 mg.m−3 seems to be more relevant to estimate the maximal
horizontal extension of the deep convection area when cloud-free satellite images are available at the same
period as the mooring records significant vertical mixing of the water column.").

**The bloom.** When the wind drops and the surface warms, the water column restratifies and the phytoplankton
grows on the nutrients that the mixing brought up from the deep. In 2013 the bloom started at the periphery
of the mixed area about a month before its centre (2 March ± 4 days against 3 April ± 4 days), peaked on
7-9 April and gave way to summer oligotrophy in May (Mayot et al. 2017). Testor et al. (2018, p. 1759):
"Later on, in February, phytoplankton seems to develop around the Mixed Patch before the bloom in April."

**Which winters.** The table lists the winters with deep convection (below 1000 m, mostly to the seafloor)
that MODIS-Aqua (2003 onwards) has seen, with the evidence used for the labels. All quotes were checked
against the source texts.

| Winter | Evidence (exact text, source, page) |
|---|---|
| 2005 | Smith et al. 2008, abstract, p. 133: "Subsequently, new deep water was formed in March of 2005 and 2006". p. 137: "Vertical profiles on 12/3/2005 indicate the MLD reaching 2000 m". Herrmann et al. 2017, p. 1469: "known strong DWF winters: 1999, 2005, 2006, 2012, and 2013." |
| 2006 | Smith et al. 2008, p. 140-141: "By 22/1/2006 the surface water density increases to 29.104 kg m−3 (15 m) and the MLD reaches 1000 m"; "The MLD reaches 2000 m on 13/3/2006". |
| 2009, 2010 | Houpert et al. 2016, Table 4, p. 8151: mixed layer reaches the bottom on 12 Feb 2009 and 10 Feb 2010; end of vertical mixing (to 1000 m) on 26 Feb 2009 and 20 Feb 2010. |
| 2011 | Houpert et al. 2016, p. 8150: "in 2011, the vertical mixing penetrates below the LIW 1 month earlier than in 2009, 2010, 2012, and 2013 (Figure 5). On 26 December 2010, the MLD reaches already 1200 m". Table 4: bottom on 27 Jan 2011, end of mixing on 5 Feb 2011. |
| 2012 | Durrieu de Madron et al. 2013, p. 1382: "deepened rapidly to reach the seabed at 2350 m on 10 February 2012". Table 4: end of mixing on 23 Feb 2012. |
| 2013 | Houpert et al. 2016, Table 4: bottom on 13 Feb 2013, end of the main mixing on 28 Feb, second mixing event 13-17 Mar (end 21 Mar). Testor et al. 2018, p. 1759: "the surface of the Mixed Patch increases until the beginning of March reaching a maximum extent of 28 ± 3 × 10⁹ m2 late February." |
| 2018 | Margirier et al. 2020, p. 6: "triggered convection down to at least 1800 m depth"; p. 7: "Globcolor and ESA-CCI-OC-v4.2 8-day products respectively gave maximum surface areas of 13,400 km 2 and 10,400 km 2 , about half of the surface reported by Houpert et al.14 or Testor et al.15 for strong convective years." Fourrier et al. 2022, p. 10: "In 2018, intense deep convection occurred reaching at least 1,900 m". |
| 2007 (contrast) | Houpert et al. 2016, p. 8155: "The area of intense dilution (<0.15 mg.m−3) is not present in 2007 and 2008", with gliders that "recorded a maximal mixed layer of 400 m depth [Testor et al., 2007]." |

Not shown: 2000 and 2003 (reported by Somot et al. 2018, Table 1; for 2003 also an above-average altimetry
signal in Herrmann et al. 2017; neither shows a MODIS patch of 10,000 km² or more) and 2015 (disputed: Coppola et al. 2026, p. 5314, give mixing to about 1500 m; Margirier et al. 2020,
p. 6, an "absence of convection deeper than 1000 m"). Since 2014 the winter mixing has mostly been much
shallower: Coppola et al. (2026, p. 5314) "since 2014 winter mixing has been considerably weaker (300–500 m on
average, except in 2015 and 2018 when mixing reached ∼ 1500 m)". The
[recent-winters](recent-winters/) project shows 2019-2026.

## How to read the maps

The colours are classes of a chlorophyll **proxy**, the same in all projects (except the week counts of
[low-chl-weeks](low-chl-weeks/)):

| Colour | Proxy class | Reading |
|---|---|---|
| dark purple | < 0.15 | the core of the mixed patch |
| dark blue | 0.15-0.25 | the rest of the patch |
| blue | 0.25-0.35 | low |
| blue-green | 0.35-0.5 | |
| light green | 0.5-0.7 | |
| pale yellow-green | 0.7-1 | |
| pale orange | 1-1.5 | |
| light orange | 1.5-2 | |
| orange | 2-3 | bloom |
| red | 3-5 | bloom; along the coast also turbid river water (Rhône) |
| dark red | > 5 | coastal water, lagoons |
| half-transparent grey | invalid | no clear view: cloud, cloud edge, some clear pixels of the patch core, coastal lagoons; land too in deep-winters-compared and recent-winters (land is transparent in 2013-sequence; low-chl-weeks has no grey) |

- The proxy is **uncalibrated**. It follows chlorophyll (more blue = less chlorophyll) and is comparable
  between weeks and winters, because every layer uses the same satellite, algorithm and class edges. It is
  not chlorophyll in mg m⁻³: against Sentinel-3 OLCI chlorophyll (OC4ME; four MODIS 8-day vs OLCI pairs, Feb
  2022 and Feb 2023) it reads 1.2-1.4x high, so its < 0.15 and < 0.25 classes cover much less than the classes
  of Houpert et al. (2016), who used MODIS-Aqua ocean-colour chlorophyll (see the table below).
- Turbid coastal water (the Rhône plume, lagoons) also reads high, so red along the coast in winter is not
  necessarily a bloom.
- Each layer is an **8-day composite**: every pixel is the best view of that pixel over the 8 days, so
  neighbouring pixels can come from different days, and a date means "during that week".
- Studio draws the layers from about map zoom 4.5 (tile zoom 6); open one layer at a time (visible layers stack semi-transparent).

**The proxy against Table 4 of Houpert et al. (2016)** (areas in km², < 0.25 / < 0.15; proxy areas counted on
tile-zoom-7 tiles over 2-9E 39.5-44.5N, in the composites of [deep-winters-compared](deep-winters-compared/)):

| Winter (composite) | Proxy | Houpert et al. 2016, Table 4, p. 8151 |
|---|---|---|
| 2009 (18-25 Feb) | 18,100 / 1,200 | 34,162 / 16,350 |
| 2010 (18-25 Feb) | 19,800 / 1,600 | 29,180 / 13,006 |
| 2011 (2-9 Feb) | 17,300 / 3,400 | 24,111 / 15,790 |
| 2012 (18-25 Feb) | 25,600 / 2,400 | 41,616 / 17,863 |
| 2013 (18-25 Feb) | 39,400 / 3,700 | 56,351 / 23,583 |

Ranked by the < 0.25 area, the proxy gives 2013 > 2012 > 2010 > 2009 > 2011 and Table 4 gives
2013 > 2012 > 2009 > 2010 > 2011: only 2009 and 2010 swap. The Table 4 areas come from the images of their
Figure 8 (10-17 Feb 2009, 2-9 Feb 2010, 2-9 Feb 2011, 18-25 Feb 2012 and 18-25 Feb 2013). For 2009 and 2010
the composites here are one or two weeks later; on Houpert's weeks the proxy still ranks 2010 above 2009
(16,189 against 13,935 km² below 0.25). Compare the winters with each other, not with the published km².

## How the maps are made

**Data.** MODIS-Aqua 8-day surface reflectance, MYD09A1 version 6.1 (500 m), from the Planetary Computer
collection `modis-09A1-061`, read with `load_collection`:
- one composite = `temporal_extent` [its first day, first day + 1]: the catalogue search returns every
  composite that overlaps the interval, end day included, so [first day, first day + 8] would return two;
- the two MODIS tiles that cover the area (h18v04, 40-50N, and h18v05, 30-40N) are mosaicked into one image;
- Aqua only, selected by item id (`id` starts with `MYD09A1`). The Terra composites (MOD09A1) give a 2-4x
  larger low-chlorophyll area over this sea (for example 79,938 against 23,632 km² below 0.25 in winter 2018,
  and 74,638 against 26,928 km² in 2020, a winter without convection) and are much cloudier, so they are not
  mixed in. The `platform` property cannot be used: it is empty for the items of 5 Mar 2024-10 Jun 2025.

**Chlorophyll proxy.** The OC3M band-ratio polynomial (O'Reilly et al. 2000) with the MODIS coefficients
that NASA refitted on NOMAD v2 data in its 2009-2010 chlorophyll update (OC3M-547: 0.2424, -2.7423, 1.8017,
0.0015, -1.2280), applied to the ratio of the 469 nm (band 3) and 555 nm (band 4) surface reflectances.
OC3M was designed for ocean remote-sensing reflectance from dedicated ocean-colour processing, at other
wavelengths (443 or 488 over 547 nm); MOD09 surface reflectance uses a land-oriented atmospheric correction.
Hence a proxy, and uncalibrated. The colour map works directly on the ratio: each chlorophyll class edge is
converted to the ratio that OC3M maps to it.

**Clear water.** A pixel is kept when blue and green are positive and NIR (858 nm, band 2) lies between
-0.5 and 0.5 times the green reflectance. The upper bound removes cloud, haze and land; the lower bound removes
over-corrected pixels at cloud edges (NIR/green -0.8 to -2.9) that would otherwise fall into the darkest
purple class. It also removes 15-29 % of the clear pixels of the patch core, which speckles the core. In the
single-composite projects, the other pixels are drawn half-transparent grey, so that cloud gaps do not read as
the dark-purple core on the dark basemap.

**Ocean mask (2013 project only).** Only pixels that the MODIS state QA (band `sur_refl_state_500m`, bits 3-5;
MOD09 user guide, collection 6.1) flags as shallow, moderate or deep ocean are drawn; land, coastline and
inland water are transparent. The QA band is read with `load_stac` at its native resolution and warped onto
the map grid with nearest-neighbour resampling, because the smoothed overviews that `load_collection` reads
at low zoom scramble bit flags. It makes tiles about 1.8x slower. deep-winters-compared and recent-winters
draw land grey, like cloud; in low-chl-weeks land, like cloud, counts 0 weeks and is transparent.

**Clear %** (in the project READMEs) is the share of the ocean in the box 2.5-8.5E 40.5-44N that the MODIS
state QA flags as clear.

**LION mixed-layer depth.** Depths and dates quoted for the LION mooring come from Houpert et al. (2016,
Table 4) for 2009-2013, except the 2013 date of first mixing below 1000 m (27 Jan), which is ours. For other
winters they are our own analysis of the LION mooring temperature records (SEANOE, doi:10.17882/44411;
quality flags 3 and 4 masked; not published): the December-March maximum of the depth of the deepest sensor
whose potential temperature stays within 0.02, 0.03 or 0.05 °C of the median of the three shallowest sensors
(about 80-170 m deep), and with an adaptation of the double criterion of Houpert et al. (2016) (0.1 °C from
the same shallow reference instead of 10 m, then 0.01 °C from 300 m). In all four, a single sensor outside
the threshold is skipped; two in a row end the layer. Ranges give the lowest and highest of the four
estimates. The depths are sensor depths, tens to hundreds of metres apart, so they are coarse, and they may
be too shallow: for 2015 the analysis gives 347-552 m against 710 m published for LION (Margirier et al.
2020, Table 1).

## Choices and limits

- **The patch is not a depth gauge.** A low-chlorophyll patch also forms when the mixing reaches only
  500-1000 m: the proxy patch in 2015 is as large as in 2009-2011 and in 2019 about three-quarters as large,
  although LION recorded mixing mostly to 350-850 m in those winters (2019: 1090 m on a single day with the
  loosest criterion). Only in-situ data (mooring, gliders, Argo floats) tell 1000 m from 500 m. Herrmann et al. (2017)
  tie their 0.35 mg m⁻³ ocean-colour threshold to mixed layers deeper than about 500 m.
- **No maps of mixed-layer depth** are on Planetary Computer (no ocean model, no temperature profiles); they
  would have to come from an ocean reanalysis (for example CMEMS MEDSEA_MULTIYEAR_PHY_006_004).
- **LION is one point** in the middle of the convection area, and it starts in 2007: 2005 and 2006 rest on
  Argo floats at the edges of the map (Catalan and Ligurian subbasins), not at LION, and 2000 m was their
  deepest profiling level.
- **Cloud** hides part of some composites (2018 most of all), and the clear-water test speckles the core.
- **Other sensors** were tried and left out: Sentinel-2 and Landsat 8/9 only give single days and their
  blue/green index is relative within a day (and Sentinel-2 starts in 2015, Landsat 8 on 22 Mar 2013, after
  the 2013 mixing); Landsat 5/7 do not follow MODIS-Aqua over this sea; sea-surface temperature at 0.25° does
  not resolve the patch; Sentinel-3 OLCI files cannot be rendered by the backend.

## References

All DOIs checked on Crossref (SEANOE and NASA LP DAAC datasets on doi.org).

Deep convection and the winters:
- Coppola et al. (2026), Earth Syst. Sci. Data 18, 5303-5327, <https://doi.org/10.5194/essd-18-5303-2026>
- Durrieu de Madron et al. (2013), Geophys. Res. Lett. 40, 1379-1385, <https://doi.org/10.1002/grl.50331>
- Fourrier et al. (2022), J. Geophys. Res. Oceans 127, e2022JC018615, <https://doi.org/10.1029/2022JC018615>
- Herrmann et al. (2017), J. Geophys. Res. Oceans 122, 1457-1475, <https://doi.org/10.1002/2016JC011833>
- Houpert et al. (2016), J. Geophys. Res. Oceans 121, 8139-8171, <https://doi.org/10.1002/2016JC011857>
- Margirier et al. (2020), Sci. Rep. 10, 20923, <https://doi.org/10.1038/s41598-020-77859-5>
- Marshall & Schott (1999), Rev. Geophys. 37, 1-64, <https://doi.org/10.1029/98RG02739>
- MEDOC Group (1970), Nature 227, 1037-1040, <https://doi.org/10.1038/2271037a0>
- Smith, Bryden & Stansfield (2008), Ocean Sci. 4, 133-149, <https://doi.org/10.5194/os-4-133-2008>
- Somot et al. (2018), Clim. Dyn. 51, 1179-1210, <https://doi.org/10.1007/s00382-016-3295-0>
- Testor et al. (2018), J. Geophys. Res. Oceans 123, 1745-1776, <https://doi.org/10.1002/2016JC012671>

The bloom:
- D'Ortenzio et al. (2014), Geophys. Res. Lett. 41, 6443-6451, <https://doi.org/10.1002/2014GL061020>
- Lavigne et al. (2013), J. Geophys. Res. Oceans 118, 3416-3430, <https://doi.org/10.1002/jgrc.20251>
- Mayot et al. (2016), Biogeosciences 13, 1901-1917, <https://doi.org/10.5194/bg-13-1901-2016>
- Mayot et al. (2017), J. Geophys. Res. Oceans 122, 9999-10019, <https://doi.org/10.1002/2016JC012052>

Data and methods:
- LION mooring, SEANOE, <https://doi.org/10.17882/44411>
- MYD09A1 v6.1: Vermote, E. (2021), NASA LP DAAC, <https://doi.org/10.5067/MODIS/MYD09A1.061>; MOD09 user guide
  (collection 6.1), <https://lpdaac.usgs.gov/documents/925/MOD09_User_Guide_V61.pdf>
- O'Reilly et al. (2000), SeaWiFS Postlaunch Calibration and Validation Analyses, Part 3, NASA Tech. Memo.
  2000-206892, Vol. 11 (no DOI)
- NASA Ocean Biology Processing Group, chlorophyll algorithm update OCv6 (2009-2010 reprocessing), OC3M-547
  coefficients; the original page (oceancolor.gsfc.nasa.gov/reprocessing/r2009/ocv6/) is no longer online

## Credits

MODIS-Aqua surface reflectance (MYD09A1 v6.1), NASA LP DAAC, via Microsoft Planetary Computer. LION mooring
data: SEANOE (doi:10.17882/44411).
