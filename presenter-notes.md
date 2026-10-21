# Presenter notes

A short script for presenting each scenario, about 2-3 minutes each. Open each project in a **fresh tab**,
show **one layer at a time** (untick the previous one: ticked layers blend), and allow a few seconds for the
first load.

## Ulysse oil spill (opens on layer 1)

Project: <https://studio.mpc.ds.io/editor/exp-ulysse-csl-virginia-oil-spill-oct-2018-sentinel-1-radar>

**Hook** (map as it opens, Corsica and the Ligurian Sea): "On 7 Oct 2018, just after 7 am, the ferry Ulysse
rammed the container ship CSL Virginia, anchored about 28 km north of Cap Corse. Fuel poured into the sea.
Can satellites follow the slick?"

1. **9 Oct, radar** (opening layer)
   - **Show:** the bright dot north of Cap Corse, which is the two ships, still locked together. Then trace
     the dark line running west-north-west for about 60 km and curling north at its end.
   - **Say:** "Radar measures how rough the sea is. Oil calms the small waves, so a slick shows up dark.
     Radar works through cloud and at night."
   - **Then point to** the big diffuse dark patch south-east of the ships: "Not every dark patch is oil.
     That one is calm water with no wind. Sharp edges are the clue."
2. **9 Oct, optical, 7 hours earlier**
   - **Show:** zoom right in on the ships, to map zoom 11 or more; the streak is invisible when zoomed out.
     A dashed bright streak leaves the ships along the same path.
   - **Say:** "A second satellite, using sunlight rather than radar, sees the same slick. Two independent
     sensors agree."
3. **13 Oct, automatic detection**
   - **Show:** zoom back out and look north-west of the ships, around 43.6N 8.8E. Orange marks the drifting
     fragments.
   - **Say:** "An algorithm flags patches much darker than their surroundings. It finds the fragments, but
     also flags the coasts, where land shelters the sea from the wind. Automation sorts the candidates; a
     person still has to judge them."
4. **19 Oct, off the Var**
   - **Show:** pan west to the sea off Saint-Tropez. Sharp dark fragments lie 30-60 km offshore.
   - **Say:** "Oil had been reaching the Var beaches since 16 Oct. These are probably more of it, but in
     light wind radar alone can't confirm it."

**Take-home:** radar followed the spill for two weeks, whatever the weather; optical imagery confirmed it;
automatic detection helps but needs checking.

## North Water polynya (opens on layer 3, the 9 May picture)

Project: <https://studio.mpc.ds.io/editor/exp-north-water-polynya-2026-sentinel-1-radar>

**Hook** (opening layer, 9 May true colour):
- **Orient:** Ellesmere Island on the left, Greenland on the right. Everything is white ice, except a black
  tongue down the middle, ending in a sharp curved edge at the top.
- **Say:** "This is the North Water, the largest polynya in the Arctic: open water or thin ice in the
  middle of the winter sea ice. That curved edge is an ice arch. Ice coming from the north jams there like a
  cork in a bottle. South of it, wind and currents keep pushing the ice away."

Then go back in time.

1. **22 Mar-15 Apr, radar change**
   - **Say:** "How do we know the ice north of the edge is stuck? Radar works in the polar night. Here we
     stack three radar images taken 12 days apart, as red, green and blue."
   - **Show:** "Grey means identical on all three dates: the ice didn't move. Colour means the surface
     changed, which is the polynya. The line between grey and colour is the arch."
2. **9 Apr, surface temperature**
   - **Say:** "Landsat measures surface temperature."
   - **Show:** a warm tongue that starts at the arch. Yellow, about -2 C, is open water; orange to purple is
     thin new ice; blue is thick ice and land below about -23 C.
   - **Say:** "Open water in the middle of an Arctic winter loses heat to the air, far more than the ice
     around it."
3. **9 May, true colour:** back to the opening picture, the same arch at the same place, now seen in
   daylight.
4. **25 Jun, true colour**
   - **Show:** the edge is gone, open water reaches further north and floes drift south.
   - **Say:** "The arch breaks up every summer, usually in June or July."

**Take-home:** three satellites, each answering a different question: is the ice moving (radar)? Is the
surface warm (thermal)? What does it look like (optical)? The 2026 dates come from these images alone.

## Practical tips

- **Zoom:** don't zoom out too far. Studio shows nothing below about map zoom 4.5.
- **Load times:** the first view of North Water's radar-change layer takes about 10 seconds, and zoomed-out
  Ulysse radar layers can take up to about 40 s the first time. Mention it, or open each layer once before
  presenting.
- **Old tabs:** if a project looks out of date, open it in a new tab, and don't Save from the old one (it
  would put the old version back).

The full explanation of each layer, with methods and references, is in each scenario's README.
