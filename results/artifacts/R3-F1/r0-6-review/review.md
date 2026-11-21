## autose independent review: APPROVE
<sub>Round 0. Reviewer model `claude-opus-5-5`, variant `isolated`. The reviewer saw only the issue, the diff and the repository at the PR head, and could run code but not push.</sub>

The PR does what the issue asks. `[[Target|Label]]` links to the same URL as `[[Target]]` and shows the label. Whitespace around the pipe is ignored. The base_url, end_url, html_class, build_url and meta settings behave as before, and links without a pipe are unchanged. I checked each of these by running code, including edge cases the PR's tests don't cover. The new tests fail when the fix is reverted, the full suite passes and flake8 is clean. The changelog and docs are updated.

### The reviewer's own acceptance checks (derived from the issue)
| Check | Command | Result |
|---|---|---|
| [[Getting Started/read the guide]] links to /Getting_Started/ with text 'read the guide' | `python -c "import markdown; print(markdown.markdown('[[Getting Started\|read the guide]]', extensions=['wikilinks']))"` | pass |
| Whitespace around the pipe is ignored | `markdown('[[Getting Started \| read the guide]]', extensions=['wikilinks'])` | pass |
| base_url/end_url/html_class settings and meta wiki_base_url still apply to labelled links | `markdown(..., extensions=[WikiLinkExtension(base_url='/wiki/',end_url='.html',html_class='c')]); and with meta 'wiki_base_url: /m/'` | pass |
| [[Page]] without a pipe and blank/padded targets behave as before | `markdown('[[Getting Started]]'), markdown('[[ Page ]]'), markdown('[[Getting   Started\|x]]')` | pass |
| Edge cases not covered by the PR's tests: empty label, empty target, multiple pipes, several links on one line, nested in emphasis | `markdown of '[[Page\|]]','[[\|Label]]','[[a\|b\|c]]','*[[Page\|lab]]*','[[A\|b]] and [[Other]]'` | pass |
| New tests fail if the fix is reverted (in a copy of the repo with the regex and label line restored to their base versions) | `cd $TMPDIR/base && python -m unittest tests.test_syntax.extensions.test_wikilinks` | pass |
| Full suite and flake8 | `python -m unittest discover tests; python -m flake8 markdown/extensions/wikilinks.py tests/test_syntax/extensions/test_wikilinks.py` | pass |

### Non-blocking
- Labels only accept the same characters as targets ([\w0-9_ -]), so `[[Page|it's]]` or a label with punctuation is left as literal text. This is documented in docs/extensions/wikilinks.md and the issue's examples don't need more. A later change could allow a wider set of characters in labels.
- Inside a `tables` row, `[[P|l]]` is split at the pipe into two cells. That is how table parsing already works (block level runs before inline), not a regression, but the docs could mention it.
- `[[ | x]]` renders as an empty paragraph, the same as the existing blank-target behaviour for `[[ ]]`.
- The test names (test_ac_fr_001_1_...) come from the pipeline's requirement IDs and don't say what each test checks, but this is only cosmetic.
- Changelog entry is present under Unreleased > Added. No ARCHITECTURE.md constraints are touched: the change stays inside the extension and the processor priority is unchanged.

### Routing
Approved. A maintainer decides whether to merge.

Run: https://github.com/AvAdiii/markdown/actions/runs/44890136597