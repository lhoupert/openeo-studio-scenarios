# Presenter notes: Larsen B, 2022

A short script for presenting this scenario, about 2-3 minutes. The full explanation of each layer, with
methods and references, is in this scenario's [README](README.md).

Project: "Exp - Larsen B 2022 fast-ice breakout and glacier retreat" (not saved in Studio yet; it opens on
layer 1, the 18 Jan 2022 picture). Open it in a **fresh tab** and show **one layer at a time** (untick the
previous one: ticked layers blend).

**Hook** (layer 1, the opening layer, 18 Jan 2022 true colour):
- **Orient:** the mountains of the Antarctic Peninsula on the left (west), the Weddell Sea on the right (east).
  The flat white-grey surface filling the bay is sea ice frozen to the coast, called fast ice. Glaciers come
  down from the mountains into it. The black strip on the right is open sea.
- **Say:** "This is the Larsen B embayment in January 2022. That sea ice had been frozen in place for eleven
  years, since 2011. It acted like a doorstop: the glaciers behind it slowed down and pushed ice tongues up to
  16 kilometres out into the bay."

Then watch it go.

2. **23 Jan-16 Feb, radar change** (layer 2)
   - **Say:** "In late January a strong ocean swell reached the coast. In the north-western Weddell Sea, sea ice
     was at a 12-year low, which left the waves a near-ice-free corridor to the coast, and the scientists who
     studied the event link the breakout to that swell. Radar sees through cloud. Here we stack three radar
     images from the same orbit, 12 days apart, as red, green and blue."
   - **Show:** the large red area in the south = ice that was there on 23 January and gone by 4 February; the
     yellow-green patches east of it = still there on 4 February, gone by 16 February. "You can see the breakout
     happen in two steps." Ice that stayed is the pale, many-coloured speckle in the centre.
   - **Caveat:** point only at the large red and yellow-green areas: not all the ice that left turned red or
     yellow (elsewhere it is purple or speckled), and the ice that stayed is not flat grey. "The red top-right
     corner is open sea roughened by wind, not ice. The colours on the mountains are melting snow, not moving
     ice." Show this layer at the opening zoom only: one step closer it is mostly speckle.
3. **10 Feb, true colour** (layer 3)
   - **Show:** half the bay is now open water (black) with floes; the glacier tongues in the west still hold
     (the dark, blurry patch on the tongue is a cloud shadow, not water).
   - **Say:** "Two weeks in, most of the doorstop is gone. What is left in front of the glacier tongues goes
     next."
4. **13 Jan 2023, true colour** (layer 4)
   - **Show:** open water reaching far into the inlets on the west side. Zoom in one step on the western half
     and switch between this layer and the 10 Feb one: the pale tongue in the middle is gone.
   - **Say:** "Within months the three main glaciers more than doubled their speed and retreated by 11 to 25
     kilometres, calving floating and grounded ice. The grounded part can add to sea level once it reaches the
     ocean; floating ice doesn't, and the studies cited here don't give an amount."

**Take-home:** a near-ice-free corridor let the swell in, the fast ice broke out after it arrived (the study
of the event links the two), and without it the glaciers sped up and retreated. Optical images show what it
looked like; radar shows when it changed, even through cloud.

## Practical tips

- **Zoom:** the project opens on the whole bay (about map zoom 9). One zoom step in on the western half is the
  best view for comparing 10 Feb 2022 and 13 Jan 2023. Don't zoom out too far: Studio shows nothing below
  about map zoom 4.5, and on the 13 Jan 2023 layer stay at map zoom 6 or closer: further out, some of its tiles
  exceed the backend's limit of 20 images and stay blank. Zoomed out, true-colour tiles can take up to a minute.
- **Colour-blind viewers:** with red-green colour blindness, the radar layer's red looks dark olive and its
  yellow-green bright yellow. Say where the areas are (the south, east of it) as well as their colour.
- **Glacier names:** the scenario does not mark which front is Crane, Hektoria or Green; don't point at one by
  name.
- **Cloud shadows:** the dark, blurry patches on the ice on 18 Jan (south-east) and 10 Feb (on the western
  tongue) are cloud shadows, not open water.
- **Load times:** the radar-change layer is the slowest: in our local tests its tiles took up to 25 s each (a
  median of 3 to 11 s, depending on the run). Mention it while it loads, or open each layer once before
  presenting.
- **Radar seam:** zoomed in on the southern bay, a dotted line can cross the radar layer (where two radar
  slices meet); if a blank strip appears there, zoom out.
- **Old tabs:** if the project looks out of date, open it in a new tab, and don't Save from the old one (it
  would put the old version back).
