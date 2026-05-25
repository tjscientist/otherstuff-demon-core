#!/usr/bin/env python3
"""
build_single_html.py — compile volume_sources/*.md → a single self-contained HTML

Default invocation (from any directory):
    python3 _shared/build/build_single_html.py

Reads vol_*.md files from Distilling/00-deep-dive/volume_sources/ in filename
order, converts markdown to HTML, and writes
Distilling/03-outputs/Distilling_Complete.html.

Features
--------
  - Sticky top header with inline full-text search (no external dependencies)
  - Fixed sidebar TOC with scroll-spy (IntersectionObserver)
  - Numbered figure placeholders  (<!-- FIGURE SLOT: description -->)
  - Numbered tables; List of Tables appendix
  - List of Figures section before Volume 1
  - Dark theme matching BrewingDistillingStartHere.html
  - Mobile-responsive: sidebar collapses behind a toggle button

Run from the project root:
    python3 _shared/build/build_single_html.py

CLI flags:
    --root PATH         project root (default: 2 levels up from this script)
    --volume-dir PATH   directory containing vol_*.md files
    --output PATH       output HTML path
    --title TEXT        document title
"""
from __future__ import annotations

import argparse
import base64
import html as html_mod
import json
import mimetypes
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VOL_DIR_REL = "02-inputs/deep_dive"
DEFAULT_OUTPUT_REL = "03-outputs/The_Demon_Core_Complete.html"
DEFAULT_PHOTOS_DIR_REL = "02-inputs/deep_dive/figs"
DEFAULT_TITLE = "The Demon Core — Complete Reference"

# Set by build(); read by the FIGURE directive handler.
_PHOTOS_DIR: Path | None = None

# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


class TocEntry(NamedTuple):
    level: int      # 1=h1, 2=h2, 3=h3, 4=h4
    text: str       # plain text (no HTML)
    anchor: str     # id attribute on the heading element


class FigureEntry(NamedTuple):
    number: int
    description: str
    vol_title: str  # text of the most recent h1


class TableEntry(NamedTuple):
    number: int
    caption: str    # first non-separator header cell(s)
    vol_title: str


# ---------------------------------------------------------------------------
# Markdown → HTML converter
# ---------------------------------------------------------------------------


class _MDState:
    """Mutable parser state passed through conversion."""

    def __init__(self, vol_title: str, fig_start: int, tbl_start: int) -> None:
        self.vol_title = vol_title
        self.fig_counter = fig_start
        self.tbl_counter = tbl_start
        self.anchor_counts: dict[str, int] = {}
        self.toc: list[TocEntry] = []
        self.figures: list[FigureEntry] = []
        self.tables: list[TableEntry] = []

    def make_anchor(self, text: str) -> str:
        base = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "section"
        if base in self.anchor_counts:
            self.anchor_counts[base] += 1
            return f"{base}-{self.anchor_counts[base]}"
        self.anchor_counts[base] = 0
        return base


def _escape(text: str) -> str:
    return html_mod.escape(text, quote=True)


def _embed_image(filename: str) -> str:
    """Resolve filename against _PHOTOS_DIR, base64-encode, emit <img> tag."""
    if _PHOTOS_DIR is None:
        return f'<div class="fig-missing">[FIGURE: photos dir not configured for {_escape(filename)}]</div>'
    path = _PHOTOS_DIR / filename
    if not path.is_file():
        return f'<div class="fig-missing">[FIGURE: file not found: {_escape(filename)}]</div>'
    mime, _ = mimetypes.guess_type(str(path))
    if not mime:
        mime = "application/octet-stream"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f'<img src="data:{mime};base64,{data}" alt="{_escape(filename)}">'


def _autolink_urls(text: str) -> str:
    """Pre-pass: turn URLs into markdown link syntax so the existing link
    extractor renders them as clickable anchors.

      - Code-span URLs (``` `https://...` ```) become ``` [`URL`](URL) ```
        — clickable, displayed as inline-code.
      - Bare prose URLs (`https://...` not already in a link or code span)
        become `[URL](URL)`.

    URLs already inside an existing markdown link `[text](URL)` are preserved
    verbatim: the function processes text between existing-link boundaries.
    """
    # 1. Code-span URLs first so the bare-URL pass below doesn't double-wrap.
    #    Exclude the typographic ellipsis (…) so prose like `https://…` is
    #    recognised as a placeholder, not an autolinkable URL.
    text = re.sub(
        r"`(https?://[^\s`…]+)`",
        lambda m: f"[`{m.group(1)}`]({m.group(1)})",
        text,
    )

    # 2. Bare URLs, skipping anything inside an existing markdown link.
    link_re = re.compile(r"\[[^\]]*\]\([^)]+\)")
    bare_url_re = re.compile(r"\bhttps?://[^\s)\]<>`\"'…]+")

    def autolink_chunk(chunk: str) -> str:
        return bare_url_re.sub(lambda m: f"[{m.group(0)}]({m.group(0)})", chunk)

    out: list[str] = []
    pos = 0
    for lm in link_re.finditer(text):
        out.append(autolink_chunk(text[pos:lm.start()]))
        out.append(lm.group(0))  # preserve existing link verbatim
        pos = lm.end()
    out.append(autolink_chunk(text[pos:]))
    return "".join(out)


def _inline(text: str) -> str:
    """Apply inline markdown → HTML (links, code, bold, italic).

    A `_autolink_urls` pre-pass turns bare URLs and code-span URLs into
    markdown link syntax so the link extractor below picks them up.

    Links are extracted FIRST so that link text containing an inline code span
    (`[\\`name\\`](url)`) renders correctly — otherwise the code-span pass would
    split the link apart at the backticks and orphan the `]` and `(url)` halves.
    Inside link text, inline code + bold + italic still render. Nested links
    are not supported (rare in practice).
    """
    text = _autolink_urls(text)
    LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    parts: list[str] = []
    last = 0
    for m in LINK_RE.finditer(text):
        parts.append(_inline_no_links(text[last:m.start()]))
        inner = _inline_no_links(m.group(1))
        href = m.group(2)
        # External links (http/https) open in a new tab so the deep dive
        # stays put while the reader browses a vendor page, Wikipedia
        # article, etc. Internal anchors (#…) and relative paths stay
        # in the same tab — they're part of this document's own navigation.
        attrs = ''
        if href.startswith('http://') or href.startswith('https://'):
            attrs = ' target="_blank" rel="noopener noreferrer"'
        parts.append(f'<a href="{_escape(href)}"{attrs}>{inner}</a>')
        last = m.end()
    parts.append(_inline_no_links(text[last:]))
    return "".join(parts)


def _inline_no_links(text: str) -> str:
    """Inline-render WITHOUT link detection: code spans, bold, italic."""
    parts: list[str] = []
    remainder = text
    code_re = re.compile(r"`([^`]+)`")
    last = 0
    for m in code_re.finditer(remainder):
        parts.append(_emphasize_and_escape(remainder[last:m.start()]))
        parts.append(f"<code>{_escape(m.group(1))}</code>")
        last = m.end()
    parts.append(_emphasize_and_escape(remainder[last:]))
    return "".join(parts)


def _process_inline_no_code(text: str) -> str:
    """Legacy alias retained for any external callers / tests."""
    return _emphasize_and_escape(text)


def _emphasize_and_escape(text: str) -> str:
    """Bold/italic substitution, then escape remaining literal characters.

    Handles three nested patterns explicitly BEFORE the standard bold/italic
    passes, because the standard passes rely on regex non-greediness which
    breaks down at triple-asterisk boundaries (`**X*Y***` would otherwise have
    the orphan trailing `*` pair with the inner italic open, capturing the
    inserted `</strong>` as italic content):
      ***X***       -> <strong><em>X</em></strong>      (CommonMark "strong-em")
      **X*Y***      -> <strong>X<em>Y</em></strong>     (italic at end of bold)
      ***X*Y**      -> <strong><em>X</em>Y</strong>     (italic at start of bold)
    """
    # 1. Asymmetric: italic at end of bold:   **X*Y*** -> <strong>X<em>Y</em></strong>
    text = re.sub(r"\*\*([^*]+)\*([^*]+)\*\*\*",
                  lambda m: f"<strong>{_escape(m.group(1))}<em>{_escape(m.group(2))}</em></strong>",
                  text)
    # 2. Asymmetric: italic at start of bold: ***X*Y** -> <strong><em>X</em>Y</strong>
    text = re.sub(r"\*\*\*([^*]+)\*([^*]+)\*\*",
                  lambda m: f"<strong><em>{_escape(m.group(1))}</em>{_escape(m.group(2))}</strong>",
                  text)
    # 3. Pure strong-em: ***X*** -> <strong><em>X</em></strong>
    text = re.sub(r"\*\*\*([^*]+)\*\*\*",
                  lambda m: f"<strong><em>{_escape(m.group(1))}</em></strong>",
                  text)

    # 4. Standard bold **text** (also handles middle-of-text italic-inside-bold
    #    via the post-bold italic pass below)
    text = re.sub(r"\*\*(.+?)\*\*", lambda m: f"<strong>{_escape(m.group(1))}</strong>", text)
    # 5. Standard italic *text* (not preceded/followed by *)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)",
                  lambda m: f"<em>{_escape(m.group(1))}</em>", text)
    # Escape remaining literal text. Two passes need preservation:
    #   1. Inline-substituted tags from earlier in this pipeline
    #      (strong/em/code/a) pass through verbatim. Any OTHER angle-bracketed
    #      sequence — including placeholders the author wrote like `<target>`,
    #      `<N>`, `<hex>` — gets escaped to &lt;...&gt; so it doesn't break
    #      HTML validity (e.g. `<target>` would orphan a phantom <target> tag
    #      with no closer).
    #   2. Existing HTML entities (`&amp;`, `&lt;`, `&gt;`, `&quot;`, `&#x27;`,
    #      `&#NN;`, `&#xNN;`, `&name;`) pass through unchanged. Without this,
    #      bold/italic substitutions that already escaped an apostrophe to
    #      `&#x27;` would have the `&` re-escaped to `&amp;`, producing
    #      `&amp;#x27;` which renders as the literal text "&#x27;" in
    #      browsers — the artifact the user reported as "wash&#x27;s ABV".
    _INLINE_TAG_RE = re.compile(r"^</?(strong|em|code|a)(\s[^>]*)?>$", re.IGNORECASE)
    _ENTITY_RE = re.compile(r"&(?:#[0-9]+|#x[0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]{1,30});")
    result = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c == '<':
            j = text.find('>', i)
            if j != -1:
                candidate = text[i:j+1]
                if _INLINE_TAG_RE.match(candidate):
                    result.append(candidate)
                    i = j + 1
                    continue
        elif c == '&':
            m = _ENTITY_RE.match(text, i)
            if m:
                result.append(m.group(0))
                i = m.end()
                continue
        result.append(html_mod.escape(c, quote=False))
        i += 1
    return "".join(result)


