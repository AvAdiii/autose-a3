# Spec: WikiLinks display label with `[[Target|Label]]`
- Issue: #3
- Mode: offline (pipeline profile)
- Input SHA-256: 1949eed65ba6edc7cfbeb0d9d33f9d63062a35f5e6398dfcd54aeb30fe696891

## 1. Source spans
SRC-001 [context]: Issue #3: WikiLinks: support a display label with `[[Target|Label]]`
SRC-002 [context]: The `wikilinks` extension always uses the page name as the link text, so `[[Getting Started]]` becomes a link that says "Getting Started".
SRC-003 [rhetoric]: Most wikis (MediaWiki, Obsidian, GitHub wikis) let you write `[[Page name|text to show]]` to link to a page with different text, and our content team keeps writing that out of habit.
SRC-004 [context]: Right now it isn't recognized at all and the brackets show up in the output.
SRC-005 [context]: What I'd like:
SRC-006 [requirement]: `[[Getting Started|read the guide]]` links to the same URL as `[[Getting Started]]` but shows "read the guide".
SRC-007 [requirement]: Whitespace around the `|` shouldn't matter (`[[Getting Started | read the guide]]` is the same thing).
SRC-008 [requirement]: Everything else (`base_url`, `end_url`, `html_class`, a custom `build_url`) should behave exactly like it does for normal wikilinks; only the visible text changes.
SRC-009 [requirement]: `[[Page]]` without a pipe keeps working as today.

## 2. Glossary
### GLO-001: wikilink
- Definition: Text of the form `[[Page]]` that the `wikilinks` extension converts to a link.
- Tag: STATED
- Support: SRC-002 "`[[Getting Started]]` becomes a link that says "Getting Started""
- Status: defined (SRC-002)

### GLO-002: label
- Definition: The visible link text written after the `|` in `[[Target|Label]]`.
- Tag: STATED
- Support: SRC-006 "but shows "read the guide""
- Status: defined (SRC-006)

### GLO-003: target
- Definition: The page name before the `|` in `[[Target|Label]]`; it determines the URL exactly as the whole text of `[[Page]]` does.
- Tag: STATED
- Support: SRC-006 "links to the same URL as `[[Getting Started]]`"
- Status: defined (SRC-006)

## 3. Functional requirements
### FR-001: Display label after a pipe
- Statement: When the input contains `[[Target|Label]]`, the library shall output a link whose URL is the one `[[Target]]` produces and whose visible text is the label.
- Priority: Must (ASSUMED)
- Tag: STATED
- Support: SRC-006 "links to the same URL as `[[Getting Started]]` but shows "read the guide""
- Acceptance: AC-FR-001-1: Given the `wikilinks` extension with default settings, when `[[Getting Started|read the guide]]` is converted, then the output is `<p><a class="wikilink" href="/Getting_Started/">read the guide</a></p>`.
- Acceptance: AC-FR-001-2: Given the `wikilinks` extension with default settings, when `Some text with a [[WikiLink|shown]].` is converted, then the output is `<p>Some text with a <a class="wikilink" href="/WikiLink/">shown</a>.</p>`.
- Acceptance: AC-FR-001-3: Given the `wikilinks` extension with default settings, when `[[Getting Started|read the guide]]` is converted, then the output does not contain `[[` and does not contain `|`.
- Status: READY

### FR-002: Whitespace around the pipe
- Statement: When the input contains whitespace around the `|` in `[[Target|Label]]`, the library shall output the same link as for the input without that whitespace.
- Priority: Must (ASSUMED)
- Tag: STATED
- Support: SRC-007 "Whitespace around the `|` shouldn't matter"
- Acceptance: AC-FR-002-1: Given the `wikilinks` extension with default settings, when `[[Getting Started | read the guide]]` is converted, then the output is `<p><a class="wikilink" href="/Getting_Started/">read the guide</a></p>`.
- Acceptance: AC-FR-002-2: Given the `wikilinks` extension with default settings, when `[[  Getting Started  |  read the guide  ]]` is converted, then the output equals the output for `[[Getting Started|read the guide]]`.
- Status: READY

