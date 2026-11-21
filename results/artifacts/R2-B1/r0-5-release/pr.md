Closes #1.

This pull request was produced by the autose workflow. A maintainer decides whether to merge it.

## What the issue asks (READY requirements from `spec.md`)
- **FR-001** If a fenced code block with an attribute list contains `linenums`, `guess_lang` or `noclasses`, with or without a value, and `codehilite` is not enabled, then the converter shall render the block as a `<pre><code>` code block and shall not raise an exception.
- **FR-003** When a fenced code block with an attribute list contains an attribute other than `linenums`, `guess_lang` and `noclasses`, and `codehilite` is not enabled, the converter shall output that attribute on the `<code>` element as it does today.
- **FR-004** While `codehilite` is enabled, the converter shall convert a fenced code block that has `linenums`, `guess_lang` or `noclasses` attributes without raising an exception.

## Approach (from `design.md`)
`FencedBlockPreprocessor.handle_attrs` converts `linenums`, `guess_lang`, `noclasses` (and `use_pygments`) to `bool`/`None` via `parseBoolValue`. In the non-highlighting branch of `FencedBlockPreprocessor.run`, every config item except `use_pygments` is passed to `_escape_attrib_html`, which raises `TypeError` for a bool/None. The fix stays inside the `fenced_code` extension (ARCHITECTURE.md: extension behaviour changes within the extension): when building `kv_pairs`, skip every key in `self.bool_options` (the highlighter-only options), not just `use_pygments`. These attributes are therefore omitted from the HTML (this matches Q-001 option (a), but FR-002 is BLOCKED and the output form is not a contract; tests only assert the READY criteria). Other attributes (`data-x`, `data-test`) are unchanged. The codehilite path is untouched.

| File | Symbol | Change | ACs | Notes |
|---|---|---|---|---|
| markdown/extensions/fenced_code.py | FencedBlockPreprocessor.run | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-003-1, AC-FR-003-2 | In the `kv_pairs` generator replace `if k != 'use_pygments'` with `if k not in self.bool_options`. Update the comment. |
| tests/test_syntax/extensions/test_fenced_code.py | new TestFencedCodeWithoutCodehilite | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-003-1, AC-FR-003-2, AC-FR-004-1, AC-FR-004-2 | New tests; use existing test style (`TestCase.assertMarkdownRenders`) or `markdown.markdown` directly. |
| docs/changelog.md | - | modify | - | Entry under `## [Unreleased]` / `### Fixed`. |

## Tests (from `test_report.md`)
| Acceptance criterion | Test | Base | Head |
|---|---|---|---|
| AC-FR-001-1 | `test_ac_fr_001_1_linenums_flag` | error | pass |
| AC-FR-001-2 | `test_ac_fr_001_2_linenums_value` | error | pass |
| AC-FR-001-3 | `test_ac_fr_001_3_guess_lang_noclasses` | - | pass |
| AC-FR-001-4 | `test_ac_fr_001_4_plain_python` | pass | pass |
| AC-FR-003-1 | `test_ac_fr_003_1_data_attr` | pass | pass |
| AC-FR-003-2 | `test_ac_fr_003_2_data_test_braces` | pass | pass |
| AC-FR-004-1 | `test_ac_fr_004_1_codehilite_linenums` | pass | pass |
| AC-FR-004-2 | `test_ac_fr_004_2_codehilite_linenums_true` | pass | pass |

## Stage checks
| Stage | Result | Attempts |
|---|---|---|
| requirements | passed | 2 |
| design | passed | 1 |
| implementation | passed | 1 |
| testing | passed | 1 |
| release | CI passed | - |

Round 0. Run and all stage artifacts: https://github.com/AvAdiii/markdown/actions/runs/44890133094

## autose check (release): PASSED
- PR: https://github.com/AvAdiii/markdown/pull/16
- head: `bf7e4a2d70957520b6e06178f4762742ecef7cf3`
- 14 checks passed
