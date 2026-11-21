# Design: attr_list empty attribute list produces invalid `:` attribute

## Summary
The `attr_list` treeprocessor (`AttrListTreeprocessor` in `markdown/extensions/attr_list.py`) builds all its regexes from `BASE_RE`. For `{: }` and `{:}` the optional `\:?` backtracks, so the colon is captured as the attribute text and becomes the bogus `:` attribute. The fix is confined to that extension: change `BASE_RE` so that `{:` followed by spaces and `}` matches with an empty capture group. `assign_attrs` then assigns nothing and the matched text is removed. `{}` without a colon still does not match, so it is unchanged. The prototype was run against all spec inputs and gives the expected output.

## Changes
| File | Symbol | Change | ACs | Notes |
|---|---|---|---|---|
| markdown/extensions/attr_list.py | AttrListTreeprocessor.BASE_RE | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-003-1, AC-FR-003-2, AC-FR-003-3, AC-FR-004-1, AC-FR-004-2 | New value: `r'\{(?:\:[ ]*(?=\})|\:?[ ]*(?=[^\}\n ]))([^\n]*)\}'`. Group 1 may now be empty. HEADER_RE, BLOCK_RE and INLINE_RE derive from it and need no edit. |
| tests/test_syntax/extensions/test_attr_list.py | new test methods in TestAttrList | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-003-1, AC-FR-003-2, AC-FR-003-3, AC-FR-004-1, AC-FR-004-2 | tests |
| docs/changelog.md | - | modify | - | entry under `## [Unreleased]` / `### Fixed` |

## Interface
No new options. Extension name `attr_list`; use `extensions=['attr_list']`.
Exact BASE_RE: `\{(?:\:[ ]*(?=\})|\:?[ ]*(?=[^\}\n ]))([^\n]*)\}` (alternation of `\:[ ]*(?=\})` and `\:?[ ]*(?=[^\}\n ])`).

Input -> output (verified against the prototype):
- AC-FR-001-1: `# Title {: }` -> `<h1>Title</h1>`
- AC-FR-001-2: `# Title {:}` and `# Title {:   }` -> `<h1>Title</h1>`
- AC-FR-001-3: `# Title {: .note }` -> `<h1 class="note">Title</h1>`
- AC-FR-002-1: `Some paragraph\n{:}` -> `<p>Some paragraph</p>`
- AC-FR-002-2: `Some paragraph\n{: }` -> `<p>Some paragraph</p>`
- AC-FR-002-3: `Some paragraph\n{: .note }` -> `<p class="note">Some paragraph</p>`
- AC-FR-003-1: `*hi*{: }` -> `<p><em>hi</em></p>`
- AC-FR-003-2: `*hi*{:}` -> `<p><em>hi</em></p>`
- AC-FR-003-3: `*hi*{: .note }` -> `<p><em class="note">hi</em></p>`
- AC-FR-004-1: `# Title {: #id }` -> `<h1 id="id">Title</h1>`
- AC-FR-004-2: `# Title {: .a .b }` -> `<h1 class="a b">Title</h1>`

Unchanged (regression): `# T {}` -> `<h1>T {}</h1>`; `P\n{}` -> `<p>P\n{}</p>`.

Tests follow the existing style: `self.assertMarkdownRenders(src, expected, extensions=['attr_list'])` in `TestAttrList`.

## Test plan
| AC | Test file | Test method (contains the AC id in snake case) | Asserts |
|---|---|---|---|
| AC-FR-001-1 | tests/test_syntax/extensions/test_attr_list.py | test_ac_fr_001_1_empty_list_heading | `<h1>Title</h1>` |
| AC-FR-001-2 | same | test_ac_fr_001_2_empty_list_no_space_and_many_spaces | both variants give `<h1>Title</h1>` |
| AC-FR-001-3 | same | test_ac_fr_001_3_nonempty_list_heading | class="note" |
| AC-FR-002-1 | same | test_ac_fr_002_1_empty_list_block_no_space | `<p>Some paragraph</p>` |
| AC-FR-002-2 | same | test_ac_fr_002_2_empty_list_block_space | `<p>Some paragraph</p>` |
| AC-FR-002-3 | same | test_ac_fr_002_3_nonempty_list_block | class="note" |
| AC-FR-003-1 | same | test_ac_fr_003_1_empty_list_inline_space | `<p><em>hi</em></p>` |
| AC-FR-003-2 | same | test_ac_fr_003_2_empty_list_inline_no_space | `<p><em>hi</em></p>` |
| AC-FR-003-3 | same | test_ac_fr_003_3_nonempty_list_inline | em class="note" |
| AC-FR-004-1 | same | test_ac_fr_004_1_id_heading | `<h1 id="id">Title</h1>` |
| AC-FR-004-2 | same | test_ac_fr_004_2_multiple_classes_heading | `class="a b"` |

## Architecture fit
The change stays inside the `attr_list` extension (an extension's behaviour changes inside that extension). The treeprocessor and its registry priority are untouched, and no core module imports from `markdown.extensions`. No new extension, so no entry point is needed.

## Risks
- Regex backtracking: the earlier quadratic-time fix (#1656) concerns unclosed lists followed by many spaces. The new `\:[ ]*(?=\})` alternative adds one more linear space scan. The existing test for that case in test_attr_list.py covers it.
- `{}` and other malformed lists must still not match; the tests in test_attr_list.py (`test_empty_attr_list`, `test_curly_after_inline`, `test_curly_after_block`) and tests/test_syntax/extensions/test_legacy_attrs.py cover this.
- The regex is also used for `li`, `dt`, `td` and `th`, so an empty `{:}` is now stripped there too. This is the same consistent behaviour; the spec asks for nothing else in those constructs, so the tester should not assert on them.
- Subclasses or users overriding `BASE_RE` are unaffected, because the group numbering is unchanged.


---
## autose check: PASSED
- 3 planned changes; every READY criterion mapped; symbols found
