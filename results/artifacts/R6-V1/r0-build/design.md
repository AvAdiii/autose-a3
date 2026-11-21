# Design: external_links extension

## Summary
Add a new built-in extension `external_links` in `markdown/extensions/external_links.py`. It registers one `Treeprocessor` (`ExternalLinksTreeprocessor`) in `md.treeprocessors` at priority 15, i.e. after `inline` (20), so every `<a>` element made by inline patterns (inline links, reference links, autolinks) already exists in the tree. The processor walks the tree and sets `target="_blank"` and `rel="noopener noreferrer"` on each `<a>` whose `href` starts with `http://` or `https://`. Images are `<img>` elements and are never touched. The extension defines no config options. It is registered via an entry point in `pyproject.toml` and does nothing unless enabled, so the core is unchanged (no core import from extensions). Docs and a changelog entry are added.

## Changes
| File | Symbol | Change | ACs | Notes |
|---|---|---|---|---|
| markdown/extensions/external_links.py | new ExternalLinksTreeprocessor | add | AC-FR-003-1, AC-FR-003-2, AC-FR-003-3, AC-FR-004-1, AC-FR-005-1, AC-FR-005-2, AC-FR-005-3, AC-FR-006-1, AC-FR-006-2 | `run(root)`: `for el in root.iter('a')`; `href = el.get('href', '')`; if `href.startswith(('http://', 'https://'))` set `target` and `rel`. Leaves everything else alone. |
| markdown/extensions/external_links.py | new ExternalLinksExtension | add | AC-FR-001-1, AC-FR-001-2, AC-FR-007-1, AC-FR-007-2 | `Extension` subclass, no `self.config` entries; `extendMarkdown(md)` registers the treeprocessor as `external_links` at priority 15. |
| markdown/extensions/external_links.py | new makeExtension | add | AC-FR-001-1, AC-FR-001-2 | `def makeExtension(**kwargs): return ExternalLinksExtension(**kwargs)  # pragma: no cover` |
| pyproject.toml | `[project.entry-points.'markdown.extensions']` | modify | AC-FR-001-1, AC-FR-001-2 | add `external_links = 'markdown.extensions.external_links:ExternalLinksExtension'` |
| docs/extensions/external_links.md | - | add | - | usage page (what counts as external, no options) |
| docs/extensions/index.md | - | modify | - | add table row and link reference for External Links |
| docs/reference/markdown.extensions.external_links.md | - | add | - | `::: markdown.extensions.external_links` like the other reference pages |
| docs/changelog.md | - | modify | - | `### Added` under `## [Unreleased]`: new `external_links` extension (create the `### Added` heading if absent) |
| tests/test_syntax/extensions/test_external_links.py | new TestExternalLinks | add | AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2, AC-FR-003-3, AC-FR-004-1, AC-FR-005-1, AC-FR-005-2, AC-FR-005-3, AC-FR-006-1, AC-FR-006-2, AC-FR-007-1, AC-FR-007-2 | tests |

## Interface
Extension name: `external_links` (entry point; module `markdown.extensions.external_links`). Class `ExternalLinksExtension`. No config options (`getConfigs() == {}`); any option key raises `KeyError`. Attribute order in output is sorted (`href`, `rel`, `target`).