def _render_table(rows: list[list[str]], state: _MDState) -> str:
    """Convert a list of rows (already text) into an HTML table, collect entry."""
    if len(rows) < 1:
        return ""
    state.tbl_counter += 1
    n = state.tbl_counter

    # Derive caption from first row header cells
    caption = " | ".join(c.strip() for c in rows[0] if c.strip()) if rows else f"Table {n}"
    state.tables.append(TableEntry(n, caption, state.vol_title))

    html_parts = [f'<table id="tbl-{n}" class="data-table">',
                  f'<caption>Table {n}</caption>']

    # Header
    html_parts.append("<thead><tr>")
    for cell in rows[0]:
        html_parts.append(f"<th>{_inline(cell.strip())}</th>")
    html_parts.append("</tr></thead>")

    # Body (skip separator row — all cells match /^[-: ]+$/)
    html_parts.append("<tbody>")
    for row in rows[1:]:
        if all(re.match(r"^[-: ]+$", c.strip()) for c in row if c.strip()):
            continue  # separator row
        html_parts.append("<tr>")
        for cell in row:
            html_parts.append(f"<td>{_inline(cell.strip())}</td>")
        html_parts.append("</tr>")
    html_parts.append("</tbody></table>")
    return "\n".join(html_parts)


def _split_table_row(line: str) -> list[str]:
    """'| a | b | c |' → ['a', 'b', 'c']"""
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return line.split("|")


def md_to_html(source: str, state: _MDState) -> str:
    """Convert a single markdown volume file to HTML body, updating state."""
    lines = source.splitlines()
    output: list[str] = []

    # Parser state machine
    IN_PARA = "para"
    IN_CODE = "code"
    IN_UL = "ul"
    IN_OL = "ol"
    IN_BQUOTE = "bquote"
    IN_TABLE = "table"
    mode = None
    para_buf: list[str] = []
    code_fence_lang = ""
    code_buf: list[str] = []
    list_buf: list[str] = []
    bquote_buf: list[str] = []
    table_rows: list[list[str]] = []

    def flush_para() -> None:
        nonlocal mode, para_buf
        if para_buf:
            text = " ".join(para_buf)
            output.append(f"<p>{_inline(text)}</p>")
        para_buf = []
        mode = None

    def flush_ul() -> None:
        nonlocal mode, list_buf
        if list_buf:
            items = "\n".join(f"<li>{_inline(item)}</li>" for item in list_buf)
            output.append(f"<ul>\n{items}\n</ul>")
        list_buf = []
        mode = None

    def flush_ol() -> None:
        nonlocal mode, list_buf
        if list_buf:
            items = "\n".join(f"<li>{_inline(item)}</li>" for item in list_buf)
            output.append(f"<ol>\n{items}\n</ol>")
        list_buf = []
        mode = None

    def flush_bquote() -> None:
        nonlocal mode, bquote_buf
        if bquote_buf:
            inner = "<br>".join(_inline(line) for line in bquote_buf)
            output.append(f'<blockquote class="callout">{inner}</blockquote>')
        bquote_buf = []
        mode = None

    def flush_table() -> None:
        nonlocal mode, table_rows
        if table_rows:
            output.append(_render_table(table_rows, state))
        table_rows = []
        mode = None

    def flush_current() -> None:
        if mode == IN_PARA:
            flush_para()
        elif mode == IN_UL:
            flush_ul()
        elif mode == IN_OL:
            flush_ol()
        elif mode == IN_BQUOTE:
            flush_bquote()
        elif mode == IN_TABLE:
            flush_table()

    for raw_line in lines:
        line = raw_line

        # ---- Code fence open/close ----
        if mode == IN_CODE:
            if line.strip().startswith("```"):
                lang_class = f' class="language-{html_mod.escape(code_fence_lang)}"' if code_fence_lang else ""
                code_text = "\n".join(code_buf)
                output.append(f"<pre><code{lang_class}>{html_mod.escape(code_text)}</code></pre>")
                code_buf = []
                mode = None
            else:
                code_buf.append(line)
            continue

        if line.strip().startswith("```"):
            flush_current()
            code_fence_lang = line.strip()[3:].strip()
            mode = IN_CODE
            continue

        # ---- Blank line: flush current block ----
        if not line.strip():
            flush_current()
            continue

        # ---- HTML comments (pass through; collect figure slots) ----
        # Filled figure: <!-- FIGURE: filename :: description :: credit -->
        fig_filled = re.match(
            r"<!--\s*FIGURE:\s*([^:]+?)\s*::\s*(.+?)\s*::\s*(.+?)\s*-->",
            line.strip(), re.IGNORECASE)
        if fig_filled:
            flush_current()
            filename, desc, credit = (g.strip() for g in fig_filled.groups())
            state.fig_counter += 1
            n = state.fig_counter
            state.figures.append(FigureEntry(n, desc, state.vol_title))
            img_html = _embed_image(filename)
            slot_html = (
                f'<figure class="figure" id="fig-{n}">'
                f'{img_html}'
                f'<figcaption>Fig. {n} — {_escape(desc)} '
                f'<span class="fig-credit">{_escape(credit)}</span>'
                f'</figcaption>'
                f'</figure>'
            )
            output.append(slot_html)
            continue

        fig_match = re.match(r"<!--\s*FIGURE SLOT:\s*(.+?)\s*-->", line.strip(), re.IGNORECASE)
        if fig_match:
            flush_current()
            desc = fig_match.group(1)
            state.fig_counter += 1
            n = state.fig_counter
            state.figures.append(FigureEntry(n, desc, state.vol_title))
            slot_html = (
                f'<figure class="figure-slot" id="fig-{n}">'
                f'<div class="fig-placeholder">'
                f'[Photo placeholder — Fig. {n}: {_escape(desc)}]'
                f'</div>'
                f'<figcaption>Fig. {n} — {_escape(desc)}</figcaption>'
                f'</figure>'
            )
            output.append(slot_html)
            continue

        # Other HTML comments: pass through verbatim
        if line.strip().startswith("<!--") and "-->" in line:
            flush_current()
            output.append(line)
            continue

        # ---- Headings ----
        hm = re.match(r"^(#{1,4})\s+(.+)$", line)
        if hm:
            flush_current()
            level = len(hm.group(1))
            text = hm.group(2).strip()
            # Strip trailing # characters
            text = re.sub(r"\s+#+\s*$", "", text).strip()
            anchor = state.make_anchor(text)
            state.toc.append(TocEntry(level, text, anchor))
            if level == 1:
                state.vol_title = text
            tag = f"h{level}"
            output.append(f'<{tag} id="{anchor}">{_inline(text)}</{tag}>')
            continue

        # ---- Horizontal rule ----
        if re.match(r"^(-{3,}|\*{3,}|_{3,})\s*$", line.strip()):
            flush_current()
            output.append("<hr>")
            continue

        # ---- Blockquote ----
        bq_match = re.match(r"^>\s*(.*)", line)
        if bq_match:
            if mode not in (None, IN_BQUOTE):
                flush_current()
            mode = IN_BQUOTE
            bquote_buf.append(bq_match.group(1))
            continue

        # ---- Table row ----
        if line.lstrip().startswith("|"):
            if mode not in (None, IN_TABLE):
                flush_current()
            mode = IN_TABLE
            table_rows.append(_split_table_row(line))
            continue
        elif mode == IN_TABLE:
            flush_table()

        # ---- Unordered list ----
        ul_match = re.match(r"^(\s*)[-*]\s+(.+)$", line)
        if ul_match:
            if mode not in (None, IN_UL):
                flush_current()
            mode = IN_UL
            list_buf.append(ul_match.group(2))
            continue

        # ---- Ordered list ----
        ol_match = re.match(r"^\s*\d+\.\s+(.+)$", line)
        if ol_match:
            if mode not in (None, IN_OL):
                flush_current()
            mode = IN_OL
            list_buf.append(ol_match.group(1))
            continue

        # ---- Paragraph text ----
        if mode != IN_PARA:
            flush_current()
            mode = IN_PARA
        para_buf.append(line.strip())

    flush_current()
    return "\n".join(output)


# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------

PAGE_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
  :root {
    --bg:          #0e1116;
    --panel:       #161b22;
    --panel2:      #1d242d;
    --panel3:      #11161d;
    --ink:         #e6edf3;
    --ink-dim:     #9ba8b6;
    --ink-faint:   #6b7681;
    --rule:        #2a323d;
    --accent:      #ffb454;
    --accent-soft: #6c4a15;
    --accent-bg:   #ffb45418;
    --link:        #79c0ff;
    --link-hover:  #ffb454;
    --mark-bg:     #ffb45433;
    --mark-fg:     #ffd793;
    --sidebar-w:   260px;
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto,
                 "Helvetica Neue", Arial, sans-serif;
  }

  html, body { background: var(--bg); color: var(--ink); margin: 0; padding: 0; }
  body { line-height: 1.6; }
  a { color: var(--link); text-decoration: none; }
  a:hover { color: var(--link-hover); text-decoration: underline; }

  /* ---- Top bar ---- */
  .top-bar {
    position: sticky; top: 0; z-index: 20;
    background: var(--panel);
    border-bottom: 1px solid var(--rule);
    display: flex; align-items: center; gap: .75rem;
    padding: .55rem 1rem .55rem .9rem;
    backdrop-filter: blur(6px);
  }
  .top-bar .menu-btn {
    display: none; background: none; border: none;
    color: var(--ink-dim); cursor: pointer; font-size: 1.3rem; padding: 0 .2rem;
  }
  .top-bar .doc-title {
    font-size: .95rem; font-weight: 600;
    color: var(--accent); white-space: nowrap;
    flex-shrink: 0;
  }
  #search {
    flex: 1; font: inherit; font-size: .92rem;
    padding: .38rem .7rem;
    background: var(--bg); color: var(--ink);
    border: 1px solid var(--rule); border-radius: 5px; outline: none;
    min-width: 0;
  }
  #search:focus { border-color: var(--accent); }
  .nav-btn {
    background: var(--panel2); color: var(--ink-dim);
    border: 1px solid var(--rule); border-radius: 5px;
    padding: .3rem .55rem; cursor: pointer; font: inherit; font-size: .9rem;
    white-space: nowrap; line-height: 1; min-width: 2rem;
  }
  .nav-btn:hover:not(:disabled) { color: var(--accent); border-color: var(--accent); }
  .nav-btn:disabled { opacity: .35; cursor: not-allowed; }
  #search-counter {
    font-size: .8rem; color: var(--ink-dim); white-space: nowrap;
    min-width: 4.5rem; text-align: right;
  }

  /* ---- Layout shell ---- */
  .shell { display: flex; min-height: calc(100vh - 48px); }

  /* ---- TOC sidebar ---- */
  .toc-sidebar {
    width: var(--sidebar-w);
    flex-shrink: 0;
    position: sticky; top: 48px;
    height: calc(100vh - 48px);
    overflow-y: auto;
    border-right: 1px solid var(--rule);
    padding: .9rem 0;
    background: var(--panel3);
    scrollbar-width: thin;
    scrollbar-color: var(--rule) transparent;
  }
  .toc-sidebar .toc-heading {
    display: block;
    font-size: .7rem; text-transform: uppercase; letter-spacing: .13em;
    color: var(--accent); padding: 0 1rem .55rem; font-weight: 600;
    text-decoration: none;
    transition: color .1s;
  }
  .toc-sidebar a.toc-heading:hover { color: var(--ink); text-decoration: none; }
  .toc-list { list-style: none; padding: 0; margin: 0; }
  .toc-list li a {
    display: block; padding: .22rem 1rem;
    font-size: .82rem; color: var(--ink-dim);
    border-left: 2px solid transparent;
    transition: color .1s, border-color .1s;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  .toc-list li a:hover { color: var(--ink); text-decoration: none; }
  .toc-list li a.active { color: var(--accent); border-left-color: var(--accent); }
  .toc-h1 > a { font-weight: 600; color: var(--ink); padding-left: 1rem; }
  .toc-h2 > a { padding-left: 1.7rem; }
  .toc-h3 > a { padding-left: 2.3rem; font-size: .78rem; }
  .toc-h4 > a { padding-left: 2.9rem; font-size: .75rem; }
  .toc-vol-sep {
    margin: .5rem 1rem .2rem;
    border-top: 1px solid var(--rule);
  }

  /* ---- Collapsible sidebar volumes ---- */
  .toc-vol { margin: 0; }
  .toc-vol-head {
    display: flex; align-items: stretch;
    border-left: 2px solid transparent;
    transition: border-color .1s, background-color .1s;
  }
  .toc-vol-head:hover { background: var(--panel2); }
  /* ---- Sidebar controls bar (Collapse all / Collapse others) ---- */
  /* Sticky to the TOP of the sidebar's own scrolling container so the
     buttons remain reachable no matter how far the TOC has been scrolled.
     The negative top compensates for the sidebar's own padding so the
     bar pins flush to the visible edge. */
  .toc-controls {
    display: flex; gap: .4rem;
    padding: .55rem .8rem;
    border-bottom: 1px solid var(--rule);
    margin-bottom: .55rem;
    position: sticky;
    top: -0.9rem;  /* counteracts the sidebar's `padding: .9rem 0` top */
    z-index: 2;
    background: var(--panel3);  /* matches sidebar background so it's opaque */
    backdrop-filter: blur(4px);
  }
  .toc-ctrl {
    flex: 1; background: var(--panel2); color: var(--ink-dim);
    border: 1px solid var(--rule); border-radius: 4px;
    padding: .28rem .35rem; font: inherit; font-size: .72rem;
    cursor: pointer; white-space: nowrap;
    transition: color .1s, border-color .1s, background-color .1s;
  }
  .toc-ctrl:hover { color: var(--accent); border-color: var(--accent-soft);
                    background: var(--accent-bg); }
  .toc-ctrl:active { transform: translateY(1px); }

  .toc-vol-head .toc-toggle {
    flex: 0 0 auto;
    background: none; border: none; cursor: pointer;
    color: var(--ink-faint); font-size: .7rem; line-height: 1;
    padding: 0 .35rem 0 .7rem;
    transition: transform .15s ease, color .1s;
  }
  .toc-vol-head .toc-toggle:hover { color: var(--accent); }
  .toc-vol-head .toc-toggle::before { content: "\25B8"; display: inline-block; transition: transform .15s ease; }
  .toc-vol[data-expanded="true"] > .toc-vol-head .toc-toggle::before { transform: rotate(90deg); }
  .toc-vol-head a {
    flex: 1; padding: .25rem .7rem .25rem 0;
    font-weight: 600; color: var(--ink); font-size: .82rem;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    border-left: none;
  }
  .toc-vol-head a:hover { color: var(--ink); text-decoration: none; }
  .toc-vol-head a.active { color: var(--accent); }
  .toc-vol[data-expanded="true"] > .toc-vol-head { border-left-color: var(--accent-soft); }
  .toc-vol-children {
    list-style: none; padding: 0; margin: 0;
    max-height: 0; overflow: hidden;
    transition: max-height .25s ease;
  }
  .toc-vol[data-expanded="true"] > .toc-vol-children {
    max-height: 4000px;
  }

  /* ---- Title page ---- */
  .title-page {
    min-height: calc(100vh - 8rem);
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center; padding: 3rem 1rem;
    border-bottom: 1px solid var(--rule);
    margin-bottom: 2.5rem;
  }
  .title-page .tp-eyebrow {
    font-size: .8rem; letter-spacing: .35em;
    text-transform: uppercase; color: var(--ink-faint);
    margin-bottom: 1.5rem;
  }
  .title-page h1.tp-title {
    font-size: 3.2rem; color: var(--accent);
    margin: 0 0 .8rem; border: none; padding: 0;
    letter-spacing: .02em; line-height: 1.15;
  }
  .title-page .tp-subtitle {
    font-size: 1.15rem; color: var(--ink); font-style: italic;
    max-width: 38rem; margin: 0 auto 2.4rem;
    line-height: 1.5;
  }
  .title-page .tp-rule {
    width: 6rem; height: 2px; background: var(--accent-soft);
    margin: 1.2rem auto 2rem;
  }
  .title-page .tp-author {
    font-size: 1rem; color: var(--ink-dim);
    margin: .3rem 0;
  }
  .title-page .tp-author strong { color: var(--ink); font-size: 1.05rem; }
  .title-page .tp-meta {
    margin-top: 2.5rem; font-size: .85rem; color: var(--ink-faint);
    line-height: 1.7;
  }
  .title-page .tp-meta div { margin: .15rem 0; }
  .title-page h1.tp-title:first-child { margin-top: 0; }

  /* ---- Formal Table of Contents (in main content) ---- */
  .formal-toc {
    margin: 0 0 2.5rem; padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--rule);
  }
  .formal-toc h2.ft-heading {
    font-size: 1.8rem; color: var(--accent);
    border: none; padding: 0; margin: 0 0 1.3rem;
    letter-spacing: .05em; text-transform: uppercase;
  }
  .formal-toc .ft-section {
    margin: 1.3rem 0 0;
  }
  .formal-toc .ft-vol-link {
    display: flex; align-items: baseline; gap: .5rem;
    font-weight: 700; color: var(--ink); font-size: 1rem;
    padding: .5rem 0 .35rem; margin-top: .8rem;
    border-bottom: 1px solid var(--rule);
  }
  .formal-toc .ft-vol-link .ft-leader {
    flex: 1; border-bottom: 1px dotted var(--ink-faint);
    margin: 0 .3rem; opacity: 0;
  }
  .formal-toc .ft-vol-link a { color: var(--ink); }
  .formal-toc .ft-vol-link a:hover { color: var(--accent); text-decoration: none; }
  .formal-toc ul.ft-children {
    list-style: none; padding: 0; margin: .25rem 0 .5rem 1.2rem;
  }
  .formal-toc ul.ft-children li {
    display: flex; align-items: baseline; gap: .4rem;
    font-size: .9rem; padding: .15rem 0;
    color: var(--ink-dim);
  }
  .formal-toc ul.ft-children li a { color: var(--ink-dim); }
  .formal-toc ul.ft-children li a:hover { color: var(--accent); text-decoration: none; }
  .formal-toc ul.ft-children li .ft-leader {
    flex: 1; border-bottom: 1px dotted var(--ink-faint);
    margin: 0 .3rem; opacity: .4;
    transform: translateY(-.25em);
  }
  .formal-toc .ft-frontmatter {
    margin-bottom: 1rem; padding-bottom: .5rem;
  }
  .formal-toc .ft-frontmatter ul {
    list-style: none; padding: 0; margin: .4rem 0 0;
  }
  .formal-toc .ft-frontmatter li {
    display: flex; align-items: baseline; gap: .4rem;
    font-size: .92rem; padding: .2rem 0; color: var(--ink-dim);
  }
  .formal-toc .ft-frontmatter li a { color: var(--ink-dim); }
  .formal-toc .ft-frontmatter li a:hover { color: var(--accent); text-decoration: none; }
  .formal-toc .ft-frontmatter li .ft-leader {
    flex: 1; border-bottom: 1px dotted var(--ink-faint);
    margin: 0 .3rem; opacity: .4; transform: translateY(-.25em);
  }
  .formal-toc .ft-label {
    font-size: .72rem; text-transform: uppercase; letter-spacing: .15em;
    color: var(--accent); margin-top: 1.6rem;
  }

  /* ---- Main content ---- */
  .main-content {
    flex: 1; min-width: 0;
    padding: 2rem 2.5rem 4rem;
    max-width: 860px;
  }

  /* ---- Typography ---- */
  /* scroll-margin-top: keeps the heading from landing UNDER the sticky
     top bar when navigated to via an in-page anchor link (sidebar TOC,
     formal TOC, "Vol N §X.Y" cross-references, etc.). The top bar is
     ~48px tall; 60px leaves a small breathing margin underneath. */
  h1, h2, h3, h4 { scroll-margin-top: 60px; }
  h1 { font-size: 1.9rem; color: var(--accent); margin: 2rem 0 .5rem;
       border-bottom: 2px solid var(--accent-soft); padding-bottom: .35rem; }
  h1:first-child { margin-top: 0; }
  h2 { font-size: 1.35rem; color: var(--ink); margin: 1.8rem 0 .4rem;
       border-bottom: 1px solid var(--rule); padding-bottom: .2rem; }
  h3 { font-size: 1.1rem; color: var(--ink); margin: 1.4rem 0 .3rem; }
  h4 { font-size: 1rem; color: var(--ink-dim); margin: 1.1rem 0 .25rem; }
  /* Also apply to <div class="volume"> wrappers (their id IS the h1's
     id when navigating via the sidebar's "Vol N" link) */
  .volume[id] { scroll-margin-top: 60px; }
  /* And to the front-matter section anchors */
  #title-page, #table-of-contents, #list-of-figures, #list-of-tables {
    scroll-margin-top: 60px;
  }
  p { margin: .6rem 0; }
  hr { border: none; border-top: 1px solid var(--rule); margin: 1.8rem 0; }
  strong { color: var(--ink); }

  /* ---- Volume separator ---- */
  .vol-break { margin-top: 3rem; }

  /* ---- Callout blockquote ---- */
  blockquote.callout {
    border-left: 3px solid var(--accent);
    background: var(--accent-bg);
    margin: 1rem 0; padding: .7rem 1rem;
    border-radius: 0 6px 6px 0;
    color: var(--ink-dim);
    font-size: .93rem;
  }

  /* ---- Tables ---- */
  .data-table {
    border-collapse: collapse; width: 100%;
    font-size: .9rem; margin: 1rem 0 1.4rem;
  }
  .data-table caption {
    caption-side: bottom; font-size: .78rem; color: var(--ink-faint);
    text-align: left; padding: .3rem .2rem;
  }
  .data-table th {
    background: var(--panel2); color: var(--accent);
    font-size: .8rem; text-transform: uppercase; letter-spacing: .07em;
    padding: .5rem .7rem; text-align: left;
    border-bottom: 1px solid var(--rule);
  }
  .data-table td {
    padding: .45rem .7rem;
    border-bottom: 1px solid var(--rule);
    vertical-align: top;
  }
  .data-table tr:last-child td { border-bottom: none; }
  .data-table tr:hover td { background: var(--panel2); }

  /* ---- Code ---- */
  pre {
    background: var(--panel2); border: 1px solid var(--rule);
    border-radius: 6px; padding: 1rem 1.1rem; overflow-x: auto;
    font-size: .85rem; line-height: 1.5; margin: .8rem 0;
  }
  code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
  p code, li code, td code {
    background: var(--panel2); border: 1px solid var(--rule);
    border-radius: 3px; padding: .05em .35em; font-size: .87em;
  }

  /* ---- Lists ---- */
  ul, ol { padding-left: 1.6rem; margin: .5rem 0; }
  li { margin: .25rem 0; }

  /* ---- Figure slots ---- */
  .figure, .figure-slot {
    margin: 1.4rem 0; text-align: center;
  }
  .figure img {
    max-width: 100%; height: auto; border-radius: 6px;
    background: var(--panel); border: 1px solid var(--rule);
    cursor: zoom-in;  /* hint that clicking enlarges */
    transition: filter .15s ease;
  }
  .figure img:hover { filter: brightness(1.08); }

  /* ---- Lightbox (click-to-enlarge for figures) ---- */
  .lightbox-overlay {
    display: none;
    position: fixed; inset: 0; z-index: 100;
    background: rgba(0, 0, 0, 0.92);
    flex-direction: column; align-items: center; justify-content: center;
    padding: 2rem 3rem 1rem;
    cursor: zoom-out;
  }
  .lightbox-overlay.visible { display: flex; }
  .lightbox-image {
    max-width: 95vw; max-height: 82vh;
    width: auto; height: auto;
    border-radius: 6px;
    background: var(--panel);
    box-shadow: 0 8px 40px #0009;
  }
  .lightbox-caption {
    color: var(--ink-dim); font-size: .92rem; font-style: italic;
    max-width: 90vw; margin-top: 1rem; text-align: center;
    line-height: 1.5;
  }
  .lightbox-caption .fig-credit {
    display: block; margin-top: .35rem;
    font-size: .78rem; color: var(--ink-faint); font-style: normal;
  }
  .lightbox-close {
    position: absolute; top: 1rem; right: 1.4rem;
    background: transparent; border: none;
    color: var(--ink); font-size: 2rem; line-height: 1;
    cursor: pointer; padding: .25rem .65rem;
    border-radius: 6px;
  }
  .lightbox-close:hover { background: rgba(255, 255, 255, 0.08); color: var(--accent); }
  .lightbox-hint {
    position: absolute; bottom: 1rem; left: 50%; transform: translateX(-50%);
    color: var(--ink-faint); font-size: .75rem; letter-spacing: .12em;
    text-transform: uppercase;
  }
  .fig-placeholder, .fig-missing {
    background: var(--panel2); border: 1px dashed var(--accent-soft);
    border-radius: 6px; padding: 2rem 1rem;
    color: var(--ink-faint); font-size: .87rem; font-style: italic;
  }
  figcaption {
    margin-top: .45rem; font-size: .82rem;
    color: var(--ink-dim); font-style: italic;
  }
  .fig-credit {
    display: block; margin-top: .2rem; font-size: .74rem;
    color: var(--ink-faint); font-style: normal;
  }

  /* ---- List of Figures / List of Tables ---- */
  .meta-list { list-style: none; padding: 0; margin: 0; }
  .meta-list li {
    display: grid;
    grid-template-columns: 4.5rem 1fr 16rem;
    gap: .8rem;
    align-items: baseline;
    padding: .3rem 0; border-bottom: 1px solid var(--rule);
    font-size: .88rem;
  }
  .meta-list li:last-child { border-bottom: none; }
  .meta-list .ml-num { color: var(--accent); font-weight: 600; }
  .meta-list .ml-vol {
    color: var(--ink-faint); font-size: .78rem;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  @media (max-width: 700px) {
    .meta-list li { grid-template-columns: 4rem 1fr; }
    .meta-list .ml-vol { grid-column: 2; padding-left: 0; }
  }

  /* ---- Search hit highlighting (find-in-page) ---- */
  mark.search-hit {
    background: var(--mark-bg); color: var(--mark-fg);
    padding: 0 .1em; border-radius: 2px; font-weight: 600;
    scroll-margin-top: 60px;  /* keep clear of the sticky top-bar on scrollIntoView */
  }
  mark.search-hit.current {
    background: var(--accent); color: var(--bg);
    outline: 2px solid var(--accent); outline-offset: 1px;
    box-shadow: 0 0 0 4px #ffb45444;
  }

  /* ---- Mobile ---- */
  @media (max-width: 700px) {
    .top-bar .menu-btn { display: block; }
    .toc-sidebar {
      position: fixed; left: 0; top: 48px; bottom: 0; z-index: 15;
      transform: translateX(-100%); transition: transform .2s ease;
      width: 280px;
    }
    .toc-sidebar.open { transform: translateX(0); box-shadow: 4px 0 24px #0008; }
    .main-content { padding: 1.2rem 1rem 3rem; }
    h1 { font-size: 1.5rem; }
  }
</style>
</head>
<body>

<header class="top-bar">
  <button class="menu-btn" id="menu-btn" title="Toggle table of contents">&#9776;</button>
  <span class="doc-title">__TITLE__</span>
  <input id="search" type="search" placeholder="Search all volumes (find-in-page)…" autocomplete="off">
  <button id="search-prev" class="nav-btn" type="button" title="Previous match (Shift+Enter)" disabled>&#9650;</button>
  <button id="search-next" class="nav-btn" type="button" title="Next match (Enter)" disabled>&#9660;</button>
  <span id="search-counter"></span>
</header>

<div class="shell">
  <nav class="toc-sidebar" id="toc-sidebar">
    <div class="toc-controls">
      <button id="toc-collapse-all" class="toc-ctrl" type="button"
              title="Collapse every volume in the sidebar">Collapse all</button>
      <button id="toc-focus-active" class="toc-ctrl" type="button"
              title="Collapse all volumes except the one you're currently reading">Collapse others</button>
    </div>
    <ul class="toc-list" id="toc-list">
__TOC_ITEMS__
    </ul>
  </nav>

  <div class="main-content" id="main-content">
    __TITLE_PAGE__
    __TABLE_OF_CONTENTS__
    __LIST_OF_FIGURES__
    __LIST_OF_TABLES__
    <div id="volumes">
__VOLUMES_HTML__
    </div>
  </div>
</div>

<script>
(function(){
  'use strict';

  // --- Scroll-spy ---
  // Watch every heading WITH an id in the main content, PLUS the four
  // front-matter section wrappers (title-page / table-of-contents /
  // list-of-figures / list-of-tables) so their sidebar entries also
  // pick up the .active highlight as the reader scrolls past them.
  const allHeadings = Array.from(document.querySelectorAll(
    '#main-content h1[id], #main-content h2[id], #main-content h3[id], #main-content h4[id],' +
    ' #title-page, #table-of-contents, #list-of-figures, #list-of-tables'
  ));
  const tocLinks = {};
  document.querySelectorAll('#toc-list a[href^="#"]').forEach(a => {
    tocLinks[a.getAttribute('href').slice(1)] = a;
  });

  // --- Collapsible sidebar volumes ---
  const STORAGE_KEY = '__STORAGE_KEY__';
  const volumeNodes = Array.from(document.querySelectorAll('.toc-vol'));

  function loadExpandedState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      const arr = JSON.parse(raw);
      return Array.isArray(arr) ? new Set(arr) : null;
    } catch (e) { return null; }
  }
  function saveExpandedState() {
    const expanded = volumeNodes
      .filter(v => v.dataset.expanded === 'true')
      .map(v => v.dataset.volId);
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(expanded)); } catch (e) {}
  }
  function setVolExpanded(vol, expanded, manual) {
    vol.dataset.expanded = expanded ? 'true' : 'false';
    if (manual) {
      // Manual interaction "pins" the volume — clear the auto-expanded
      // flag so the accordion won't auto-collapse this volume next time
      // the user scrolls away from it. (If the user collapsed manually,
      // that's also a pin: the vol won't be re-opened by scroll-spy
      // unless the user enters a DIFFERENT volume first.)
      delete vol.dataset.autoExpanded;
    }
    const btn = vol.querySelector('.toc-toggle');
    if (btn) btn.setAttribute('aria-expanded', expanded ? 'true' : 'false');
  }

  // Initial state: restore from localStorage, or expand only the first volume.
  // Mark restored-expanded vols as autoExpanded so the accordion auto-collapses
  // them when the user scrolls into a different volume. (Otherwise opening the
  // page would leave every previously-expanded vol stuck open forever.)
  const restored = loadExpandedState();
  volumeNodes.forEach((vol, i) => {
    const id = vol.dataset.volId;
    const expand = restored ? restored.has(id) : (i === 0);
    setVolExpanded(vol, expand);
    if (expand) vol.dataset.autoExpanded = 'true';
  });

  // Toggle button (▸ disclosure arrow) — manual toggle
  document.querySelectorAll('.toc-toggle').forEach(btn => {
    btn.addEventListener('click', e => {
      e.preventDefault();
      e.stopPropagation();
      const vol = btn.closest('.toc-vol');
      if (!vol) return;
      const currentlyExpanded = vol.dataset.expanded === 'true';
      setVolExpanded(vol, !currentlyExpanded, true);
      saveExpandedState();
    });
  });

  // Volume TITLE link — clicking it also toggles, with two modes:
  //   - If currently collapsed: expand AND navigate (default link behavior)
  //   - If currently expanded:  collapse only (preventDefault — the user is
  //                             asking to hide, not to jump there again)
  document.querySelectorAll('.toc-vol-head > a').forEach(a => {
    a.addEventListener('click', e => {
      const vol = a.closest('.toc-vol');
      if (!vol) return;
      const isExpanded = vol.dataset.expanded === 'true';
      if (isExpanded) {
        e.preventDefault();
        setVolExpanded(vol, false, true);
      } else {
        setVolExpanded(vol, true, true);
        // navigation happens via the anchor href
      }
      saveExpandedState();
    });
  });

  // Map: heading anchor id → containing .toc-vol node (for auto-expand)
  const anchorToVol = {};
  volumeNodes.forEach(vol => {
    vol.querySelectorAll('a[href^="#"]').forEach(a => {
      anchorToVol[a.getAttribute('href').slice(1)] = vol;
    });
  });

  // --- Sidebar control buttons (Collapse all / Collapse others) ---
  const collapseAllBtn = document.getElementById('toc-collapse-all');
  const focusActiveBtn = document.getElementById('toc-focus-active');
  if (collapseAllBtn) {
    collapseAllBtn.addEventListener('click', () => {
      volumeNodes.forEach(v => setVolExpanded(v, false, true));
      saveExpandedState();
    });
  }
  if (focusActiveBtn) {
    focusActiveBtn.addEventListener('click', () => {
      // Find the currently-active volume (whichever contains the active
      // scroll-spy heading; fall back to the first if none).
      let target = (activeId && anchorToVol[activeId]) || volumeNodes[0];
      volumeNodes.forEach(v => setVolExpanded(v, v === target, true));
      saveExpandedState();
      // Scroll the sidebar so the now-expanded volume is visible
      if (target) {
        const sidebar = document.getElementById('toc-sidebar');
        const headRect = target.getBoundingClientRect();
        const sideRect = sidebar.getBoundingClientRect();
        if (headRect.top < sideRect.top || headRect.bottom > sideRect.bottom) {
          target.scrollIntoView({block: 'start', behavior: 'smooth'});
        }
      }
    });
  }

  let activeId = null;
  let activeVol = null;  // the .toc-vol element containing the active heading
  function setActive(id) {
    if (id === activeId) return;
    if (activeId && tocLinks[activeId]) tocLinks[activeId].classList.remove('active');
    activeId = id;

    // Accordion behaviour, run ONLY when the active VOLUME actually changes
    // (not on every heading change within the same vol):
    //   - Auto-collapse the volume the user just LEFT, if that vol was
    //     opened automatically (autoExpanded flag set). Manually-pinned
    //     vols stay open.
    //   - Auto-expand the volume the user just ENTERED, if it isn't already.
    //     Mark it autoExpanded so the next scroll-out will fold it again.
    const newActiveVol = id ? anchorToVol[id] : null;
    if (newActiveVol !== activeVol) {
      if (activeVol && activeVol.dataset.autoExpanded === 'true') {
        setVolExpanded(activeVol, false);    // auto-collapse, no manual flag
        delete activeVol.dataset.autoExpanded;
        saveExpandedState();
      }
      if (newActiveVol && newActiveVol.dataset.expanded !== 'true') {
        setVolExpanded(newActiveVol, true);  // auto-expand, no manual flag
        newActiveVol.dataset.autoExpanded = 'true';
        saveExpandedState();
      }
      activeVol = newActiveVol;
    }

    if (id && tocLinks[id]) {
      tocLinks[id].classList.add('active');
      // Scroll toc to show active link
      const sidebar = document.getElementById('toc-sidebar');
      const link = tocLinks[id];
      const sTop = sidebar.scrollTop, sH = sidebar.clientHeight;
      const lTop = link.offsetTop, lH = link.offsetHeight;
      if (lTop < sTop) sidebar.scrollTop = lTop - 40;
      else if (lTop + lH > sTop + sH) sidebar.scrollTop = lTop + lH - sH + 40;
    }
  }

  if (window.IntersectionObserver) {
    // Track every element currently intersecting the scroll-spy "active zone"
    // (the strip between rootMargin's top and bottom). On every state change,
    // pick the topmost element WHOSE TOP IS STILL IN THE VIEWPORT — i.e.
    // elements with non-negative rect.top. An element that has scrolled
    // partially above the viewport has rect.top < 0, which would otherwise
    // out-rank a heading that's actually visible at the top of the page.
    //
    // Concrete bug this fixes: clicking "Vol 1" while List of Tables is the
    // previous active section. During the smooth scroll, both LoT (exiting
    // the top, rect.top going very negative) and Vol 1 (entering, rect.top
    // a small positive value) intersect briefly. Without the >= 0 filter,
    // LoT wins because its top is "smaller" (more negative) and the LoT
    // sidebar entry stays highlighted instead of Vol 1.
    const intersecting = new Set();
    const io = new IntersectionObserver(entries => {
      for (const e of entries) {
        if (e.isIntersecting) intersecting.add(e.target);
        else                  intersecting.delete(e.target);
      }
      let best = null, bestTop = Infinity;
      intersecting.forEach(el => {
        const top = el.getBoundingClientRect().top;
        if (top < 0) return;          // skip headings scrolled above the viewport
        if (top < bestTop) { best = el; bestTop = top; }
      });
      // Fallback: if everything's been scrolled above, keep the highest-top
      // element (the one most recently scrolled past) so we don't lose the
      // active highlight entirely.
      if (!best && intersecting.size > 0) {
        let highest = null, highestTop = -Infinity;
        intersecting.forEach(el => {
          const top = el.getBoundingClientRect().top;
          if (top > highestTop) { highest = el; highestTop = top; }
        });
        best = highest;
      }
      if (best) setActive(best.id);
    }, { rootMargin: '-48px 0px -60% 0px', threshold: 0 });
    allHeadings.forEach(h => io.observe(h));
  }

  // --- Mobile TOC toggle ---
  const menuBtn = document.getElementById('menu-btn');
  const tocSidebar = document.getElementById('toc-sidebar');
  menuBtn.addEventListener('click', () => tocSidebar.classList.toggle('open'));
  document.addEventListener('click', e => {
    if (tocSidebar.classList.contains('open') &&
        !tocSidebar.contains(e.target) && e.target !== menuBtn)
      tocSidebar.classList.remove('open');
  });
  tocSidebar.querySelectorAll('a').forEach(a =>
    a.addEventListener('click', () => tocSidebar.classList.remove('open')));

  // --- Find-in-page search ---
  // Walks all text nodes in #main-content, wraps every literal match of the
  // query in <mark class="search-hit">, scrolls to the first match, and
  // exposes Prev/Next navigation through the resulting hits.
  const searchInput   = document.getElementById('search');
  const prevBtn       = document.getElementById('search-prev');
  const nextBtn       = document.getElementById('search-next');
  const counterEl     = document.getElementById('search-counter');
  const mainContent   = document.getElementById('main-content');

  let allHits = [];      // ordered array of <mark.search-hit> elements
  let currentHit = -1;   // index of the .current hit, or -1
  let lastQuery = '';

  // Tags whose contents must never be touched by the highlighter:
  //  - SCRIPT/STYLE: not displayed text
  //  - existing MARK: avoid recursion on re-search
  //  - A: leave anchor TEXT highlightable but skip the href attribute
  //    (we use TreeWalker over text nodes, attributes already excluded)
  const SKIP_TAGS = new Set(['SCRIPT', 'STYLE', 'MARK']);

  function clearHits() {
    if (allHits.length === 0) return;
    // Replace each <mark.search-hit> with its text content, then normalize
    // adjacent text nodes so the next search sees a clean tree.
    allHits.forEach(m => {
      const text = document.createTextNode(m.textContent);
      m.parentNode.replaceChild(text, m);
    });
    mainContent.normalize();
    allHits = [];
    currentHit = -1;
  }

  function collectTextNodes(query) {
    const out = [];
    const walker = document.createTreeWalker(mainContent, NodeFilter.SHOW_TEXT, {
      acceptNode: (node) => {
        // Skip nodes inside excluded ancestors
        let p = node.parentElement;
        while (p && p !== mainContent) {
          if (SKIP_TAGS.has(p.tagName)) return NodeFilter.FILTER_REJECT;
          p = p.parentElement;
        }
        return node.nodeValue.toLowerCase().includes(query)
          ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      }
    });
    let n;
    while ((n = walker.nextNode())) out.push(n);
    return out;
  }

  function highlightAll(query) {
    clearHits();
    if (!query) return;
    const q = query.toLowerCase();
    const textNodes = collectTextNodes(q);
    for (const node of textNodes) {
      const text = node.nodeValue;
      const lc = text.toLowerCase();
      const frag = document.createDocumentFragment();
      let last = 0, idx = lc.indexOf(q);
      while (idx !== -1) {
        if (idx > last) frag.appendChild(document.createTextNode(text.slice(last, idx)));
        const m = document.createElement('mark');
        m.className = 'search-hit';
        m.textContent = text.slice(idx, idx + q.length);
        frag.appendChild(m);
        allHits.push(m);
        last = idx + q.length;
        idx = lc.indexOf(q, last);
      }
      if (last < text.length) frag.appendChild(document.createTextNode(text.slice(last)));
      node.parentNode.replaceChild(frag, node);
    }
  }

  function jumpTo(idx) {
    if (allHits.length === 0) return;
    // Wrap-around
    if (idx < 0) idx = allHits.length - 1;
    if (idx >= allHits.length) idx = 0;
    if (currentHit >= 0 && allHits[currentHit]) {
      allHits[currentHit].classList.remove('current');
    }
    currentHit = idx;
    const hit = allHits[idx];
    hit.classList.add('current');
    hit.scrollIntoView({behavior: 'smooth', block: 'center'});
    updateCounter();
  }

  function updateCounter() {
    if (!lastQuery) {
      counterEl.textContent = '';
      prevBtn.disabled = true;
      nextBtn.disabled = true;
    } else if (allHits.length === 0) {
      counterEl.textContent = '0 matches';
      prevBtn.disabled = true;
      nextBtn.disabled = true;
    } else {
      counterEl.textContent = (currentHit + 1) + ' / ' + allHits.length;
      prevBtn.disabled = false;
      nextBtn.disabled = false;
    }
  }

  function runSearch(query) {
    lastQuery = (query || '').trim();
    if (lastQuery.length < 2) {
      clearHits();
      updateCounter();
      if (lastQuery.length === 1) counterEl.textContent = 'type 2+ chars';
      return;
    }
    highlightAll(lastQuery);
    if (allHits.length > 0) {
      jumpTo(0);
    } else {
      updateCounter();
    }
  }

  // Debounced input handler
  let timer = null;
  searchInput.addEventListener('input', e => {
    clearTimeout(timer);
    timer = setTimeout(() => runSearch(e.target.value), 150);
  });
  // Enter = next, Shift+Enter = prev, Esc = clear
  searchInput.addEventListener('keydown', e => {
    if (e.key === 'Enter') {
      e.preventDefault();
      if (e.shiftKey) jumpTo(currentHit - 1);
      else            jumpTo(currentHit + 1);
    } else if (e.key === 'Escape') {
      searchInput.value = '';
      runSearch('');
    }
  });
  prevBtn.addEventListener('click', () => jumpTo(currentHit - 1));
  nextBtn.addEventListener('click', () => jumpTo(currentHit + 1));
  // Global "/" focuses search
  document.addEventListener('keydown', e => {
    if (e.key === '/' && document.activeElement !== searchInput) {
      e.preventDefault();
      searchInput.focus();
      searchInput.select();
    }
  });

  // --- Lightbox (click any figure image to enlarge to viewport) ---
  // Built lazily on first click — no DOM overhead until the user actually
  // wants it. Reused thereafter.
  let lightbox = null;
  function ensureLightbox() {
    if (lightbox) return lightbox;
    lightbox = document.createElement('div');
    lightbox.className = 'lightbox-overlay';
    lightbox.setAttribute('role', 'dialog');
    lightbox.setAttribute('aria-modal', 'true');
    lightbox.innerHTML =
      '<button class="lightbox-close" type="button" aria-label="Close (Esc)">&times;</button>' +
      '<img class="lightbox-image" alt="">' +
      '<div class="lightbox-caption"></div>' +
      '<div class="lightbox-hint">click anywhere or press Esc to close</div>';
    document.body.appendChild(lightbox);
    // Close on ANY click inside the overlay — including on the image itself,
    // since the cursor over the image is `zoom-out` (a magnifying glass with
    // a minus) which signals exactly that affordance to the user.
    lightbox.addEventListener('click', closeLightbox);
    return lightbox;
  }
  function openLightbox(img) {
    const lb = ensureLightbox();
    const lbImg = lb.querySelector('.lightbox-image');
    const lbCap = lb.querySelector('.lightbox-caption');
    lbImg.src = img.src;
    lbImg.alt = img.alt || '';
    // Pull the caption text from the surrounding <figcaption>, if any
    const fig = img.closest('figure');
    const cap = fig ? fig.querySelector('figcaption') : null;
    lbCap.innerHTML = cap ? cap.innerHTML : '';
    lb.classList.add('visible');
    // Lock body scroll while the lightbox is open
    document.documentElement.style.overflow = 'hidden';
  }
  function closeLightbox() {
    if (!lightbox) return;
    lightbox.classList.remove('visible');
    document.documentElement.style.overflow = '';
  }
  // Delegate clicks: any <figure> img in main content opens the lightbox
  document.getElementById('main-content').addEventListener('click', e => {
    const img = e.target.closest('figure img');
    if (img) {
      e.preventDefault();
      openLightbox(img);
    }
  });
  // Esc closes
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && lightbox && lightbox.classList.contains('visible')) {
      closeLightbox();
    }
  });
})();
</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# TOC rendering
# ---------------------------------------------------------------------------


