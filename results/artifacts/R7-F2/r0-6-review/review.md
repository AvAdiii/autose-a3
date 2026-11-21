## autose independent review: APPROVE
<sub>Round 0. Reviewer model `claude-opus-5-5`, variant `isolated`. The reviewer saw only the issue, the diff and the repository at the PR head, and could run code but not push.</sub>

The PR adds one condition to TocTreeprocessor: headings whose class list contains `no-toc` are left out of toc_tokens, and therefore out of md.toc and the [TOC] output. They still get their id and permalink. I ran the issue's example and two edge cases (a similar class name, an excluded heading with children), and all behaved correctly. The full suite passes and the changelog entry is present. The change stays inside the toc extension and doesn't violate ARCHITECTURE.md. The only gap is missing user docs in docs/extensions/toc.md, which doesn't block merging.

### The reviewer's own acceptance checks (derived from the issue)
| Check | Command | Result |
|---|---|---|
| Issue example with toc+attr_list: TOC lists Guide, Install, Usage but not Contents | `python -c "import markdown; md=markdown.Markdown(extensions=['toc','attr_list']); print(md.convert('# Guide\n\n## Contents {: .no-toc }\n\n[TOC]\n\n## Install\n` | pass |
| Excluded heading still rendered with id="contents" | `same probe` | pass |
| md.toc_tokens excludes the Contents heading | `same probe, print(md.toc_tokens)` | pass |
| Edge case: a class that only looks similar (no-toc-x) is not excluded; a child under an excluded heading still appears in the TOC | `python -c "... md.convert('# A\n\n## Skip {: .no-toc }\n\n### Child\n\n## B {: .no-toc-x }') ..."` | pass |
| With permalink=True, the excluded heading still gets its permalink and is missing from md.toc | `python -c "... extension_configs={'toc':{'permalink':True}} ..."` | pass |
| Full test suite passes | `python -m unittest discover tests` | pass |

### Non-blocking
- The extension docs (docs/extensions/toc.md) don't mention the `no-toc` class, which is the place users would look for it. Consider adding a short section next to the `data-toc-label` docs.
- The class name is hard-coded. The issue says a configurable name is optional, so this is acceptable.
- Without the code change, the new tests would fail: test_ac_fr_001_1_hrefs asserts that href="#contents" is missing. I could not re-run them against the base code because git operations are blocked in this environment.
- When a no-toc heading has children, they move up to the previous ancestor in the TOC (e.g. h3 Child appears under h1 A). This is reasonable but not documented.

### Routing
Approved. A maintainer decides whether to merge.

Run: https://github.com/AvAdiii/markdown/actions/runs/44890548514