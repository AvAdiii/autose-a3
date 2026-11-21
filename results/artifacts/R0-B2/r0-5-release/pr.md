Closes #2.

This pull request was produced by the autose workflow. A maintainer decides whether to merge it.

## What the issue asks (READY requirements from `spec.md`)
- **FR-001** When a header line ends with an empty attribute list, the library shall output the header element without any attribute and without the list text.
- **FR-002** When the last line of a block is an empty attribute list, the library shall output the block element without any attribute and without the list text.
- **FR-003** When an empty attribute list directly follows an inline element, the library shall output the inline element without any attribute and without the list text.
- **FR-004** When an attribute list contains at least one attribute, the library shall assign those attributes as before.
- **FR-005** While the `attr_list` extension is enabled, the library shall treat text of the form `{ }` (no colon) exactly as it did before this change.

## Approach (from `design.md`)
`AttrListTreeprocessor.BASE_RE` is `\{\:?[ ]*([^\}\n ][^\n]*)\}`. For `{: }` and `{:}` the optional colon backtracks and the group captures `:`, so `get_attrs_and_remainder(':')` yields a bogus `:` attribute (`<h1 :>`). The fix stays inside the `attr_list` extension (Treeprocessor, ARCHITECTURE.md): `BASE_RE` gets a first alternative that matches `{:` + spaces + `}` as an explicit empty list (no capture), and the existing call sites treat a `None` group as an empty attribute string, so `assign_attrs` assigns nothing and the matched text is stripped exactly as for a non-empty list. `{ }` (no colon) still fails to match, as before. Note: I could not run probes (the sandbox was unavailable), so the regex reasoning comes from reading the code; the implementer should verify the Interface outputs.

| File | Symbol | Change | ACs | Notes |
|---|---|---|---|---|
| markdown/extensions/attr_list.py | AttrListTreeprocessor.BASE_RE | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2, AC-FR-004-1, AC-FR-004-2, AC-FR-004-3, AC-FR-005-1 | New pattern: `\{(?:\:[ ]*\}|\:?[ ]*([^\}\n ][^\n]*)\})`. The empty alternative is tried first, so `{: }`/`{:}` never reach the group that captured `:`. HEADER_RE/BLOCK_RE/INLINE_RE are built from it unchanged. Group 1 is `None` for an empty list. |
| markdown/extensions/attr_list.py | AttrListTreeprocessor.run | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2 | Every `m.group(1)` passed to `assign_attrs` becomes `m.group(1) or ''` (7 call sites). |
| markdown/extensions/attr_list.py | AttrListTreeprocessor.assign_attrs | modify | AC-FR-001-1, AC-FR-002-1, AC-FR-003-1 | Make sure an empty `attrs_string` returns `''` with no attributes (check `get_attrs_and_remainder('')` returns `([], '')`; add an early return if not). |
| tests/test_syntax/extensions/test_attr_list.py | new test methods in existing attr_list test class | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2, AC-FR-004-1, AC-FR-004-2, AC-FR-004-3, AC-FR-005-1 | One method per AC |
| docs/changelog.md | - | modify | - | Entry under `## [Unreleased]` / `### Fixed` |

## Tests (from `test_report.md`)
| Acceptance criterion | Test | Base | Head |
|---|---|---|---|
| AC-FR-001-1 | `test_ac_fr_001_1_empty_list_header_space` | fail | pass |
| AC-FR-001-2 | `test_ac_fr_001_2_empty_list_header_no_space` | fail | pass |
| AC-FR-002-1 | `test_ac_fr_002_1_empty_list_block_no_space` | fail | pass |
| AC-FR-002-2 | `test_ac_fr_002_2_empty_list_block_space` | fail | pass |
| AC-FR-003-1 | `test_ac_fr_003_1_empty_list_inline_space` | fail | pass |
| AC-FR-003-2 | `test_ac_fr_003_2_empty_list_inline_no_space` | fail | pass |
| AC-FR-004-1 | `test_ac_fr_004_1_nonempty_header` | pass | pass |
| AC-FR-004-2 | `test_ac_fr_004_2_nonempty_inline` | pass | pass |
| AC-FR-004-3 | `test_ac_fr_004_3_nonempty_block` | pass | pass |
| AC-FR-005-1 | `test_ac_fr_005_1_braces_without_colon_unchanged` | pass | pass |

## Stage checks
| Stage | Result | Attempts |
|---|---|---|
| requirements | passed | 1 |
| design | passed | 1 |
| implementation | passed | 1 |
| testing | passed | 1 |
| release | CI passed | - |

Round 0. Run and all stage artifacts: https://github.com/AvAdiii/markdown/actions/runs/44887224113

## autose check (release): PASSED
- PR: https://github.com/AvAdiii/markdown/pull/12
- head: `07fbef4cf68f06a774921a5d3e5904e8726b1a2a`
- 14 checks passed
