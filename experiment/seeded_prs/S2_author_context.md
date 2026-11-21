## Specification
- **FR-001** When a wikilink contains `|`, the system shall display the text after the pipe as the link text.
  - AC-FR-001-1: Given `wikilinks`, when `[[Getting Started|read the guide]]` is converted, then the link text is `read the guide`.
  - AC-FR-001-2: Given `wikilinks`, when `[[Getting Started | read the guide]]` is converted, then the link text is `read the guide`.

## Design
`WIKILINK_RE` gains an optional `|label` group. `WikiLinksInlineProcessor.handleMatch` uses the label when present and otherwise the page name, so `[[Page]]` behaves as before. URL building still goes through the configured `build_url`, so `base_url`, `end_url` and custom builders apply unchanged.

## Test report
2 new tests, both pass. Full suite: 1116 passed, 52 skipped. Changelog entry added.
