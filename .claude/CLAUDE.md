# Project: The Demon Core

## Project Overview

A two-track personal project covering the 6.2 kg plutonium-gallium sphere — originally codenamed **"Rufus,"** later **"the demon core"** — that was cast at Los Alamos in August 1945 to serve as the fissile pit of a third atomic bomb scheduled for delivery against Japan, and that instead killed Harry Daghlian (August 21, 1945) and Louis Slotin (May 21, 1946) in two separate criticality accidents before being melted down in the summer of 1946. Track 1 is a citation-rich history (`02-inputs/deep_dive/vol1.md`); Track 2 is a maker build of (a) a ~89 mm 3D-printed replica of the core and (b) a reproduction of the magnesium **plutonium carrying box** designed by Philip Morrison and machined by Ralph Sparks, built in the style of Adam Savage's 2024 *Tested* one-day build (`02-inputs/deep_dive/vol2.md` + `03-outputs/manufacturing/`).

## Key Information

- **Status**: Deep Dive (history) + Engineering (replica)
- **Owner**: Jeff
- **Created**: 2026-05-24
- **Key Stakeholders**: Jeff (sole)

## Directory Guide

- **`.claude/CLAUDE.md`** — this file
- **`01-about-me/README.md`** — tone, decisions to ask first, citation style
- **`02-inputs/research/links.md`** — primary sources, replica references, image-sourcing strategy
- **`02-inputs/deep_dive/vol1.md`** — history of the demon core (publishable)
- **`02-inputs/deep_dive/vol2.md`** — replica build (publishable)
- **`02-inputs/deep_dive/figs/`** — historical and reference images
- **`03-outputs/engineering/`** — calcs (mass/volume of a tungsten or PLA stand-in to hit 6.2 kg / 14 lb), color-match notes for zinc-chromate yellow
- **`03-outputs/prototype/`** — build log, paint tests, fit notes
- **`03-outputs/manufacturing/3mf/`** — printable core (sliced from Printables #1390266 or audin's Trinity Device pit)
- **`03-outputs/manufacturing/fusion/`** — case CAD (parametric reproduction of the Morrison/Savage geometry)
- **`03-outputs/manufacturing/dxf/`** — if the case sides are CNC-cut from sheet stock
- **`03-outputs/figs/`** — build photos for the website
- **`04-templates/`** — figure-caption template, BOM template
- **`05-resources/`** — local cache of the Sparks memoir excerpts, LANL Flickr stills

## Project Goals & Objectives

- **Goal 1** — Ship a historically accurate, publishable history of the demon core that gets dates, doses, and configurations right, citing primary and tertiary sources, and presents the two fatalities with the gravity they deserve. Target ~6,000 words in vol1.
- **Goal 2** — Build a display-quality replica of the core (~89 mm sphere) and its carrying box, with photographs documenting the build for vol2. The replica is non-functional, non-fissile, and made from inert hobby materials (PLA / resin / wood / aluminum or steel hardware).
- **Goal 3** — Have both volumes ready for ingestion into `tjscientist/jeff-web` (MyWebssite) without further editing, per `WEBSITE_SYNC.md`.

**Success criteria**: vol1 reads like a museum panel; vol2 reads like a Tested write-up; the finished replica sits on a shelf and looks the part.

## Context & Background

The demon core is one of the most-told stories of the early atomic age, but it is also one of the most-mistold — internet retellings routinely confuse Daghlian's tungsten-carbide reflector with Slotin's beryllium hemispheres, attribute the screwdriver demonstration to both men, or claim the core "went critical" (it went *prompt critical*, briefly, twice). The primary purpose of vol1 is to get the technical details right. The accompanying replica build is partly tribute, partly memento mori for criticality-safety practice — the post-Slotin reforms (no more hands-on assembly, remote-controlled rigs, two-person rule, formal protocol review) are the reason no Western criticality experiment has killed anyone since 1958.

The carrying box itself is a smaller, quieter story. Philip Morrison — who would later co-host *Powers of Ten* — designed it; machinist Ralph Sparks built it at Los Alamos and wrote about doing so in his 2000 memoir *Twilight Time*. The Trinity-era box was raw magnesium; the Fat Man-era box was painted zinc-chromate yellow to match the bomb casing. Adam Savage milled a museum-quality reproduction on the 2024 *Tested* "Builds a Demon Core" episode using Rich Light phenolic (a paper-laminate composite, easier than magnesium and entirely inert), and that's the practical template this project follows.

## Team & Roles

- **Project Lead**: Jeff
- **Contributors**: none

## Custom Skills & Behaviors

- **Historical accuracy comes first.** If a source can be verified, cite it. If two sources disagree (e.g. Daghlian's dose figures), say so in the prose rather than silently picking one.
- **Photo Helper everywhere.** All figures placed via the helper's queue protocol, captions include the returned `creditLine` verbatim.
- **No memetic framing.** Avoid "spicy rock," "atomic Roomba," etc. — those belong in the cultural-legacy section at most, and even there sparingly.
- **Units**: SI primary, US customary in parentheses (e.g., "89 mm (3.5 in)"); doses in **rad** and **rem/Sv** as the sources cite them, with conversions noted.
- **Names**: full at first mention ("Harry K. Daghlian Jr."), last name thereafter.

## Important Decisions

- **2026-05-24** — Scaffolded as a single project under `OtherStuff/` umbrella (not its own top-level hub). Mirrors the Electronics-template skeleton.
- **2026-05-24** — History will be **one long vol1** to start, not split per incident. Easy to split later if it sprawls.
- **2026-05-24** — Replica build documented in a **single vol2** covering both the core and the case. Easy to split if the case build alone grows past ~3,000 words.
- **2026-05-24** — Default replica path = **Savage-style Rich-Light-or-equivalent box + 3D-printed sphere**, not historically accurate magnesium. Reasons: safety (magnesium machining = fire risk), cost, and the painted result is indistinguishable in photographs.

## Known Constraints & Limitations

- **Sourcing the magnesium look** without magnesium: Adam Savage used Rich Light phenolic + crackle paint. Approximating crackle paint over MDF or 3D-printed PLA is the practical path.
- **Sphere mass.** A solid PLA sphere at 89 mm weighs ~580 g, not the 6.2 kg of the original. If display weight matters, the sphere can be cast hollow and weighted (lead shot + epoxy, ~5.6 kg added). Optional.
- **Zinc-chromate yellow** is a discontinued color in most paint lines; closest modern matches are Rust-Oleum Specialty *Industrial Choice* yellow or any "school-bus yellow" enamel with a touch of olive added.
- **Hardware.** The Morrison box used four bolts at the perimeter rather than hinges + latches. Modern reproductions typically substitute small butterfly-latches or piano hinge + clasp for usability. Decide before CAD.

## Key Dependencies

- Photo Helper (CLAUDE.md global protocol)
- 3D printer (any FDM ≥200 mm bed for full-scale sphere)
- Optional CNC or table saw for the case shell
- Adam Savage *Tested* "Builds a Demon Core" video (URL in `02-inputs/research/links.md`)
- Printables #451707 (case) and #1390266 (full-scale core sphere) — link only, do not redistribute

## Progress Log

- **2026-05-24** — Project scaffolded under `OtherStuff/`. Wrote substantive `CLAUDE.md`, `README.md`, `WEBSITE_SYNC.md`, `links.md`, `01-about-me/README.md`, `vol1.md` (history), `vol2.md` (replica build). Source-of-truth references pulled from Wikipedia (*Demon core*, *Harry Daghlian*, *Louis Slotin*, *Pit (nuclear weapon)*), Alex Wellerstein's *Restricted Data* "The plutonium box" (2014), Rare Historical Photos (Agnew/Tinian context), and Adam Savage *Tested* / Attoparsec replica references. No CAD or print files yet; no photos pulled yet.
- **2026-05-24** — Copied `Brewing and Distilling/_shared/build/build_single_html.py` (1969 lines, pure Python, no external deps) to `_build/build_single_html.py` and adapted: (1) DEFAULT_ROOT now `parents[1]` since the script sits one level deeper; (2) DEFAULT_VOL_DIR_REL = `02-inputs/deep_dive`; (3) DEFAULT_OUTPUT_REL = `03-outputs/The_Demon_Core_Complete.html`; (4) DEFAULT_PHOTOS_DIR_REL = `02-inputs/deep_dive/figs`; (5) DEFAULT_TITLE = "The Demon Core — Complete Reference"; (6) `vol_*.md` glob replaced with `vol*.md` + `vol\d+\.md` regex (Hack Tools style) to match this project's `vol1.md`/`vol2.md` filenames; (7) storage-key namespaced as `demon-core-deepdive-toc-expanded` to avoid localStorage collision with other deep dives. Built first cut: **2 volumes, 38 TOC entries, 105 KB**. Six `fig-missing` placeholders showing — corresponds to the three FIGURE directives in vol1+vol2 (each appears inline + in the List of Figures). Output: `03-outputs/The_Demon_Core_Complete.html`. Rebuild with `python _build/build_single_html.py`.
- **2026-05-25** — Pulled all four fetchable figures via Photo Helper queue (watcher started ad-hoc; `_queue/done/` IDs `REQ_20260525_001..014`). Saved to `02-inputs/deep_dive/figs/`: (a) `omega_site_recreation.jpg` = `File:Partially-reflected-plutonium-sphere.jpeg` from Wikimedia Commons, LANL "Attribution" license, 1.7 MB; (b) `agnew_tinian_1945.jpg` = `File:Agnew NagasakiPuCore.jpg`, U.S. Gov public domain, 142 KB; (c) `slotin_recreation_beryllium.jpg` = `File:Tickling the Dragons Tail.jpg`, LANL public domain, 425 KB; (d) `savage_demon_core_overview.jpg` = pagefetch of the Tested YouTube `maxresdefault.jpg` thumbnail (`V1Y4UR8xqxA`), 228 KB — credited "courtesy of Adam Savage / Tested" as a reference placeholder pending Jeff's own build photo. Replaced all four placeholder captions with verbatim `creditLine` strings; also corrected the Daghlian caption (was attributed to "Wikipedia editors' re-creation" — actually a LANL recreation per Commons metadata). Rebuilt: **3,337 KB**, 38 TOC entries. Sole remaining `fig-missing` marker is `build_progress_grid.jpg` (vol2 §8) — intentional, awaiting Jeff's actual build photos.

## Contact & Resources

- History deep dive: `02-inputs/deep_dive/vol1.md`
- Replica build deep dive: `02-inputs/deep_dive/vol2.md`
- Research bookmarks: `02-inputs/research/links.md`
- Umbrella conventions: `../.claude/CLAUDE.md`
- Canonical structure reference: `../../Electronics/_shared/structure.md`
- Website contract: `./WEBSITE_SYNC.md`
