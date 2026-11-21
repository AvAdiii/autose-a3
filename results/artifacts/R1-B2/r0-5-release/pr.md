Closes #2.

This pull request was produced by the autose workflow. A maintainer decides whether to merge it.

## What the issue asks (READY requirements from `spec.md`)
- **FR-001** When the `attr_list` extension is enabled and a heading line ends with an empty attribute list, the library shall output the heading element with no attributes and without the list text.
- **FR-002** When the `attr_list` extension is enabled and the last line of a block is an empty attribute list, the library shall output the block element with no attributes and without the list text.
- **FR-003** When the `attr_list` extension is enabled and an empty attribute list directly follows an inline element, the library shall output that inline element with no attributes and without the list text.
- **FR-004** When the `attr_list` extension is enabled, the library shall continue to apply the attributes of a non-empty attribute list as it did before this change.

## Approach (from `design.md`)
The `attr_list` treeprocessor (`AttrListTreeprocessor` in `markdown/extensions/attr_list.py`) builds all its regexes from `BASE_RE`. For `{: }` and `{:}` the optional `\:?` backtracks, so the colon is captured as the attribute text and becomes the bogus `:` attribute. The fix is confined to that extension: change `BASE_RE` so that `{:` followed by spaces and `}` matches with an empty capture group. `assign_attrs` then assigns nothing and the matched text is removed. `{}` without a colon still does not match, so it is unchanged. The prototype was run against all spec inputs and gives the expected output.

| File | Symbol | Change | ACs | Notes |
|---|---|---|---|---|
| markdown/extensions/attr_list.py | AttrListTreeprocessor.BASE_RE | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-003-1, AC-FR-003-2, AC-FR-003-3, AC-FR-004-1, AC-FR-004-2 | New value: `r'\{(?:\:[ ]*(?=\})|\:?[ ]*(?=[^\}\n ]))([^\n]*)\}'`. Group 1 may now be empty. HEADER_RE, BLOCK_RE and INLINE_RE derive from it and need no edit. |
| tests/test_syntax/extensions/test_attr_list.py | new test methods in TestAttrList | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-003-1, AC-FR-003-2, AC-FR-003-3, AC-FR-004-1, AC-FR-004-2 | tests |
| docs/changelog.md | - | modify | - | entry under `## [Unreleased]` / `### Fixed` |

## Tests (from `test_report.md`)
| Acceptance criterion | Test | Base | Head |
|---|---|---|---|
| AC-FR-001-1 | `test_ac_fr_001_1_empty_list_heading` | fail | pass |
| AC-FR-001-2 | `test_ac_fr_001_2_empty_list_no_space_and_many_spaces` | fail | pass |
| AC-FR-001-3 | `test_ac_fr_001_3_nonempty_list_heading` | pass | pass |
| AC-FR-002-1 | `test_ac_fr_002_1_empty_list_block_no_space` | fail | pass |
| AC-FR-002-2 | `test_ac_fr_002_2_empty_list_block_space` | fail | pass |
| AC-FR-002-3 | `test_ac_fr_002_3_nonempty_list_block` | pass | pass |
| AC-FR-003-1 | `test_ac_fr_003_1_empty_list_inline_space` | fail | pass |
| AC-FR-003-2 | `test_ac_fr_003_2_empty_list_inline_no_space` | fail | pass |
| AC-FR-003-3 | `test_ac_fr_003_3_nonempty_list_inline` | pass | pass |
| AC-FR-004-1 | `test_ac_fr_004_1_id_heading` | pass | pass |
| AC-FR-004-2 | `test_ac_fr_004_2_multiple_classes_heading` | pass | pass |

## Stage checks
| Stage | Result | Attempts |
|---|---|---|
| requirements | passed | 1 |
| design | passed | 1 |
| implementation | passed | 1 |
| testing | passed | 1 |
| release | CI passed | - |

Round 0. Run and all stage artifacts: https://github.com/AvAdiii/markdown/actions/runs/44889589134

## autose check (release): PASSED
- PR: https://github.com/AvAdiii/markdown/pull/12
- head: `30f96554b289096fb54ae27fd2d73f8f8dd9283c`
- 14 checks passed
