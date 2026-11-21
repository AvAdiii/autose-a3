## autose independent review: REQUEST CHANGES
<sub>Round 0. Reviewer model `claude-sonnet-5-5`, variant `isolated`. The reviewer saw only the issue, the diff and the repository at the PR head, and could run code but not push.</sub>

The processing logic works, but there is no entry point in pyproject.toml. The issue's required usage, `extensions=['external_links']`, therefore raises ModuleNotFoundError. ARCHITECTURE.md also requires an entry point for every built-in extension. The tests only pass because they import the class directly.

### The reviewer's own acceptance checks (derived from the issue)
| Check | Command | Result |
|---|---|---|
| Load by short name extensions=['external_links'] | `python -c "import markdown; markdown.markdown('x', extensions=['external_links'])"` | fail |
| Autolink, inline, reference and image behaviour (class loaded directly) | `python -c "... extensions=[ExternalLinksExtension()]"` | pass |
| Full test suite | `python -m unittest discover tests` | pass |

### Blocking findings
- **[implementation] Missing entry point: extensions=['external_links'] fails** (`pyproject.toml`)
  <details><summary>evidence</summary>

```
`python -c "import markdown; markdown.markdown('<https://example.com>', extensions=['external_links'])"` raised `ModuleNotFoundError: No module named 'external_links'`. pyproject.toml has no `external_links` line under `[project.entry-points.'markdown.extensions']`. ARCHITECTURE.md requires one for every built-in extension, and the issue requires loading by short name.
```
</details>
- **[testing] Tests never load the extension by its short name** (`tests/test_syntax/extensions/test_external_links.py`)
  <details><summary>evidence</summary>

```
Both tests pass `ExternalLinksExtension()` directly, so the missing entry point goes undetected. The tests also do not cover autolinks, images, `mailto:` links, `#anchor` links, or reference-style links. The issue explicitly names autolinks and images.
```
</details>

### Non-blocking
- [design] Treeprocessor priority 3 runs after unescape (0 < 3 is earlier, but ordering is arbitrary) (`markdown/extensions/external_links.py`)
- Raw inline HTML `<a href="https://...">` is not modified. The issue's wording ('every external <a> element') arguably covers it, but this is debatable.
- The `HTTPS://` uppercase scheme is not treated as external. The issue says 'starts with', so this is acceptable.
- The changelog entry is present.

### Routing
Earliest stage named by a blocking finding: **implementation**. Review rounds are used up; a maintainer decides.

Run: https://github.com/AvAdiii/markdown/actions/runs/44896984226