def render_toc(toc: list[TocEntry], frontmatter_links: list[tuple[str, str]] | None = None) -> str:
    """
    Render the sidebar TOC as collapsible per-volume sections.

    Each h1 entry starts a new <li class="toc-vol"> whose nested <ul> contains all
    subsequent entries (h2/h3/h4) until the next h1. A toggle button (CSS-styled
    disclosure triangle) collapses/expands the nested list.

    If `frontmatter_links` is provided, a non-collapsible "Front Matter" section
    is rendered at the top with those (anchor, label) pairs.
    """
    items: list[str] = []

    # Front matter section (always visible at top, not collapsible, no heading)
    if frontmatter_links:
        items.append('<li class="toc-frontmatter">')
        items.append('<ul class="toc-list" style="margin-bottom:.4rem">')
        for anchor, label in frontmatter_links:
            items.append(
                f'<li class="toc-h2">'
                f'<a href="#{html_mod.escape(anchor)}">{html_mod.escape(label)}</a>'
                f'</li>'
            )
        items.append('</ul></li>')
        items.append('<li class="toc-vol-sep" aria-hidden="true"></li>')

    # Volume groups
    current_vol_open = False
    for entry in toc:
        lvl = entry.level
        if lvl == 1:
            # Close previous volume if any
            if current_vol_open:
                items.append('</ul></li>')
            anchor_esc = html_mod.escape(entry.anchor)
            text_esc = html_mod.escape(entry.text)
            items.append(
                f'<li class="toc-vol" data-vol-id="{anchor_esc}" data-expanded="false">'
                f'<div class="toc-vol-head">'
                f'<button class="toc-toggle" type="button" aria-expanded="false" '
                f'aria-label="Toggle volume" tabindex="0"></button>'
                f'<a href="#{anchor_esc}">{text_esc}</a>'
                f'</div>'
                f'<ul class="toc-vol-children">'
            )
            current_vol_open = True
        else:
            css = f"toc-h{lvl}"
            items.append(
                f'<li class="{css}">'
                f'<a href="#{html_mod.escape(entry.anchor)}">'
                f'{html_mod.escape(entry.text)}'
                f'</a></li>'
            )

    if current_vol_open:
        items.append('</ul></li>')
    return "\n".join(items)


