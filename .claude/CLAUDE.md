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
- **2026-05-25** — **Default replica path upgraded** (supersedes the 2026-05-24 default). New plan: **two boxes built in parallel** to Adam Savage's exact *Tested* methods — one finished in black crackle (Trinity gadget-core style, Adam-exact) and one in zinc-chromate yellow (Fat Man / Sackett 2017 style). **Single 3.5″ MT-17F WNF tungsten-heavy-alloy sphere** shared between them, **bisected on the equator** with **send-out wire EDM** and machined with a **25 mm central cavity for a hand-fabricated Po-Be "Urchin" initiator replica**. Cost ~$2,500 (sphere is the dominant line, ~$1,300). Tooling: Bridgeport-class mill, lathe with radius cutter, paint oven. Sphere finish: as-machined for now; optional electroless nickel plating (~$120) documented as a future upgrade with rationale in vol2 §2.5. The previous default (PLA sphere + plywood box) demoted to a budget appendix (vol2 §10 Path α/β/γ).
- **2026-05-25** — Build-two-boxes-share-one-sphere decision: avoids a second $1,300 sphere; the bisected pit moves between display boxes; each box is a complete display piece on its own.

## Known Constraints & Limitations

- **Sourcing the magnesium look** without magnesium: Adam Savage used Richlite phenolic + crackle paint. The default build uses the same. Richlite source: Maker Material Supply / Boedeker / Professional Plastics.
- **Sphere mass and material.** A 3.5″ MT-17F WNF tungsten-heavy-alloy sphere at 17 g/cm³ hits **6.27 kg** — within 1.2% of the original 6.2 kg. No other off-the-shelf metal at that volume is closer (lead = 4.17 kg / DU = 6.96 kg unobtainable / pure W = 7.12 kg but unmachinable). Cost: $1,200–$1,500 custom-quote from Midwest Tungsten Service. 6-8 week lead time.
- **Splitting the sphere.** Wire EDM at a local job shop is the only path that protects the sphere's value. Band-sawing works but leaves a 1.5 mm kerf and ugly cut faces. Lathe parting is a safety hazard; skip. Budget $200–300 for send-out EDM.
- **Urchin geometry.** 20 mm OD Be shell (6 mm wall), 8 mm Be inner pellet, 15 latitudinal wedge grooves, gold + Ni surface, ~7 g, in a 25 mm cavity. Wikipedia *Urchin (detonator)* article is the cite.
- **Zinc-chromate yellow** is a discontinued color in most paint lines; closest modern match is Rust-Oleum Specialty *Industrial Choice* Safety Yellow #1644 + a dust-coat of Olive Drab for the olive-cast offset. Sackett 2017 replica is the visual reference.
- **Hardware.** The Morrison box used four bolts at the perimeter (Wellerstein-confirmed, with rubber test-tube stopper bumpers and threaded urchin port caps). Build reproduces all four bolts AND adds piano hinge + small antique-brass latches for day-to-day display use — both for redundancy and visual fidelity to Adam's reproduction.

## Key Dependencies

- Photo Helper (CLAUDE.md global protocol)
- 3D printer (any FDM ≥200 mm bed for full-scale sphere)
- Optional CNC or table saw for the case shell
- Adam Savage *Tested* "Builds a Demon Core" video (URL in `02-inputs/research/links.md`)
- Printables #451707 (case) and #1390266 (full-scale core sphere) — link only, do not redistribute

## Progress Log

> Older Progress Log entries are in [`PROGRESS_ARCHIVE.md`](PROGRESS_ARCHIVE.md) — only the 3 most recent are kept inline here, to keep this file lean for session loading. `tools/trim_progress_logs.py` (run by the wrap skill) maintains this split.

