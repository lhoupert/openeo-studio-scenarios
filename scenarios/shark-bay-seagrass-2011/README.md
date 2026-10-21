# Shark Bay seagrass and the 2010-11 marine heatwave

Studio project (not created yet): title "Exp - Shark Bay seagrass loss 2011 heatwave Landsat", which Studio will
save as <https://studio.mpc.ds.io/editor/exp-shark-bay-seagrass-loss-2011-heatwave-landsat>.
Files: `studio_script.py` (the code pasted in Studio), `seed.js` (seeds the Studio editor with it),
`run_config.json` (the editor settings used for local tests).
Status: every layer rendered on a local copy of the backend (titiler-openeo c9b6ee3, the production commit)
against Planetary Computer; nothing has been rendered in production yet.

> **Presenting this scenario?** Follow the [presenter notes](presenter-notes.md): the layer to open
> with, then what to show and what to say at each step (2-3 minutes).

## Shark Bay and the heatwave

Shark Bay, a World Heritage Area on the coast of Western Australia, is a shallow bay of seagrass banks cut by
channels. It has "the largest C stock reported for a seagrass ecosystem" (Arias-Ortiz et al. 2018). "An
extreme MHW occurred across the Western Australian coastline in the austral summer of 2010–2011, exposing
marine communities to summer seawater temperatures 2–5°C warmer than average" (Strydom et al. 2020; MHW =
marine heatwave; its rise and fall off Western Australia: Pearce & Feng 2013).
Strydom et al. (2020) mapped the bay before (2002 and 2010) and after (2014 and 2016) and found "the single
largest loss in dense seagrass extent globally (1,310 km2) following an acute disturbance", "with the most
extensive declines occurring in the Western Gulf, Wooramel Bank and Faure Sill". Their ground truthing (622
points) showed the change was mostly a loss of the seagrass *Amphibolis antarctica* rather than *Posidonia
australis*. Arias-Ortiz et al. (2018) "estimate that 36% of Shark Bay's seagrass meadows were damaged" and
that "between 2 and 9 Tg CO2 could have been released to the atmosphere during the following three years" from
the exposed sediment: a warming-driven extreme that turns a carbon sink into a source.

The four layers use the same satellites as the published maps: Landsat 5 TM before the heatwave and Landsat 8
OLI after it (Arias-Ortiz et al. 2018), plus Landsat 5's thermal band during it.

![The four layers at tile zoom 10](figures/layers_zoom10.png)

*The four layers at tile zoom 10 (Studio map zoom ~9, the opening view), rendered on a local copy of the
backend (identical to production). Layer 2 exists only in the east of the bay: the satellite's swath that day
missed the rest.*

![The Faure Sill and Hamelin Pool at tile zoom 11](figures/faure_sill_zoom11.png)

*Zoom on the Faure Sill and Hamelin Pool (tile zoom 11, Studio map zoom ~10), where the change is clearest and
where layer 2 has data.*

## The four layers

### 1. 12 May 2010: before (Landsat 5) (opens here)

- **What you see:** the bay in true colour, about seven months before the heatwave summer. On the shallow
  banks, **dark green to black patches** are dense seagrass meadows; the **long dark fingers** cutting across the
  banks are channels (deeper water); **bright turquoise** is bare or sparsely covered sand in shallow water; deep
  water is **black**; the land (Peron Peninsula in the middle, the mainland to the east, Faure Island in the
  eastern gulf) is orange and saturated. The meadows are clearest on the Wooramel Bank
  (along the east shore) and on the Faure Sill (the banks and channels between Faure Island and the mainland).
- **How it is made, for non-specialists:** Landsat measures how much sunlight each 30 m patch of the surface
  reflects in red, green and blue light; put together, they make a normal colour photo. In clear, shallow
  water the light reaches the bottom and comes back: bare sand reflects a lot, seagrass absorbs most of it,
  so meadows look dark on bright sand. Deeper water lets less light come back from the bottom, so depth also
  darkens the picture.