# ---------------------------------------------------------------------------
# Title page + formal Table of Contents (main column)
# ---------------------------------------------------------------------------


def link_vol_refs(html_text: str,
                  vol_anchors: dict[int, str],
                  section_anchors: dict[tuple[int, str], str]) -> str:
    """Wrap "Vol N" and "Vol N §X.Y" prose references in rendered HTML with
    anchor links pointing at the corresponding in-page section.

    Conservatively avoids inserting links inside <a>, <code>, <pre>,
    <h1>..<h6>, and <figcaption> tags (where they would either duplicate an
    existing link or pollute structural content).
    """
    sentinels: dict[str, str] = {}

    def stash(m: re.Match) -> str:
        token = f"\x00MASK{len(sentinels)}\x00"
        sentinels[token] = m.group(0)
        return token

    def mask_structural(text: str) -> str:
        """Mask existing anchors, code spans, pre blocks, headings, figcaptions."""
        text = re.sub(r'<a [^>]*>.*?</a>', stash, text, flags=re.DOTALL)
        text = re.sub(r'<code[^>]*>.*?</code>', stash, text, flags=re.DOTALL)
        text = re.sub(r'<pre[^>]*>.*?</pre>', stash, text, flags=re.DOTALL)
        text = re.sub(r'<h[1-6][^>]*>.*?</h[1-6]>', stash, text, flags=re.DOTALL)
        text = re.sub(r'<figcaption[^>]*>.*?</figcaption>', stash, text, flags=re.DOTALL)
        return text

    masked = mask_structural(html_text)

    def repl_sec(m: re.Match) -> str:
        v = int(m.group(1))
        sec = m.group(2)
        anchor = section_anchors.get((v, sec))
        if anchor:
            return f'<a href="#{anchor}">{m.group(0)}</a>'
        # Fall back to the volume anchor if the section anchor is unknown
        vol_anchor = vol_anchors.get(v)
        if vol_anchor:
            return f'<a href="#{vol_anchor}">{m.group(0)}</a>'
        return m.group(0)

    def repl_bare_sec(m: re.Match) -> str:
        """Bare `§X.Y` reference — derive vol from first numeric component."""
        sec = m.group(1)
        v = int(sec.split(".", 1)[0])
        anchor = section_anchors.get((v, sec))
        if anchor:
            return f'<a href="#{anchor}">{m.group(0)}</a>'
        # Fall back to the volume anchor if section unknown but volume exists
        vol_anchor = vol_anchors.get(v)
        if vol_anchor:
            return f'<a href="#{vol_anchor}">{m.group(0)}</a>'
        return m.group(0)

    def repl_vol(m: re.Match) -> str:
        v = int(m.group(1))
        anchor = vol_anchors.get(v)
        if anchor:
            return f'<a href="#{anchor}">{m.group(0)}</a>'
        return m.group(0)

    # Three-pass linking (in specificity order). After each pass we re-mask
    # the newly-created <a> tags so a subsequent pass can't re-match text
    # that's already inside a link.
    #
    # Pass 1: "Vol N §X.Y[.Z]" — most specific; "Vol 1 §1.13.6"
    masked = re.sub(r'\bVol\s+(\d+)\s*§\s*(\d+(?:\.\d+)+)', repl_sec, masked)
    masked = mask_structural(masked)
    # Pass 2: bare "§X.Y[.Z]" — vol inferred from first component; "§1.13.6"
    masked = re.sub(r'§\s*(\d+(?:\.\d+)+)', repl_bare_sec, masked)
    masked = mask_structural(masked)
    # Pass 3: bare "Vol N" with no §; "Vol 4"
    masked = re.sub(r'\bVol\s+(\d+)\b(?!\s*§)', repl_vol, masked)

    # Restore in reverse order (sentinels CAN nest — e.g. <a href> containing <code>)
    for token, original in reversed(sentinels.items()):
        masked = masked.replace(token, original)
    return masked


