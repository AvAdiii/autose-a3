Closes #5.

This pull request was produced by the autose workflow. A maintainer decides whether to merge it.

## What the issue asks (READY requirements from `spec.md`)
- **FR-001** When `external_links` is passed in the `extensions` list, the library shall load the extension without error.
- **FR-002** While `external_links` is not enabled, the library shall render external links exactly as it did before this extension existed.
- **FR-003** While `external_links` is enabled, when a Markdown inline link has an external `href`, the library shall render the `<a>` element with `target="_blank"` and `rel="noopener noreferrer"`.
- **FR-004** While `external_links` is enabled, when the text contains an automatic link whose address starts with `http://` or `https://`, the library shall render the `<a>` element with `target="_blank"` and `rel="noopener noreferrer"`.
- **FR-005** While `external_links` is enabled, when a reference-style link resolves to an external `href`, the library shall render the `<a>` element with `target="_blank"` and `rel="noopener noreferrer"`.
- **FR-006** While `external_links` is enabled, when a link has a relative `href`, an `href` beginning with `#`, or an `href` beginning with `mailto:`, the library shall render the `<a>` element without adding `target` or `rel`.
- **FR-007** While `external_links` is enabled, when the text contains an image with an external `src`, the library shall render the `<img>` element without adding `target` or `rel`.
- **FR-008** The `external_links` extension shall behave identically for every use, with no configuration options.

## Approach (from `design.md`)
Add a new built-in extension `external_links` (component 7, Extension API). It registers one tree processor that runs after `InlineProcessor` (priority 20), walks the ElementTree and sets `target="_blank"` and `rel="noopener noreferrer"` on every `<a>` whose `href` starts with `http://` or `https://`. Working on the finished tree covers inline, reference and automatic links with one code path, and never touches `<img>`. Raw HTML is stashed (ADR-3), so it is untouched, which keeps the BLOCKED FR-009/FR-010 out of scope. The extension is opt-in, so default output does not change. It needs no config and no per-document state. It subclasses `Extension`, defines `makeExtension` and gets a `pyproject.toml` entry point.

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

## Tests (from `test_report.md`)
| Acceptance criterion | Test | Base | Head |
|---|---|---|---|
| AC-FR-001-1 | `test_ac_fr_001_1_loads_by_name` | error | pass |
| AC-FR-001-2 | `test_ac_fr_001_2_plain_text_unchanged` | error | pass |
| AC-FR-002-1 | `test_ac_fr_002_1_disabled_inline_link` | pass | pass |
| AC-FR-002-2 | `test_ac_fr_002_2_disabled_autolink` | pass | pass |
| AC-FR-003-1 | `test_ac_fr_003_1_https_inline_link` | error | pass |
| AC-FR-003-2 | `test_ac_fr_003_2_http_link_with_query` | error | pass |
| AC-FR-003-3 | `test_ac_fr_003_3_text_and_href_unchanged` | error | pass |
| AC-FR-004-1 | `test_ac_fr_004_1_autolink` | error | pass |
| AC-FR-004-2 | `test_ac_fr_004_2_mailto_autolinks` | error | pass |
| AC-FR-005-1 | `test_ac_fr_005_1_reference_link` | error | pass |
| AC-FR-006-1 | `test_ac_fr_006_1_relative_absolute_path` | error | pass |
| AC-FR-006-2 | `test_ac_fr_006_2_anchor` | error | pass |
| AC-FR-006-3 | `test_ac_fr_006_3_mailto_link` | error | pass |
| AC-FR-006-4 | `test_ac_fr_006_4_relative_file` | error | pass |
| AC-FR-007-1 | `test_ac_fr_007_1_image_only` | error | pass |
| AC-FR-007-2 | `test_ac_fr_007_2_linked_image` | error | pass |
| AC-FR-008-1 | `test_ac_fr_008_1_no_config_needed` | error | pass |

## Stage checks
| Stage | Result | Attempts |
|---|---|---|
| requirements | passed | 1 |
| design | passed | 1 |
| implementation | passed | 2 |
| testing | passed | 2 |
| release | CI passed | - |

Round 0. Run and all stage artifacts: https://github.com/AvAdiii/markdown/actions/runs/44896794171

## autose check (release): PASSED
- PR: https://github.com/AvAdiii/markdown/pull/18
- head: `ee14a6b56b8322c897f1107d0808cf76e23618be`
- 14 checks passed
