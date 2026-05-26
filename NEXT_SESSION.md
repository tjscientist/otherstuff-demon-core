# NEXT_SESSION — The Demon Core

Last touched: **2026-05-26** — added 13 new figures to vol2: 8 component photos, 2 PD reference drawings, 3 original labeled SVG drawings.

## State

- **Vol 1 (history):** complete, publishable. 4/5 figures in. One open errata: Daghlian dose figure (200 rad neutron + 110 rad gamma vs. ~510 rem total) cited both ways — resolve before website publication.
- **Vol 2 (build):** fully rewritten 2026-05-25; figure pass on 2026-05-26 brings vol2 from 7 → 20 figures. Adam-Savage-exact dual-box build (one black crackle / one zinc-chromate yellow) sharing one bisected 3.5″ MT-17F WNF tungsten heavy-alloy sphere with a hand-fabricated Po-Be Urchin replica in the central cavity. Legacy PLA/plywood path demoted to budget appendix §10.
- **Consolidated HTML:** `03-outputs/The_Demon_Core_Complete.html`, 2 vols / 56 TOC entries / **4.6 MB** (up from 2.6 MB after the figure pass). Rebuild with `python _build/build_single_html.py`.
- **Figures:** 27 files in `02-inputs/deep_dive/figs/` (14 prior + 10 new photos + 3 original SVG drawings). All FIGURE markers resolve cleanly. No `fig-missing` placeholders remain; `build_progress_grid.jpg` was removed during the 2026-05-25 rewrite, so the build is fig-complete pending Jeff's actual progress photos which can replace any reference photo in §2–§6.
- **Original labeled drawings (new 2026-05-26):**
  - `drawing_box_assembly_labeled.svg` — full box cutaway, 21 numbered callouts, material key + build sequence panels (§4 end)
  - `drawing_sphere_urchin_cross_section.svg` — assembled + exploded views, per-hemisphere machining sequence (§2 end)
  - `drawing_urchin_replica_detail.svg` — equator + polar views at 3× scale, original-vs-replica comparison table (§3 end)
- **Git:** not initialized. Per OtherStuff umbrella convention, Jeff runs `git init` + `gh repo create tjscientist/otherstuff-demon-core` when ready to back up.
- **CAD / manufacturing files:** none yet. `03-outputs/manufacturing/` directories empty.

## What to do next (in priority order)

1. **Place the MT-17F WNF custom-quote order with Midwest Tungsten Service** — 6-8 week lead time, ~$1,300 estimate. Email `mts@tungsten.com` referencing Adam Savage's certification format (3.500″ ± 0.005″, MT-17F WNF, mercury-free cert, as-ground finish). The whole build is gated on this part.
2. **Order Richlite** in parallel — 8× 8″×8″×2″ slabs from Maker Material Supply (~$320). 1-week lead.
3. **Identify a wire-EDM job shop** locally. Get a quote for a single equatorial cut on a 3.5″ tungsten heavy-alloy sphere with a custom V-block cradle (~$250 expected). Have this contact ready before the sphere arrives.
4. **Resolve the Daghlian dose discrepancy** in vol1 §3 — pick the better-sourced figure and add a single footnote on the alternate. Required for website publication.
5. **Once the sphere arrives**, measure its actual diameter to 0.001″ and update vol2 §4.3 with the exact cavity-target dimension before the radius-cutter setup.
6. **As you build**, drop progress photos into `02-inputs/deep_dive/figs/build_*.jpg` and replace the `build_progress_grid.jpg` placeholder in vol2.
7. **Design the LANL property tag** — `04-templates/property_tag.pdf` from a vector master. Sample field text already drafted in vol2 §7.2 (includes the HKD/LAS inspector-initial memorial to Daghlian and Slotin).

## Open questions

- Whether to send the finished sphere out for electroless nickel plating (~$120) post-bisection — vol2 §2.5 documents the rationale either way; decision deferred until the bare-tungsten finish is in hand for visual comparison.
- Whether to git-init this project now or wait until Jeff is closer to public-ready (current convention is the latter).
- Whether the "third pit" demon-core box was historically yellow or black — only B&W photos survive; the dual-box build hedges this.

## References on hand

- `02-inputs/Adam Savage Youtube Build Transcript.txt` — full Tested transcript with verbatim machinist commentary
- `02-inputs/Reference pics and infrmation.txt` — Jeff's seed URLs (Wellerstein, rarehistoricalphotos, BREDL)
- `02-inputs/research/links.md` — full source bookmark list, expanded 2026-05-25 with build-specific material/supplier links
- `02-inputs/deep_dive/figs/` — 27 reference images: 4 historical, 6 schematic/cutaway (PD), 3 Adam-box, 3 Sackett-yellow, 8 component photos (Richlite, tungsten sphere, EDM, magnets, thermometer, hinge, stopper, wrinkle paint), 3 original labeled SVG drawings
- `.claude/CLAUDE.md` — project conventions, current decisions, Progress Log

## Commands quick-reference

```powershell
# Rebuild the consolidated HTML (run from project root)
python _build/build_single_html.py

# Photo Helper queue is at C:\Users\Jeff\Documents\Claude\Projects\Photo Helper\_queue
# (See global CLAUDE.md for the queue protocol)
```
