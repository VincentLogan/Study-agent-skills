---
name: courseware-study-notes
description: Read PPTX or PDF courseware and write source-ordered Markdown study notes with proof explanations, examples, and revision aids. Use for lecture slides, scanned lecture PDFs, and technical course handouts.
metadata:
  short-description: Create study notes from PPTX or PDF courseware
---

# Courseware Study Notes

Create a complete, accurate study note from a PPTX or PDF. Use this skill when the requested outcome is a local Markdown lecture note, not a slide conversion or a short chat summary.

## Outcome and boundaries

- Write the complete note to a Markdown file; do not paste the note body into chat. After verification, report the saved path and a short status only.
- Preserve the source's page/slide sequence in the note's main body. Adjacent pages on one idea may be combined, but do not move a later idea earlier merely to make topics look tidier.
- Explain the material instead of mechanically transcribing it. Do not invent unreadable formulas, labels, or claims.
- Use standard Markdown and LaTeX. `assets/courseware-note.css` is optional visual enhancement: the note must be complete in an ordinary Markdown renderer without it.

## Select the extraction route

### PPTX

Run `scripts/extract_pptx.py` to extract titles, text blocks, tables, speaker notes, positions, font sizes, and paragraph levels into JSON. Treat slide order as canonical; use coordinates and title hierarchy to repair text-box ordering when needed.

- Retain titles, definitions, formulas, proof text, pseudocode, warnings, captions, and explanatory sentences.
- Ignore animation frames, decorative labels, isolated tree-node values, and diagram-only symbols unless they express a rule or conclusion essential to the prose.
- If native extraction omits material needed for a conclusion, add `[待核对 S<n>]` rather than guessing.

### Legacy PPT

`python-pptx` cannot read binary `.ppt` files. For an old PowerPoint file, first use `scripts/convert_legacy_ppt.py` to make a local `.pptx` copy through LibreOffice, then follow the PPTX route. Preserve the original file and record the converted copy as a processing artifact; do not overwrite the source. If LibreOffice is unavailable or conversion fails, explain the blocker instead of treating the `.ppt` as a PPTX.

### PDF

Run `scripts/extract_pdf.py` first. It classifies pages as `text-led`, `mixed`, or `image-led` from native text and page content.

- For `text-led` pages, use extracted text and layout directly.
- For `mixed` pages, use text first; inspect a figure only when it carries a key claim.
- For `image-led` pages, render only that page with `scripts/render_pdf_pages.py`, then visually recover the concept, formula, component relationship, or conclusion required for the note. Do not transcribe every label or decorative detail.
- For computer-systems diagrams, explain components plus the relevant data/control flow, timing relation, bottleneck, invariant, or trade-off—not a literal inventory of every wire or register.
- Mark unreadable image text as `[待核对 P<n>]`.

## Handle long courseware without omissions

Never silently stop at a context limit or discard later pages.

1. Extract lightweight metadata for every page: page number, title candidates, available text, and page classification.
2. Build a course map and split it into **continuous** ranges, preferring chapter boundaries. Keep each range small enough for reliable analysis.
3. Analyze ranges in page order. For each range, retain a compact working outline containing only its definitions, notation, conclusions, and source references.
4. Carry forward only the preceding material necessary to understand the next range.
5. Merge the range outlines into one final note in original order. Its `课件范围` section must list every processed range.
6. If a range cannot be processed, record it in `待核对` with its page range and the reason; never imply that it was covered.

## Decide importance from the source

Use learning-priority labels; do not label content as an exam focus unless the source says so.

- **A · 必须掌握**: definitions, core algorithms, primary theorems, proof ideas, complexity results, repeatedly emphasized rules.
- **B · 重点理解**: examples, derived properties, implementation details, and comparisons that make A-level ideas understandable.
- **C · 了解即可**: content explicitly marked optional, appendix, extension, further reading, or genuinely peripheral to the main lecture.

## Explain proofs and complex examples

Before any long proof, multi-step derivation, algorithm analysis, or example whose bare steps would be hard to remember, include `### 核心原理解析`.

It must state, in plain language:

1. the question or conclusion at stake;
2. the condition, invariant, mechanism, or key observation that makes it work;
3. the route the proof or solution will take; and
4. the short memory hook the learner should retain.

Then provide the detailed argument: prerequisites and notation, objective, each step, why that step is valid, the conclusion, and how the source example illustrates it. For explicit extension material, state its relation and takeaway but omit the full proof unless requested.

## Output location and naming

1. Obey an explicitly supplied output folder or file name.
2. Otherwise inspect folders adjacent to the source for an existing notes directory and infer its naming pattern from existing notes.
3. If no notes directory exists, create `notes/` next to the source.
4. Never overwrite an existing note. Add a meaningful suffix only when a name collision occurs.
5. Write to a temporary sibling file and rename it after all content is complete and validated, so an error never leaves a partial final note.

Read `references/note-schema.md` before drafting the final note. Use the supplied CSS only when the user's Markdown environment supports it.

## Final checks

Before reporting completion, verify that the final file exists and includes:

- source file and complete coverage ranges;
- a source-ordered main body with `[S<n>]` or `[P<n>]` references;
- learning-priority labels;
- `核心原理解析` for each substantial proof/derivation/complex example;
- detailed but source-faithful proof or example explanations;
- summaries, pitfalls, and revision aids after the main body; and
- an honest `待核对` section when extraction was incomplete.
