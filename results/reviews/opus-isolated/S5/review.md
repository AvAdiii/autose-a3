## autose independent review: REQUEST CHANGES
<sub>Round 0. Reviewer model `claude-opus-5-5`, variant `isolated`. The reviewer saw only the issue, the diff and the repository at the PR head, and could run code but not push.</sub>

The link handling works: external http/https links and autolinks get target="_blank" and rel="noopener noreferrer", while relative links, anchors, mailto links and images are left alone. But the extension can't be loaded the way the issue asks. `extensions=['external_links']` raises ModuleNotFoundError because the PR adds no entry point to pyproject.toml, which breaks ARCHITECTURE.md constraint 4. The PR's tests don't catch this because they pass an `ExternalLinksExtension()` instance instead of the short name.

### The reviewer's own acceptance checks (derived from the issue)
| Check | Command | Result |
|---|---|---|
| Extension loads by short name: extensions=['external_links'] (issue decision 1) | `python -c "import markdown; markdown.markdown('[d](https://e.com)', extensions=['external_links'])"` | fail |
| http/https inline and reference links get target=_blank and rel=noopener noreferrer | `python -c "... markdown.markdown(s, extensions=[ExternalLinksExtension()])" for [d](https://e.com), [h](http://e.com), [r][1] reference` | pass |
| Automatic links <https://...> are marked, including ones with & in the URL | `same probe with '<https://e.com>' and '<http://e.com/a?b=1&c=2>'` | pass |
| mailto links, automail, #anchors and relative links are unchanged | `same probe with '[m](mailto:a@b.c)', '<a@b.c>', '[a](#x)'` | pass |
| Images are unaffected | `same probe with '![i](https://e.com/i.png)'` | pass |
| Default output is unchanged when the extension is not enabled | `python -c "import markdown; print(markdown.markdown('<https://e.com>'))"` | pass |
| Full test suite passes | `python -m unittest discover tests` | pass |

### Blocking findings
- **[implementation] No entry point for external_links, so extensions=['external_links'] fails** (`pyproject.toml:74`)
  <details><summary>evidence</summary>

```
pyproject.toml has no `external_links = 'markdown.extensions.external_links:ExternalLinksExtension'` under [project.entry-points.'markdown.extensions'] (grep for 'external' finds nothing). Running `markdown.markdown('[d](https://e.com)', extensions=['external_links'])` raises `ModuleNotFoundError: No module named 'external_links'`. The issue requires loading by this name, and ARCHITECTURE.md constraint 4 says every built-in extension needs an entry point.
```
</details>
- **[testing] Tests use the extension class directly, so loading by name is never tested** (`tests/test_syntax/extensions/test_external_links.py:12`)
  <details><summary>evidence</summary>

```
Both tests pass `extensions=[ExternalLinksExtension()]`, which is why they pass even though the short name is broken. The tests also don't cover autolinks (`<https://...>`), mailto links, #anchors or images, all of which the maintainer's decisions list explicitly.
```
</details>

### Non-blocking
- The tree processor's priority of 3 fits: it runs after inline (20) and prettify (10) and before unescape (0), and the generated hrefs are already available at that point.
- makeExtension has `# pragma: no cover`. Once tests load the extension by string name, that path is exercised, so the pragma can come off.
- Consider adding a docs page under docs/extensions/ and listing the extension in the docs index the way the other built-in extensions are.
- The changelog entry is present.

### Routing
Earliest stage named by a blocking finding: **implementation**. Review rounds are used up; a maintainer decides.

Run: https://github.com/AvAdiii/markdown/actions/runs/44890867863