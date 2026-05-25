# 01-about-me — The Demon Core

How Claude should approach this project.

## Project shape

Two threads run in parallel:

1. **History deep-dive** (vol1). Treat this as a careful, citation-rich technical history — closer in tone to Wellerstein's *Restricted Data* than to clickbait. Doses, dates, names, and configurations need to match authoritative sources (Wikipedia *Demon core* / *Daghlian* / *Slotin* / *Pit (nuclear weapon)*, AHF Nuclear Museum, McLaughlin's *Review of Criticality Accidents* if obtainable). Where sources disagree, flag the disagreement in the prose rather than picking silently.
2. **Replica build** (vol2). Treat this as a maker how-to grounded in three reference builds — Adam Savage's *Tested* video, the Attoparsec Halloween 2019 build, and the FuzzyRaptor + blackrat Printables models. Cite all three. The replica is non-functional, non-fissile, and is explicitly a *display piece* and *educational prop*; nothing here should read as instructions for anything other than a 3D-printed sphere and a painted box.

## Tone

- Solemn for the history sections — two scientists died and several more had their lives shortened. Avoid the meme-y "spicy rock" tone the demon core has accumulated online; reserve a brief cultural-legacy note for the end of vol1.
- Practical and chatty for the build sections, matching how Jeff writes elsewhere.

## What to do automatically

- Pull figures via the Photo Helper into `02-inputs/deep_dive/figs/` (history imagery) and `03-outputs/figs/` (build photos). Always include the `creditLine` verbatim in the caption.
- Resolve relative dates to absolute dates ("today" / "Thursday") whenever they appear in Jeff's messages, and write only absolute dates into the files.

## What to ask first

- Whether to split history into multiple volumes (vol1 history of the program, vol2 Daghlian, vol3 Slotin, vol4 disposition + legacy) vs. one long vol1. Current scaffold is **one long vol1**; ask before splitting.
- Whether the build vol covers *both* the core and the case in one document or two (current scaffold: one combined vol2).
- Whether to attempt the historically accurate magnesium box (machinable but expensive and reactive) or to mimic Adam Savage's Rich-Light-phenolic + crackle-paint approach (current scaffold assumes Savage-style).

## Citations

Inline links in prose for canonical sources; a `## References` section at the bottom of each volume mirrors the bibliography style used in `Brewing and Distilling/Distilling/02-inputs/deep_dive/vol*.md`.
