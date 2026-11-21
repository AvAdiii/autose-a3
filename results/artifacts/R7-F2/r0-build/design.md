# Design: Exclude a heading from the TOC via the `no-toc` class

## Summary
The change lives entirely in the `toc` extension (`TocTreeprocessor.run` in `markdown/extensions/toc.py`). `attr_list` is a treeprocessor that runs before `toc` and has already put `class="no-toc"` on the heading element, so `run` only needs to check the element's `class` attribute. A heading whose space-separated classes include `no-toc` still gets its id (generated through `unique`, so `contents`, `contents_1`, ...), anchors and permalinks, but is not appended to `toc_tokens`. Because the TOC markup and `md.toc_tokens` are both built from that list, one check satisfies FR-001 to FR-003. Rework: the tests are now planned as a new class in the already existing `tests/test_syntax/extensions/test_toc.py` (change `modify`, not `add`). No option is added (FR-005 is BLOCKED) and no new import is needed, so core and extension boundaries are untouched.

## Changes
| File | Symbol | Change | ACs | Notes |
|---|---|---|---|---|
| markdown/extensions/toc.py | TocTreeprocessor.run | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2 | Add `and 'no-toc' not in el.attrib.get('class', '').split()` to the condition that appends to `toc_tokens`. Id generation, anchors and permalinks stay unchanged for such headings. |
| tests/test_syntax/extensions/test_toc.py | new TestTOCNoToc | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2 | File exists (classes `TestTOC`, `testStripTags`); append a new class `TestTOCNoToc(TestCase)` using `Markdown(extensions=['toc','attr_list'])` directly (`from markdown import Markdown` is already imported). |
| docs/changelog.md | - | modify | - | Unreleased currently has only `### Fixed`; add a new `### Added` subsection above it with an entry: headings with the `no-toc` class (via `attr_list`) are excluded from the `toc` output and `md.toc_tokens`. |

## Interface
No new options. Headings whose `class` attribute contains the token `no-toc` are excluded; the class stays in the output (`class="no-toc"`, id after it, as `attr_list` renders today).

Text T = `# Guide\n\n## Contents {: .no-toc }\n\n[TOC]\n\n## Install\n\n## Usage`, extensions `['toc', 'attr_list']`. Expected output of `md.convert(T)`:
```
<h1 id="guide">Guide</h1>
<h2 class="no-toc" id="contents">Contents</h2>
<div class="toc">
<ul>
<li><a href="#guide">Guide</a><ul>
<li><a href="#install">Install</a></li>
<li><a href="#usage">Usage</a></li>
</ul>
</li>
</ul>
</div>
<h2 id="install">Install</h2>
<h2 id="usage">Usage</h2>
```
- AC-FR-001-1: output contains `href="#guide"`, `href="#install"`, `href="#usage"`; not `href="#contents"`.
- AC-FR-001-2: `md.toc` does not contain `>Contents<`.
- AC-FR-001-3: `## Contents {: .a .no-toc }\n\n[TOC]\n\n## Install` -> no `href="#contents"`, contains `href="#install"`.
- AC-FR-002-1: output contains `<h2 class="no-toc" id="contents">Contents</h2>` (an `<h2` tag with `id="contents"`, and `>Contents</h2>`).
- AC-FR-002-2: `## Contents {: .no-toc }\n\n## Contents {: .no-toc }` -> `<h2 class="no-toc" id="contents">Contents</h2>\n<h2 class="no-toc" id="contents_1">Contents</h2>`.
- AC-FR-003-1: `md.toc_tokens` has one top-level entry, id `guide`, whose `children` ids are `['install', 'usage']`.
- AC-FR-003-2: recursive search of `md.toc_tokens` finds no id `contents`.

## Test plan
| AC | Test file | Test method (contains the AC id in snake case) | Asserts |
|---|---|---|---|
| AC-FR-001-1 | tests/test_syntax/extensions/test_toc.py | test_ac_fr_001_1_hrefs | the three hrefs present, no `#contents` href |
| AC-FR-001-2 | tests/test_syntax/extensions/test_toc.py | test_ac_fr_001_2_md_toc | `>Contents<` not in `md.toc` |
| AC-FR-001-3 | tests/test_syntax/extensions/test_toc.py | test_ac_fr_001_3_multiple_classes | `.a .no-toc` excluded, install present |
| AC-FR-002-1 | tests/test_syntax/extensions/test_toc.py | test_ac_fr_002_1_heading_keeps_id | `<h2 class="no-toc" id="contents">Contents</h2>` in output |
| AC-FR-002-2 | tests/test_syntax/extensions/test_toc.py | test_ac_fr_002_2_unique_ids | `contents` and `contents_1` ids |
| AC-FR-003-1 | tests/test_syntax/extensions/test_toc.py | test_ac_fr_003_1_toc_tokens | nested ids guide -> [install, usage] |
| AC-FR-003-2 | tests/test_syntax/extensions/test_toc.py | test_ac_fr_003_2_no_contents_token | no recursive `contents` id |

## Architecture fit
The behaviour change stays inside the `toc` extension's Treeprocessor; `attr_list` is only observed through the element's `class` attribute, so there is no import between extensions and no core change. No new extension, entry point or registry priority change. The changelog row satisfies the CI rule.

## Risks
- Existing toc tests (`tests/test_syntax/extensions/test_toc.py`, `tests/test_extensions.py`) cover headings without `no-toc`; they are unaffected because the check only triggers on that class token.
- A `class` value that merely contains `no-toc` as a substring (e.g. `no-toc-x`) must not match; token comparison via `.split()` handles this.
- Excluded headings still receive permalinks/anchors when those options are on; deliberate, since they remain linkable headings.


---
## autose check: PASSED
- 3 planned changes; every READY criterion mapped; symbols found
