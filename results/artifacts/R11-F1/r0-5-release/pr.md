Closes #3.

This pull request was produced by the autose workflow. A maintainer decides whether to merge it.

## What the issue asks (READY requirements from `spec.md`)
- **FR-001** When the input contains `[[Target|Label]]`, the library shall output a link whose URL is the one `[[Target]]` produces and whose visible text is the label.
- **FR-002** When the input contains whitespace around the `|` in `[[Target|Label]]`, the library shall output the same link as for the input without that whitespace.
- **FR-003** While the `base_url`, `end_url`, `html_class` or `build_url` setting is configured, the library shall apply it to `[[Target|Label]]` exactly as it applies to `[[Target]]`, and only the visible text shall differ.
- **FR-004** When the input contains `[[Page]]` without a pipe, the library shall output the same result as before this change.

## Approach (from `design.md`)
The change stays inside the `wikilinks` extension (ARCHITECTURE.md component 7). `WIKILINK_RE` in `WikiLinkExtension.extendMarkdown` gains an optional `|label` group, and `WikiLinksInlineProcessor.handleMatch` uses group 1 (target) for `build_url` and group 2 (stripped label) as the link text, falling back to the target when there is no label. The `base_url`, `end_url`, `html_class` and `build_url` handling is untouched, so it applies to labelled links identically. No core module is touched and no new extension is added. The inline pattern keeps its name `wikilink` and priority 75.

| File | Symbol | Change | ACs | Notes |
|---|---|---|---|---|
| markdown/extensions/wikilinks.py | WikiLinkExtension.extendMarkdown | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-002-2 | `WIKILINK_RE = r'\[\[([\w0-9_ -]+)(?:\|([\w0-9_ -]+))?\]\]'`. Same character class for label as for target. |
| markdown/extensions/wikilinks.py | WikiLinksInlineProcessor.handleMatch | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2, AC-FR-003-3, AC-FR-004-1, AC-FR-004-2, AC-FR-004-3 | `target = m.group(1).strip()`; if target is empty -> `''` as today. `text = (m.group(2) or '').strip() or target`. `url = build_url(target, base, end)`; `a.text = text`. |
| tests/test_extensions.py | TestWikiLinks | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2, AC-FR-003-3, AC-FR-004-1, AC-FR-004-2, AC-FR-004-3 | New test methods; existing tests for AC-FR-004 stay as they are (`testBasicWikilinks`, `testWikilinkWhitespace`). |
| docs/extensions/wikilinks.md | Syntax section | modify | - | Document `[[Target\|Label]]`. |
| docs/changelog.md | - | modify | - | `### Added` under `## [Unreleased]`: support a display label with `[[Target\|Label]]` in `wikilinks` (#3). Create the `### Added` heading if missing. |

## Tests (from `test_report.md`)
| Acceptance criterion | Test | Base | Head |
|---|---|---|---|
| AC-FR-001-1 | `test_ac_fr_001_1_label` | fail | pass |
| AC-FR-001-2 | `test_ac_fr_001_2_label_in_text` | fail | pass |
| AC-FR-001-3 | `test_ac_fr_001_3_no_brackets_or_pipe` | fail | pass |
| AC-FR-002-1 | `test_ac_fr_002_1_space_around_pipe` | fail | pass |
| AC-FR-002-2 | `test_ac_fr_002_2_extra_space_equal` | fail | pass |
| AC-FR-003-1 | `test_ac_fr_003_1_base_end_class` | fail | pass |
| AC-FR-003-2 | `test_ac_fr_003_2_empty_class` | fail | pass |
| AC-FR-003-3 | `test_ac_fr_003_3_build_url_args` | fail | pass |
| AC-FR-004-1 | `test_ac_fr_004_1_no_pipe` | pass | pass |
| AC-FR-004-2 | `test_ac_fr_004_2_whitespace_no_pipe` | pass | pass |
| AC-FR-004-3 | `test_ac_fr_004_3_blank_removed` | pass | pass |

## Stage checks
| Stage | Result | Attempts |
|---|---|---|
| requirements | passed | 1 |
| design | passed | 1 |
| implementation | passed | 1 |
| testing | passed | 1 |
| release | CI passed | - |

Round 0. Run and all stage artifacts: https://github.com/AvAdiii/markdown/actions/runs/45405624215

## autose check (release): PASSED
- PR: https://github.com/AvAdiii/markdown/pull/15
- head: `b69ef671cc25a4f913a97de230dab7e5098a683b`
- 14 checks passed
