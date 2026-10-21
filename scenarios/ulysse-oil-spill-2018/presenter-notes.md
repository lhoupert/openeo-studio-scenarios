# Presenter notes: Ulysse oil spill, October 2018

A short script for presenting this scenario, about 2-3 minutes. The full explanation of each layer, with
methods and references, is in this scenario's [README](README.md).

Project: <https://studio.mpc.ds.io/editor/exp-ulysse-csl-virginia-oil-spill-oct-2018-sentinel-1-radar>
(opens on layer 1). Open it in a **fresh tab** and show **one layer at a time** (untick the previous one:
ticked layers blend).

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

## Practical tips

- **Zoom:** don't zoom out too far. Studio shows nothing below about map zoom 4.5.
- **Load times:** zoomed-out radar layers can take up to about 40 s the first time. Mention it, or open each
  layer once before presenting.
- **Old tabs:** if the project looks out of date, open it in a new tab, and don't Save from the old one (it
  would put the old version back).
