## Specification
- **FR-001** When an attribute list contains no attributes (`{: }` or `{:}`), the system shall not emit an attribute named `:`.
  - AC-FR-001-1: Given `attr_list`, when `# Title {: }` is converted, then the output contains no ` :` attribute.
  - AC-FR-001-2: Given `attr_list`, when `Some paragraph\n{:}` is converted, then the output contains no ` :` attribute.

## Design
The bogus attribute comes from `AttrListTreeprocessor.BASE_RE`: when the list is empty, the optional `\:?` backtracks and the colon is captured as the first attribute character. Excluding `:` from the first-character class is the smallest change and leaves the attribute scanner untouched.

## Test report
2 new tests, both pass. Full suite: 1116 passed, 52 skipped. flake8 clean. Changelog entry added.
