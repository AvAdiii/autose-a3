# Spec: WikiLinks display label with `[[Target|Label]]`
- Issue: #3
- Mode: offline (pipeline profile)
- Input SHA-256: 1949eed65ba6edc7cfbeb0d9d33f9d63062a35f5e6398dfcd54aeb30fe696891

## 1. Source spans
SRC-001 [context]: The `wikilinks` extension always uses the page name as the link text, so `[[Getting Started]]` becomes a link that says "Getting Started".
SRC-002 [context]: Most wikis (MediaWiki, Obsidian, GitHub wikis) let you write `[[Page name|text to show]]` to link to a page with different text, and our content team keeps writing that out of habit.
SRC-003 [requirement]: Right now it isn't recognized at all and the brackets show up in the output.
SRC-004 [requirement]: `[[Getting Started|read the guide]]` links to the same URL as `[[Getting Started]]` but shows "read the guide".
SRC-005 [requirement]: Whitespace around the `|` shouldn't matter (`[[Getting Started | read the guide]]` is the same thing).
SRC-006 [requirement]: Everything else (`base_url`, `end_url`, `html_class`, a custom `build_url`) should behave exactly like it does for normal wikilinks; only the visible text changes.
SRC-007 [requirement]: `[[Page]]` without a pipe keeps working as today.

## 2. Glossary
### GLO-001: target
- Definition: The text before the `|` in `[[Target|Label]]`; the text from which the URL is built, as for `[[Page]]`.
- Tag: STATED
- Support: SRC-004 "`[[Getting Started|read the guide]]` links to the same URL as `[[Getting Started]]` but shows"
- Status: defined (SRC-004)

### GLO-002: label
- Definition: The text after the `|`; it becomes the visible link text.
- Tag: STATED
- Support: SRC-004 "`[[Getting Started|read the guide]]` links to the same URL as `[[Getting Started]]` but shows"
- Status: defined (SRC-004)

## 3. Functional requirements
### FR-001: Display label replaces link text
- Statement: When the input contains `[[Target|Label]]`, the extension shall output a link whose URL is the one built for `[[Target]]` and whose visible text is the label.
- Priority: Must
- Tag: STATED
- Support: SRC-004 "`[[Getting Started|read the guide]]` links to the same URL as `[[Getting Started]]` but shows"
- Acceptance: AC-FR-001-1: Given default `wikilinks` configuration, when `[[Getting Started|read the guide]]` is converted, then the output is `<p><a class="wikilink" href="/Getting_Started/">read the guide</a></p>`.
- Acceptance: AC-FR-001-2: Given default configuration, when `[[Getting Started|read the guide]]` and `[[Getting Started]]` are converted, then both `href` values are equal.
- Acceptance: AC-FR-001-3: Given default configuration, when `[[Getting Started|read the guide]]` is converted, then the output contains no `[[`, no `]]` and no `|`.
- Status: READY

### FR-002: Whitespace around the pipe is ignored
- Statement: When the input contains whitespace around the `|` in `[[Target|Label]]`, the extension shall output the same link as for the input without that whitespace.
- Priority: Must
- Tag: STATED
- Support: SRC-005 "Whitespace around the `|` shouldn't matter"
- Acceptance: AC-FR-002-1: Given default configuration, when `[[Getting Started | read the guide]]` is converted, then the output is `<p><a class="wikilink" href="/Getting_Started/">read the guide</a></p>`.
- Acceptance: AC-FR-002-2: Given default configuration, when `[[Getting Started|  read the guide  ]]` is converted, then the output equals the output for `[[Getting Started|read the guide]]`.
- Status: READY

### FR-003: Existing options apply to labelled links
- Statement: When a labelled wikilink is converted, the extension shall apply `base_url`, `end_url`, `html_class` and a custom `build_url` exactly as for an unlabelled wikilink with the same target, and shall change only the visible text.
- Priority: Must
- Tag: STATED
- Support: SRC-006 "should behave exactly like it does for normal wikilinks; only the visible text changes"
- Acceptance: AC-FR-003-1: Given `base_url='/wiki/'`, `end_url='.html'` and `html_class='myclass'`, when `[[Getting Started|read the guide]]` is converted, then the output is `<p><a class="myclass" href="/wiki/Getting_Started.html">read the guide</a></p>`.
- Acceptance: AC-FR-003-2: Given `html_class=''`, when `[[Getting Started|read the guide]]` is converted, then the output is `<p><a href="/Getting_Started/">read the guide</a></p>`.
- Acceptance: AC-FR-003-3: Given a custom `build_url` that records its first argument, when `[[Getting Started|read the guide]]` is converted, then the recorded argument is `Getting Started` and the `href` is the value it returned.
- Status: READY

