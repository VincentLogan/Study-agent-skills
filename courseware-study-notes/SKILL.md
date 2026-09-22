---
name: courseware-study-notes
description: Read PPT, PPTX, or PDF courseware and write source-ordered Markdown study notes with proof explanations, examples, and revision aids. Use for lecture slides, scanned lecture PDFs, and technical course handouts.
metadata:
short-description: Create study notes from PPT, PPTX, or PDF courseware
---

# Courseware Study Notes

Create a complete, accurate study note from a PPT, PPTX, or PDF. Use this skill when the requested outcome is a local Markdown lecture note, not a slide conversion or a short chat summary.

## Outcome and boundaries

- Write the complete note to a Markdown file; do not paste the note body into chat. After verification, report the saved path and a short status only.
- Preserve the source's page/slide sequence in the note's main body. Adjacent pages on one idea may be combined, but do not move a later idea earlier merely to make topics look tidier.
- Explain the material instead of mechanically transcribing it. Do not invent unreadable formulas, labels, or claims.
- State knowledge directly. Do not use report-like wording such as “the courseware says,” “this slide mentions,” or “the lecturer explains”; use the source references to show provenance instead.
- Use standard Markdown and LaTeX. `assets/courseware-note.css` is optional visual enhancement: the note must be complete in an ordinary Markdown renderer without it.

## Select the extraction route

### Default: text coverage before visual evidence

The goal is a complete source-ordered **knowledge outline**, not a visual transcription of every slide. Use native text as the primary evidence and complete coverage mechanism. Do not visually inspect a page or slide during the first pass.

1. Run the relevant extractor with `--mode index` for the entire source. Its output is a compact course map: page/slide number, title candidate, native text, notes, and visual-risk indicators.
2. Build the course map and draft the knowledge outline from that text in continuous source order. A `mixed`, `image-led`, or high `non_text_shape_count` classification is only a risk indicator; it is **not** permission to perform visual analysis.
3. Treat missing minor labels, decorative diagrams, animation states, layout polish, and an occasionally unclear sentence as non-blocking. Summarize the readable rule or conclusion; otherwise add `[待核对 S<n>/P<n>]`. Do not use visual analysis to make the note more exhaustive.
4. A visual check is allowed only when the text record has a **serious, material gap**: (a) a substantive page/slide has no usable native text or notes; (b) a key definition, formula, table, algorithm step, or conclusion is explicitly referenced by surrounding text but is absent from the extraction; or (c) a continuous run of content pages is effectively textless and cannot honestly be represented in the note. Record the specific gap and the intended knowledge point before reading the visual.
5. Read only the smallest affected page/slide set. Never re-read a whole deck/PDF, a chapter, or every `mixed`/`image-led` item merely to improve completeness. If the source is predominantly scanned or visual-only, state that full text-faithful coverage requires a separate visual pass and ask before starting one; otherwise leave scoped `待核对` items.

### PPTX

Run `scripts/extract_pptx.py --mode index` to obtain titles, ordered native text, and speaker notes. Treat slide order as canonical. The index intentionally omits coordinates, font runs, and paragraph metadata to keep context small.

- Retain titles, definitions, formulas, proof text, pseudocode, warnings, captions, and explanatory sentences.
- Ignore animation frames, decorative labels, isolated tree-node values, and diagram-only symbols unless they express a rule or conclusion essential to the prose.
- Do not use a slide's non-text shape count as a visual-reading trigger. If native extraction omits material needed for a conclusion, add `[待核对 S<n>]` unless it meets the serious-gap gate above.
- Request the full extractor output only when reading order or heading hierarchy cannot be resolved from the index. Do not use full metadata as a substitute for a visual audit.

### Legacy PPT

Binary `.ppt` is not a ZIP/XML `.pptx` file and must never be sent to `python-pptx`. Use the bundled single-command wrapper instead of manually converting and then extracting:

```bash
python3 scripts/extract_legacy_ppt.py \
  --input <source.ppt> \
  --output <course-map.json> \
  --cache-dir <source-folder>/.courseware-cache \
  --mode index
```

The wrapper is the default and only normal `.ppt` route. It uses bundled `convert_legacy_ppt.py` to locate LibreOffice/`soffice`, creates an isolated temporary LibreOffice profile, converts into a hash-keyed cached `.pptx`, then calls the bundled PPTX extractor. This is the most efficient robust path: LibreOffice preserves far more slide text, tables, order, and notes than ad-hoc OLE text readers, while the content-hash cache avoids repeat conversions for an unchanged source. The original `.ppt` is never modified; the JSON records the converted artifact and whether the cache was used.

Do not call LibreOffice directly, use an external web converter, or install a separate `.ppt` parser. LibreOffice is the only system dependency; all orchestration and extraction tools are contained in this skill. If it is unavailable or conversion fails, report the blocker instead of treating the source as `.pptx`. Use `--force` only to redo a known-bad cached conversion.

Use a conservative, text-first workflow for converted legacy decks:

- Do not render or page-by-page compare the converted deck by default. The compact extracted text, titles, and notes are the primary evidence.
- Render/inspect a page only after it passes the serious-gap gate above. Do not inspect a slide because it looks sparse, contains a diagram, or would benefit from a more detailed explanation.
- Never use image inspection to audit diagrams, animation frames, decorative labels, or content that is already readable in the text extraction.
- If a visual-only item remains unclear, do not reconstruct it. Record the slide number, what is missing, and a practical manual check in the final `待核对` section.

### PDF

Run `scripts/extract_pdf.py --mode index` first. It classifies pages as `text-led`, `mixed`, or `image-led` from native text and page content, but classification is for triage only.

- For `text-led` pages, use extracted text and layout directly.
- For `mixed` and `image-led` pages, use extracted text first and do not render by default. A figure is inspected only after the serious-gap gate is met.
- When a visual check is justified, render only that page with `scripts/render_pdf_pages.py`, then recover just the blocked concept, formula, component relationship, or conclusion. Do not transcribe labels or decorative detail.
- For computer-systems diagrams, explain components plus the relevant data/control flow, timing relation, bottleneck, invariant, or trade-off—not a literal inventory of every wire or register.
- Mark unreadable image text as `[待核对 P<n>]`.

## Handle long courseware without omissions

Never silently stop at a context limit or discard later pages.

1. Extract a compact index for every page: page number, title candidates, available text/notes, and page classification. This establishes coverage; do not load full layout JSON for all pages.
2. Build a course map and split it into **continuous** ranges, preferring chapter boundaries. Keep each range small enough for reliable analysis.
3. Analyze ranges in page order. For each range, retain a compact working outline containing only its definitions, notation, conclusions, and source references.
4. Carry forward only the preceding material necessary to understand the next range.
5. Merge the range outlines into one final note in original order. Its `课件范围` section must list every processed range.
6. If a range has a serious text gap that is not visually checked, record it in `待核对` with its page range, missing knowledge point, and reason; never imply that it was covered.

## Build a source-faithful hierarchy

Infer the note's heading hierarchy from the course map, chapter/section pages, title numbering, overview slides, and adjacent-topic continuity. Keep each parent section's source range continuous and retain the source order within it.

- Use a parent section for a shared concept that introduces several consecutive methods, variants, or cases, then make those methods child sections. For example, introduce “摊还分析方法（Amortized Analysis Methods）” before its consecutive sub-sections “聚合分析（Aggregate Analysis）”, “记账法（Accounting Method）”, and “势能分析法（Potential Method）”.
- Do not promote every slide topic to a top-level heading or impose a fixed number of heading levels. Use only the levels that make the source's actual conceptual structure clear.
- Start a parent chapter with a concise declarative sentence that states what it introduces, establishes, or enables. Do not introduce it with a question heading. For example: “引入平衡因子（Balance Factor, BF），以确保二叉搜索树（Binary Search Tree, BST）的树结构保持平衡。”

## Use bilingual terminology precisely

At the first meaningful occurrence of an important technical term, write `中文（English, Abbreviation）` when there is a standard English original, for example `平衡因子（Balance Factor, BF）`. Later occurrences may use Chinese or the abbreviation as readability requires.

- Do not force an English gloss for ordinary prose or terms without a reliable conventional translation.
- If the English original or translation is uncertain, write `[待核对]` rather than inventing it.
- In `术语速查`, use the same Chinese-English correspondence for important terms.

## Decide importance from the source

Use learning-priority labels; do not label content as an exam focus unless the source says so.

- **A · 必须掌握**: definitions, core algorithms, primary theorems, proof ideas, complexity results, repeatedly emphasized rules.
- **B · 重点理解**: examples, derived properties, implementation details, and comparisons that make A-level ideas understandable.
- **C · 了解即可**: content explicitly marked optional, appendix, extension, further reading, or genuinely peripheral to the main lecture.

## Explain proofs and complex examples

Before any long proof, multi-step derivation, algorithm analysis, or example whose bare steps would be hard to remember, include `### 核心原理`.

Begin that section with one short, untitled Markdown blockquote that directly frames the reasoning, such as `> 从……出发，利用……说明/证明……。` Do not add a `问题` heading.

Then state, in plain language:

1. the conclusion being established;
2. the condition, invariant, mechanism, or key observation that makes it work; and
3. the route the proof or solution will take.

Then provide the detailed argument: prerequisites and notation, each step, why that step is valid, the conclusion, and how the source example illustrates it. For explicit extension material, state its relation and takeaway but omit the full proof unless requested.

When the source skips an algebraic transformation, lemma, boundary case, or transition needed to make a proof or derivation understandable and logically complete, add the minimum necessary material. Mark it explicitly as `> **补充推导：** ...` or `> **解释补充：** ...`, state the assumption or preceding result it relies on, and never present it as a direct quotation or explicit source claim.

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
- `核心原理` for each substantial proof/derivation/complex example, beginning with an untitled explanatory blockquote;
- detailed but source-faithful proof or example explanations;
- explicit labels for any necessary supplementary derivation or explanation;
- a source-faithful parent/child heading structure and bilingual first occurrences of important technical terms;
- summaries, pitfalls, and revision aids after the main body; and
- an honest `待核对` section when extraction was incomplete.