- **Method:** Shark Bay's seagrass was mapped with "a supervised classification of imagery captured by
  Landsat–5 Thematic Mapper (TM) in 2002 and Landsat–8 Operational Land Imager (OLI) in 2014", at 30 m, in three
  classes: dense seagrass (more than 40 % cover), sparse seagrass (less than 40 %) and other (Arias-Ortiz et al.
  2018). Strydom et al. (2020) used 2010 as their second "before" year. This layer shows the 2010 picture the
  classification would start from; it does not classify it (Studio cannot train the paper's classifier).
- **Technical chain:** `load_collection("landsat-c2-l2", bands=["red", "green", "blue"])` filtered on
  `platform = landsat-5`, 12 May 2010 02:10-02:16 UTC (2 scenes of one overpass, path 115 rows 77-78) ->
  `apply_pixel_selection("first")` (mosaic) -> mask pixels whose blue is exactly -0.2 (DN 0 = no data after the
  backend's scale and offset; the test is `< -0.19999`, and DN 1 is -0.1999725) -> clip reflectance 0-0.15 ->
  stretch to 0-255.

### 2. 21 Mar 2011: the heatwave, water temperature against the same week of other years

- **What you see:** the east of the bay only (Hamelin Pool and the eastern Faure Sill; see Choices and limits),
  coloured by how much warmer the water was on 21 Mar 2011 than on average over the same week in 2004, 2005
  and 2007. One colour step = 1 C; **white** = within 0.5 C of usual; **salmon** = 0.5-1.5 C warmer, **light red**
  = 1.5-2.5 C, **red** = 2.5-3.5 C, **dark red** = 3.5-5.5 C; blues would be colder; differences beyond 5.5 C
  either way are left uncoloured (edge effects, see Choices and limits). Almost all of it is light red to red:
  over Hamelin Pool the water was 2-3 C warmer, on the Faure Sill 1-2 C (our reading of the classes). In our
  count at tile zoom 11, 91 % of the water pixels are 1.5-3.5 C warmer and 99 % are more than 0.5 C warmer. The
  water itself read about 28-29 C over Hamelin Pool, against about 24-25 C (2004), 27-28 C (2005) and 25-26 C
  (2007) (our reading). Thin horizontal lines are the striping of Landsat 5's thermal sensor; land and cloud are
  left uncoloured.
- **How it is made, for non-specialists:** everything warm glows in thermal infrared, which Landsat 5 measures
  at the same time as the colour picture, in coarser pixels (thermal band measured at 120 m, served at 30 m).
  Planetary Computer serves it already converted to a surface temperature in kelvin. One picture of warm water
  in summer does not say whether it is unusually warm, so the layer subtracts the average of three pictures of
  the same place taken in the same week of other years (17 Mar 2004, 20 Mar 2005, 26 Mar 2007), all at the same
  time of day (10:06 local time in 2011, the references within 11 minutes of it): what remains is how much
  warmer 2011 was.
- **Method:** Landsat Collection 2 surface temperature comes from per-pixel atmospheric compensation of the
  thermal band, with ancillary emissivity data (Cook et al. 2014). The heatwave brought "summer seawater
  temperatures 2–5°C warmer than average", and the loss of seagrass was largest "when degree heating weeks
  (DHWm) was ≥10 and the number of days exposed to extreme sea surface temperature during the MHW (DaysOver)
  was ≥94" (Strydom et al. 2020): both are measures of heat above the usual. This layer is a one-day snapshot
  of that excess at the end of the austral summer, not the paper's accumulated heat stress, and its "usual" is
  three days, not a climatology (our computation).
- **Technical chain:** for 21 Mar 2011 and each reference date, `load_collection("landsat-c2-l2",
  bands=["lwir", "nir08"])` filtered on `platform = landsat-5`, overpass time +/- 2-3 min (path 114, rows 78-79;
  7 scenes in all) -> `apply_pixel_selection("first")` -> keep `lwir` (ST_B6, kelvin) and mask where `nir08` >= 0.05
  (land and cloud) -> mean of the three references (`merge_cubes` adding them, then / 3) -> 2011 minus that mean
  (`merge_cubes` with a subtracting resolver) -> `colormap` in 1 C classes centred on 0, from -5.5 to +5.5 C
  (values outside: no colour).

### 3. 10 Jul 2014: after (Landsat 8)

- **What you see:** the same view, more than three years after the heatwave. Many banks that were dark in 2010
  are lighter, most clearly on the Faure Sill, where the dark green banks between the channels turned bright
  turquoise while the channels themselves (the long dark fingers) kept their shape, and on parts of the Wooramel
  Bank. Compare with layer 1 by ticking one, then the other.
- **How it is made:** as layer 1, from Landsat 8 (whose bands are narrower but cover the same colours), on an
  overpass of the same orbit track as layer 1, at a similar sun height (32 degrees, against 36 degrees on 12 May
  2010).
- **Method:** as layer 1; 2014 is the "after" year of both papers (Arias-Ortiz et al. 2018; Strydom et al. 2020).
- **Technical chain:** as layer 1, filtered on `platform = landsat-8`, 10 Jul 2014 02:19-02:25 UTC (2 scenes,
  path 115 rows 77-78).

### 4. 2010 to 2014: change in green brightness over water

- **What you see:** water only, coloured by how much brighter (2014 minus 2010) it is in green light. **Brown** =
  brighter in 2014 (from light, +0.005 to +0.01 in reflectance, to dark brown, more than +0.03): seagrass thinned
  or lost, exposing sand. **White** = within 0.005: unchanged. **Teal** = darker in 2014. The Faure Sill is broadly
  brown, with its channels as white streaks through it; the Wooramel Bank has brown patches; the shallow shores
  of Hamelin Pool are fringed with brown (lost seagrass or a lower tide: the layer cannot tell them apart); the
  north of the Western Gulf, west of Peron Peninsula, is broadly light to mid brown too (see Choices and
  limits); the deep basins and the south of the Western Gulf are white to light teal. In our count over the
  opening view, 46 % of the water is unchanged, 31 % brighter (19 % by more than 0.01) and 23 % darker (4.5 % by
  more than 0.01).
- **How it is made, for non-specialists:** layer 3 minus layer 1, in green light only, where both dates are water
  (land, cloud and sand that dries at low tide are left out because they reflect near-infrared light, which
  water absorbs). Green light reaches the bottom well in shallow water, so a meadow replaced by sand makes the
  water look brighter.
- **Method:** where the bottom is visible, a meadow's loss shows as a brighter bottom: the published maps used
  this contrast in a supervised classification of the same two sensors (Arias-Ortiz et al. 2018). This layer
  is a plain difference, not that classification. Water is defined by its low near-infrared reflectance, the
  contrast the NDWI uses (McFeeters 1996); the 0.05 threshold is ours. Landsat 7 and 8 surface reflectances
  differ on average, and the atmospheric correction makes the mean difference larger in the visible bands
  (Roy et al. 2016), so a small offset between Landsat 5 and 8 is expected: in our check the median difference
  over all water is +0.0005 and over the darkest water -0.002, inside the white class, so no correction is
  applied.
- **Technical chain:** for each overpass of layers 1 and 3, `load_collection(bands=["green", "nir08"])` ->
  `apply_pixel_selection("first")` -> bands renamed `green0`/`nir0` and `green1`/`nir1` -> `merge_cubes` (4 bands) ->
  where `nir0` and `nir1` < 0.05 and both greens have data: `green1 - green0`, elsewhere -99 (no colour) ->
  `colormap` (classes at +/-0.005, 0.01, 0.02, 0.03).

## Choices and limits

- **The change layer is relative, not a seagrass map.** It compares two different sensors, processed with
  different atmospheric corrections, on two days with different tides and water clarity. The tide at the two
  overpasses was not checked: on the shallowest sand, brighter water can mean a lower tide rather than lost
  seagrass (the brightest 2010 water, green above 0.06, is on average 0.008-0.014 brighter in 2014; our
  computation). Teal in the deep basins most likely reflects clearer water, not new meadows. Even the
  published maps have gaps: "The entire extent was not mapped due to poor image quality caused by depth and
  water clarity and the lack of data in some areas" (Arias-Ortiz et al. 2018).
- **The Western Gulf** (west of Peron Peninsula), one of the three areas with the largest published losses; the
  box covers only its eastern half. In layer 4 its northern part is broadly light to mid brown, as much as the
  Faure Sill: 72 % of its water is brighter, 49 % by more than 0.01, against 71 % and 53 % on the Faure Sill and
  29 % and 11 % on the Wooramel Bank. Its southern part (Freycinet) is white to light teal: 18 % brighter, 37 %
  darker (our counts at tile zoom 11). The 2014 water there also looks bluer overall (by eye), so clearer or
  different water may explain part of the brown: the layer cannot separate lost seagrass from water clarity or tide.
- **Layer 2 covers only the east of the bay.** Landsat 5's orbit tracks over Shark Bay are path 115 (99 % of the
  box) and path 114 (about a third of it, mostly land). Planetary Computer has no Landsat 5 scene of path 115
  between 1 January and 28 April 2011 (the next one is 29 Apr, Tier 2), and the clear Landsat 7 scenes of
  path 115 (4 and 20 Mar 2011) have the data gaps of Landsat 7's failed scan-line corrector (since 2003), so
  they are not used. The 21 Mar 2011 scenes have 5-7 % cloud, masked with land.
- **Layer 2's swath edge.** Along the west edge of the 21 Mar 2011 swath, the temperature over- and undershoots
  by up to tens of degrees in a comb of small hooks, probably where the 120 m thermal band was resampled to 30 m
  next to the no-data area. Differences beyond 5.5 C either way are therefore left uncoloured: at tile zoom 11
  that is 1.4 % of the water pixels, 88 % of them within 8 pixels (about 550 m) of the swath edge and most of
  the rest next to coasts and cloud; away from those, 99.8 % of the differences lie between +0.4 and +3.8 C (our
  computation). The comb's outline and a few dark pixels at its tips remain.
- **Three reference days are not a climatology.** Each day's skin temperature also depends on that day's wind,
  sun and tide, and the three references span 3 C between them. The references were chosen as the only clear
  Landsat 5 scenes of the same track within 6 days of 21 Mar and 15 minutes of its overpass time (the
  satellite's overpass time drifted from 01:26 to 02:11 UTC over the years); the other clear scenes within
  6 days of 21 Mar (1988-1995) were taken 20-40 minutes earlier in the morning and are left out.
- **Landsat 5 2002, the papers' other "before" year, is not used:** Planetary Computer has no Landsat 5 scene of
  2002 with less than 10 % cloud over the box; 2010 is Strydom et al.'s second "before" year.
- **One overpass per layer.** Both optical dates come from path 115, which covers 99 % of the box, so each
  layer is one moment in time. The 12 May 2010 scene of row 78 is Tier 2 (its geometric model error is 17 m, above
  the 12 m Tier 1 limit; its verification error is 1.6 m): fine for 30 m pixels.
- **A comb along the east edge of layer 1,** over land in the south-east of the box: at the zoom levels Studio
  uses, the scene's edge pixels are probably mixed with the no-data fill, so their blue and green drop below zero
  (down to -0.1; elsewhere in the opening view every band is above +0.002, our check) and they show red to
  black. Hiding them would need a threshold that also hides real dark pixels of the 2014 Landsat 8 scene (its
  red and blue go down to -0.1 and -0.16 in places), so they are left as they are; the bay is not affected.
- **Colour scales:** reflectance 0-0.15 keeps the banks and channels readable and saturates land. Change and
  temperature classes are fixed, so the same colour means the same number everywhere.
- **Load times** (three local runs, median per tile at tile zoom 10 / 11): true colour 0.6-2.2 s, change 1-1.6 s,
  temperature 2-6 s (four overpasses per tile) and up to 13 s, even for tiles that come back fully transparent;
  the first tile from a freshly started server took 14-19 s. Temperature tiles west of the path-114 swath
  answer 404 (no data), which Studio shows as empty map.

## Data

| Layer | Collection | Time window (UTC) | Bands |
|---|---|---|---|
| 1 | `landsat-c2-l2` (Landsat 5, path 115) | 2010-05-12 02:10-02:16 | red, green, blue |
| 2 | `landsat-c2-l2` (Landsat 5, path 114) | 2011-03-21 02:04-02:09; references 2004-03-17 01:53-01:59, 2005-03-20 02:01-02:07, 2007-03-26 02:09-02:15 | lwir, nir08 |
| 3 | `landsat-c2-l2` (Landsat 8, path 115) | 2014-07-10 02:19-02:25 | red, green, blue |
| 4 | `landsat-c2-l2` (Landsat 5 and 8, path 115) | as layers 1 and 3 | green, nir08 |

Scenes: LT05_L2SP_115077_20100512_02_T1, LT05_L2SP_115078_20100512_02_T2; LT05_L2SP_114078_20110321_02_T1,
LT05_L2SP_114079_20110321_02_T1, LT05_L2SP_114078_20040317_02_T1, LT05_L2SP_114078_20050320_02_T1,
LT05_L2SP_114079_20050320_02_T1, LT05_L2SP_114078_20070326_02_T1, LT05_L2SP_114079_20070326_02_T1;
LC08_L2SP_115077_20140710_02_T1, LC08_L2SP_115078_20140710_02_T1.

## References

Every DOI checked on Crossref.
- Arias-Ortiz et al. (2018), Nature Climate Change 8, 338-344, <https://doi.org/10.1038/s41558-018-0096-y>
- Cook, Schott, Mandel & Raqueno (2014), Remote Sens. 6, 11244-11266, <https://doi.org/10.3390/rs61111244>
- McFeeters (1996), Int. J. Remote Sens. 17, 1425-1432, <https://doi.org/10.1080/01431169608948714>
- Pearce & Feng (2013), J. Mar. Syst. 111-112, 139-156, <https://doi.org/10.1016/j.jmarsys.2012.10.009>
- Roy et al. (2016), Remote Sens. Environ. 185, 57-70, <https://doi.org/10.1016/j.rse.2015.12.024>
- Strydom et al. (2020), Global Change Biology 26, 3525-3538, <https://doi.org/10.1111/gcb.15065>

## Credits

Landsat data courtesy of the U.S. Geological Survey, via Microsoft Planetary Computer.
