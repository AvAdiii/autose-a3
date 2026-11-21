## autose independent review: REQUEST CHANGES
<sub>Round 0. Reviewer model `claude-opus-5-5`, variant `isolated`. The reviewer saw only the issue, the diff and the repository at the PR head, and could run code but not push.</sub>

The regex now matches `[[Target|Label]]` and the label is shown as link text. But the PR builds the URL from the label, not the target. `[[Getting Started|read the guide]]` links to `/read_the_guide/` when it should link to `/Getting_Started/`. That breaks the issue's main requirement: same URL as `[[Getting Started]]`, only the visible text changes. A custom `build_url` also receives the label instead of the target. The PR's tests only check the visible text, so they don't catch this.

### The reviewer's own acceptance checks (derived from the issue)
| Check | Command | Result |
|---|---|---|
| [[Getting Started/read the guide]] links to /Getting_Started/ with text 'read the guide' | `python -c "import markdown; print(markdown.markdown('[[Getting Started\|read the guide]]', extensions=['wikilinks']))"` | fail |
| Whitespace around the pipe is ignored and the URL is still built from the target | `python -c "... '[[Getting Started \| read the guide]]' ..."` | fail |
| A custom build_url, base_url, end_url and html_class get the target, not the label | `python -c "... WikiLinkExtension(base_url='/wiki/', end_url='.html', html_class='wl', build_url=lambda l,b,e: 'X:'+l) ..."` | fail |
| [[Page]] without a pipe is unchanged | `python -c "... '[[Page]]', '[[Getting Started]]' ..."` | pass |
| Full test suite passes | `python -m unittest discover tests` | pass |

### Blocking findings
- **[implementation] The URL is built from the display label instead of the target page** (`markdown/extensions/wikilinks.py:78`)
  <details><summary>evidence</summary>

```
`label = (m.group(2) or m.group(1)).strip()` is then passed to `self.config['build_url'](label, base_url, end_url)`. Running markdown.markdown('[[Getting Started|read the guide]]', extensions=['wikilinks']) gives href="/read_the_guide/" but should give "/Getting_Started/". The target (group 1) has to go to build_url, and only a.text should use group 2.
```
</details>
- **[testing] The tests never check href, so they miss the wrong URL** (`tests/test_extensions.py:310`)
  <details><summary>evidence</summary>

```
Both tests only do assertIn('>read the guide</a>', html). They pass even though the href is wrong. They should compare the full output, e.g. '<p><a class="wikilink" href="/Getting_Started/">read the guide</a></p>', and also cover base_url/end_url/html_class/build_url with a label.
```
</details>

### Non-blocking
- The changelog entry is present.
- docs/extensions/wikilinks.md is not updated to describe the new `[[Target|Label]]` syntax. This is worth adding but does not block the PR.
- The label character class `[\w0-9_ -]` is narrow: labels with punctuation such as `[[Page|Read this!]]` won't match. This does not block the PR, but consider allowing a wider label set.

### Routing
Earliest stage named by a blocking finding: **implementation**. Review rounds are used up; a maintainer decides.

Run: https://github.com/AvAdiii/markdown/actions/runs/44890825281