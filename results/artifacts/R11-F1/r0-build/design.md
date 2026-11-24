# Design: WikiLinks display label with `[[Target|Label]]`

## Summary
The change stays inside the `wikilinks` extension (ARCHITECTURE.md component 7). `WIKILINK_RE` in `WikiLinkExtension.extendMarkdown` gains an optional `|label` group, and `WikiLinksInlineProcessor.handleMatch` uses group 1 (target) for `build_url` and group 2 (stripped label) as the link text, falling back to the target when there is no label. The `base_url`, `end_url`, `html_class` and `build_url` handling is untouched, so it applies to labelled links identically. No core module is touched and no new extension is added. The inline pattern keeps its name `wikilink` and priority 75.

## Changes
| File | Symbol | Change | ACs | Notes |
|---|---|---|---|---|
| markdown/extensions/wikilinks.py | WikiLinkExtension.extendMarkdown | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-002-2 | `WIKILINK_RE = r'\[\[([\w0-9_ -]+)(?:\|([\w0-9_ -]+))?\]\]'`. Same character class for label as for target. |
| markdown/extensions/wikilinks.py | WikiLinksInlineProcessor.handleMatch | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2, AC-FR-003-3, AC-FR-004-1, AC-FR-004-2, AC-FR-004-3 | `target = m.group(1).strip()`; if target is empty -> `''` as today. `text = (m.group(2) or '').strip() or target`. `url = build_url(target, base, end)`; `a.text = text`. |
| tests/test_extensions.py | TestWikiLinks | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2, AC-FR-003-3, AC-FR-004-1, AC-FR-004-2, AC-FR-004-3 | New test methods; existing tests for AC-FR-004 stay as they are (`testBasicWikilinks`, `testWikilinkWhitespace`). |
| docs/extensions/wikilinks.md | Syntax section | modify | - | Document `[[Target\|Label]]`. |
| docs/changelog.md | - | modify | - | `### Added` under `## [Unreleased]`: support a display label with `[[Target\|Label]]` in `wikilinks` (#3). Create the `### Added` heading if missing. |

## Interface
No new options. Default settings unless stated; `md = markdown.Markdown(extensions=['wikilinks'])`.

- AC-FR-001-1: `[[Getting Started|read the guide]]` -> `<p><a class="wikilink" href="/Getting_Started/">read the guide</a></p>`
- AC-FR-001-2: `Some text with a [[WikiLink|shown]].` -> `<p>Some text with a <a class="wikilink" href="/WikiLink/">shown</a>.</p>`
- AC-FR-001-3: output for the AC-FR-001-1 input contains neither `[[` nor `|`.
- AC-FR-002-1: `[[Getting Started | read the guide]]` -> `<p><a class="wikilink" href="/Getting_Started/">read the guide</a></p>`
- AC-FR-002-2: `[[  Getting Started  |  read the guide  ]]` output equals the output of `[[Getting Started|read the guide]]`.
- AC-FR-003-1: `WikiLinkExtension(base_url='/wiki/', end_url='.html', html_class='foo')`, input `[[Getting Started|read the guide]]` -> `<p><a class="foo" href="/wiki/Getting_Started.html">read the guide</a></p>`
- AC-FR-003-2: `WikiLinkExtension(html_class='')` -> `<p><a href="/Getting_Started/">read the guide</a></p>`
- AC-FR-003-3: `build_url` callable recording `(label, base, end)` and returning `/bar/`; it is called with `('Getting Started', '/', '/')` and the output is `<p><a class="wikilink" href="/bar/">read the guide</a></p>`.
- AC-FR-004-1: `Some text with a [[WikiLink]].` -> `<p>Some text with a <a class="wikilink" href="/WikiLink/">WikiLink</a>.</p>`
- AC-FR-004-2: `[[ foo bar_baz ]]` -> `<p><a class="wikilink" href="/foo_bar_baz/">foo bar_baz</a></p>`
- AC-FR-004-3: `foo [[ ]] bar` -> `<p>foo  bar</p>`

Edge cases (Q-001..Q-003) are unspecified; the tester should not assert them.

## Test plan
| AC | Test file | Test method (contains the AC id in snake case) | Asserts |
|---|---|---|---|
| AC-FR-001-1 | tests/test_extensions.py | test_ac_fr_001_1_label | exact HTML |
| AC-FR-001-2 | tests/test_extensions.py | test_ac_fr_001_2_label_in_text | exact HTML |
| AC-FR-001-3 | tests/test_extensions.py | test_ac_fr_001_3_no_brackets_or_pipe | `[[` and `\|` not in output |
| AC-FR-002-1 | tests/test_extensions.py | test_ac_fr_002_1_space_around_pipe | exact HTML |
| AC-FR-002-2 | tests/test_extensions.py | test_ac_fr_002_2_extra_space_equal | outputs equal |
| AC-FR-003-1 | tests/test_extensions.py | test_ac_fr_003_1_base_end_class | exact HTML |
| AC-FR-003-2 | tests/test_extensions.py | test_ac_fr_003_2_empty_class | exact HTML |
| AC-FR-003-3 | tests/test_extensions.py | test_ac_fr_003_3_build_url_args | recorded args and HTML |
| AC-FR-004-1 | tests/test_extensions.py | test_ac_fr_004_1_no_pipe | exact HTML |
| AC-FR-004-2 | tests/test_extensions.py | test_ac_fr_004_2_whitespace_no_pipe | exact HTML |
| AC-FR-004-3 | tests/test_extensions.py | test_ac_fr_004_3_blank_removed | exact HTML |

## Architecture fit
Constraint 3 (core never imports extensions) is respected: only `markdown/extensions/wikilinks.py` changes. The extension's own processor stays registered in `inlinepatterns` as `wikilink` at priority 75, and no new extension, entry point or `makeExtension` is needed. The changelog row satisfies the CI rule. The docs note that the extension is in maintenance mode; this change is requested by the issue and is small and backward compatible.

## Risks
- Existing `[[...]]` behaviour: the pipe group is optional, so inputs without `|` match as before. Covered by `testBasicWikilinks`, `testWikilinkWhitespace`, `testSimpleSettings`, `testComplexSettings`, `testWikilinkMetaData` (if present) in `tests/test_extensions.py`.
- Text previously left literal, such as `[[a|b]]`, now becomes a link, which is the intended change.
- The label shares the target's character class, so punctuation in labels (e.g. `[[A|Hello, world]]`) is not recognised and stays literal. This is an accepted limitation (Q-003).


---
## autose check: PASSED
- 5 planned changes; every READY criterion mapped; symbols found
