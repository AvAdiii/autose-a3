# Design: WikiLinks display label with `[[Target|Label]]`

## Summary
The change lives entirely in the `wikilinks` extension (component 7 in ARCHITECTURE.md). `WikiLinkExtension.extendMarkdown` gets a regex with an optional `|label` group, and `WikiLinksInlineProcessor.handleMatch` uses the target for `build_url` and the label (when present) as the link text. Everything else (`_getMeta`, `base_url`, `end_url`, `html_class`, `build_url`) is untouched, so FR-003 holds by construction. The label uses the same character class as the target (`[\w0-9_ -]`), which is the smallest choice and leaves the BLOCKED edge cases (FR-005, Q-001..Q-003) unspecified and untested. Text is set via `a.text`, so it is escaped like today (ASM-001). No core module changes, no new extension.

## Changes
| File | Symbol | Change | ACs | Notes |
|---|---|---|---|---|
| markdown/extensions/wikilinks.py | WikiLinkExtension.extendMarkdown | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-002-2, AC-FR-004-1, AC-FR-004-2 | `WIKILINK_RE = r'\[\[([\w0-9_ -]+?)(?:[ ]*\|[ ]*([\w0-9_ -]+))?\]\]'`; group 1 = target, group 2 = label (optional). Must not change matching for pipe-less input. |
| markdown/extensions/wikilinks.py | WikiLinksInlineProcessor.handleMatch | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2, AC-FR-003-3, AC-FR-004-1, AC-FR-004-2 | `target = m.group(1).strip()`; if empty return `''` as today; `url = build_url(target, ...)`; `a.text = (m.group(2) or '').strip() or target`. |
| tests/test_syntax/extensions/test_wikilinks.py | new TestWikiLinks | add | all READY ACs | new file, `TestCase` from `markdown.test_tools`, `default_kwargs = {'extensions': ['wikilinks']}` |
| docs/extensions/wikilinks.md | - | modify | - | document `[[Target\|Label]]` syntax |
| docs/changelog.md | - | modify | - | entry under `## [Unreleased]` -> `### Added` (add the heading before `### Fixed` if absent): "Support `[[Target\|Label]]` display labels in the `wikilinks` extension." |

## Interface
No new options. Syntax `[[Target|Label]]`; optional whitespace around `|`; target and label restricted to letters, digits, `_`, space, `-`. Default config unless stated.

- AC-FR-001-1: `[[Getting Started|read the guide]]` -> `<p><a class="wikilink" href="/Getting_Started/">read the guide</a></p>`
- AC-FR-001-2: href of the above equals href of `[[Getting Started]]` (`/Getting_Started/`).
- AC-FR-001-3: output of AC-FR-001-1 contains none of `[[`, `]]`, `|`.
- AC-FR-002-1: `[[Getting Started | read the guide]]` -> `<p><a class="wikilink" href="/Getting_Started/">read the guide</a></p>`
- AC-FR-002-2: `[[Getting Started|  read the guide  ]]` output equals that of `[[Getting Started|read the guide]]`.
- AC-FR-003-1: `base_url='/wiki/'`, `end_url='.html'`, `html_class='myclass'`, `[[Getting Started|read the guide]]` -> `<p><a class="myclass" href="/wiki/Getting_Started.html">read the guide</a></p>`
- AC-FR-003-2: `html_class=''` -> `<p><a href="/Getting_Started/">read the guide</a></p>`
- AC-FR-003-3: `build_url=fn` where `fn(label, base, end)` records `label` and returns e.g. `'/custom/'`; recorded value is `Getting Started`, output `<p><a class="wikilink" href="/custom/">read the guide</a></p>`.
- AC-FR-004-1: `[[Getting Started]]` -> `<p><a class="wikilink" href="/Getting_Started/">Getting Started</a></p>`
- AC-FR-004-2: `[[ ]]` -> `<p></p>`

Extension kwargs are passed as `extensions=[WikiLinkExtension(...)]` or `extension_configs={'wikilinks': {...}}`.

## Test plan
| AC | Test file | Test method | Asserts |
|---|---|---|---|
| AC-FR-001-1 | tests/test_syntax/extensions/test_wikilinks.py | test_ac_fr_001_1_label | exact HTML |
| AC-FR-001-2 | same | test_ac_fr_001_2_same_href | hrefs equal |
| AC-FR-001-3 | same | test_ac_fr_001_3_no_syntax_left | no `[[`, `]]`, `\|` |
| AC-FR-002-1 | same | test_ac_fr_002_1_spaces_around_pipe | exact HTML |
| AC-FR-002-2 | same | test_ac_fr_002_2_label_padding | outputs equal |
| AC-FR-003-1 | same | test_ac_fr_003_1_options | exact HTML |
| AC-FR-003-2 | same | test_ac_fr_003_2_empty_class | exact HTML |
| AC-FR-003-3 | same | test_ac_fr_003_3_custom_build_url | recorded arg and href |
| AC-FR-004-1 | same | test_ac_fr_004_1_unlabelled | exact HTML |
| AC-FR-004-2 | same | test_ac_fr_004_2_blank_wikilink | `<p></p>` |

## Architecture fit
Constraint 3 (core never imports extensions) is respected: only `markdown/extensions/wikilinks.py` changes. The processor stays registered as `wikilink` at priority 75 in `inlinepatterns`; no new extension, so constraints 1 and 4 are not triggered. The changelog row satisfies the CI rule.

## Risks
- The regex change could alter matching of pipe-less input; the lazy `+?` with optional group still yields the same group 1 after `.strip()`. Covered by AC-FR-004 tests plus `tests/test_extensions.py` (`TestWikiLinks`) and `tests/test_legacy.py`.
- Meta-driven `wiki_base_url` etc. use `_getMeta`, unchanged.
- Inputs like `[[A|B|C]]`, `[[Page|]]`, `[[Page|Hello, world!]]` stay literal; intentionally untested (BLOCKED).


---
## autose check: PASSED
- 5 planned changes; every READY criterion mapped; symbols found
