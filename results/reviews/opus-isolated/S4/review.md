## autose independent review: APPROVE
<sub>Round 0. Reviewer model `claude-opus-5-5`, variant `isolated`. The reviewer saw only the issue, the diff and the repository at the PR head, and could run code but not push.</sub>

The fix is a small, targeted change. In the branch without codehilite, `fenced_code` now emits only string-valued config entries as attributes, so boolean or None values from Pygments options (`linenums`, `guess_lang`, `noclasses`, also `linenums="false"`) no longer make serialization raise TypeError. String attributes such as data-x and linenostart are still emitted, and output with codehilite enabled is unchanged. The new tests fail with TypeError when the fix is removed and pass with it, and the full suite passes. There is a changelog entry. I found no blocking problems.

### The reviewer's own acceptance checks (derived from the issue)
| Check | Command | Result |
|---|---|---|
| Issue repro: bare `linenums` with fenced_code + attr_list (no codehilite) renders a plain code block with no TypeError | `python $TMPDIR/p.py (markdown.markdown('``` { .python linenums }\nprint(1)\n```', extensions=['fenced_code','attr_list']))` | pass |
| `linenums="true"`, `guess_lang` and `noclasses` without codehilite do not crash | `python $TMPDIR/p.py` | pass |
| Other string key/value attributes (data-x, linenostart) are still emitted | `python $TMPDIR/p.py` | pass |
| Output with codehilite enabled is unchanged, including codehilite with use_pygments=False | `python $TMPDIR/p.py` | pass |
| Full test suite passes | `python -m unittest discover tests` | pass |
| New tests fail without the fix (copy of the package with `and isinstance(v, str)` removed) | `cd $TMPDIR/rv && python -m unittest tests.test_syntax.extensions.test_fenced_code.TestFencedCodeBoolOptionsWithoutCodehilite` | pass |
| Edge case not covered by the PR's tests: linenums="false" (bool False) also crashed before the fix and works after it | `reverted copy vs HEAD probe for '``` { .python linenums="false" }'` | pass |

### Non-blocking
- Side effect outside the issue's scope: without codehilite, `hl_lines="1 2"` used to produce the attribute `hl_lines="[1, 2]"` (a stringified Python list) and is now dropped. The filter drops any value that isn't a string, so this follows from it. The new behaviour is arguably better, but neither the changelog nor a test mentions it.
- Changelog: the new entry is followed by a blank line before the existing bullets, so this section's list is split in two. This is cosmetic.
- Pygments is not installed in this environment, so codehilite ran without Pygments. The code path with codehilite enabled is unchanged by the diff anyway.
- I could not compare against the base commit through git because the hook blocks it. Instead I made a copy of the package with the one-line filter removed and used it as the baseline.

### Routing
Approved. A maintainer decides whether to merge.

Run: https://github.com/AvAdiii/markdown/actions/runs/44890851656