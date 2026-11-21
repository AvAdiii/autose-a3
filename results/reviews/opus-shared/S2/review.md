## autose independent review: REQUEST CHANGES
<sub>Round 0. Reviewer model `claude-opus-5-5`, variant `shared`. The reviewer saw only the issue, the diff and the repository at the PR head, and could run code but not push.</sub>

The link text is now correct, but the URL is wrong. `handleMatch` passes the label, not the target page name, to `build_url`. So `[[Getting Started|read the guide]]` links to `/read_the_guide/` when it should link to `/Getting_Started/`. That breaks the issue's main requirement that the URL be the same as for `[[Getting Started]]`. The new tests only check the link text, so they don't catch this.

### The reviewer's own acceptance checks (derived from the issue)
| Check | Command | Result |
|---|---|---|
| Plain [[Getting Started]] works as before | `python -c "import markdown; print(markdown.markdown('[[Getting Started]]', extensions=['wikilinks']))"` | pass |
| [[Getting Started/read the guide]] has href /Getting_Started/ and text 'read the guide' | `python -c "import markdown; print(markdown.markdown('[[Getting Started\|read the guide]]', extensions=['wikilinks']))"` | fail |
| Whitespace around the pipe is ignored, and href still points to the target | `python -c "import markdown; print(markdown.markdown('[[Getting Started \| read the guide]]', extensions=['wikilinks']))"` | fail |
| base_url, end_url and html_class apply to the target | `markdown.markdown('[[Getting Started\|read the guide]]', extensions=[WikiLinkExtension(base_url='/wiki/', end_url='.html', html_class='x')])` | fail |
| A custom build_url receives the target | `WikiLinkExtension(build_url=lambda l,b,e: 'URL:'+l)` | fail |
| Full test suite passes | `python -m unittest discover tests` | pass |

### Blocking findings
- **[implementation] The URL is built from the label instead of the target page** (`markdown/extensions/wikilinks.py:77`)
  <details><summary>evidence</summary>

```
`label = (m.group(2) or m.group(1)).strip()` is then passed to `self.config['build_url'](label, base_url, end_url)`. Converting `[[Getting Started|read the guide]]` gives `href="/read_the_guide/"`, but it should be `/Getting_Started/`. A custom build_url also receives 'read the guide'. The fix is to build the URL from `m.group(1).strip()` and use the label only for `a.text`.
```
</details>
- **[testing] The tests check only the link text, not the href** (`tests/test_extensions.py:310`)
  <details><summary>evidence</summary>

```
Both new tests only call `assertIn('>read the guide</a>', html)`, so they pass even though the href is wrong. There should be full-output assertions, e.g. `<p><a class="wikilink" href="/Getting_Started/">read the guide</a></p>`, plus tests with base_url/end_url/html_class and a custom build_url.
```
</details>

### Non-blocking
- The changelog entry is present.
- The label pattern only accepts `[\w0-9_ -]`, so labels with punctuation (e.g. 'Read the guide!') won't match and the brackets stay in the output. That's worth considering, but the issue doesn't require it.
- The new tests are in tests/test_extensions.py instead of tests/test_syntax/extensions/test_wikilinks.py, where the existing wikilinks tests live.

### Routing
Earliest stage named by a blocking finding: **implementation**. Review rounds are used up; a maintainer decides.

Run: https://github.com/AvAdiii/markdown/actions/runs/44896830144