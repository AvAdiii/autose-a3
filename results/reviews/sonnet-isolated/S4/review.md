## autose independent review: APPROVE
<sub>Round 0. Reviewer model `claude-sonnet-5-5`, variant `isolated`. The reviewer saw only the issue, the diff and the repository at the PR head, and could run code but not push.</sub>

The fix is correct and minimal. With fenced_code and attr_list but no codehilite, non-string Pygments options such as linenums are now left out of the output. Other attributes still render. The full suite passes.

### The reviewer's own acceptance checks (derived from the issue)
| Check | Command | Result |
|---|---|---|
| The issue's example no longer crashes and renders a plain code block | `markdown.markdown('``` { .python linenums }\nx\n```', extensions=['fenced_code','attr_list'])` | pass |
| Other attributes are kept alongside bool options (data-x with linenums="true") | `same call with { .python data-x="1" linenums="true" }` | pass |
| hl_lines, both inside attrs and in the legacy form outside them, does not crash without codehilite | `two probes: { .python hl_lines="1" } and ```python hl_lines="1 2"` | pass |
| Valueless non-bool attributes and a string value of "0" are still output, so existing behaviour is unchanged | `probes with data-n="0" title="a" and a bare data-n` | pass |
| Full test suite | `python -m unittest discover tests` | pass |

### Non-blocking
- The isinstance(v, str) filter also drops the list value of hl_lines without codehilite. Before the change this would have crashed, so dropping it is consistent with the fix.
- The changelog entry has no issue number. The existing entries do.
- The new tests cover the bare flag, explicit bool values, use_pygments="false" and a mix with another attribute. They do not cover hl_lines without codehilite.

### Routing
Approved. A maintainer decides whether to merge.

Run: https://github.com/AvAdiii/markdown/actions/runs/44896965636