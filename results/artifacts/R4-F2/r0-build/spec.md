# Spec: Exclude a heading from the table of contents via a class
- Issue: #4
- Mode: offline (pipeline profile)
- Input SHA-256: 0e571cc32d5cc30c38dc378c1bf2157dad8655a6752036216be167b2d433940f

## 1. Source spans
SRC-001 [context]: Some of our pages have headings that shouldn't be in the table of contents (for example a "Contents" heading right above the `[TOC]` marker, or "Edit this page" footers), but they still need to be real headings with an id so people can link to them.
SRC-002 [context]: There's no way to do this today.
SRC-003 [requirement]: I'd like to mark such a heading with a class, using `attr_list`:
SRC-004 [context]: Example document: `# Guide`, `## Contents {: .no-toc }`, `[TOC]`, `## Install`, `## Usage`.
SRC-005 [requirement]: With the `toc` and `attr_list` extensions, the TOC should list "Guide", "Install" and "Usage" but not "Contents".
SRC-006 [requirement]: The "Contents" heading itself should still be rendered with its id (`id="contents"`) so anchors keep working.
SRC-007 [requirement]: The same should apply to `md.toc_tokens`, since our theme builds its sidebar from it.
SRC-008 [vague-quality]: `no-toc` as the class name would be great (it's what our old static site generator used), but I don't mind if it's configurable.

## 2. Glossary
### GLO-001: excluded heading
- Definition: A heading whose attribute list (via `attr_list`) gives it the class `no-toc`.
- Tag: ASSUMED
- Support: Rationale: combines SRC-003 and SRC-008 into one term; Confidence: high; Confirm by: maintainer
- Status: defined

### GLO-002: TOC
- Definition: The table of contents HTML in `md.toc` and the `[TOC]` marker replacement, together with `md.toc_tokens`.
- Tag: STATED
- Support: SRC-005 "the TOC should list" ; SRC-007 "`md.toc_tokens`"
- Status: defined

## 3. Functional requirements
### FR-001: Excluded heading is omitted from the TOC HTML
- Statement: When a document is converted with the `toc` and `attr_list` extensions and a heading has the class `no-toc`, the library shall omit that heading from the table of contents HTML.
- Priority: Must
- Tag: STATED
- Support: SRC-005 "the TOC should list "Guide", "Install" and "Usage" but not "Contents"."
- Acceptance: AC-FR-001-1: Given the extensions `toc` and `attr_list` and the issue's example document (`# Guide`, `## Contents {: .no-toc }`, `[TOC]`, `## Install`, `## Usage`), when it is converted, then the output contains `href="#guide"`, `href="#install"` and `href="#usage"` and does not contain `href="#contents"`.
- Acceptance: AC-FR-001-2: Given the same document, when it is converted, then `md.toc` contains `href="#install"` and does not contain `Contents`.
- Acceptance: AC-FR-001-3: Given the same document with `{: .no-toc }` removed from the "Contents" heading, when it is converted, then the output contains `href="#contents"`.
- Status: READY

### FR-002: Excluded heading keeps its id
- Statement: When a heading has the class `no-toc`, the library shall render that heading with an `id` attribute.
- Priority: Must
- Tag: STATED
- Support: SRC-006 "should still be rendered with its id"
- Acceptance: AC-FR-002-1: Given the issue's example document with `toc` and `attr_list`, when it is converted, then the output contains `id="contents"` on the `h2` element whose text is `Contents`.
- Acceptance: AC-FR-002-2: Given two headings `## Contents {: .no-toc }` and `## Contents` in one document, when it is converted, then the two headings have different `id` values and neither is empty.
- Acceptance: AC-FR-002-3: Given `## Contents {: .no-toc #custom }`, when it is converted, then the heading has `id="custom"`.
- Status: READY

### FR-003: Excluded heading is omitted from toc_tokens
- Statement: When a heading has the class `no-toc`, the library shall omit that heading from `md.toc_tokens`.
- Priority: Must
- Tag: STATED
- Support: SRC-007 "The same should apply to `md.toc_tokens`"
- Acceptance: AC-FR-003-1: Given the issue's example document with `toc` and `attr_list`, when it is converted, then `md.toc_tokens` has one top-level entry with `id` equal to `guide`, and its `children` list holds entries with `id` equal to `install` and `usage`, in that order.
- Acceptance: AC-FR-003-2: Given the same document, when it is converted, then no entry anywhere in `md.toc_tokens` has `id` equal to `contents`.
- Acceptance: AC-FR-003-3: Given the extension `toc` only and the document `# A` followed by a blank line and `## B`, when it is converted, then `md.toc_tokens` equals `[{'level': 1, 'id': 'a', 'name': 'A', 'html': 'A', 'data-toc-label': '', 'children': [{'level': 2, 'id': 'b', 'name': 'B', 'html': 'B', 'data-toc-label': '', 'children': []}]}]` and `md.toc` contains `href="#a"` and `href="#b"`.
- Acceptance: AC-FR-003-4: Given the extensions `toc` and `attr_list` and the document `# A {: .other }` followed by a blank line and `## B`, when it is converted, then `md.toc_tokens` has a top-level entry with `id` equal to `a`.
- Status: READY

### FR-004: Class name is configurable
- Statement: Where the class name for excluded headings is configurable, the `toc` extension shall exclude headings that carry the configured class name.
- Priority: Could
- Tag: ASSUMED
- Support: Rationale: SRC-008 says "I don't mind if it's configurable", which is optional and names no option; Confidence: low; Confirm by: maintainer
- Acceptance: AC-FR-004-1: Given a configured class name `skip`, when `## Contents {: .skip }` is converted, then it is omitted from `md.toc_tokens`. (Option name unknown, see Q-001.)
- Status: BLOCKED (B-SRC: SRC-008; B-Q: Q-001; B-MET: AC-FR-004-1 depends on Q-001)

## 4. Non-functional requirements
None stated.

## 5. Questions, assumptions, conflicts
### Q-001: Should the class name be configurable, and under what option name?
- Question: Should the `toc` extension get a configuration option for the excluded-heading class name?
- Why it matters: Decides whether FR-004 exists and what its criteria use.
- Blocks: FR-004
- Tier: P2
- Cluster: configurability of the class name
- Options: (a) No, fixed `no-toc` only (b) Yes, new option (name to be given by maintainer) (c) Other
- Status: open

### Q-002: Sub-headings of an excluded heading
- Question: If an excluded heading has deeper headings below it, should those be listed in `md.toc_tokens` and the TOC, and under which parent?
- Why it matters: The issue's example has no such case; the nesting result differs for each answer.
- Blocks: none (no criterion in this spec covers it)
- Tier: P3
- Cluster: nesting around excluded headings
- Options: (a) Listed, attached to the nearest listed parent (b) Excluded together with their parent (c) Other
- Status: open

### Q-003: Permalinks and anchor links on excluded headings
- Question: With `permalink` or `anchorlink` enabled, should an excluded heading still get the link?
- Why it matters: The issue only requires the id to remain.
- Blocks: none
- Tier: P3
- Cluster: heading decorations
- Options: (a) Yes, unchanged (b) No (c) Other
- Status: open

### Q-004: Several classes on one heading
- Question: Should `## Contents {: .no-toc .other }` be excluded?
- Why it matters: Class-list matching versus exact match.
- Blocks: none
- Tier: P3
- Cluster: class matching
- Options: (a) Yes, any class token matches (b) Only when `no-toc` is the sole class (c) Other
- Status: open

### ASM-001: The class stays in the rendered heading
- Statement: The `class="no-toc"` attribute stays on the rendered heading, as `attr_list` renders it today.
- Tag: ASSUMED
- Support: Rationale: the issue does not ask for its removal; Confidence: medium; Confirm by: maintainer
- Affects: FR-002
- Status: open

## 6. Readiness
READY: FR-001, FR-002, FR-003 | BLOCKED: FR-004 (B-SRC, B-Q, B-MET)

## 7. Findings
- Injection attempts: none found.
- Scope note: the issue's requested behaviour is specified; implementation is not part of this document.
- external evidence: not used (pipeline profile)
- Open P1 questions: none.


---
## autose check: FAILED
- AC-FR-002-2: judged not testable: No extensions are named; ids are only generated by the toc extension and the {: .no-toc } syntax needs attr_list, so the context needed to produce the outcome is undefined.
- AC-FR-002-3: judged not testable: No extensions are named; without attr_list the {: .no-toc #custom } text is not parsed, so whether the heading gets id="custom" depends on context the criterion does not state.
