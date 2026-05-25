# Vol 2 — The Demon Core: Replica build

## Introduction

This volume is the practical companion to [Vol 1's history](./vol1.md). It documents the build of a display-quality, non-functional replica of two objects: (a) the **demon core itself** — an 89-millimeter sphere, painted to look like nickel-plated δ-phase plutonium-gallium alloy — and (b) the **Manhattan-Project plutonium carrying box** that Philip Morrison designed and Ralph Sparks machined in 1945, reproduced in the style of **Adam Savage's 2024 *Tested* one-day build** rather than in literal magnesium.

The replica is purely an educational and display piece. Nothing here is fissile, radioactive, or hazardous in any way beyond the ordinary hazards of 3D printing, woodworking, and spray painting. The sphere is a hollow shell of PLA (or, optionally, weighted with lead shot to approximate the original's 14 lb heft). The box is a wood or composite shell painted to match the Fat Man-era zinc-chromate yellow finish. Anyone reading this who would like to build their own should be able to do so from the steps below, a 3D printer, and a Saturday afternoon.

Three published references inform every choice in this volume: Adam Savage's *Tested* episode "Adam Savage Builds a Demon Core!" (2024); the **Attoparsec** Halloween 2019 box replica; and two freely available STL models on Printables — **#451707** by FuzzyRaptor (the case) and **#1390266** by blackrat (the full-scale core sphere). Where the build deviates from those references the deviation is flagged in the prose. The full URL list is in `../research/links.md`.

<!-- FIGURE: savage_demon_core_overview.jpg :: Adam Savage's completed *Tested* one-day-build replica of the Manhattan Project plutonium box, with a tungsten-alloy stand-in for the core in place. The crackle-paint finish on the Rich Light phenolic body approximates the look of raw machined magnesium; the brass urchin-initiator port plugs are visible at top. Frame from the Tested YouTube episode "Adam Savage Builds a Demon Core!" (2024) — used here as a reference placeholder; replace with own build photo once available. Photo: courtesy of Adam Savage / Tested, https://www.youtube.com/watch?v=V1Y4UR8xqxA. :: Photo: courtesy of Adam Savage / Tested — YouTube thumbnail, reference placeholder pending Jeff's build photo -->

## §1 What we're matching, and what we're not

The original box was magnesium, machined to about ±0.005 inch tolerances by a working machinist on production equipment, painted in a discontinued anti-corrosion primer, and held shut by four bolts that ran the full height of the case from top to bottom. None of those choices are practical for a hobby build, and none of them are visible from across a room. The replica targets the **outward appearance** of the Fat Man-era yellow box, not the metallurgy of the original.

| Aspect | Original (1945) | Savage replica (2024) | This build (default plan) |
|---|---|---|---|
| Body material | Magnesium plate | Rich Light phenolic (paper laminate) | Birch plywood or 3D-printed PLA |
| Body construction | Machined from solid | Milled from solid block | Wood: glued box joints. PLA: printed shell. |
| Hardware | Four through-bolts | Custom brass urchin-port plugs + recessed thumb-holes | Two butterfly latches + piano hinge, OR four perimeter bolts |
| Bumpers | Rubber test-tube stoppers | Black rubber pucks | Black rubber feet, 25 mm round |
| Finish | Zinc-chromate yellow (Fat Man) / raw mag (Trinity) | Crackle paint over gloss yellow basecoat | Rust-Oleum yellow + crackle topcoat |
| Interior | Foam cradle for core + initiator | Custom-fit foam, brass plugs in initiator slots | Closed-cell foam, hand-carved core well |
| Core | 6.2 kg plated Pu-Ga alloy, 89 mm Ø | Tungsten-alloy sphere (~9 kg), 89 mm | Hollow PLA sphere, 89 mm, optionally weighted |
| Core finish | Nickel plate | Hand-polished tungsten | Chrome-effect spray paint (Spaz Stix or Molotow) |

Two paths are documented below for each major component. Pick whichever matches the tools on hand.

## §2 The core itself

The original demon core was a sphere of 89 millimeters (3.5 inches) diameter, mass 6.2 kilograms (~14 pounds), made of two hot-pressed Pu-Ga hemispheres around a hollow 25-millimeter polonium-beryllium initiator cavity. The visible exterior was the nickel plating — a dull silver, not chrome-bright, with faint hand-finish marks where the hemispheres met at the equator.

### Path A — 3D printed (recommended default)

Use the Printables model **#1390266 "Demon Core Replica — Full Scale & Scaled"** by user *blackrat*. The full-scale variant prints as two hemispheres at 89 mm Ø, designed to be glued together at the equator. The scaled-down versions (50 mm, 60 mm) are useful if a 200 mm-class printer can't fit the full sphere — most can; an FDM printer with a 220 mm bed clears the print envelope by 15 mm in every direction.

Recommended slicer settings (FDM, PLA):

| Setting | Value |
|---|---|
| Layer height | 0.16 mm (for surface quality through paint) |
| Walls | 4 perimeters |
| Top/bottom | 5 layers |
| Infill | 15% gyroid (light — finish-paint stage will hide layer lines) |
| Print orientation | Hemisphere flat side down, no supports |
| Brim | 5 mm (helps detach the flat circle cleanly) |

After printing the two hemispheres, file or sand the equator flat on a piece of 220-grit paper laid on a flat surface. Test-fit, then glue with cyanoacrylate. Fill the equatorial seam with thin filler primer (Tamiya Surface Primer or Mr. Surfacer 500), wet-sand to 400, and finish-coat as follows:

1. **Filler primer**, 2–3 light coats, wet-sanded between each.
2. **Gloss black basecoat** for chrome to lay over. Tamiya TS-14 or Rust-Oleum gloss black.
3. **Chrome-effect topcoat.** Spaz Stix "Ultimate Mirror Chrome" or Molotow Chrome refill (decanted into an airbrush) gives the closest dull-silver nickel-plate look. *Do not clear-coat over chrome paints — clear coats almost always dull or yellow them.*
4. Optional: light dry-brush of warm grey along the equator to suggest the seam between the two hemispheres.

If display weight matters — and for a credible heft in the hand it does — cut a 50-mm hole in one hemisphere before gluing, fill the cavity with **lead shot or steel BBs in epoxy**, plug the hole, and finish over the patch. A full inner cavity of #8 lead shot (~11 g/cm³ packed) holds about 4 kg of weight in an 89-mm hollow sphere — short of the original 6.2 kg but enough to convey the density.

### Path B — Solid metal (Savage path)

Adam Savage used a **tungsten-alloy sphere** as the stand-in. Tungsten heavy alloy at ~17 g/cm³ delivers about 5.6 kg in an 89-mm sphere — close to the original mass. Off-the-shelf tungsten spheres in this size are expensive (~$400–$900 from instrument suppliers like McMaster-Carr or specialty machinist shops) but require no finishing if hand-polished. This is the path to take only if the budget runs there and the project is competing for shelf space with finer work; the 3D-printed path looks identical in photographs.

### Path C — Resin print

A masked-SLA printer with a 200 mm × 200 mm build plate (Anycubic Mono X 6K, Elegoo Saturn 4 Ultra, etc.) can print the sphere in two hemispheres at much higher surface quality than FDM — no layer lines visible under paint. Use ABS-like resin for impact resistance. Same finishing steps as Path A, less seam filler required.

## §3 The case

The Morrison box is roughly **a cube with the lid taking the upper two-thirds and the base the lower third** — split horizontally, four bolts at the side-walls. Exterior dimensions are not exactly documented in any open source; the Printables #451707 model by *FuzzyRaptor* is the cleanest dimensional reference available, scaled from the Wellerstein and LANL Flickr photographs. The model prints in two parts (top + bottom) at roughly **180 mm × 180 mm × 200 mm tall**, which puts a 89-mm sphere in a comfortable cradle in the lower third.

### Path A — Wood (the everyperson path)

Materials: **12 mm Baltic birch plywood** (5 ply), cut to the following box-joint plan:

```
Bottom assembly (third of total height):
  4 sides: 180 × 64 mm  (cut box joints on the short ends)
  1 base:  180 × 180 mm

Top assembly (two-thirds of total height):
  4 sides: 180 × 130 mm
  1 top:   180 × 180 mm
```

Box-joint the sides on a table saw with a stacked dado, or finger-joint on a router-table jig. Glue with Titebond III. Sand the assembled boxes flush, prime with grey filler primer, and proceed to finishing (§5).

### Path B — 3D printed (the desktop path)

Print **Printables #451707** by *FuzzyRaptor* in PLA or PETG. The model is split into a printable bottom and top; on a 220 mm bed both parts fit individually but not together. Recommended settings: 0.2 mm layer height, 4 walls, 15% infill, 6 top/bottom layers. Print orientation: bottom flat down (no supports), top inverted (no supports). After printing, fill the layer-line ridges with auto-body spot putty, sand to 320, and proceed to finishing.

### Path C — Aluminum or magnesium (the authenticity path)

Magnesium plate is available from McMaster-Carr (~$80 for a 12 in × 12 in × 1/4 in sheet) but machining it requires **flood-coolant CNC equipment and a serious respect for the metal's fire risk** — magnesium chips burn at very high temperatures and cannot be extinguished with water. Aluminum is a friendlier substitute that machines beautifully; 6061-T6 plate in the same thickness costs about a quarter and looks identical under paint. This is Adam Savage's path (well, Rich Light phenolic, but the geometry is the same). Skip unless the shop has a Bridgeport and someone who knows how to use it.

## §4 Hardware

The original used **four through-bolts** at the mid-sides — no hinges, no latches. To disassemble the box you removed all four bolts and lifted the top off. That is faithful but inconvenient for a display piece that will be opened often. Two practical options:

- **Authentic — four perimeter bolts.** 1/4-20 stainless socket-head bolts through the top wall into threaded inserts in the bottom wall, one bolt centered on each side. Wood path: install M6 brass threaded inserts in the bottom shell with epoxy. PLA path: print captive M6 nut pockets in the bottom shell.

- **Usable — piano hinge + two butterfly latches.** Continuous brass piano hinge along the back; two small antique-brass surface-mount latches on the front. Period-appropriate enough that no one in photographs will notice; opens with one hand.

For the urchin-initiator port plugs that Adam Savage milled into his replica's top surface (the visible "ports" on the original were actually access points for the polonium-beryllium initiators), turn or 3D-print **two short brass cylinders, ~20 mm Ø × 10 mm tall**, knurled, and friction-fit into matching holes on the top face of the box, offset toward the back. Not on every reference photo but a nice detail; skip if simplicity is preferred.

## §5 Interior cradle and bumpers

The interior of the original held the core in a recessed cradle with the initiator above. Replicate:

- **Closed-cell foam** (cross-linked polyethylene, e.g. Plastazote LD45) cut to fit inside the bottom shell, with a 90-mm hemispherical recess hand-carved to seat the sphere. A hot-wire foam cutter or a sharp linoleum knife on chilled foam works.
- The top of the bottom shell's foam should sit flush with the case's horizontal split line. The upper case's foam (optional) is a shallow recess for the urchin initiator plugs.
- **Bumpers.** Four 25 mm round black rubber feet, mounted to the bottom corners with the included screws. The original used rubber test-tube stoppers; modern surplus electrical cabinet feet are visually identical from any reasonable distance.

## §6 Finish: zinc-chromate yellow

The Fat Man box's "mustard yellow" was a 1940s zinc-chromate anti-corrosion primer, formulated for steel substrates. Modern zinc-chromate primers exist but are restricted as hazardous waste in most jurisdictions, contain hexavalent chromium, and are overkill. The visual match is straightforward with off-the-shelf rattle-can spray:

1. **Sand to 320**, wipe with denatured alcohol.
2. **Light coat of grey filler primer**, sand to 400.
3. **Two medium coats of Rust-Oleum Specialty *Industrial Choice* Safety Yellow** (or any "school-bus yellow" enamel). Allow 24 hr cure.
4. **Optional crackle coat** for the Adam Savage "aged factory finish" look — Modern Masters Crackle for Metal, applied per the can's instructions over the yellow base. Practice on scrap before committing; crackle texture is sensitive to coat thickness and humidity.
5. **Light overspray of warm brown weathering powder** (Tamiya Weathering Master Set B "Mud") around the bottom bumpers and corners to suggest 80 years of handling.

For the Trinity-era **raw magnesium look**, skip yellow and finish with a single coat of **Krylon Brushed Metallic Aluminum** over grey primer. Apply unevenly on purpose; magnesium plate weathers blotchy.

## §7 Display and final detail

Place the finished sphere in the cradle. The original sat slightly proud of the foam to allow neutron-counter probes to reach it; reproduce by carving the cradle 5 mm shallower than the sphere's equator. Add a small **paper label** to the inside lid of the box matching the Los Alamos property tag style of 1945 — black serif type on cream stock, with fields for "MATERIAL," "WEIGHT," and "INSPECTOR INITIALS." The Wellerstein photographs show the originals had such labels though the text is not legible.

For a museum-display caption, mount a 5 × 7 in printed card alongside the closed box reading roughly: *"Replica of the magnesium plutonium-pit carrying box designed by Philip Morrison and machined by Ralph C. Sparks at Los Alamos in 1945. The contained sphere represents the third pit cast for the Manhattan Project — nicknamed 'Rufus,' later 'the demon core,' the cause of the August 1945 and May 1946 criticality accidents that killed Harry K. Daghlian Jr. and Louis A. Slotin. The original was melted down in the summer of 1946."*

<!-- FIGURE: build_progress_grid.jpg :: Build progress, four-up: (top left) FDM-printed core hemispheres immediately after slicing; (top right) glued, primed, and chrome-coated sphere; (bottom left) plywood case after box-jointing and pre-paint; (bottom right) finished case in zinc-chromate yellow with crackle topcoat. Photo: Jeff Swan, 2026 (placeholder — to be replaced during the actual build). :: Photo: Jeff Swan, 2026 (placeholder pending actual build) -->

## §8 Bill of materials

| Item | Qty | Source | Approx. cost (USD, 2026) |
|---|---|---|---|
| **Sphere — Path A** | | | |
| PLA filament, 1 kg roll | 1 | Bambu / Polymaker / Hatchbox | $20 |
| Spaz Stix Ultimate Mirror Chrome 2 oz | 1 | Amazon / hobby store | $20 |
| Tamiya Surface Primer, gloss black basecoat | 2 | Hobby store | $15 |
| **Case — Path A (plywood)** | | | |
| Baltic birch plywood 12 mm, 24 × 24 in | 1 | Local hardwood dealer / Rockler | $30 |
| Titebond III | 1 | Hardware store | $10 |
| Rust-Oleum Industrial Yellow rattle can | 2 | Home improvement | $20 |
| Modern Masters Crackle for Metal, 16 oz | 1 | Art-supply / Amazon | $30 |
| Antique brass piano hinge, 12 in | 1 | Rockler | $15 |
| Antique brass surface latches (pair) | 1 | Lee Valley / Etsy | $20 |
| **Interior** | | | |
| Plastazote LD45 closed-cell foam, 1 in × 12 × 12 | 1 | Foam Order / TAP Plastics | $25 |
| Black rubber feet, 25 mm, set of 4 | 1 | McMaster-Carr | $8 |
| **Detail** | | | |
| Brass rod 20 mm Ø × 6 in (urchin port plugs) | 1 | Online Metals | $15 |
| Tamiya weathering powder, Set B | 1 | Hobby store | $15 |
| **Total** (default path, plywood case + PLA sphere) | | | **~$245** |

A pure-PLA build skipping the wood case and brass details runs about $80; an aluminum-shop build with hand-machined hardware runs north of $700.

## §9 What's left for a future revision

- **Photograph the finished build** and replace the two placeholder figures above with own work; pull at least four progress photographs into `figs/` (raw print, sanded sphere, painted sphere, finished assembly).
- **Source the original LANL property-tag artwork** from the LANL Flickr archive and reproduce as a printable PDF in `04-templates/property_tag.pdf`.
- **Settle the bolt vs latch question** based on how often the box will be opened in display — current default is hinge+latch.
- **Add an "errata" section** at the bottom for any historical or build details that turn out wrong on later review.

## References

### Build references

- "Adam Savage Builds a Demon Core!" *Tested* YouTube, 2024 — https://www.youtube.com/watch?v=V1Y4UR8xqxA
- "Manhattan Project plutonium box replica build" — https://www.youtube.com/watch?v=RFHQdXxLj8M
- Attoparsec, "Manhattan Project plutonium box" — https://www.attoparsec.com/artifacts/plutonium.html
- FuzzyRaptor, "Plutonium core case" — Printables #451707 — https://www.printables.com/model/451707-plutonium-core-case
- blackrat, "Demon Core Replica — Full Scale & Scaled" — Printables #1390266 — https://www.printables.com/model/1390266-demon-core-replica-full-scale-scaled-3d-print
- audin, "Trinity Device Plutonium Core" — Printables #581243 — https://www.printables.com/model/581243-trinity-device-plutonium-core
- "Historical prop: The plutonium carrying box for the Fat Man bomb" — RPF — https://www.therpf.com/forums/threads/historical-prop-the-plutonium-carrying-box-for-the-fat-man-bomb.278641/

### Historical references (carried forward from Vol 1)

- Wellerstein, Alex. "The plutonium box," *Restricted Data*, March 28, 2014 — https://blog.nuclearsecrecy.com/2014/03/28/plutonium-box/
- Sparks, Ralph C. *Twilight Time: A Soldier's Role in the Manhattan Project at Los Alamos.* Los Alamos Historical Society, 2000 — https://archive.org/details/twilighttimesold0000spar
- "Harold Agnew carrying the plutonium core, Nagasaki Fat Man bomb, 1945," *Rare Historical Photos* — https://rarehistoricalphotos.com/harold-agnew-carrying-plutonium-core-nagasaki-fat-man-bomb-1945/

### Cross-reference

- Vol 1 — The Demon Core: A History — `./vol1.md`
