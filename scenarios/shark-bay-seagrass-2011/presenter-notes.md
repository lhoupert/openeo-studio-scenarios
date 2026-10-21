# Presenter notes: Shark Bay seagrass and the 2010-11 marine heatwave

A short script for presenting this scenario, about 2-3 minutes. The full explanation of each layer, with
methods and references, is in this scenario's [README](README.md).

Project: <https://studio.mpc.ds.io/editor/exp-shark-bay-seagrass-loss-2011-heatwave-landsat>
(once saved; opens on layer 1, the 2010 picture). Open it in a **fresh tab** and show **one layer at a time**
(untick the previous one: ticked layers blend).

**Hook** (opening layer, 12 May 2010 true colour):
- **Orient:** Western Australia. Peron Peninsula in the middle, orange; the mainland on the right; little Faure
  Island in the eastern gulf. The shallow banks are turquoise with dark patches, cut by long dark fingers
  (channels).
- **Say:** "This is Shark Bay, a World Heritage Area. The dark patches on these shallow banks are seagrass
  meadows, on bright sand. Shark Bay's seagrass holds the largest carbon stock reported for any seagrass
  ecosystem. This is 2010."

Then the heatwave.

2. **4 Mar 2011, heatwave**
   - **Say:** "In the summer of 2010-11 a marine heatwave ran along the Western Australian coast: summer
     water 2 to 5 degrees warmer than average."
   - **Show:** the whole bay is red, darkest in the Western Gulf on the left. "Landsat also measures
     temperature. Here we subtract the average of three late-summer days in 2000 and 2002, same satellite,
     same time of day. In the Western Gulf the water was about 4 degrees warmer, over Hamelin Pool about 2 to
     3, and in both places warmer than on any of those three days. On the Faure Sill it was about 2 degrees
     above the average, but not clearly warmer than the warmest of the three days." If asked about the thin
     lines: gaps in the image, because the satellite's scan-line corrector failed in 2003.
3. **10 Jul 2014, after**
   - **Show:** the banks between Faure Island and the mainland, the Faure Sill: the dark green banks of 2010
     between the channels are now bright turquoise; the channels themselves (the long dark fingers) have not
     changed. Tick layer 1 and this one in turn to compare.
   - **Say:** "Across the whole World Heritage Area, 1,310 square kilometres of dense seagrass were lost: the
     largest loss of dense seagrass recorded worldwide after a single event."
4. **2010 to 2014, change**
   - **Show:** brown = water that got brighter. Point at the Faure Sill: the banks between the channels are
     brown, the channels stay white, which fits the published loss there. The north of the Western Gulf, west of
     Peron Peninsula, is brown too, but clearer water may add to it there. The dark brown ring round Hamelin
     Pool and along the shores is most likely lower water in 2014, not lost seagrass; the light teal over the
     open ocean is a difference between the two satellites and days. White = unchanged.
   - **Say:** "It's a simple difference between two satellites and two days, so tide and water clarity matter:
     it shows where to look. The scientists made the real maps with field data, from the same two Landsat
     sensors."

**Take-home:** one summer of hot water damaged about a third of the meadows (lost or thinned; losses were worst
where the accumulated heat reached 10 degree heating weeks or more and extreme temperatures lasted 94 days or
more). If 10 to 50 % of the carbon in their exposed sediment met oxygen, it may have released 2 to 9 million
tonnes of CO2 over the following three years: a carbon store that may have become a source of CO2.

## Practical tips

- **Zoom:** every layer covers the whole bay. Don't zoom out below about map zoom 4.5: Studio shows nothing
  there.
- **Load times:** the heat layer is the slowest (median 2-6 s per tile in local tests, up to 20 s, even where
  it shows nothing; it reads four overpasses). Open each layer once before presenting.
- **Old tabs:** if the project looks out of date, open it in a new tab, and don't Save from the old one (it
  would put the old version back).
