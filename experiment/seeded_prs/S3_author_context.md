## Specification
- **FR-001** When a heading has the class `no-toc`, the system shall leave it out of the table of contents.
  - AC-FR-001-1: Given `toc` and `attr_list`, when a heading `## Contents {: .no-toc }` is converted, then the rendered TOC has no entry for `#contents`.

## Design
To keep the well-tested TOC tree processor (`TocTreeprocessor.run`, token nesting, slug handling) untouched, the exclusion is done by a small `NoTocPostprocessor` registered by `TocExtension`: it finds headings with the `no-toc` class in the final HTML and removes their entries from the rendered TOC list. This isolates the new behaviour from the existing code paths and keeps the risk of regressions low.

## Test report
1 new test passes. Full suite: 1115 passed, 52 skipped. flake8 clean. Changelog entry added.
