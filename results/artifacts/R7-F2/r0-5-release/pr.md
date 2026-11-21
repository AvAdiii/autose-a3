Closes #4.

This pull request was produced by the autose workflow. A maintainer decides whether to merge it.

## What the issue asks (READY requirements from `spec.md`)
- **FR-001** When a heading carries the class `no-toc` and the `toc` and `attr_list` extensions are enabled, the library shall omit that heading from the table of contents it produces.
- **FR-002** When a heading carries the class `no-toc`, the library shall render it as a heading that has an id derived in the usual way.
- **FR-003** When a heading carries the class `no-toc`, the library shall omit it from `md.toc_tokens`.

## Approach (from `design.md`)
The change lives entirely in the `toc` extension (`TocTreeprocessor.run` in `markdown/extensions/toc.py`). `attr_list` is a treeprocessor that runs before `toc` and has already put `class="no-toc"` on the heading element, so `run` only needs to check the element's `class` attribute. A heading whose space-separated classes include `no-toc` still gets its id (generated through `unique`, so `contents`, `contents_1`, ...), anchors and permalinks, but is not appended to `toc_tokens`. Because the TOC markup and `md.toc_tokens` are both built from that list, one check satisfies FR-001 to FR-003. Rework: the tests are now planned as a new class in the already existing `tests/test_syntax/extensions/test_toc.py` (change `modify`, not `add`). No option is added (FR-005 is BLOCKED) and no new import is needed, so core and extension boundaries are untouched.

| File | Symbol | Change | ACs | Notes |
|---|---|---|---|---|
| markdown/extensions/toc.py | TocTreeprocessor.run | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2 | Add `and 'no-toc' not in el.attrib.get('class', '').split()` to the condition that appends to `toc_tokens`. Id generation, anchors and permalinks stay unchanged for such headings. |
| tests/test_syntax/extensions/test_toc.py | new TestTOCNoToc | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2 | File exists (classes `TestTOC`, `testStripTags`); append a new class `TestTOCNoToc(TestCase)` using `Markdown(extensions=['toc','attr_list'])` directly (`from markdown import Markdown` is already imported). |
| docs/changelog.md | - | modify | - | Unreleased currently has only `### Fixed`; add a new `### Added` subsection above it with an entry: headings with the `no-toc` class (via `attr_list`) are excluded from the `toc` output and `md.toc_tokens`. |

## Tests (from `test_report.md`)
| Acceptance criterion | Test | Base | Head |
|---|---|---|---|
| AC-FR-001-1 | `test_ac_fr_001_1_hrefs` | fail | pass |
| AC-FR-001-2 | `test_ac_fr_001_2_md_toc` | fail | pass |
| AC-FR-001-3 | `test_ac_fr_001_3_multiple_classes` | fail | pass |
| AC-FR-002-1 | `test_ac_fr_002_1_heading_keeps_id` | pass | pass |
| AC-FR-002-2 | `test_ac_fr_002_2_unique_ids` | pass | pass |
| AC-FR-003-1 | `test_ac_fr_003_1_toc_tokens` | fail | pass |
| AC-FR-003-2 | `test_ac_fr_003_2_no_contents_token` | fail | pass |

## Stage checks
| Stage | Result | Attempts |
|---|---|---|
| requirements | passed | 1 |
| design | passed | 2 |
| implementation | passed | 1 |
| testing | passed | 1 |
| release | CI passed | - |

Round 0. Run and all stage artifacts: https://github.com/AvAdiii/markdown/actions/runs/44890548514

## autose check (release): PASSED
- PR: https://github.com/AvAdiii/markdown/pull/19
- head: `d9de0814b1f8eed18c8017cdedc14dfe8d79320e`
- 14 checks passed
