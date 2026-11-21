## autose independent review: REQUEST CHANGES
<sub>Round 0. Reviewer model `claude-sonnet-5-5`, variant `isolated`. The reviewer saw only the issue, the diff and the repository at the PR head, and could run code but not push.</sub>

The link URL is built from the label instead of the target. `[[Getting Started|read the guide]]` links to /read_the_guide/, not /Getting_Started/. This is the opposite of what the issue asks for. The PR's tests only check the visible text, so they pass anyway.

### The reviewer's own acceptance checks (derived from the issue)
| Check | Command | Result |
|---|---|---|
| [[Getting Started/read the guide]] has the same href as [[Getting Started]] and shows the label | `python -c "import markdown; print(markdown.markdown('[[Getting Started\|read the guide]]', extensions=['wikilinks']))"` | fail |
| base_url, end_url and html_class apply to the target, not the label | `python -c "import markdown; print(markdown.markdown('[[A b\|c]]', extensions=['wikilinks'], extension_configs={'wikilinks':{'base_url':'/w/','end_url':'.html','` | fail |
| Existing test suite still passes | `python -m unittest discover tests` | pass |

### Blocking findings
- **[implementation] URL is built from the label instead of the target** (`markdown/extensions/wikilinks.py:78`)
  <details><summary>evidence</summary>

```
The PR sets `label = (m.group(2) or m.group(1)).strip()` and then calls `build_url(label, ...)`. The URL is therefore derived from the display text. With `[[Getting Started|read the guide]]` the output was `<a class="wikilink" href="/read_the_guide/">read the guide</a>`. The issue requires the same URL as `[[Getting Started]]`, which is `/Getting_Started/`. A custom `build_url` also receives the label instead of the target.
```
</details>
- **[testing] Tests only check the link text, not the href** (`tests/test_extensions.py:311`)
  <details><summary>evidence</summary>

```
Both new tests use `assertIn('>read the guide</a>', html)`. Neither checks the href, and neither covers `base_url`, `end_url`, a custom `build_url`, or a plain `[[Page]]`. They pass even though the URL is wrong.
```
</details>

### Non-blocking
- The label regex `[\w0-9_ -]+` rejects punctuation, so `[[A|b-c!]]` is left as literal text. Consider allowing wider label characters.
- The changelog entry is present.

### Routing
Earliest stage named by a blocking finding: **implementation**. Review rounds are used up; a maintainer decides.

Run: https://github.com/AvAdiii/markdown/actions/runs/44896933378