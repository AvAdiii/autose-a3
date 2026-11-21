Closes #3.

This pull request was produced by the autose workflow. A maintainer decides whether to merge it.

## What the issue asks (READY requirements from `spec.md`)
- **FR-001** When the input contains `[[Target|Label]]`, the extension shall output a link whose URL is the one built for `[[Target]]` and whose visible text is the label.
- **FR-002** When the input contains whitespace around the `|` in `[[Target|Label]]`, the extension shall output the same link as for the input without that whitespace.
- **FR-003** When a labelled wikilink is converted, the extension shall apply `base_url`, `end_url`, `html_class` and a custom `build_url` exactly as for an unlabelled wikilink with the same target, and shall change only the visible text.
- **FR-004** When the input contains `[[Page]]` without a pipe, the extension shall output the same result as for `[[Page]]` in the current release, in which a whitespace-only wikilink produces no link.

## Approach (from `design.md`)
The change lives entirely in the `wikilinks` extension (component 7 in ARCHITECTURE.md). `WikiLinkExtension.extendMarkdown` gets a regex with an optional `|label` group, and `WikiLinksInlineProcessor.handleMatch` uses the target for `build_url` and the label (when present) as the link text. Everything else (`_getMeta`, `base_url`, `end_url`, `html_class`, `build_url`) is untouched, so FR-003 holds by construction. The label uses the same character class as the target (`[\w0-9_ -]`), which is the smallest choice and leaves the BLOCKED edge cases (FR-005, Q-001..Q-003) unspecified and untested. Text is set via `a.text`, so it is escaped like today (ASM-001). No core module changes, no new extension.

| File | Symbol | Change | ACs | Notes |
|---|---|---|---|---|
| markdown/extensions/wikilinks.py | WikiLinkExtension.extendMarkdown | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-002-2, AC-FR-004-1, AC-FR-004-2 | `WIKILINK_RE = r'\[\[([\w0-9_ -]+?)(?:[ ]*\|[ ]*([\w0-9_ -]+))?\]\]'`; group 1 = target, group 2 = label (optional). Must not change matching for pipe-less input. |
| markdown/extensions/wikilinks.py | WikiLinksInlineProcessor.handleMatch | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2, AC-FR-003-3, AC-FR-004-1, AC-FR-004-2 | `target = m.group(1).strip()`; if empty return `''` as today; `url = build_url(target, ...)`; `a.text = (m.group(2) or '').strip() or target`. |
| tests/test_syntax/extensions/test_wikilinks.py | new TestWikiLinks | add | all READY ACs | new file, `TestCase` from `markdown.test_tools`, `default_kwargs = {'extensions': ['wikilinks']}` |
| docs/extensions/wikilinks.md | - | modify | - | document `[[Target\|Label]]` syntax |
| docs/changelog.md | - | modify | - | entry under `## [Unreleased]` -> `### Added` (add the heading before `### Fixed` if absent): "Support `[[Target\|Label]]` display labels in the `wikilinks` extension." |

## Tests (from `test_report.md`)
| Acceptance criterion | Test | Base | Head |
|---|---|---|---|
| AC-FR-001-1 | `test_ac_fr_001_1_label` | fail | pass |
| AC-FR-001-2 | `test_ac_fr_001_2_same_href` | fail | pass |
| AC-FR-001-3 | `test_ac_fr_001_3_no_syntax_left` | fail | pass |
| AC-FR-002-1 | `test_ac_fr_002_1_spaces_around_pipe` | fail | pass |
| AC-FR-002-2 | `test_ac_fr_002_2_label_padding` | fail | pass |
| AC-FR-003-1 | `test_ac_fr_003_1_options` | fail | pass |
| AC-FR-003-2 | `test_ac_fr_003_2_empty_class` | fail | pass |
| AC-FR-003-3 | `test_ac_fr_003_3_custom_build_url` | fail | pass |
| AC-FR-004-1 | `test_ac_fr_004_1_unlabelled` | pass | pass |
| AC-FR-004-2 | `test_ac_fr_004_2_blank_wikilink` | pass | pass |

## Stage checks
| Stage | Result | Attempts |
|---|---|---|
| requirements | passed | 2 |
| design | passed | 1 |
| implementation | passed | 1 |
| testing | passed | 1 |
| release | CI passed | - |

Round 0. Run and all stage artifacts: https://github.com/AvAdiii/markdown/actions/runs/44890136597

## autose check (release): PASSED
- PR: https://github.com/AvAdiii/markdown/pull/15
- head: `e1488058841a8af03dcd99cf1637205202ba3195`
- 14 checks passed