- **2026-05-25** — Pulled all four fetchable figures via Photo Helper queue (watcher started ad-hoc; `_queue/done/` IDs `REQ_20260525_001..014`). Saved to `02-inputs/deep_dive/figs/`: (a) `omega_site_recreation.jpg` = `File:Partially-reflected-plutonium-sphere.jpeg` from Wikimedia Commons, LANL "Attribution" license, 1.7 MB; (b) `agnew_tinian_1945.jpg` = `File:Agnew NagasakiPuCore.jpg`, U.S. Gov public domain, 142 KB; (c) `slotin_recreation_beryllium.jpg` = `File:Tickling the Dragons Tail.jpg`, LANL public domain, 425 KB; (d) `savage_demon_core_overview.jpg` = pagefetch of the Tested YouTube `maxresdefault.jpg` thumbnail (`V1Y4UR8xqxA`), 228 KB — credited "courtesy of Adam Savage / Tested" as a reference placeholder pending Jeff's own build photo. Replaced all four placeholder captions with verbatim `creditLine` strings; also corrected the Daghlian caption (was attributed to "Wikipedia editors' re-creation" — actually a LANL recreation per Commons metadata). Rebuilt: **3,337 KB**, 38 TOC entries. Sole remaining `fig-missing` marker is `build_progress_grid.jpg` (vol2 §8) — intentional, awaiting Jeff's actual build photos.
- **2026-05-25 (PM)** — **Major vol2 rewrite for split-pit + dual-box build plan.** Jeff added ten reference images and the full Adam Savage YouTube transcript to `02-inputs/`. Moved/renamed all ten into `02-inputs/deep_dive/figs/` (3× Savage box references = `savage_box_*.{jpeg,jpg}`; 3× Sackett yellow replica = `sackett_yellow_replica_*.jpg`; pit cross-section from *Day of Trinity* = `pit_cross_section_lamont1965.webp`; urchin cutaway = `urchin_initiator_cutaway.gif`; sealed-pit schematic + implosion-device cutaway saved for future use). Researched Midwest Tungsten MT-17F pricing/sphere catalog (3.5″ is custom-only), tungsten-heavy-alloy splittability (HRC25, wire EDM is the recommended path), Urchin geometry (Wikipedia: 20 mm Be shell, 8 mm Po-coated inner pellet, 15 wedge grooves, ~7 g, in 25 mm cavity), Richlite specs and suppliers, and the PJ1 Fast Black wrinkle-paint bake recipe (250–300 °F / 121–149 °C, 30–60 min — Adam's "125-150" was Celsius). Rewrote `02-inputs/deep_dive/vol2.md` end-to-end (~580 lines, ~9,000 words) covering: §1 scope-and-deltas table; §2 split-tungsten-sphere build with wire-EDM bisection + 25 mm Urchin cavity + 4 neodymium-magnet equator hold-together; §3 hand-fabricated Urchin replica (20 mm brass, 15 wedge grooves, gold finish); §4 Adam-exact Richlite box body (8″ slab lamination → 7.25″ cube → radius-cutter sphere cavity → cooling fins); §5 full hardware suite (×4 aluminum urchin port plugs, thermometer, knife-style handle, hinge + latches, ×20 rubber-stopper bumpers per box); §6 parallel-finish paths (§6A black crackle / §6B zinc-chromate yellow); §7 LANL property tag with HKD+LAS inspector initials; §8 BOM ~$2,469 + $120 optional Ni plating; §9 build-order timeline (~10-week calendar, gated by MT lead time); §10 abbreviated legacy paths (PLA / plywood / steel-ball-bearing) demoted to budget appendix; §11 future-revision items. Seven figures embedded inline (one hero, two new technical diagrams, two Adam box references, one Sackett hardware-detail, one yellow-finish reference; plus the carry-over `build_progress_grid.jpg` placeholder). HTML rebuild pending.

- **2026-05-26** — **Vol2 figure pass.** Added thirteen new figures, taking vol2 from 7 → 20 inline figures. Eight component photos via Photo Helper (started watcher manually, queued 20 requests across two rounds; Commons hits got literal-match misses on subject names like "piano" / "neodymium" video, so retried with `webfetch` for vendor product pages): `richlite_material_sample.jpg` (EcoSupply), `tungsten_sphere_reference.jpg` (Elmet Technologies), `wire_edm_reference.jpg` (Wikimedia PD — Ona AE300), `neodymium_disc_magnets_reference.jpg` (Luxtrada N52 6×3 mm), `process_thermometer_reference.jpg` (2″ bimetal), `brass_piano_hinge_reference.jpg` (HDC Hinge), `rubber_stopper_reference.jpg` (Wikimedia CC-BY-SA), `wrinkle_paint_texture_reference.jpg` (PJ1 product). Two PD reference drawings: `implosion_weapon_diagram_reference.jpg` (Fastfission's Wikimedia shock-wave diagram) + `fat_man_cutaway_reference.jpg` (Wikipedia Fat Man Internal Components). Three original labeled SVG drawings authored: `drawing_box_assembly_labeled.svg` (full box cutaway, 21 numbered callouts covering all hardware + body + cavities + sphere + Urchin, with material key and per-body build-sequence panels); `drawing_sphere_urchin_cross_section.svg` (assembled equatorial cross-section + exploded view with per-hemisphere machining sequence); `drawing_urchin_replica_detail.svg` (equator + polar views at 3× scale, with original-vs-replica comparison table). SVG support confirmed via mimetypes.guess_type → base64 in `_embed_image()`. One Scientific American "Christy pit" webfetch result was discarded for copyright; one PDF / one Euphonicon-piano / one webm-magnet misfire were retried successfully on round 2. Wire-EDM photo downsized 3264×2448 → 1400×1050 (3.3 MB → 196 KB) to keep total HTML size reasonable. Rebuilt: **2 vols, 56 TOC entries, 4.6 MB**, all FIGURE markers resolve (zero `fig-missing`). Updated `NEXT_SESSION.md` to reflect new figure inventory.

## Contact & Resources

- History deep dive: `02-inputs/deep_dive/vol1.md`
- Replica build deep dive: `02-inputs/deep_dive/vol2.md`
- Research bookmarks: `02-inputs/research/links.md`
- Umbrella conventions: `../.claude/CLAUDE.md`
- Canonical structure reference: `../../Electronics/_shared/structure.md`
- Website contract: `./WEBSITE_SYNC.md`
