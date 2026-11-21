## autose independent review: APPROVE
<sub>Round 0. Reviewer model `claude-opus-5-5`, variant `shared`. The reviewer saw only the issue, the diff and the repository at the PR head, and could run code but not push.</sub>

The fix is minimal and in the right place, in the non-Pygments branch of FencedBlockPreprocessor.run: only string values are written as <code> attributes. Every case in the issue (bare linenums, linenums="true"/"false"/1, guess_lang, noclasses) now renders a plain code block. In a copy with the fix reverted, those same inputs raise the reported TypeErrors and the 3 new tests fail, so the tests do exercise the change. Other attributes (data-x, bare non-bool flags) are kept. Output without attr_list or with codehilite is unchanged. The full suite passes (1169 tests, 52 skipped), flake8 is clean, and a changelog entry is present. One side effect: the old `hl_lines="[1, 2]"` repr output is now dropped. That is acceptable but not mentioned in the changelog, so I've left it as a note.

### The reviewer's own acceptance checks (derived from the issue)
| Check | Command | Result |
|---|---|---|
| Issue reproducer: '``` { .python linenums }' with fenced_code+attr_list renders a plain code block instead of raising TypeError | `python $TMPDIR/p.py (probe over cases × extension sets, head)` | pass |
| linenums="true", linenums="false", linenums=1, guess_lang, noclasses all render without raising | `python $TMPDIR/p.py` | pass |
| Base (fix reverted in a copy) reproduces the issue, so the probe and new tests exercise the change | `cd $TMPDIR/base && PYTHONPATH=$TMPDIR/base python $TMPDIR/p.py \| grep attr_list; python -m unittest tests...TestFencedCodeBoolOptionsWithoutCodehilite` | pass |
| Other attributes still emitted: data-x="1", bare non-bool flag foo -> foo="foo", use_pygments=false with data-y kept | `python $TMPDIR/p.py` | pass |
| Without attr_list and with codehilite (no Pygments installed), output unchanged vs base | `diff of probe outputs for fenced_code-only and codehilite columns, head vs reverted copy` | pass |
| Full test suite and flake8 | `python -m unittest discover tests; flake8 markdown/extensions/fenced_code.py tests/test_syntax/extensions/test_fenced_code.py` | pass |

### Non-blocking
- Side effect outside the issue: `hl_lines` (parsed to a list) was emitted as `hl_lines="[1, 2]"` (a Python repr) at base and is now dropped, both inside attr braces and in the legacy ```python hl_lines="1" form. This is arguably an improvement and no test pins the old output, but the changelog only mentions boolean options. Consider mentioning `hl_lines` in the changelog too.
- docs/extensions/fenced_code_blocks.md 'Key/Value Pairs' section says key/value pairs are assigned as attributes when highlighting is off. A sentence noting that Pygments-only options (linenums, hl_lines, ...) are omitted would keep the docs accurate.
- With codehilite enabled, bare `linenums` parses to None (because of preserve_none), so it doesn't turn on line numbers while `linenums="true"` does. That behaviour existed before this PR and is out of scope.
- Pygments isn't installed in this environment, so the codehilite path was only checked in its no-Pygments fallback mode.

### Routing
Approved. A maintainer decides whether to merge.

Run: https://github.com/AvAdiii/markdown/actions/runs/44896854333