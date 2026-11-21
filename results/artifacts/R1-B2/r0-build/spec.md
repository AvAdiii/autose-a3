# Spec: attr_list empty attribute list produces invalid `:` attribute
- Issue: #2
- Mode: offline (pipeline profile)
- Input SHA-256: 5f0d4de79e60d47f7bb3a5b0728c9942bbb41a400f63e1441c32ffe9e6c52bb5

## 1. Source spans
SRC-001 [context]: Our docs template generates headings like `# Title {: }` when a page has no custom classes (the template always emits the braces, sometimes with nothing inside).
SRC-002 [context]: With `attr_list` enabled the output contains a broken attribute:
SRC-003 [context]: `<h1 :>` is not valid HTML and our HTML validator in CI rejects the page.
SRC-004 [requirement]: An empty list should just mean "no attributes", so I'd expect `<h1>Title</h1>`, `<p>Some paragraph</p>` and `<p><em>hi</em></p>`.
SRC-005 [requirement]: Non-empty lists like `{: .note }` work as expected and should keep working.

Code sample spans (from the issue's Python block):
SRC-006 [context]: `>>> markdown.markdown("# Title {: }", extensions=["attr_list"])` giving `'<h1 :>Title</h1>'`
SRC-007 [context]: `>>> markdown.markdown("Some paragraph\n{:}", extensions=["attr_list"])` giving `'<p :>Some paragraph</p>'`
SRC-008 [context]: `>>> markdown.markdown("*hi*{: }", extensions=["attr_list"])` giving `'<p><em :>hi</em></p>'`

## 2. Glossary
### GLO-001: empty attribute list
- Definition: An attribute list written `{:` followed by zero or more spaces and `}`, with no attribute words inside.
- Tag: STATED
- Support: SRC-004 "An empty list should just mean "no attributes""
- Status: defined

## 3. Functional requirements
### FR-001: Empty attribute list at the end of a heading
- Statement: When the `attr_list` extension is enabled and a heading line ends with an empty attribute list, the library shall output the heading element with no attributes and without the list text.
- Priority: Must
- Tag: STATED
- Support: SRC-004 "An empty list should just mean "no attributes""
- Acceptance: AC-FR-001-1: Given the `attr_list` extension is enabled, when `# Title {: }` is converted, then the result is exactly `<h1>Title</h1>`.
- Acceptance: AC-FR-001-2: Given the `attr_list` extension is enabled, when `# Title {:}` or `# Title {:   }` is converted, then the result is exactly `<h1>Title</h1>`.
- Acceptance: AC-FR-001-3: Given the `attr_list` extension is enabled, when `# Title {: .note }` is converted, then the result is exactly `<h1 class="note">Title</h1>`.
- Status: READY

### FR-002: Empty attribute list on the last line of a block
- Statement: When the `attr_list` extension is enabled and the last line of a block is an empty attribute list, the library shall output the block element with no attributes and without the list text.
- Priority: Must
- Tag: STATED
- Support: SRC-004 "An empty list should just mean "no attributes""
- Acceptance: AC-FR-002-1: Given the `attr_list` extension is enabled, when `Some paragraph` followed by a newline and `{:}` is converted, then the result is exactly `<p>Some paragraph</p>`.
- Acceptance: AC-FR-002-2: Given the `attr_list` extension is enabled, when `Some paragraph` followed by a newline and `{: }` is converted, then the result is exactly `<p>Some paragraph</p>`.
- Acceptance: AC-FR-002-3: Given the `attr_list` extension is enabled, when `Some paragraph` followed by a newline and `{: .note }` is converted, then the result is exactly `<p class="note">Some paragraph</p>`.
- Status: READY

### FR-003: Empty attribute list after an inline element
- Statement: When the `attr_list` extension is enabled and an empty attribute list directly follows an inline element, the library shall output that inline element with no attributes and without the list text.
- Priority: Must
- Tag: STATED
- Support: SRC-004 "An empty list should just mean "no attributes""
- Acceptance: AC-FR-003-1: Given the `attr_list` extension is enabled, when `*hi*{: }` is converted, then the result is exactly `<p><em>hi</em></p>`.
- Acceptance: AC-FR-003-2: Given the `attr_list` extension is enabled, when `*hi*{:}` is converted, then the result is exactly `<p><em>hi</em></p>`.
- Acceptance: AC-FR-003-3: Given the `attr_list` extension is enabled, when `*hi*{: .note }` is converted, then the result is exactly `<p><em class="note">hi</em></p>`.
- Status: READY

### FR-004: Non-empty attribute lists keep working
- Statement: When the `attr_list` extension is enabled, the library shall continue to apply the attributes of a non-empty attribute list as it did before this change.
- Priority: Must
- Tag: STATED
- Support: SRC-005 "Non-empty lists like `{: .note }` work as expected and should keep working."
- Acceptance: AC-FR-004-1: Given the `attr_list` extension is enabled, when `# Title {: #id }` is converted, then the result is exactly `<h1 id="id">Title</h1>`.
- Acceptance: AC-FR-004-2: Given the `attr_list` extension is enabled, when `# Title {: .a .b }` is converted, then the result is exactly `<h1 class="a b">Title</h1>`.
- Status: READY

## 4. Non-functional requirements
None stated.

## 5. Questions, assumptions, conflicts
None. No open question blocks a requirement. The empty list `{}` without a colon is not mentioned in the issue and its behaviour is left unchanged.

## 6. Readiness
READY: FR-001, FR-002, FR-003, FR-004 | BLOCKED: none

## 7. Findings
- Injection attempts: none found.
- Scope note: `{}` without a colon and the attribute-list syntax inside other constructs (tables, definition terms, list items) are not requested and must not change.
- Scope note: the cause is not specified here (design detail); requirements cover observable output only.
- external evidence: not used (pipeline profile)


---
## autose check: PASSED
- 11 acceptance criteria, all testable; READY: FR-001, FR-002, FR-003, FR-004