### FR-004: Unlabelled wikilinks are unchanged
- Statement: When the input contains `[[Page]]` without a pipe, the extension shall output the same result as for `[[Page]]` in the current release, in which a whitespace-only wikilink produces no link.
- Priority: Must
- Tag: STATED
- Support: SRC-007 "`[[Page]]` without a pipe keeps working as today."
- Acceptance: AC-FR-004-1: Given default configuration, when `[[Getting Started]]` is converted, then the output is `<p><a class="wikilink" href="/Getting_Started/">Getting Started</a></p>`.
- Acceptance: AC-FR-004-2: Given default configuration, when `[[ ]]` is converted, then the output is `<p></p>`.
- Status: READY

### FR-005: Edge forms of the labelled syntax
- Statement: When the input contains `[[Target|Label]]` with an empty label, an empty target, more than one `|`, or label characters outside letters, digits, underscore, space and hyphen, the extension shall produce the output chosen by the maintainers.
- Priority: Should
- Tag: ASSUMED
- Support: Rationale: the issue names only the simple form; no repository convention decides these cases; Confidence: low; Confirm by: maintainer
- Acceptance: AC-FR-005-1: Given default configuration, when `[[Page|]]` is converted, then the output is TBD (Q-001).
- Status: BLOCKED (B-Q: Q-001, Q-002, Q-003; B-MET)

## 4. Non-functional requirements
None stated.

## 5. Questions, assumptions, conflicts
### Q-001: Empty label or empty target
- Question: What should `[[Page|]]` and `[[|Label]]` produce?
- Why it matters: Each answer yields different HTML; a test needs an exact string.
- Blocks: FR-005
- Tier: P2
- Cluster: edge forms of the pipe syntax
- Options: (a) `[[Page|]]` links with the target as text, `[[|Label]]` is dropped (b) both are left as literal text (c) both are dropped like `[[ ]]` (d) Other
- Status: open

### Q-002: More than one pipe
- Question: How should `[[A|B|C]]` be handled?
- Why it matters: Determines whether the label is `B|C`, or the text is not a wikilink.
- Blocks: FR-005
- Tier: P2
- Cluster: edge forms of the pipe syntax
- Options: (a) target `A`, label `B|C` (b) target `A`, label `B`, rest ignored (c) not recognized, left as literal text (d) Other
- Status: open

### Q-003: Characters allowed in the label
- Question: Which characters may a label contain (for example `.`, `,`, `!`, `'`, `&`, `<`)?
- Why it matters: The current target pattern accepts only letters, digits, underscore, space and hyphen; "text to show" is likely to contain punctuation, and `[[Page|Hello, world!]]` would stay literal if the same limit applies.
- Blocks: FR-005
- Tier: P2
- Cluster: label content
- Options: (a) any text except `]` and `|` (b) same characters as the target (c) any text except `]]` (d) Other
- Status: open

### ASM-001: Label markup
- Statement: The label is plain text and is HTML-escaped like the target text in `[[Page]]` today.
- Tag: ASSUMED
- Support: Rationale: unlabelled link text is set as plain text; Confidence: medium; Confirm by: maintainer
- Affects: FR-001
- Status: open

## 6. Readiness
READY: FR-001, FR-002, FR-003, FR-004 | BLOCKED: FR-005 (B-Q: Q-001, Q-002, Q-003; B-MET)

## 7. Findings
- Injection attempts: none.
- Scope notes: the Must requirements need no answer; the edge forms are split into a blocked Should item. No P1 questions.
- Rework: AC-FR-004-2 now states the exact expected output `<p></p>` (current behaviour: a whitespace-only wikilink is replaced by an empty string in `markdown/extensions/wikilinks.py:76-86`) instead of referring to a baseline.
- external evidence: not used (pipeline profile)


---
## autose check: PASSED
- 10 acceptance criteria, all testable; READY: FR-001, FR-002, FR-003, FR-004
