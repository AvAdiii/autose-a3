# Design: Opt-in external_links extension

## Summary
Add a new built-in extension `external_links` (component 7, Extension API). It registers one tree processor that runs after `InlineProcessor` (priority 20), walks the ElementTree and sets `target="_blank"` and `rel="noopener noreferrer"` on every `<a>` whose `href` starts with `http://` or `https://`. Working on the finished tree covers inline, reference and automatic links with one code path, and never touches `<img>`. Raw HTML is stashed (ADR-3), so it is untouched, which keeps the BLOCKED FR-009/FR-010 out of scope. The extension is opt-in, so default output does not change. It needs no config and no per-document state. It subclasses `Extension`, defines `makeExtension` and gets a `pyproject.toml` entry point.

## Changes
| File | Symbol | Change | ACs | Notes |
|---|---|---|---|---|
| markdown/extensions/external_links.py | new ExternalLinksTreeprocessor | add | AC-FR-003-1, AC-FR-003-2, AC-FR-003-3, AC-FR-004-1, AC-FR-004-2, AC-FR-005-1, AC-FR-006-1, AC-FR-006-2, AC-FR-006-3, AC-FR-006-4, AC-FR-007-1, AC-FR-007-2 | `Treeprocessor` subclass. `run(root)` iterates `root.iter('a')`; if `href` is a str and starts with `http://` or `https://` (case-sensitive), `set('target','_blank')` and `set('rel','noopener noreferrer')`. |
| markdown/extensions/external_links.py | new ExternalLinksExtension.extendMarkdown | add | AC-FR-001-1, AC-FR-001-2, AC-FR-008-1 | `Extension` subclass with no config. Registers `ExternalLinksTreeprocessor(md)` in `md.treeprocessors` as `external_links` at priority 15 (after `inline` 20, before `prettify` 10). |
| markdown/extensions/external_links.py | new makeExtension | add | AC-FR-001-1, AC-FR-001-2 | Returns `ExternalLinksExtension(**kwargs)`, with `# pragma: no cover` like the other extensions. |
| pyproject.toml | project.entry-points.'markdown.extensions' | modify | AC-FR-001-1, AC-FR-001-2, AC-FR-008-1 | Add `external_links = 'markdown.extensions.external_links:ExternalLinksExtension'`. |
| tests/test_syntax/extensions/test_external_links.py | new TestExternalLinks | add | AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2, AC-FR-003-3, AC-FR-004-1, AC-FR-004-2, AC-FR-005-1, AC-FR-006-1, AC-FR-006-2, AC-FR-006-3, AC-FR-006-4, AC-FR-007-1, AC-FR-007-2, AC-FR-008-1 | Uses `markdown.test_tools.TestCase`, with `extensions=['external_links']`. |
| docs/extensions/external_links.md | - | add | - | Short user page. |
| docs/extensions/index.md | - | modify | - | Add a table row and a link reference. |
| mkdocs.yml | - | modify | - | Add a nav entry. |
| docs/reference/markdown.extensions.external_links.md | - | add | - | `::: markdown.extensions.external_links`, as for the other extensions. |
| docs/changelog.md | - | modify | - | Add `### Added` under `## [Unreleased]`: "Add the `external_links` extension, which adds `target="_blank"` and `rel="noopener noreferrer"` to external links." |

## Interface
- Name: `external_links`. Usage: `markdown.markdown(text, extensions=['external_links'])`. No config options and no defaults.
- Module `markdown.extensions.external_links`, with `ExternalLinksExtension` and `makeExtension`.
- External means `href` starts with the lowercase `http://` or `https://`. Anything else is unchanged.
- Attribute order in the serialized `<a>` is not guaranteed. The tester should assert on attribute presence, for example by checking for the substrings `href="https://example.com"`, `target="_blank"` and `rel="noopener noreferrer"`. The attributes are expected in the order href, target, rel, because ElementTree keeps insertion order and `href` is set first. Substring checks are still safer.