def render_title_page(title: str, n_vols: int, gen_date: str) -> str:
    """
    Render the book title page. The `title` may contain an em-dash or colon
    separating main title from subtitle; we split on the first such separator.
    """
    main_title = title
    subtitle = ""
    for sep in [" — ", ": ", " - "]:
        if sep in title:
            main_title, subtitle = title.split(sep, 1)
            break
    main_esc = html_mod.escape(main_title.strip())
    sub_esc = html_mod.escape(subtitle.strip())

    subtitle_html = ""
    if sub_esc:
        subtitle_html = f'<div class="tp-subtitle">{sub_esc}</div>'

    return (
        '<section class="title-page" id="title-page">'
        '<div class="tp-eyebrow">Deep Dive Reference</div>'
        f'<h1 class="tp-title">{main_esc}</h1>'
        f'{subtitle_html}'
        '<div class="tp-rule" aria-hidden="true"></div>'
        '<div class="tp-author">By <strong>tjscientist</strong></div>'
        '<div class="tp-meta">'
        f'<div>{n_vols} volumes</div>'
        f'<div>Generated {html_mod.escape(gen_date)}</div>'
        '</div>'
        '</section>'
    )


def render_table_of_contents(toc: list[TocEntry], has_lof: bool, has_lot: bool) -> str:
    """
    Render the formal in-page Table of Contents.

    Lists Front Matter (TOC self-link, LoF, LoT), then each volume with its
    h2-level subsections. h3/h4 entries are omitted to keep the page scannable.
    """
    parts: list[str] = []
    parts.append('<section class="formal-toc" id="table-of-contents">')
    parts.append('<h2 class="ft-heading">Table of Contents</h2>')

    # Front matter links
    fm_items: list[str] = []
    fm_items.append(
        '<li><a href="#table-of-contents">Table of Contents</a>'
        '<span class="ft-leader"></span></li>'
    )
    if has_lof:
        fm_items.append(
            '<li><a href="#list-of-figures">List of Figures</a>'
            '<span class="ft-leader"></span></li>'
        )
    if has_lot:
        fm_items.append(
            '<li><a href="#list-of-tables">List of Tables</a>'
            '<span class="ft-leader"></span></li>'
        )
    parts.append('<div class="ft-frontmatter">')
    parts.append('<ul>')
    parts.extend(fm_items)
    parts.append('</ul>')
    parts.append('</div>')

    # Volumes
    current_vol_open = False
    for entry in toc:
        if entry.level == 1:
            if current_vol_open:
                parts.append('</ul></div>')
            parts.append('<div class="ft-section">')
            parts.append(
                f'<div class="ft-vol-link">'
                f'<a href="#{html_mod.escape(entry.anchor)}">{html_mod.escape(entry.text)}</a>'
                f'<span class="ft-leader"></span>'
                f'</div>'
            )
            parts.append('<ul class="ft-children">')
            current_vol_open = True
        elif entry.level == 2 and current_vol_open:
            parts.append(
                f'<li><a href="#{html_mod.escape(entry.anchor)}">'
                f'{html_mod.escape(entry.text)}</a>'
                f'<span class="ft-leader"></span></li>'
            )
        # Skip h3/h4 in the formal TOC (sidebar still has them)

    if current_vol_open:
        parts.append('</ul></div>')
    parts.append('</section>')
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# List of Figures / Tables
# ---------------------------------------------------------------------------


