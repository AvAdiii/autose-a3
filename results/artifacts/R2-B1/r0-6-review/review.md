## autose independent review: APPROVE
<sub>Round 0. Reviewer model `claude-opus-5-5`, variant `isolated`. The reviewer saw only the issue, the diff and the repository at the PR head, and could run code but not push.</sub>

The fix is correct and small. When fenced_code and attr_list are used without codehilite, the code that writes key/value attributes now skips all the highlighter-only boolean options instead of only `use_pygments`. Before, these options were parsed into a bool or None, which crashed the output. Every variant from the issue now renders a plain code block. Other attributes such as data-x are still output, the codehilite path is unchanged, the full suite passes (1174 tests), and the changelog has an entry. Nothing blocks the merge. A small docs update would be nice.

### The reviewer's own acceptance checks (derived from the issue)
| Check | Command | Result |
|---|---|---|
| `linenums` as a flag on its own (from the issue) renders a plain code block with no TypeError | `python - <<EOF ... markdown.markdown('``` { .python linenums }\nprint(1)\n```', extensions=['fenced_code','attr_list'])` | pass |
| linenums="true"/"false"/"foo", guess_lang and noclasses="true" do not crash | `same probe script looping over the attribute variants` | pass |
| Other key/value attributes are still output, including when mixed with linenums (this case is not in the PR's tests) | `probe with 'data-x="1"' and 'linenums data-x="1"'` | pass |
| With codehilite enabled, highlighting still works; with codehilite use_pygments=False, it still renders; fenced_code without attr_list is unchanged | `probe with extensions=['fenced_code','attr_list','codehilite'], with extension_configs use_pygments False, and with ['fenced_code'] alone` | pass |
| The full test suite passes | `python -m unittest discover tests` | pass |
| flake8 passes on the changed module | `python -m flake8 markdown/extensions/fenced_code.py` | pass |

### Non-blocking
- The fix leaves out every key in `bool_options` (linenums, guess_lang, noclasses, use_pygments) from the `<code>` attributes when highlighting is off. Before this change, any value for these keys passed through parseBoolValue and became a bool or None, which made the output crash. So no output that used to render has changed.
- docs/extensions/fenced_code_blocks.md (around lines 202-216 and 254-259) still says that only `use_pygments` is left out of the output. Consider adding a sentence that linenums, guess_lang and noclasses are also dropped when highlighting is off.
- There is a separate problem outside this issue's scope: `hl_lines="1"` without codehilite outputs `hl_lines="[1]"` because the parsed list gets serialized. It behaved the same way before this PR.
- test_ac_fr_004_* (with codehilite) pass with or without the fix. They are fine as regression guards. The tests for linenums, guess_lang and noclasses without codehilite would crash without the fix, so they do test the change.
- The test names (`test_ac_fr_...`) come from the pipeline and don't follow the descriptive names used elsewhere in the file. This is cosmetic only.

### Routing
Approved. A maintainer decides whether to merge.

Run: https://github.com/AvAdiii/markdown/actions/runs/44890133094