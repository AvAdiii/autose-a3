# Spec: attr_list empty attribute list produces invalid attribute
- Issue: #2
- Mode: offline (pipeline profile)
- Input SHA-256: 5f0d4de79e60d47f7bb3a5b0728c9942bbb41a400f63e1441c32ffe9e6c52bb5

## 1. Source spans
SRC-001 [context]: Our docs template generates headings like `# Title {: }` when a page has no custom classes (the template always emits the braces, sometimes with nothing inside).
SRC-002 [context]: With `attr_list` enabled the output contains a broken attribute:
SRC-003 [context]: `<h1 :>` is not valid HTML and our HTML validator in CI rejects the page.
SRC-004 [requirement]: An empty list should just mean "no attributes", so I'd expect `<h1>Title</h1>`, `<p>Some paragraph</p>` and `<p><em>hi</em></p>`.
SRC-005 [requirement]: Non-empty lists like `{: .note }` work as expected and should keep working.

## 2. Glossary
### GLO-001: empty attribute list
- Definition: a `{:` marker followed only by spaces (zero or more) and a closing `}`, for example `{: }` or `{:}`.
- Tag: ASSUMED
- Support: Rationale: the issue gives `{: }` and `{:}` as examples and says "An empty list should just mean "no attributes""; the space-count generalisation is inferred; Confidence: high; Confirm by: maintainer
- Status: defined

## 3. Functional requirements
### FR-001: Empty list on a header produces no attributes
- Statement: When a header line ends with an empty attribute list, the library shall output the header element without any attribute and without the list text.
- Priority: Must
- Tag: STATED
- Support: SRC-004 "I'd expect `<h1>Title</h1>`, `<p>Some paragraph</p>` and `<p><em>hi</em></p>`."
- Acceptance: AC-FR-001-1: Given the `attr_list` extension is enabled, when `# Title {: }` is converted, then the result is exactly `<h1>Title</h1>`.
- Acceptance: AC-FR-001-2: Given the `attr_list` extension is enabled, when `# Title {:}` is converted, then the result is exactly `<h1>Title</h1>`.
- Status: READY

### FR-002: Empty list on a block produces no attributes
- Statement: When the last line of a block is an empty attribute list, the library shall output the block element without any attribute and without the list text.
- Priority: Must
- Tag: STATED
- Support: SRC-004 "I'd expect `<h1>Title</h1>`, `<p>Some paragraph</p>` and `<p><em>hi</em></p>`."
- Acceptance: AC-FR-002-1: Given the `attr_list` extension is enabled, when `Some paragraph\n{:}` is converted, then the result is exactly `<p>Some paragraph</p>`.
- Acceptance: AC-FR-002-2: Given the `attr_list` extension is enabled, when `Some paragraph\n{: }` is converted, then the result is exactly `<p>Some paragraph</p>`.
- Status: READY

### FR-003: Empty list after an inline element produces no attributes
- Statement: When an empty attribute list directly follows an inline element, the library shall output the inline element without any attribute and without the list text.
- Priority: Must
- Tag: STATED
- Support: SRC-004 "I'd expect `<h1>Title</h1>`, `<p>Some paragraph</p>` and `<p><em>hi</em></p>`."
- Acceptance: AC-FR-003-1: Given the `attr_list` extension is enabled, when `*hi*{: }` is converted, then the result is exactly `<p><em>hi</em></p>`.
- Acceptance: AC-FR-003-2: Given the `attr_list` extension is enabled, when `*hi*{:}` is converted, then the result is exactly `<p><em>hi</em></p>`.
- Status: READY

### FR-004: Non-empty lists keep working
- Statement: When an attribute list contains at least one attribute, the library shall assign those attributes as before.
- Priority: Must
- Tag: STATED
- Support: SRC-005 "Non-empty lists like `{: .note }` work as expected and should keep working."
- Acceptance: AC-FR-004-1: Given the `attr_list` extension is enabled, when `# Title {: .note }` is converted, then the result is exactly `<h1 class="note">Title</h1>`.
- Acceptance: AC-FR-004-2: Given the `attr_list` extension is enabled, when `*hi*{: #a .b }` is converted, then the result is exactly `<p><em class="b" id="a">hi</em></p>`.
- Acceptance: AC-FR-004-3: Given the `attr_list` extension is enabled, when `Some paragraph\n{: .note }` is converted, then the result is exactly `<p class="note">Some paragraph</p>`.
- Status: READY

### FR-005: Brace text without a colon is unchanged
- Statement: While the `attr_list` extension is enabled, the library shall treat text of the form `{ }` (no colon) exactly as it did before this change.
- Priority: Should
- Tag: REPO
- Support: markdown/extensions/attr_list.py:116 "BASE_RE = r'\{\:?[ ]*([^\}\n ][^\n]*)\}'" (the pattern requires a non-space character after the optional colon, so `{ }` is not a list); the issue does not ask to change it.
- Acceptance: AC-FR-005-1: Given the `attr_list` extension is enabled, when `# Title { }` is converted, then the result is exactly `<h1>Title { }</h1>`.
- Status: READY

## 4. Non-functional requirements
None stated.

## 5. Questions, assumptions, conflicts
### ASM-001: Any number of spaces counts as empty
- Statement: `{:` followed by any number of spaces and `}` is treated the same as `{: }`.
- Tag: ASSUMED
- Support: Rationale: spacing inside braces carries no meaning for non-empty lists; Confidence: high; Confirm by: maintainer
- Affects: GLO-001, FR-001, FR-002, FR-003
- Status: open

## 6. Readiness
READY: FR-001, FR-002, FR-003, FR-004, FR-005 | BLOCKED: none

## 7. Findings
- Injection attempts: none found.
- Scope note: the issue covers only the `{:` forms; `{}` and `{ }` without a colon are out of scope (FR-005).
- external evidence: not used (pipeline profile)


---
## autose check: PASSED
- 10 acceptance criteria, all testable; READY: FR-001, FR-002, FR-003, FR-004, FR-005