def render_lof(figures: list[FigureEntry]) -> str:
    if not figures:
        return ""
    items = "\n".join(
        f'<li>'
        f'<span class="ml-num"><a href="#fig-{f.number}">Fig. {f.number}</a></span>'
        f'<span class="ml-desc">{html_mod.escape(f.description)}</span>'
        f'<span class="ml-vol">{html_mod.escape(f.vol_title)}</span>'
        f'</li>'
        for f in figures
    )
    return (
        '<section id="list-of-figures">'
        '<h2>List of Figures</h2>'
        f'<ul class="meta-list">{items}</ul>'
        '</section>'
    )


def render_lot(tables: list[TableEntry]) -> str:
    if not tables:
        return ""
    items = "\n".join(
        f'<li>'
        f'<span class="ml-num"><a href="#tbl-{t.number}">Table {t.number}</a></span>'
        f'<span class="ml-desc">{html_mod.escape(t.caption)}</span>'
        f'<span class="ml-vol">{html_mod.escape(t.vol_title)}</span>'
        f'</li>'
        for t in tables
    )
    return (
        '<section id="list-of-tables">'
        '<h2>List of Tables</h2>'
        f'<ul class="meta-list">{items}</ul>'
        '</section>'
    )


# ---------------------------------------------------------------------------
# Search-index builder
# ---------------------------------------------------------------------------


