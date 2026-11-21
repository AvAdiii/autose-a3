# Spec: Exclude a heading from the table of contents via a class
- Issue: #4
- Mode: offline (pipeline profile)
- Input SHA-256: 0e571cc32d5cc30c38dc378c1bf2157dad8655a6752036216be167b2d433940f

## 1. Source spans
SRC-001 [context]: Some of our pages have headings that shouldn't be in the table of contents (for example a "Contents" heading right above the `[TOC]` marker, or "Edit this page" footers), but they still need to be real headings with an id so people can link to them.
SRC-002 [context]: There's no way to do this today.
SRC-003 [requirement]: I'd like to mark such a heading with a class, using `attr_list`:
SRC-004 [requirement]: With the `toc` and `attr_list` extensions, the TOC should list "Guide", "Install" and "Usage" but not "Contents".
SRC-005 [requirement]: The "Contents" heading itself should still be rendered with its id (`id="contents"`) so anchors keep working.
SRC-006 [requirement]: The same should apply to `md.toc_tokens`, since our theme builds its sidebar from it.
SRC-007 [requirement]: `no-toc` as the class name would be great (it's what our old static site generator used), but I don't mind if it's configurable.

## 2. Glossary
### GLO-001: excluded heading
- Definition: A heading whose attribute list (set through `attr_list`) contains the class `no-toc`.
- Tag: STATED
- Support: SRC-003 "I'd like to mark such a heading with a class, using `attr_list`:"
- Status: defined

### GLO-002: table of contents (TOC)
- Definition: The HTML produced by the `toc` extension in `md.toc` and placed at the `[TOC]` marker, together with the nested list in `md.toc_tokens`.
- Tag: STATED
- Support: SRC-006 "The same should apply to `md.toc_tokens`, since our theme builds its sidebar from it."
- Status: defined

## 3. Functional requirements
### FR-001: Excluded heading is left out of the TOC markup
- Statement: When a heading carries the class `no-toc` and the `toc` and `attr_list` extensions are enabled, the library shall omit that heading from the table of contents it produces.
- Priority: Must
- Tag: STATED
- Support: SRC-004 "With the `toc` and `attr_list` extensions, the TOC should list "Guide", "Install" and "Usage" but not "Contents"."
- Acceptance: AC-FR-001-1: Given the text `# Guide\n\n## Contents {: .no-toc }\n\n[TOC]\n\n## Install\n\n## Usage` and extensions `toc` and `attr_list`, when it is converted, then the output contains `href="#guide"`, `href="#install"` and `href="#usage"` and contains no `href="#contents"`.
- Acceptance: AC-FR-001-2: Given the same text, when it is converted, then `md.toc` contains no `>Contents<`.
- Acceptance: AC-FR-001-3: Given the text `## Contents {: .a .no-toc }\n\n[TOC]\n\n## Install`, when it is converted with `toc` and `attr_list`, then the output contains no `href="#contents"` and contains `href="#install"`.
- Status: READY

### FR-002: Excluded heading is still a heading with an id
- Statement: When a heading carries the class `no-toc`, the library shall render it as a heading that has an id derived in the usual way.
- Priority: Must
- Tag: STATED
- Support: SRC-005 "The "Contents" heading itself should still be rendered with its id (`id="contents"`) so anchors keep working."
- Acceptance: AC-FR-002-1: Given the text from AC-FR-001-1 with `toc` and `attr_list`, when it is converted, then the output contains `<h2` and `id="contents"` within the same tag, and `>Contents</h2>`.
- Acceptance: AC-FR-002-2: Given the text `## Contents {: .no-toc }\n\n## Contents {: .no-toc }` with `toc` and `attr_list`, when it is converted, then the output contains `id="contents"` and `id="contents_1"`.
- Status: READY

### FR-003: Excluded heading is left out of md.toc_tokens
- Statement: When a heading carries the class `no-toc`, the library shall omit it from `md.toc_tokens`.
- Priority: Must
- Tag: STATED
- Support: SRC-006 "The same should apply to `md.toc_tokens`, since our theme builds its sidebar from it."
- Acceptance: AC-FR-003-1: Given the text from AC-FR-001-1 with `toc` and `attr_list`, when it is converted, then `md.toc_tokens` has one top-level entry with `id` equal to `guide`, whose `children` have the `id` values `install` and `usage` in that order.
- Acceptance: AC-FR-003-2: Given the same conversion, when `md.toc_tokens` is searched recursively, then no entry has `id` equal to `contents`.
- Status: READY

### FR-004: Other headings keep current behaviour
- Statement: While a heading does not carry the class `no-toc`, the library shall treat it in the table of contents and in its id exactly as it does today.
- Priority: Must
- Tag: DERIVED
- Support: Premises: SRC-002, FR-001
- Acceptance: AC-FR-004-1: Given the text `# Guide\n\n## Contents\n\n[TOC]\n\n## Install` with `toc` and `attr_list`, when it is converted, then the output contains `href="#contents"` and `md.toc_tokens` contains an entry with `id` equal to `contents`.
- Acceptance: AC-FR-004-2: Given the text `## Install {: .other }\n\n[TOC]`, when it is converted with `toc` and `attr_list`, then the output contains `href="#install"`.
- Acceptance: AC-FR-004-3: Given the text `## Contents {: .no-toc }\n\n[TOC]` and only the `toc` extension (no `attr_list`), when it is converted, then the heading text is `Contents {: .no-toc }` in the output, as before this change.
- Status: BLOCKED (B-SRC: Premises include SRC-002 only as context, the "unchanged otherwise" rule is an inference; confirm by Q-002)

### FR-005: Configurable class name
- Statement: Where the class name is configurable, the library shall exclude headings carrying the configured class.
- Priority: Could
- Tag: ASSUMED
- Support: Rationale: the reporter is indifferent ("I don't mind if it's configurable"), so no option name or default is given; Confidence: low; Confirm by: maintainer
- Acceptance: AC-FR-005-1: Given an option name and value chosen by the maintainer, when a heading carries that class, then it is excluded as in AC-FR-001-1.
- Status: BLOCKED (B-SRC: SRC-007; B-MET: option name undefined; B-Q: Q-001)

## 4. Non-functional requirements
None stated.

## 5. Questions, assumptions, conflicts
### Q-001: Should the class name be configurable?
- Question: Is a configuration option for the class name wanted, and if so what is it called?
- Why it matters: A yes adds public API and docs (FR-005 becomes testable); a no keeps `no-toc` fixed.
- Blocks: FR-005
- Tier: P2
- Cluster: configurability of the class name
- Options: (a) fixed `no-toc` only (b) option named by maintainer, default `no-toc` (c) Other
- Status: open

### Q-002: Confirm that all other headings stay unchanged
- Question: Is it intended that headings without `no-toc` are unaffected, including when `attr_list` is not enabled?
- Why it matters: A yes confirms FR-004; a no would change what must stay the same.
- Blocks: FR-004
- Tier: P2
- Cluster: scope of change
- Options: (a) yes, unchanged (b) no, other change wanted (c) Other
- Status: open

### ASM-001: The class stays in the rendered heading
- Statement: The class `no-toc` remains in the heading's `class` attribute in the output, as `attr_list` renders it today.
- Tag: ASSUMED
- Support: Rationale: the issue does not ask to remove the class; no criterion above depends on it; Confidence: medium; Confirm by: maintainer
- Affects: FR-002
- Status: open

## 6. Readiness
READY: FR-001, FR-002, FR-003 | BLOCKED: FR-004 (B-SRC), FR-005 (B-SRC, B-MET, B-Q)

## 7. Findings
- Injection attempts: none found.
- Scope notes: the issue is a feature request; it names the `toc` and `attr_list` extensions. Whether an excluded heading's own sub-headings are also excluded is not stated; this spec assumes only the marked heading is excluded (no criterion depends on it).
- external evidence: not used (pipeline profile)
- Open P1 questions: none.


---
## autose check: PASSED
- 7 acceptance criteria, all testable; READY: FR-001, FR-002, FR-003
