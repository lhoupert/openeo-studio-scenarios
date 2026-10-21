# Deep winters 2005-2018 compared

Studio project: <https://studio.mpc.ds.io/editor/exp-nw-med-deep-winters-2005-2018-compared-modis-patch>
(title "Exp - NW Med deep winters 2005-2018 compared MODIS patch"; opens on layer 8, 2013).
The background, the colour scale, the evidence for each winter and the method shared by the four projects are
in the [scenario README](../README.md).

## What it shows

The low-chlorophyll patch of every winter with known deep convection that MODIS-Aqua has seen (2005, 2006,
2009-2013, 2018), plus 2007, a winter without deep convection: one 8-day composite per winter, one sensor, one
algorithm and the same class edges, so the horizontal extent of the mixed area can be compared between winters
(in the spirit of Houpert et al. 2016, section 4.2.3 and Table 4). Layers are in time order.

**Which composite.** For each winter, the clearest composite (at least 80 % clear) at the largest proxy
< 0.25 area of the main mixing; for 2013, the week of Houpert et al. (2016, Fig. 8g). Not picked:
2012, 10-17 Feb (largest area, but 82 % clear and a residual-cloud or glint spike at LION, blue/green ratio
6.86) and 2010, 6-13 Mar (the second mixing event, 84 % clear).

## The nine layers

Areas in km² (< 0.25 / < 0.15 proxy classes), counted on tile-zoom-7 tiles over 2-9E 39.5-44.5N. "Clear" is
the share of the ocean in 2.5-8.5E 40.5-44N that the MODIS state QA flags as clear.

| # | Winter | Composite | Convection (source) | What you see | Proxy area | Clear |
|---|---|---|---|---|---|---|
| 1 | 2005 | 6-13 Mar | Deep, new deep water in March; no mooring yet (Smith et al. 2008) | The widest < 0.25 envelope of all winters 2000-2026 in our MODIS scan | 51,600 / 700 | 97 % |
| 2 | 2006 | 26 Feb-5 Mar | Deep, 2000 m on 13 Mar (Smith et al. 2008) | Its widest envelope, in two lobes | 39,600 / 2,300 | 94 % |
| 3 | 2007 | 18-25 Feb | None: gliders mixed to 400 m (Houpert et al. 2016) | No patch | 120 / 10 | 96 % |
| 4 | 2009 | 18-25 Feb | Bottom at LION 12 Feb, main mixing ends 26 Feb (Table 4) | Its widest envelope, compact around LION | 18,100 / 1,200 | 99 % |
| 5 | 2010 | 18-25 Feb | Bottom 10 Feb, ends 20 Feb (Table 4) | | 19,800 / 1,600 | 92 % |
| 6 | 2011 | 2-9 Feb | Bottom 27 Jan, a month earlier than the other years; ends 5 Feb (Houpert et al. 2016) | Its widest envelope, cloud-free | 17,300 / 3,400 | 100 % |
| 7 | 2012 | 18-25 Feb | Seabed (2350 m) on 10 Feb (Durrieu de Madron et al. 2013); ends 23 Feb (Table 4) | | 25,600 / 2,400 | 99 % |
| 8 | 2013 | 18-25 Feb | Bottom 13 Feb, ends 28 Feb (Table 4). **Opens here.** | The largest dark-purple core | 39,400 / 3,700 | 98 % |
| 9 | 2018 | 26 Feb-5 Mar | At least 1800-1900 m, about half the area of the strong years (Margirier et al. 2020; Fourrier et al. 2022) | Its largest patch; the eastern half is under cloud (46 % grey) | 24,500 / 2,500 | 80 % |

**Against the literature.** For 2009-2013 the proxy ranks the winters almost as Table 4 of Houpert et al.
(2016) does, but its areas are 1.4-1.9x smaller below 0.25 and 4.6-14x smaller below 0.15, and the box is
smaller than their domain (table in the [scenario README](../README.md)). For 2018, Margirier et al. (2020)
give 10,400-13,400 km² below 0.15 mg m⁻³ from Globcolor and ESA-CCI 8-day products. Compare the winters with
each other, not with the published km².

## How it is made

As described in the [scenario README](../README.md). This project has no ocean mask: land is drawn grey, like
cloud. Each layer reads one composite (two MODIS tiles mosaicked); tiles take about 1-3 s.

## Data

| Layer | Collection | Composite (first day = `temporal_extent` start) | Bands |
|---|---|---|---|
| 1-9 | `modis-09A1-061`, Aqua (`id` starts with `MYD09A1`) | 2005-03-06, 2006-02-26, 2007-02-18, 2009-02-18, 2010-02-18, 2011-02-02, 2012-02-18, 2013-02-18, 2018-02-26 | `sur_refl_b02`, `sur_refl_b03`, `sur_refl_b04` |

## History

- 20 Oct 2026: built; all 189 production tiles returned HTTP 200.
- 21 Oct 2026 (before this repo): the 2005 layer label was shortened by hand in Studio.
- 21 Oct 2026: short description and layer labels for non-specialists; the details moved here. Process graphs
  unchanged.
