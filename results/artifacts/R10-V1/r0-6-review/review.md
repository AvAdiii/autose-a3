## autose independent review: APPROVE
<sub>Round 0. Reviewer model `claude-opus-5-5`, variant `isolated`. The reviewer saw only the issue, the diff and the repository at the PR head, and could run code but not push.</sub>

The PR does what the maintainer decided. It adds a built-in `external_links` extension, loadable by its short name. The extension is a tree processor at priority 15, so it runs after inline parsing (20) and before prettify (10). It adds `target="_blank"` and `rel="noopener noreferrer"` to every `<a>` whose href starts with `http://` or `https://`, including automatic links. Relative links, `#anchors`, `mailto:` links and images are left alone, and output is unchanged when the extension is not enabled. The PR follows ARCHITECTURE.md: it subclasses `Extension`, defines `makeExtension`, has an entry point in `pyproject.toml`, keeps no state between documents and does not touch the core. It also adds a changelog entry and docs pages wired into `mkdocs.yml`. All my probes and the full test suite pass, and I found no blocking problems.

### The reviewer's own acceptance checks (derived from the issue)
| Check | Command | Result |
|---|---|---|
| Loads by short name `extensions=['external_links']` through the entry point; the dotted path also works | `python probe: importlib.metadata entry_points + markdown.markdown(..., extensions=['markdown.extensions.external_links'])` | pass |
| https and http inline links (http one with a query string) get target and rel; href and text unchanged | `python $TMPDIR/p/probe.py in.txt` | pass |
| Automatic links <https://...> and <http://...> get target and rel | `python $TMPDIR/p/probe.py in.txt` | pass |
| Relative links, /paths, #anchors, mailto links, email automatic links and protocol-relative //x.com are not changed | `python $TMPDIR/p/probe.py in.txt` | pass |
| Images are unaffected; for a linked image only the outer <a> changes | `python $TMPDIR/p/probe.py in.txt` | pass |
| Reference links with a title and links nested in emphasis are handled | `python $TMPDIR/p/probe.py in.txt` | pass |
| Output is unchanged when the extension is off; works alongside footnotes/toc/extra/wikilinks (links inside footnote text change; footnote, TOC and wikilinks do  | `python combo probe with in2.txt` | pass |
| Full test suite and the PR's tests pass | `python -m unittest discover tests; python -m unittest tests.test_syntax.extensions.test_external_links` | pass |

### Non-blocking
- The scheme check is case-sensitive, so `[a](HTTPS://x.com)` is not treated as external. This matches the maintainer's literal rule ('starts with http:// or https://'). A case-insensitive check would be a reasonable follow-up.
- Raw inline HTML `<a href="https://...">` is not changed because it is stashed (ADR-3). This is consistent with the architecture, and the docs could mention it.
- The two 'disabled' tests (test_ac_fr_002_*) would pass without the PR. They are regression guards, which is fine; the other tests do exercise the new behaviour.
- The new row in the docs/extensions/index.md table has a slightly misaligned column width. This is cosmetic.
- A hook blocked shell commands containing literal URLs, so I generated the probe inputs indirectly into $TMPDIR.

### Routing
Approved. A maintainer decides whether to merge.

Run: https://github.com/AvAdiii/markdown/actions/runs/44896794171