- AC-FR-001-1: `markdown.markdown('x', extensions=['external_links'])` -> `<p>x</p>`
- AC-FR-001-2: `markdown.Markdown(extensions=['external_links'])` constructs without error.
- AC-FR-002-1: no extensions, `[a](https://example.com)` -> `<p><a href="https://example.com">a</a></p>`
- AC-FR-002-2: no extensions, `<https://example.com>` -> `<p><a href="https://example.com">https://example.com</a></p>`
- AC-FR-003-1: `[a](https://example.com)` -> `<p><a href="https://example.com" rel="noopener noreferrer" target="_blank">a</a></p>`
- AC-FR-003-2: `[a](http://example.com)` -> `<p><a href="http://example.com" rel="noopener noreferrer" target="_blank">a</a></p>`
- AC-FR-003-3: `[a][1]\n\n[1]: https://example.com` -> output `<a>` contains `target="_blank"` and `rel="noopener noreferrer"` (assert with `assertIn`, or the full string `<p><a href="https://example.com" rel="noopener noreferrer" target="_blank">a</a></p>`).
- AC-FR-004-1: `<https://example.com>` -> `<p><a href="https://example.com" rel="noopener noreferrer" target="_blank">https://example.com</a></p>`
- AC-FR-005-1: `[a](page.html)` -> `<p><a href="page.html">a</a></p>`
- AC-FR-005-2: `[a](#top)` -> `<p><a href="#top">a</a></p>`
- AC-FR-005-3: `[a](mailto:me@example.com)` -> output contains neither `target=` nor `rel=`. (Note: Markdown may obfuscate nothing here for inline links; only assert absence.)
- AC-FR-006-1: `![a](https://example.com/i.png)` -> `<p><img alt="a" src="https://example.com/i.png" /></p>`
- AC-FR-006-2: `[![a](https://example.com/i.png)](page.html)` -> `<p><a href="page.html"><img alt="a" src="https://example.com/i.png" /></a></p>` (no `target`/`rel` anywhere).
- AC-FR-007-1: `Markdown(extensions=['external_links']).registeredExtensions[0].getConfigs() == {}`. **The extension must call `md.registerExtension(self)` in `extendMarkdown`** (otherwise `registeredExtensions[0]` would not be it; check: `Markdown.registerExtensions` / `registerExtension` — add `md.registerExtension(self)` to be safe; `reset()` is a no-op in the base class).
- AC-FR-007-2: `Markdown(extensions=['external_links'], extension_configs={'external_links': {'target': '_self'}})` raises `KeyError`.

## Test plan
| AC | Test file | Test method | Asserts |
|---|---|---|---|
| AC-FR-001-1 | tests/test_syntax/extensions/test_external_links.py | test_ac_fr_001_1_loads_by_name | `assertMarkdownRenders('x', '<p>x</p>')` |
| AC-FR-001-2 | same | test_ac_fr_001_2_construct | construction doesn't raise |
| AC-FR-002-1 | same | test_ac_fr_002_1_disabled_inline | `default_kwargs` overridden with `extensions=[]`; plain output |
| AC-FR-002-2 | same | test_ac_fr_002_2_disabled_autolink | plain autolink output |
| AC-FR-003-1 | same | test_ac_fr_003_1_https | exact HTML |
| AC-FR-003-2 | same | test_ac_fr_003_2_http | exact HTML |
| AC-FR-003-3 | same | test_ac_fr_003_3_reference_link | attrs present |
| AC-FR-004-1 | same | test_ac_fr_004_1_autolink | exact HTML |
| AC-FR-005-1 | same | test_ac_fr_005_1_relative | exact HTML |
| AC-FR-005-2 | same | test_ac_fr_005_2_anchor | exact HTML |
| AC-FR-005-3 | same | test_ac_fr_005_3_mailto | no `target=`/`rel=` |
| AC-FR-006-1 | same | test_ac_fr_006_1_image | exact HTML |
| AC-FR-006-2 | same | test_ac_fr_006_2_linked_image | exact HTML |
| AC-FR-007-1 | same | test_ac_fr_007_1_no_configs | `getConfigs() == {}` |
| AC-FR-007-2 | same | test_ac_fr_007_2_unknown_option | `assertRaises(KeyError)` |

## Architecture fit
- ADR-1: behaviour added by registering a `Treeprocessor` in a `Registry` at a chosen priority (15, after `inline` 20, before `prettify` 10).
- ADR-2: works on ElementTree `<a>` elements, not HTML strings; the serializer sorts attributes.
- ADR-3: raw HTML `<a ...>` is stashed and untouched (out of scope).
- Constraint 3: nothing in core imports the extension. Constraints 1 and 4: `makeExtension`, an `Extension` subclass and a `pyproject.toml` entry point are all provided.

## Risks
- The entry point is only visible after the package is reinstalled (`pip install -e .`); the string name `external_links` fails to load in a stale environment. Test environment must be reinstalled after the change.
- The extension count in ARCHITECTURE.md ("18 built-in extensions") and `docs/extensions/index.md` become stale; update the docs table. Existing tests that enumerate entry points, if any, would need checking (`tests/test_apis.py`).
- Links with existing `target`/`rel` (FR-008) and `HTTP://`/`//` (FR-009) are BLOCKED; current plan overwrites existing values and is case-sensitive, which is not covered by tests.
- No change to the default pipeline, so all existing tests (`tests/test_syntax/inline/test_links.py`, `test_autolinks.py`) cover the disabled case.


---
## autose check: PASSED
- 9 planned changes; every READY criterion mapped; symbols found
