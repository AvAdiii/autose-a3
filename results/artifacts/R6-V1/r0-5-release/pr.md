Closes #5.

This pull request was produced by the autose workflow. A maintainer decides whether to merge it.

## What the issue asks (READY requirements from `spec.md`)
- **FR-001** Where the extension `external_links` is listed in `extensions`, the library shall load it by that name.
- **FR-002** While the extension `external_links` is not enabled, the library shall render links exactly as it does without the extension.
- **FR-003** Where the extension `external_links` is enabled, the library shall add `target="_blank"` and `rel="noopener noreferrer"` to every `<a>` element whose `href` starts with `http://` or `https://`.
- **FR-004** Where the extension `external_links` is enabled, the library shall add `target="_blank"` and `rel="noopener noreferrer"` to the `<a>` element created from an automatic link whose address starts with `http://` or `https://`.
- **FR-005** Where the extension `external_links` is enabled, the library shall leave unchanged every link whose `href` does not start with `http://` or `https://`, including relative links, `#anchors` and `mailto:` links.
- **FR-006** Where the extension `external_links` is enabled, the library shall render images exactly as it does without the extension.
- **FR-007** The extension `external_links` shall define no configuration options.

## Approach (from `design.md`)
Add a new built-in extension `external_links` in `markdown/extensions/external_links.py`. It registers one `Treeprocessor` (`ExternalLinksTreeprocessor`) in `md.treeprocessors` at priority 15, i.e. after `inline` (20), so every `<a>` element made by inline patterns (inline links, reference links, autolinks) already exists in the tree. The processor walks the tree and sets `target="_blank"` and `rel="noopener noreferrer"` on each `<a>` whose `href` starts with `http://` or `https://`. Images are `<img>` elements and are never touched. The extension defines no config options. It is registered via an entry point in `pyproject.toml` and does nothing unless enabled, so the core is unchanged (no core import from extensions). Docs and a changelog entry are added.

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

## Tests (from `test_report.md`)
| Acceptance criterion | Test | Base | Head |
|---|---|---|---|
| AC-FR-001-1 | `test_ac_fr_001_1_loads_by_name` | error | pass |
| AC-FR-001-2 | `test_ac_fr_001_2_construct` | error | pass |
| AC-FR-002-1 | `test_ac_fr_002_1_disabled_inline` | pass | pass |
| AC-FR-002-2 | `test_ac_fr_002_2_disabled_autolink` | pass | pass |
| AC-FR-003-1 | `test_ac_fr_003_1_https` | error | pass |
| AC-FR-003-2 | `test_ac_fr_003_2_http` | error | pass |
| AC-FR-003-3 | `test_ac_fr_003_3_reference_link` | error | pass |
| AC-FR-004-1 | `test_ac_fr_004_1_autolink` | error | pass |
| AC-FR-005-1 | `test_ac_fr_005_1_relative` | error | pass |
| AC-FR-005-2 | `test_ac_fr_005_2_anchor` | error | pass |
| AC-FR-005-3 | `test_ac_fr_005_3_mailto` | error | pass |
| AC-FR-006-1 | `test_ac_fr_006_1_image` | error | pass |
| AC-FR-006-2 | `test_ac_fr_006_2_linked_image` | error | pass |
| AC-FR-007-1 | `test_ac_fr_007_1_no_configs` | error | pass |
| AC-FR-007-2 | `test_ac_fr_007_2_unknown_option` | error | pass |

## Stage checks
| Stage | Result | Attempts |
|---|---|---|
| requirements | passed | 2 |
| design | passed | 1 |
| implementation | passed | 1 |
| testing | passed | 1 |
| release | CI FAILED | - |

Round 0. Run and all stage artifacts: https://github.com/AvAdiii/markdown/actions/runs/44890315260

## autose check (release): FAILED
- PR: https://github.com/AvAdiii/markdown/pull/18
- head: `6755d1319d76a87028da205c960b2ec0780b5dfc`
- failing checks: lint (checklinks) (failure) https://github.com/AvAdiii/markdown/actions/runs/44890691958/job/136805627065, lint (checkspelling) (failure) https://github.com/AvAdiii/markdown/actions/runs/44890691958/job/136805626878
