## Specification
- **FR-001** Where the `external_links` extension is enabled, every link whose href starts with `http://` or `https://` shall get `target="_blank"` and `rel="noopener noreferrer"`.
- **FR-002** Relative links, `#anchors` and `mailto:` links shall be unchanged.

## Design
New module `markdown/extensions/external_links.py` following ARCHITECTURE.md constraint 1: an `Extension` subclass, a `Treeprocessor` registered at priority 3 (after inline parsing, so automatic links are covered), and `makeExtension`. No core module changes.

## Test report
2 new tests pass. Full suite: 1116 passed, 52 skipped. flake8 clean. Changelog entry added.
