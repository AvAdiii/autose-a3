## autose independent review: REQUEST CHANGES
<sub>Round 0. Reviewer model `claude-opus-5-5`, variant `shared`. The reviewer saw only the issue, the diff and the repository at the PR head, and could run code but not push.</sub>

The rendered [TOC] for the issue's exact example is correct, but the fix is incomplete and fragile. The issue explicitly asks for md.toc_tokens to exclude the heading, and it doesn't: md.toc_tokens and md.toc still list 'contents'. The regex postprocessor also produces malformed lists when the excluded heading has children, deletes the user's own <li> links elsewhere in the document, and treats a class like 'no-tocx' as 'no-toc'. The exclusion belongs in TocTreeprocessor, when the token list is built.

### The reviewer's own acceptance checks (derived from the issue)
| Check | Command | Result |
|---|---|---|
| Issue example: rendered [TOC] lists Guide, Install, Usage but not Contents | `python -c "import markdown; md=markdown.Markdown(extensions=['toc','attr_list']); print(md.convert('# Guide\n\n## Contents {: .no-toc }\n\n[TOC]\n\n## Install\n` | pass |
| Contents heading keeps id="contents" | `same probe` | pass |
| md.toc_tokens excludes the no-toc heading (explicit issue requirement) | `same probe; print(md.toc_tokens)` | fail |
| md.toc excludes the no-toc heading | `same probe; print(md.toc)` | fail |
| Excluding a heading that has child headings produces valid HTML | `md.convert('[TOC]\n\n# A {: .no-toc }\n\n## B\n\n# C\n')` | fail |
| Only the exact class no-toc triggers exclusion | `md.convert('[TOC]\n\n# A {: .no-tocx }\n\n# C\n')` | fail |
| Content outside the TOC is untouched | `markdown.markdown('# A {: .no-toc }\n\n<ul>\n<li><a href="#a">jump</a></li>\n</ul>\n', extensions=['toc','attr_list'])` | fail |
| Full test suite | `python -m unittest discover tests` | pass |

### Blocking findings
- **[design] md.toc_tokens and md.toc still include no-toc headings** (`markdown/extensions/toc.py:442`)
  <details><summary>evidence</summary>

```
The issue says the exclusion must also apply to md.toc_tokens. After converting the issue example, md.toc_tokens still has {'id': 'contents', ...} in Guide's children, and md.toc still has <li><a href="#contents">. The postprocessor only rewrites the output string, so the data the TocTreeprocessor builds never changes. The heading should be skipped in TocTreeprocessor.run when the token list is built. The heading should still get its id there.
```
</details>
- **[implementation] Regex postprocessor breaks markup and deletes content that is not part of the TOC** (`markdown/extensions/toc.py:446`)
  <details><summary>evidence</summary>

```
Nested case: '[TOC]\n\n# A {: .no-toc }\n\n## B\n\n# C' renders '<ul>\n<ul>\n<li><a href="#b">B</a></li>\n</ul>\n</li>', which has a stray </li> and an unwrapped nested <ul>. The pattern `re.sub(r'<li><a href="#id">...')` runs on the whole document, so a user's own raw-HTML list item linking to #a was deleted ('<ul>\n</ul>'). The pattern `class="[^"]*no-toc[^"]*"` is a substring match, so the class `no-tocx` also drops the heading. The regex also assumes class comes before id, and the TOC only nests correctly when the work is done on the token tree.
```
</details>
- **[testing] Tests miss the toc_tokens requirement, the issue's full expected output and edge cases** (`tests/test_syntax/extensions/test_toc.py:1579`)
  <details><summary>evidence</summary>

```
The only test checks for the absence of one <li> substring. Nothing asserts the heading keeps id="contents", nothing checks md.toc_tokens or md.toc (both still contain 'contents' today), and nothing covers a no-toc heading with child headings.
```
</details>

### Non-blocking
- ARCHITECTURE.md is followed: the processor is registered through the registry and core does not import from extensions. The problem is the method: rewriting the HTML string after serialization instead of filtering in TocTreeprocessor, which owns the TOC data.
- Consider making the class name a config option (for example `exclude_class`, default 'no-toc'), and document it in docs/extensions/toc.md.
- The changelog entry is present.

### Routing
Earliest stage named by a blocking finding: **design**. Review rounds are used up; a maintainer decides.

Run: https://github.com/AvAdiii/markdown/actions/runs/44896839711