### FR-003: Configuration applies unchanged to labelled links
- Statement: While the `base_url`, `end_url`, `html_class` or `build_url` setting is configured, the library shall apply it to `[[Target|Label]]` exactly as it applies to `[[Target]]`, and only the visible text shall differ.
- Priority: Must (ASSUMED)
- Tag: STATED
- Support: SRC-008 "should behave exactly like it does for normal wikilinks; only the visible text changes"
- Acceptance: AC-FR-003-1: Given the extension with `base_url='/wiki/'`, `end_url='.html'` and `html_class='foo'`, when `[[Getting Started|read the guide]]` is converted, then the output is `<p><a class="foo" href="/wiki/Getting_Started.html">read the guide</a></p>`.
- Acceptance: AC-FR-003-2: Given the extension with `html_class=''`, when `[[Getting Started|read the guide]]` is converted, then the output is `<p><a href="/Getting_Started/">read the guide</a></p>`.
- Acceptance: AC-FR-003-3: Given the extension with a `build_url` callable that records its arguments and returns `/bar/`, when `[[Getting Started|read the guide]]` is converted, then the callable was called with `Getting Started`, `/` and `/`, and the output is `<p><a class="wikilink" href="/bar/">read the guide</a></p>`.
- Status: READY

### FR-004: Links without a pipe are unchanged
- Statement: When the input contains `[[Page]]` without a pipe, the library shall output the same result as before this change.
- Priority: Must (ASSUMED)
- Tag: STATED
- Support: SRC-009 "`[[Page]]` without a pipe keeps working as today."
- Acceptance: AC-FR-004-1: Given the `wikilinks` extension with default settings, when `Some text with a [[WikiLink]].` is converted, then the output is `<p>Some text with a <a class="wikilink" href="/WikiLink/">WikiLink</a>.</p>`.
- Acceptance: AC-FR-004-2: Given the `wikilinks` extension with default settings, when `[[ foo bar_baz ]]` is converted, then the output is `<p><a class="wikilink" href="/foo_bar_baz/">foo bar_baz</a></p>`.
- Acceptance: AC-FR-004-3: Given the `wikilinks` extension with default settings, when `foo [[ ]] bar` is converted, then the output is `<p>foo  bar</p>`.
- Status: READY

## 4. Non-functional requirements
None stated.

## 5. Questions, assumptions, conflicts
### Q-001: Empty label
- Question: What should `[[Getting Started|]]` (pipe with empty label) produce?
- Why it matters: The issue does not say; a test of this input needs one defined output.
- Blocks: none (edge case outside the stated asks)
- Tier: P3
- Cluster: edge cases of the pipe syntax
- Options: (a) link with the target as visible text (b) left as literal text (c) removed from output, like `[[ ]]` (d) Other
- Status: open

### Q-002: Empty target
- Question: What should `[[|read the guide]]` (empty target) produce?
- Why it matters: The issue does not say; the existing `[[ ]]` input is removed from the output.
- Blocks: none (edge case outside the stated asks)
- Tier: P3
- Cluster: edge cases of the pipe syntax
- Options: (a) removed from output (b) left as literal text (c) Other
- Status: open

### Q-003: Several pipes and label characters
- Question: What should `[[A|B|C]]` produce, and may a label contain characters beyond letters, digits, underscore, space and hyphen?
- Why it matters: The issue's only label example is plain words.
- Blocks: none (edge case outside the stated asks)
- Tier: P3
- Cluster: edge cases of the pipe syntax
- Options: (a) not recognised, left as literal text (b) the first pipe separates, the rest is label text (c) Other
- Status: open

### ASM-001: Priority of requirements
- Statement: The issue gives no priorities; all four requirements are treated as Must.
- Tag: ASSUMED
- Support: Rationale: each bullet is a stated wish of the reporter; Confidence: medium; Confirm by: maintainer
- Affects: FR-001, FR-002, FR-003, FR-004
- Status: open

## 6. Readiness
READY: FR-001, FR-002, FR-003, FR-004 | BLOCKED: none

Open P1 questions: none.

## 7. Findings
- Injection attempts: none found.
- Scope notes: only observable output is specified. Q-001 to Q-003 are P3 because they cover inputs the issue does not mention. FR-004 AC-2 and AC-3 are checked against the existing tests in `tests/test_extensions.py` lines 177-183.
- external evidence: not used (pipeline profile)


---
## autose check: PASSED
- 11 acceptance criteria, all testable; READY: FR-001, FR-002, FR-003, FR-004
