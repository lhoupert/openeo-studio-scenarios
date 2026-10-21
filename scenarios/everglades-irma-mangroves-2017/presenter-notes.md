# Presenter notes: Everglades mangroves after Hurricane Irma

A short script for presenting this scenario, about 2-3 minutes. The full explanation of each layer, with
methods and references, is in this scenario's [README](README.md).

Project: "Exp - Everglades mangroves after Hurricane Irma 2017" (not created in Studio yet; it opens on
layer 1, greenness lost). Open it in a **fresh tab** a few minutes before the talk and show **one layer at a
time** (untick the previous one: ticked layers blend).

**Hook** (opening layer, greenness lost):
- **Orient:** the southern tip of Florida, Everglades National Park. The Gulf of Mexico on the left, Florida
  Bay at the bottom, both dark grey (not classed); the dark grey inland in the north-east is sparse marsh,
  not water. A red band runs along the south shore, from Cape Sable to Flamingo.
- **Say:** "In September 2017 Hurricane Irma pushed the sea more than a metre above the ground into these
  mangrove forests. Landsat compares the dry season before the storm with the same season after it. Red is
  where the forest lost its green and had not got it back a year and a half later."

Then explain why there.

1. **Greenness lost** (already open)
   - **Show:** most of the forest is light grey: little change. "Most trees grew new leaves within a year."
   - **Say:** "Red means the greenness index fell by 0.2 or more, the drop the scientists used to flag
     dieback. In southwest Florida they counted about 10,760 hectares of dead forest, one of the largest
     mangrove diebacks on record."
2. **Ground elevation**
   - **Show:** zoom on the red band (map zoom 12, around 25.18N 81.0W), untick layer 1, tick layer 2. Point
     at the purple ground where layer 1 was red, not at the dark purple rims around the ponds (those are
     water).
   - **Say:** "Here the elevation was measured by airborne lidar. The red sat on the purple and blue ground,
     below 0 to 0.2 metres. Along the shore runs a higher strip, green and yellow: a natural ridge. The surge
     went over it and could not drain back. Like a bathtub: the sea water stayed, turned salty and toxic,
     and the trees died."
3. **22 Mar 2019, false colour**
   - **Say:** "The same place from Sentinel-2, at 10 metres. Living forest is red in this colour scheme, dead
     forest is a dull grey-green, darker than the marsh."
4. **25-26 Nov 2019, aerial photo**
   - **Show:** zoom in to map zoom 14 on the grey-green patch.
   - **Say:** "An aerial photo, 60 cm per pixel, two years after the storm: grey dead trees still standing
     around the ponds. The green crowns along the creeks grow on better-drained ground, where the study
     found that forests recovered."

**Take-home:** the wind damaged most of the mangroves of southwest Florida, but the forest died where the
ground was lowest and the sea water stayed. The scientists warn that rising seas lower the threshold for this
kind of dieback after the next hurricane.

## Practical tips

- **Zoom:** Studio shows no zoom number. Layer 4 needs at least one zoom step in from the opening view (on a
  small screen it is blank or patchy at the opening view, too many photos per map tile) and shows single
  trees three to four steps in. Zoomed out to the whole of Florida, layers 1 and 3 show only the strip around
  the scenario (by design), layer 4 is blank and layer 2 has holes in the north-west of the state.
- **Elevation outside the lidar:** east of about 80.9W, and in the north of the box east of about 81.0W, the
  elevation comes from old topographic maps, smooth and blocky, with flat marsh shown pale blue like water;
  don't read its colours there as precise. The straight north-south edge near 80.9W is where the two sources
  meet.
- **Load times:** the first view of layer 1 takes about 10 and up to 20 seconds per tile on a local copy of
  the backend (two seasons of Landsat scenes). Open the project a few minutes before, in the tab you will present from, and view each layer at
  the zooms you will show; don't reload or re-run that tab, so the tiles stay in its cache.
- **First use in production:** layers 2 (3DEP) and 4 (NAIP) have only been rendered on a local copy of the
  backend. Check them in Studio before the talk.
- **Old tabs:** if the project looks out of date, open it in a new tab, and don't Save from the old one (it
  would put the old version back).