| AC | Input | Expected |
|---|---|---|
| AC-FR-001-1 | `[a](https://example.com)`, ext enabled | No exception. |
| AC-FR-001-2 | `markdown.Markdown(extensions=['external_links']).convert('text')` | `<p>text</p>` |
| AC-FR-002-1 | `[a](https://example.com)`, no ext | `<p><a href="https://example.com">a</a></p>` |
| AC-FR-002-2 | `<https://example.com>`, no ext | Output has no `target=` and no `rel=`. Today's output is `<p><a href="https://example.com">https://example.com</a></p>`. |
| AC-FR-003-1 | `[a](https://example.com)` | One `<a` tag, with `href="https://example.com"`, `target="_blank"` and `rel="noopener noreferrer"`. Expected: `<p><a href="https://example.com" target="_blank" rel="noopener noreferrer">a</a></p>`. |
| AC-FR-003-2 | `[a](http://example.com/x?y=1)` | The `<a` tag has `target="_blank"` and `rel="noopener noreferrer"`. |
| AC-FR-003-3 | `[a](https://example.com)` | Output contains `href="https://example.com"` and `>a</a>`. |
| AC-FR-004-1 | `<https://example.com>` | `<p><a href="https://example.com" target="_blank" rel="noopener noreferrer">https://example.com</a></p>` |
| AC-FR-004-2 | `<mailto:a@example.com>` and `<a@example.com>` | No `target=` and no `rel=`. |
| AC-FR-005-1 | `[a][1]\n\n[1]: https://example.com` | The `<a` tag has `target="_blank"` and `rel="noopener noreferrer"`. |
| AC-FR-006-1 | `[a](/docs/page.html)` | `<p><a href="/docs/page.html">a</a></p>` |
| AC-FR-006-2 | `[a](#section)` | `<p><a href="#section">a</a></p>` |
| AC-FR-006-3 | `[a](mailto:a@example.com)` | No `target=` and no `rel=`. |
| AC-FR-006-4 | `[a](page.html)` | `<p><a href="page.html">a</a></p>` |
| AC-FR-007-1 | `![alt](https://example.com/i.png)` | `<p><img alt="alt" src="https://example.com/i.png" /></p>` |
| AC-FR-007-2 | `[![alt](https://example.com/i.png)](https://example.com)` | The `<a` tag has `target` and `rel`. The `<img` tag has neither `target=` nor `rel=`. Both come from the same string, so the `<img ... />` substring can be checked separately. |
| AC-FR-008-1 | `[a](https://example.com)` with no configs | Same output as AC-FR-003-1. |

## Test plan
| AC | Test file | Test method (contains the AC id in snake case) | Asserts |
|---|---|---|---|
| AC-FR-001-1 | tests/test_syntax/extensions/test_external_links.py | test_ac_fr_001_1_loads_by_name | No exception. |
| AC-FR-001-2 | same | test_ac_fr_001_2_plain_text_unchanged | `<p>text</p>` |
| AC-FR-002-1 | same | test_ac_fr_002_1_disabled_inline_link | Exact HTML. |
| AC-FR-002-2 | same | test_ac_fr_002_2_disabled_autolink | No `target=` or `rel=`. |
| AC-FR-003-1 | same | test_ac_fr_003_1_https_inline_link | Exact HTML or attribute substrings. |
| AC-FR-003-2 | same | test_ac_fr_003_2_http_link_with_query | Attribute substrings. |
| AC-FR-003-3 | same | test_ac_fr_003_3_text_and_href_unchanged | Substrings. |
| AC-FR-004-1 | same | test_ac_fr_004_1_autolink | Exact HTML. |
| AC-FR-004-2 | same | test_ac_fr_004_2_mailto_autolinks | No `target=` or `rel=`. |
| AC-FR-005-1 | same | test_ac_fr_005_1_reference_link | Attribute substrings. |
| AC-FR-006-1 | same | test_ac_fr_006_1_relative_absolute_path | Exact HTML. |
| AC-FR-006-2 | same | test_ac_fr_006_2_anchor | Exact HTML. |
| AC-FR-006-3 | same | test_ac_fr_006_3_mailto_link | No `target=` or `rel=`. |
| AC-FR-006-4 | same | test_ac_fr_006_4_relative_file | Exact HTML. |
| AC-FR-007-1 | same | test_ac_fr_007_1_image_only | Exact HTML. |
| AC-FR-007-2 | same | test_ac_fr_007_2_linked_image | The `<a` tag has the attributes, and `<img` has no `target` or `rel`. |
| AC-FR-008-1 | same | test_ac_fr_008_1_no_config_needed | Same as AC-FR-003-1. |

## Architecture fit
- Constraint 1: `ExternalLinksExtension` subclasses `Extension`, implements `extendMarkdown`, and the module defines `makeExtension`.
- Constraint 2 and ADR-1: the extension only registers a named processor in `md.treeprocessors` at priority 15. Core code is not edited.
- Constraint 3: nothing in the core imports the new module.
- Constraint 4: entry point added in `pyproject.toml`.
- Constraint 5: no per-document state, so no `reset()`.
- ADR-2: the extension edits Elements and does not write HTML text.
- ADR-3: raw HTML anchors are stashed placeholders, so they are not seen, which is the intended behaviour while Q-001 is open.

## Risks
- Priority 15 is after `inline` (20), so all `<a>` elements exist by then. A tree processor from another extension that creates links later, for example `toc` at 5, is not affected. Existing extension tests in `tests/test_syntax/extensions` and `tests/test_extensions.py` do not enable the new extension, so they are unaffected.
- The entry-point table is read from `pyproject.toml`. The installed entry point metadata may need a reinstall to resolve the short name. If the tester runs against an uninstalled checkout, the fallback is the dotted path, `markdown.extensions.external_links`, though the short name is the contract. A test for the short name needs the package installed in editable mode with metadata regenerated.
- The docs build (mkdocs nav and reference page) must stay consistent. The `docs/extensions/index.md` link reference and the `mkdocs.yml` nav entry both need adding.
- ARCHITECTURE.md says "18 built-in extensions". It is not under the pipeline's change paths, so it is left alone.


---
## autose check: PASSED
- 10 planned changes; every READY criterion mapped; symbols found