def build_search_index(toc: list[TocEntry], vol_body_map: dict[str, str]) -> list[dict]:
    """
    Build a per-heading search index. Each entry has anchor, title, vol, and
    the text content of that section up to the next same-or-higher-level heading.
    """
    # Flatten body text by extracting plain text between heading anchors.
    # Simple approach: strip all tags from the body HTML.
    def strip_tags(s: str) -> str:
        return re.sub(r"<[^>]+>", " ", s)

    # Combine all body html
    combined_html = "\n".join(vol_body_map.values())
    plain = strip_tags(combined_html)
    plain = re.sub(r"\s+", " ", plain).strip()

    # For each TOC entry, produce a search doc using the heading text + nearby context
    # (simplified: just use heading text; more accurate would parse the HTML)
    docs = []
    for entry in toc:
        docs.append({
            "anchor": entry.anchor,
            "title": entry.text,
            "vol": f"Level {entry.level} heading",
            "body": entry.text,
        })

    # Also add a single full-text doc for bulk searching
    docs.append({
        "anchor": "volumes",
        "title": "Full text",
        "vol": "All volumes",
        "body": plain[:200000],  # cap at ~200k chars
    })
    return docs


# ---------------------------------------------------------------------------
# Main build function
# ---------------------------------------------------------------------------


def build(volume_dir: Path, output: Path, title: str, photos_dir: Path | None = None,
          storage_key: str = "demon-core-deepdive-toc-expanded") -> tuple[int, int]:
    global _PHOTOS_DIR
    _PHOTOS_DIR = photos_dir

    vol_files = sorted(
        [p for p in volume_dir.glob("vol*.md") if re.match(r"vol\d+\.md$", p.name)],
        key=lambda p: int(re.match(r"vol(\d+)\.md$", p.name).group(1)),
    )
    if not vol_files:
        raise SystemExit(f"No vol*.md files found in {volume_dir}")

    all_toc: list[TocEntry] = []
    all_figures: list[FigureEntry] = []
    all_tables: list[TableEntry] = []
    vol_htmls: list[str] = []

    fig_counter = 0
    tbl_counter = 0

    for vol_path in vol_files:
        source = vol_path.read_text(encoding="utf-8")
        state = _MDState(
            vol_title=vol_path.stem,
            fig_start=fig_counter,
            tbl_start=tbl_counter,
        )
        body_html = md_to_html(source, state)
        fig_counter = state.fig_counter
        tbl_counter = state.tbl_counter
        all_toc.extend(state.toc)
        all_figures.extend(state.figures)
        all_tables.extend(state.tables)
        css_class = "vol-break" if vol_htmls else ""
        vol_htmls.append(f'<div class="volume {css_class}" id="{state.toc[0].anchor if state.toc else vol_path.stem}">\n{body_html}\n</div>')

    # Build anchor lookups for intra-doc volume cross-references.
    # vol_anchors    : {volnum: h1_anchor}    e.g. {1: "vol-1-history-..."}
    # section_anchors: {(volnum, secnum): heading_anchor}
    #   h2 entries like "2.4 Yeast Selection"             -> (2, "2.4")  -> "2-4-yeast-selection"
    #   h3 entries like "1.13.6 Cleaning..."              -> (1, "1.13.6") -> "1-13-6-cleaning..."
    #   h4 entries like "2.3.1.2 Sugar Wash..."           -> (2, "2.3.1.2") -> ...
    # We accept h2/h3/h4 so any "§X.Y[.Z[.W]]" reference can be linked.
    vol_anchors: dict[int, str] = {}
    section_anchors: dict[tuple[int, str], str] = {}
    current_vol: int | None = None
    for entry in all_toc:
        if entry.level == 1:
            m = re.match(r"Vol\s+(\d+)", entry.text)
            if m:
                current_vol = int(m.group(1))
                vol_anchors[current_vol] = entry.anchor
        elif entry.level in (2, 3, 4) and current_vol is not None:
            m = re.match(r"(\d+(?:\.\d+)+)", entry.text)
            if m:
                section_anchors[(current_vol, m.group(1))] = entry.anchor

    # Post-process every volume's HTML, wrapping prose "Vol N" / "Vol N §X.Y"
    # cross-references with anchor links to the right in-page section.
    vol_htmls = [link_vol_refs(h, vol_anchors, section_anchors) for h in vol_htmls]

    lof_html = render_lof(all_figures)
    lot_html = render_lot(all_tables)
    volumes_html = "\n".join(vol_htmls)

    # Sidebar front-matter links — all rendered as regular toc entries,
    # in document reading order: Title Page → Contents → LoF → LoT.
    sidebar_fm_links: list[tuple[str, str]] = [
        ("title-page", "Title Page"),
        ("table-of-contents", "Contents"),
    ]
    if all_figures:
        sidebar_fm_links.append(("list-of-figures", "List of Figures"))
    if all_tables:
        sidebar_fm_links.append(("list-of-tables", "List of Tables"))

    toc_html = render_toc(all_toc, frontmatter_links=sidebar_fm_links)

    from datetime import datetime, timezone
    gen_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    title_page_html = render_title_page(title, len(vol_files), gen_date)
    formal_toc_html = render_table_of_contents(
        all_toc, has_lof=bool(all_figures), has_lot=bool(all_tables)
    )

    # (The old JSON search-index has been retired — the new find-in-page
    # search walks the rendered DOM directly, so no precomputed index is
    # needed. `build_search_index()` is kept in this module as a no-cost
    # vestigial helper in case a future build wants per-heading scoring.)

    title_esc = html_mod.escape(title)

    page = (
        PAGE_TEMPLATE
        .replace("__TITLE__", title_esc)
        .replace("__TOC_ITEMS__", toc_html)
        .replace("__TITLE_PAGE__", title_page_html)
        .replace("__TABLE_OF_CONTENTS__", formal_toc_html)
        .replace("__LIST_OF_FIGURES__", lof_html)
        .replace("__VOLUMES_HTML__", volumes_html)
        .replace("__LIST_OF_TABLES__", lot_html)
        .replace("__STORAGE_KEY__", storage_key)
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8")
    return len(vol_files), len(all_toc)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT,
                    help="Project root (default: 2 levels above this script)")
    ap.add_argument("--volume-dir", type=Path, default=None,
                    help="Directory containing vol_*.md files")
    ap.add_argument("--output", type=Path, default=None,
                    help="Output HTML path")
    ap.add_argument("--photos-dir", type=Path, default=None,
                    help="Directory containing figure images for FIGURE: directives")
    ap.add_argument("--title", default=DEFAULT_TITLE,
                    help="Document title")
    ap.add_argument("--storage-key", default="demon-core-deepdive-toc-expanded",
                    help="localStorage key for sidebar TOC expand/collapse state. "
                         "Must be unique per book so multiple deep dives don't "
                         "collide in a browser (e.g. brewing-deepdive-toc-expanded).")
    args = ap.parse_args()

    root = args.root.resolve()
    vol_dir = (args.volume_dir or (root / DEFAULT_VOL_DIR_REL)).resolve()
    out = (args.output or (root / DEFAULT_OUTPUT_REL)).resolve()
    photos = (args.photos_dir or (root / DEFAULT_PHOTOS_DIR_REL)).resolve()

    print(f"root:       {root}")
    print(f"volume-dir: {vol_dir}")
    print(f"photos-dir: {photos}")
    print(f"output:     {out}")

    n_vols, n_headings = build(vol_dir, out, args.title, photos_dir=photos,
                               storage_key=args.storage_key)
    size_kb = out.stat().st_size / 1024
    print(f"built {n_vols} volumes, {n_headings} TOC entries -> {out.name}  ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
