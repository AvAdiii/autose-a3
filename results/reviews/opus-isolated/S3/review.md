## autose independent review: REQUEST CHANGES
<sub>Round 0. Reviewer model `claude-opus-5-5`, variant `isolated`. The reviewer saw only the issue, the diff and the repository at the PR head, and could run code but not push.</sub>

The PR removes `no-toc` entries by running a regex over the final HTML in a postprocessor. That only changes the TOC rendered at the `[TOC]` marker. `md.toc_tokens` and `md.toc` still include the excluded heading, and the issue explicitly asks for `toc_tokens` to exclude it. The regex also matches the class as a substring, so a class like `no-tocx` triggers exclusion. When an excluded heading has child headings, the output HTML is malformed. The fix belongs in `TocTreeprocessor`, which builds the tokens, not in string post-processing. The existing test suite passes (1167 tests).

### The reviewer's own acceptance checks (derived from the issue)
| Check | Command | Result |
|---|---|---|
| Issue example: the rendered TOC lists Guide, Install and Usage but not Contents | `python -c "import markdown; md=markdown.Markdown(extensions=['toc','attr_list']); print(md.convert('# Guide\n\n## Contents {: .no-toc }\n\n[TOC]\n\n## Install\n` | pass |
| The Contents heading still renders with id="contents" | `same probe` | pass |
| md.toc_tokens excludes the no-toc heading | `same probe, print([t['name'] for t in md.toc_tokens[0]['children']])` | fail |
| md.toc excludes the no-toc heading | `same probe, print(repr(md.toc))` | fail |
| A heading whose class only contains no-toc as a substring (no-tocx) is not excluded | `md.convert('[TOC]\n\n# Not-toc-ish {: .no-tocx }\n\n## C\n')` | fail |
| A no-toc heading with child headings still produces well-formed TOC HTML | `md.convert('[TOC]\n\n# A\n\n## B {: .no-toc }\n\n### B1\n\n## C\n')` | fail |
| The full test suite passes | `python -m unittest discover tests` | pass |

### Blocking findings
- **[design] md.toc_tokens and md.toc still include no-toc headings** (`markdown/extensions/toc.py:442`)
  <details><summary>evidence</summary>

```
Running the issue's example gives [t['name'] for t in md.toc_tokens[0]['children']] == ['Contents', 'Install', 'Usage'], and md.toc still contains <li><a href="#contents">. The issue says: "The same should apply to md.toc_tokens". The exclusion has to happen in TocTreeprocessor.run, where the tokens are built. A postprocessor that regex-edits the output string cannot reach them.
```
</details>
- **[implementation] The regex matches no-toc as a substring and breaks the HTML structure** (`markdown/extensions/toc.py:446`)
  <details><summary>evidence</summary>

```
The pattern class="[^"]*no-toc[^"]*" matches class="no-tocx": '# Not-toc-ish {: .no-tocx }' is removed from the TOC. The substitution removes '<li><a ...>..</a>' together with an optional '</li>', but leaves the nested <ul>. For '## B {: .no-toc }' followed by '### B1', the result is '<li><a href="#a">A</a><ul>\n<ul>\n<li><a href="#b1">B1</a></li>\n</ul>\n</li>...', which is unbalanced markup. The regex also depends on class being serialized before id.
```
</details>
- **[testing] The test does not cover toc_tokens or edge cases** (`tests/test_syntax/extensions/test_toc.py:1579`)
  <details><summary>evidence</summary>

```
The only test checks the rendered HTML string. It has no assertion on md.toc_tokens or md.toc, which the issue requires, so it passes even though toc_tokens is wrong. It also has no case for nested children or a class that only contains no-toc as a substring.
```
</details>

### Non-blocking
- The postprocessor is registered at priority 5, after raw_html (30). Every conversion with toc enabled now runs this regex pass over the whole output document.
- The issue allows the class name to be configurable. Consider adding a toc config option (for example `exclude_class`, default 'no-toc') and documenting it in docs/extensions/toc.md. The docs are not updated in this PR.

### Routing
Earliest stage named by a blocking finding: **design**. Review rounds are used up; a maintainer decides.

Run: https://github.com/AvAdiii/markdown/actions/runs/44890841473