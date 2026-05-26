# .claude — Progress Log archive

Older Progress Log entries moved out of `CLAUDE.md` to keep that file
lean for session loading. The 3 most recent entries stay inline in
`CLAUDE.md`; everything else lives here, oldest-first, append-only.
Maintained by `tools/trim_progress_logs.py` (run by the wrap skill).
First archived: 2026-05-26.

---
- **2026-05-24** — Project scaffolded under `OtherStuff/`. Wrote substantive `CLAUDE.md`, `README.md`, `WEBSITE_SYNC.md`, `links.md`, `01-about-me/README.md`, `vol1.md` (history), `vol2.md` (replica build). Source-of-truth references pulled from Wikipedia (*Demon core*, *Harry Daghlian*, *Louis Slotin*, *Pit (nuclear weapon)*), Alex Wellerstein's *Restricted Data* "The plutonium box" (2014), Rare Historical Photos (Agnew/Tinian context), and Adam Savage *Tested* / Attoparsec replica references. No CAD or print files yet; no photos pulled yet.
- **2026-05-24** — Copied `Brewing and Distilling/_shared/build/build_single_html.py` (1969 lines, pure Python, no external deps) to `_build/build_single_html.py` and adapted: (1) DEFAULT_ROOT now `parents[1]` since the script sits one level deeper; (2) DEFAULT_VOL_DIR_REL = `02-inputs/deep_dive`; (3) DEFAULT_OUTPUT_REL = `03-outputs/The_Demon_Core_Complete.html`; (4) DEFAULT_PHOTOS_DIR_REL = `02-inputs/deep_dive/figs`; (5) DEFAULT_TITLE = "The Demon Core — Complete Reference"; (6) `vol_*.md` glob replaced with `vol*.md` + `vol\d+\.md` regex (Hack Tools style) to match this project's `vol1.md`/`vol2.md` filenames; (7) storage-key namespaced as `demon-core-deepdive-toc-expanded` to avoid localStorage collision with other deep dives. Built first cut: **2 volumes, 38 TOC entries, 105 KB**. Six `fig-missing` placeholders showing — corresponds to the three FIGURE directives in vol1+vol2 (each appears inline + in the List of Figures). Output: `03-outputs/The_Demon_Core_Complete.html`. Rebuild with `python _build/build_single_html.py`.
