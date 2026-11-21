# Design: Fenced code with `linenums`/`guess_lang`/`noclasses` must not crash without codehilite

## Summary
`FencedBlockPreprocessor.handle_attrs` converts `linenums`, `guess_lang`, `noclasses` (and `use_pygments`) to `bool`/`None` via `parseBoolValue`. In the non-highlighting branch of `FencedBlockPreprocessor.run`, every config item except `use_pygments` is passed to `_escape_attrib_html`, which raises `TypeError` for a bool/None. The fix stays inside the `fenced_code` extension (ARCHITECTURE.md: extension behaviour changes within the extension): when building `kv_pairs`, skip every key in `self.bool_options` (the highlighter-only options), not just `use_pygments`. These attributes are therefore omitted from the HTML (this matches Q-001 option (a), but FR-002 is BLOCKED and the output form is not a contract; tests only assert the READY criteria). Other attributes (`data-x`, `data-test`) are unchanged. The codehilite path is untouched.

## Changes
| File | Symbol | Change | ACs | Notes |
|---|---|---|---|---|
| markdown/extensions/fenced_code.py | FencedBlockPreprocessor.run | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-003-1, AC-FR-003-2 | In the `kv_pairs` generator replace `if k != 'use_pygments'` with `if k not in self.bool_options`. Update the comment. |
| tests/test_syntax/extensions/test_fenced_code.py | new TestFencedCodeWithoutCodehilite | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-003-1, AC-FR-003-2, AC-FR-004-1, AC-FR-004-2 | New tests; use existing test style (`TestCase.assertMarkdownRenders`) or `markdown.markdown` directly. |
| docs/changelog.md | - | modify | - | Entry under `## [Unreleased]` / `### Fixed`. |

## Interface
No new options or signatures. Extensions: `['fenced_code', 'attr_list']` unless stated.

- AC-FR-001-1: "``` { .python linenums }\nprint(1)\n```" -> no exception; output contains `<pre><code class="language-python"` and `print(1)`.
- AC-FR-001-2: same with `linenums="true"` -> same assertions.
- AC-FR-001-3: each of `guess_lang`, `guess_lang="true"`, `guess_lang="false"`, `noclasses`, `noclasses="true"`, `noclasses="false"` (source "``` { .python X }\nprint(1)\n```") -> no exception; output contains `<pre><code class="language-python"` and `print(1)`.
- AC-FR-001-4: "``` { .python }\nprint(1)\n```" -> exactly `<pre><code class="language-python">print(1)\n</code></pre>` (unchanged today).
- AC-FR-003-1: "``` { .python data-x=\"1\" }\nprint(1)\n```" -> exactly `<pre><code class="language-python" data-x="1">print(1)\n</code></pre>` (unchanged today).
- AC-FR-003-2: "``` { data-test=\"{}\" }\n# Some python code\n```" -> exactly `<pre><code data-test="{}"># Some python code\n</code></pre>` (unchanged today).
- AC-FR-004-1: extensions `fenced_code`, `attr_list`, `codehilite`; "``` { .python linenums=\"true\" }\nprint(1)\n```" -> no exception; output contains `codehilite`.
- AC-FR-004-2: same extensions; "``` { .python linenums=True }\n# Some python code\n```" -> no exception; output contains `codehilite` and `# Some python code`.
  (Pygments may split tokens into spans; the tester should run the base to confirm the `# Some python code` substring appears, else compare against whatever the base gives for the comment text, e.g. check for `Some python code`. AC-FR-004 passes today, so it is a regression guard.)

Do not assert the output form of the omitted attributes (FR-002 blocked).

## Test plan
| AC | Test file | Test method (contains the AC id in snake case) | Asserts |
|---|---|---|---|
| AC-FR-001-1 | tests/test_syntax/extensions/test_fenced_code.py | test_ac_fr_001_1_linenums_flag | no exception; contains `<pre><code class="language-python"` and `print(1)` |
| AC-FR-001-2 | same | test_ac_fr_001_2_linenums_value | same |
| AC-FR-001-3 | same | test_ac_fr_001_3_guess_lang_noclasses | loops over six sources; same assertions |
| AC-FR-001-4 | same | test_ac_fr_001_4_plain_python | exact output |
| AC-FR-003-1 | same | test_ac_fr_003_1_data_attr | exact output |
| AC-FR-003-2 | same | test_ac_fr_003_2_data_test_braces | exact output |
| AC-FR-004-1 | same | test_ac_fr_004_1_codehilite_linenums | contains `codehilite` |
| AC-FR-004-2 | same | test_ac_fr_004_2_codehilite_linenums_true | contains `codehilite` and `# Some python code` |

## Architecture fit
Change is confined to `markdown/extensions/fenced_code.py`; no core module imports from extensions (constraint 3); no new extension, so constraints 1 and 4 are not triggered; no new per-document state (constraint 5). Changelog row added for CI.

## Risks
- `use_pygments` handling is preserved because it is a member of `bool_options`.
- Behaviour for users who relied on a (crashing) path is nil; no previously working output changes, since bool/None values always raised.
- Existing tests in `tests/test_syntax/extensions/test_fenced_code.py` (attr_list and codehilite cases) cover regressions.
- `hl_lines` (a list) without codehilite may have its own issue; out of scope.


---
## autose check: PASSED
- 3 planned changes; every READY criterion mapped; symbols found
