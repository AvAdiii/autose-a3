## autose independent review: APPROVE
<sub>Round 0. Reviewer model `claude-sonnet-5-5`, variant `isolated`. The reviewer saw only the issue, the diff and the repository at the PR head, and could run code but not push.</sub>

The PR adds `[[Target|Label]]` support to wikilinks. The link text changes and the URL is still built from the target. Whitespace around the pipe is ignored, and `[[Page]]` behaves as before. The full suite passes and my own probes behaved as the issue asks.

### The reviewer's own acceptance checks (derived from the issue)
| Check | Command | Result |
|---|---|---|
| Full test suite passes | `python -m unittest discover tests` | pass |
| [[Target/Label]] gives the label as text and the target's URL | `markdown.markdown('[[Getting Started\|read the guide]]', extensions=['wikilinks'])` | pass |
| Whitespace around the pipe does not matter | `markdown.markdown('[[Getting Started \| read the guide]]', extensions=['wikilinks'])` | pass |
| base_url, end_url and html_class still apply to labelled links | `markdown.markdown('[[A b\|c]]', extensions=[WikiLinkExtension(base_url='/w/', end_url='.html', html_class='x')])` | pass |
| Edge cases outside the PR's tests: empty label, extra pipes, mixed labelled and plain links, non-ASCII label | `probes for [[A\|]], [[A\|B\|C]], '[[A\|b]] and [[C]]', [[A\|é]]` | pass |

### Non-blocking
- A label containing characters outside the target charset, such as `.` or `*`, is not recognised and stays literal text (`[[A|b.c]]`). The docs say the label accepts the same characters as the target, so this is consistent with the documented behaviour.
- `[[A|]]` with an empty label stays literal rather than falling back to the target text. This is a reasonable choice, and the issue does not cover it.
- The `docs/changelog.md` entry is present, and the docs page was updated.

### Routing
Approved. A maintainer decides whether to merge.

Run: https://github.com/AvAdiii/markdown/actions/runs/45405624215