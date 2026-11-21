## autose independent review: REQUEST CHANGES
<sub>Round 0. Reviewer model `claude-sonnet-5-5`, variant `isolated`. The reviewer saw only the issue, the diff and the repository at the PR head, and could run code but not push.</sub>

The PR strips entries from the rendered `[TOC]` HTML with a regex postprocessor. That fixes the issue's example only. `md.toc_tokens` and `md.toc` still list the excluded heading, which the issue explicitly asks to change. The regex also gives wrong output for nested and similarly named classes. The fix belongs in `TocTreeprocessor`, before the tokens and the TOC HTML are built.

### The reviewer's own acceptance checks (derived from the issue)
| Check | Command | Result |
|---|---|---|
| Rendered TOC omits Contents but keeps Guide, Install and Usage; heading keeps id | `python -c "import markdown; md=markdown.Markdown(extensions=['toc','attr_list']); print(md.convert('# Guide\n\n## Contents {: .no-toc }\n\n[TOC]\n\n## Install\n` | pass |
| md.toc_tokens excludes the no-toc heading | `python -c "... print(md.toc_tokens)"` | fail |
| md.toc excludes the no-toc heading | `python -c "... print(repr(md.toc))"` | fail |
| A class like no-toc-x is not excluded, and nested headings render a valid TOC | `python -c "... '[TOC]\n\n# A\n## B {: .foo .no-toc }\n## C {: .no-toc-x }\n'"` | fail |
| Whole test suite | `python -m unittest discover tests` | pass |

### Blocking findings
- **[design] md.toc_tokens and md.toc still include no-toc headings** (`markdown/extensions/toc.py:442`)
  <details><summary>evidence</summary>

```
Running `Markdown(extensions=['toc','attr_list'])` on the issue's example, `md.toc_tokens` still contains {'id':'contents',...} as a child of Guide. `md.toc` still contains `<li><a href="#contents">Contents</a></li>`. Only the `[TOC]` placeholder output in the body was changed, by a postprocessor that edits the final HTML. The issue says the exclusion must also apply to `md.toc_tokens`. The filtering needs to happen in TocTreeprocessor when the toc tokens are collected.
```
</details>
- **[implementation] Regex postprocessor is wrong for nesting and class matching** (`markdown/extensions/toc.py:445`)
  <details><summary>evidence</summary>

```
Input `[TOC]\n\n# A\n## B {: .foo .no-toc }\n## C {: .no-toc-x }` rendered a TOC with both B and C removed and an empty `<ul>` left behind. C's class is only `no-toc-x`, but `class="[^"]*no-toc[^"]*"` is a substring match. Input `# A\n## Sub {: .no-toc }\n### Deep\n## B` produced a malformed nested `<ul><ul>` structure with Sub's child orphaned. The regex also assumes `class` comes before `id` in the heading tag.
```
</details>
- **[testing] Test only covers the rendered-HTML case** (`tests/test_syntax/extensions/test_toc.py:1577`)
  <details><summary>evidence</summary>

```
The single new test only checks two `assertIn`/`assertNotIn` substrings in the HTML output. It does not check `md.toc_tokens` or `md.toc`. It does not check that the heading keeps `id="contents"`. It does not check nested headings or a class that merely contains `no-toc`.
```
</details>

### Non-blocking
- The existing suite passes (1167 tests, OK), but none of those tests exercise the new behaviour.
- The issue allows the class name to be configurable. The PR hard-codes `no-toc`, which is acceptable, but a config option would be nicer.
- The changelog entry is present.

### Routing
Earliest stage named by a blocking finding: **design**. Review rounds are used up; a maintainer decides.

Run: https://github.com/AvAdiii/markdown/actions/runs/44896946310