## autose independent review: REQUEST CHANGES
<sub>Round 0. Reviewer model `claude-opus-5-5`, variant `shared`. The reviewer saw only the issue, the diff and the repository at the PR head, and could run code but not push.</sub>

The link rewriting works when the extension is passed as an instance: external http/https links, autolinks and reference links are marked, while mailto, anchors and images are left alone. But the PR adds no pyproject entry point, so `extensions=['external_links']` raises ModuleNotFoundError. That breaks maintainer decision 1 and ARCHITECTURE.md constraint 4. The tests miss this because they only use instances.

### The reviewer's own acceptance checks (derived from the issue)
| Check | Command | Result |
|---|---|---|
| Extension loads by its short name 'external_links' | `python -c "import markdown; print(markdown.markdown('[d](https://e.com)', extensions=['external_links']))"` | fail |
| Automatic link <https://example.com> gets target and rel | `python -c "... markdown.markdown('<https://example.com>', extensions=[E()])"` | pass |
| http:// links and reference-style links are marked | `python -c "... '[h](http://e.com)' and '[r][1]\n\n[1]: https://e.com'"` | pass |
| mailto: links, #anchors and images are unchanged | `python -c "... '[m](mailto:a@b.c)', '[x](#top)', '![i](https://e.com/i.png)'"` | pass |
| Full test suite | `python -m unittest discover tests` | pass |

### Blocking findings
- **[implementation] Extension cannot be loaded as extensions=['external_links']: no entry point in pyproject.toml** (`pyproject.toml:91`)
  <details><summary>evidence</summary>

```
Maintainer decision 1 says the extension is loaded with `extensions=['external_links']`, and ARCHITECTURE.md constraint 4 says every built-in extension needs an entry point under [project.entry-points.'markdown.extensions']. The diff adds no entry point; the list ends at `legacy_em` (line 91). Running `python -c "import markdown; markdown.markdown('[d](https://e.com)', extensions=['external_links'])"` fails with: ModuleNotFoundError No module named 'external_links'. Fix: add `external_links = 'markdown.extensions.external_links:ExternalLinksExtension'` and reinstall.
```
</details>
- **[testing] Tests skip the short-name loading and most of the cases the issue lists** (`tests/test_syntax/extensions/test_external_links.py`)
  <details><summary>evidence</summary>

```
Both tests pass an `ExternalLinksExtension()` instance, so the missing entry point goes unnoticed. The maintainer explicitly listed automatic links (`<https://example.com>`), `http://`, `#anchors`, `mailto:` and images, and none of them has a test. Add tests that use `extensions=['external_links']` and cover each of these cases.
```
</details>

### Non-blocking
- The treeprocessor at priority 3 runs after the inline treeprocessor (20) and before prettify, so it sees autolinks and reference links. The behaviour is correct when the extension is passed as an instance.
- Raw HTML `<a href="https://...">` is stashed and not changed. That seems acceptable because the issue only covers Markdown links, but it could be documented.
- There is no docs page for the new extension under docs/extensions/ (no blocking).
- The changelog entry is present.

### Routing
Earliest stage named by a blocking finding: **implementation**. Review rounds are used up; a maintainer decides.

Run: https://github.com/AvAdiii/markdown/actions/runs/44896874565