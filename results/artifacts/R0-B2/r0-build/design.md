# Design: attr_list empty attribute list produces no attribute

## Summary
`AttrListTreeprocessor.BASE_RE` is `\{\:?[ ]*([^\}\n ][^\n]*)\}`. For `{: }` and `{:}` the optional colon backtracks and the group captures `:`, so `get_attrs_and_remainder(':')` yields a bogus `:` attribute (`<h1 :>`). The fix stays inside the `attr_list` extension (Treeprocessor, ARCHITECTURE.md): `BASE_RE` gets a first alternative that matches `{:` + spaces + `}` as an explicit empty list (no capture), and the existing call sites treat a `None` group as an empty attribute string, so `assign_attrs` assigns nothing and the matched text is stripped exactly as for a non-empty list. `{ }` (no colon) still fails to match, as before. Note: I could not run probes (the sandbox was unavailable), so the regex reasoning comes from reading the code; the implementer should verify the Interface outputs.

## Changes
| File | Symbol | Change | ACs | Notes |
|---|---|---|---|---|
| markdown/extensions/attr_list.py | AttrListTreeprocessor.BASE_RE | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2, AC-FR-004-1, AC-FR-004-2, AC-FR-004-3, AC-FR-005-1 | New pattern: `\{(?:\:[ ]*\}|\:?[ ]*([^\}\n ][^\n]*)\})`. The empty alternative is tried first, so `{: }`/`{:}` never reach the group that captured `:`. HEADER_RE/BLOCK_RE/INLINE_RE are built from it unchanged. Group 1 is `None` for an empty list. |
| markdown/extensions/attr_list.py | AttrListTreeprocessor.run | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2 | Every `m.group(1)` passed to `assign_attrs` becomes `m.group(1) or ''` (7 call sites). |
| markdown/extensions/attr_list.py | AttrListTreeprocessor.assign_attrs | modify | AC-FR-001-1, AC-FR-002-1, AC-FR-003-1 | Make sure an empty `attrs_string` returns `''` with no attributes (check `get_attrs_and_remainder('')` returns `([], '')`; add an early return if not). |
| tests/test_syntax/extensions/test_attr_list.py | new test methods in existing attr_list test class | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2, AC-FR-004-1, AC-FR-004-2, AC-FR-004-3, AC-FR-005-1 | One method per AC |
| docs/changelog.md | - | modify | - | Entry under `## [Unreleased]` / `### Fixed` |

## Interface
No new options or API. With `extensions=['attr_list']` (`self.assertMarkdownRenders(src, html, extensions=['attr_list'])`):

| AC | Input | Output |
|---|---|---|
| AC-FR-001-1 | `# Title {: }` | `<h1>Title</h1>` |
| AC-FR-001-2 | `# Title {:}` | `<h1>Title</h1>` |
| AC-FR-002-1 | `Some paragraph\n{:}` | `<p>Some paragraph</p>` |
| AC-FR-002-2 | `Some paragraph\n{: }` | `<p>Some paragraph</p>` |
| AC-FR-003-1 | `*hi*{: }` | `<p><em>hi</em></p>` |
| AC-FR-003-2 | `*hi*{:}` | `<p><em>hi</em></p>` |
| AC-FR-004-1 | `# Title {: .note }` | `<h1 class="note">Title</h1>` |
| AC-FR-004-2 | `*hi*{: #a .b }` | `<p><em class="b" id="a">hi</em></p>` |
| AC-FR-004-3 | `Some paragraph\n{: .note }` | `<p class="note">Some paragraph</p>` |
| AC-FR-005-1 | `# Title { }` | `<h1>Title { }</h1>` |

Any number of spaces between `{:` and `}` is empty (ASM-001).

## Test plan
| AC | Test file | Test method | Asserts |
|---|---|---|---|
| AC-FR-001-1 | tests/test_syntax/extensions/test_attr_list.py | test_ac_fr_001_1_empty_list_header_space | exact HTML above |
| AC-FR-001-2 | same | test_ac_fr_001_2_empty_list_header_no_space | exact HTML |
| AC-FR-002-1 | same | test_ac_fr_002_1_empty_list_block_no_space | exact HTML |
| AC-FR-002-2 | same | test_ac_fr_002_2_empty_list_block_space | exact HTML |
| AC-FR-003-1 | same | test_ac_fr_003_1_empty_list_inline_space | exact HTML |
| AC-FR-003-2 | same | test_ac_fr_003_2_empty_list_inline_no_space | exact HTML |
| AC-FR-004-1 | same | test_ac_fr_004_1_nonempty_header | exact HTML |
| AC-FR-004-2 | same | test_ac_fr_004_2_nonempty_inline | exact HTML |
| AC-FR-004-3 | same | test_ac_fr_004_3_nonempty_block | exact HTML |
| AC-FR-005-1 | same | test_ac_fr_005_1_braces_without_colon_unchanged | exact HTML |

## Architecture fit
The change is confined to the `attr_list` extension's Treeprocessor; no core module imports from `markdown.extensions` and no new extension, registry entry or entry point is needed. The treeprocessor priority (8) and registration are untouched.

## Risks
- `{: } text }` on one line: the empty alternative now matches the first `}` instead of the greedy last one. This is an obscure edge case.
- Non-empty lists use the unchanged second alternative, so existing tests in tests/test_syntax/extensions/test_attr_list.py and the legacy attr_list tests in tests/test_extensions.py cover regressions, including the `#1656` backtracking fix (the new alternative has no nested quantifiers beyond `[ ]*`).


---
## autose check: PASSED
- 5 planned changes; every READY criterion mapped; symbols found
