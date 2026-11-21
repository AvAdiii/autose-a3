# Spec: Fenced code block with `linenums`, `guess_lang` or `noclasses` crashes without codehilite
- Issue: #1
- Mode: offline (pipeline profile)
- Input SHA-256: 48ae068b3c169b93ea6909a3987b9af649982f5c19b0ef736ec6261d28b87dd6

## 1. Source spans
SRC-001 [context]: I use `fenced_code` together with `attr_list` and turned off `codehilite` because we highlight on the client with highlight.js.
SRC-002 [context]: Some of our older docs still have `linenums` on their fenced blocks from when we used Pygments, and now the build blows up on them.
SRC-003 [context]: Minimal example:
SRC-004 [context]: `TypeError: cannot serialize None (type NoneType)`
SRC-005 [context]: `linenums="true"` gives `TypeError: cannot serialize True (type bool)` instead.
SRC-006 [requirement]: Same story with `guess_lang` and `noclasses`.
SRC-007 [requirement]: Something like `data-x="1"` works fine, and if I add `codehilite` to the extensions everything renders.
SRC-008 [requirement]: I'd expect the block to just render as a normal code block when codehilite isn't there, instead of the whole conversion failing.
SRC-009 [rhetoric]: One stray attribute shouldn't take down the page.
SRC-010 [context]: Markdown 3.x (current main), Python 3.12, Linux.

## 2. Glossary
### GLO-001: normal code block
- Definition: undefined (Q-001)
- Tag: ASSUMED
- Support: Rationale: the issue says "normal code block" but does not say whether the offending attributes appear in the output; Confidence: medium; Confirm by: maintainer
- Status: undefined (Q-001)

### GLO-002: codehilite not enabled
- Definition: the `codehilite` extension is not in the extension list passed to the converter.
- Tag: STATED
- Support: SRC-008 "when codehilite isn't there"
- Status: defined (SRC-008)

## 3. Functional requirements
### FR-001: No exception for highlighter-only attributes without codehilite
- Statement: If a fenced code block with an attribute list contains `linenums`, `guess_lang` or `noclasses`, with or without a value, and `codehilite` is not enabled, then the converter shall render the block as a `<pre><code>` code block and shall not raise an exception.
- Priority: Must
- Tag: STATED
- Support: SRC-008 "I'd expect the block to just render as a normal code block when codehilite isn't there, instead of the whole conversion failing."
- Acceptance: AC-FR-001-1: Given the extensions `fenced_code` and `attr_list` and the source "``` { .python linenums }\nprint(1)\n```", when the source is converted, then no exception is raised and the output contains `<pre><code class="language-python"` and `print(1)`.
- Acceptance: AC-FR-001-2: Given the extensions `fenced_code` and `attr_list` and the source "``` { .python linenums=\"true\" }\nprint(1)\n```", when the source is converted, then no exception is raised and the output contains `<pre><code class="language-python"` and `print(1)`.
- Acceptance: AC-FR-001-3: Given the extensions `fenced_code` and `attr_list` and each of these six sources: "``` { .python guess_lang }\nprint(1)\n```", "``` { .python guess_lang=\"true\" }\nprint(1)\n```", "``` { .python guess_lang=\"false\" }\nprint(1)\n```", "``` { .python noclasses }\nprint(1)\n```", "``` { .python noclasses=\"true\" }\nprint(1)\n```", "``` { .python noclasses=\"false\" }\nprint(1)\n```", when each source is converted, then no exception is raised and the output contains `<pre><code class="language-python"` and `print(1)`.
- Acceptance: AC-FR-001-4: Given the extensions `fenced_code` and `attr_list` and the source "``` { .python }\nprint(1)\n```", when the source is converted, then the output is exactly `<pre><code class="language-python">print(1)\n</code></pre>`.
- Status: READY

### FR-002: Output of highlighter-only attributes without codehilite
- Statement: When a fenced code block with an attribute list contains `linenums`, `guess_lang` or `noclasses` and `codehilite` is not enabled, the converter shall output the attribute in the form chosen in Q-001.
- Priority: Should
- Tag: ASSUMED
- Support: Rationale: the issue asks only for a normal code block and does not say whether these attributes are kept or dropped; Confidence: low; Confirm by: maintainer
- Acceptance: AC-FR-002-1: Given the extensions `fenced_code` and `attr_list` and the source "``` { .python linenums }\nprint(1)\n```", when the source is converted, then the output is exactly TBD (Q-001).
- Status: BLOCKED (B-Q: Q-001; B-MET: AC-FR-002-1; B-SRC: FR-002)

### FR-003: Other attributes keep their current output
- Statement: When a fenced code block with an attribute list contains an attribute other than `linenums`, `guess_lang` and `noclasses`, and `codehilite` is not enabled, the converter shall output that attribute on the `<code>` element as it does today.
- Priority: Must
- Tag: STATED
- Support: SRC-007 "Something like `data-x="1"` works fine"
- Acceptance: AC-FR-003-1: Given the extensions `fenced_code` and `attr_list` and the source "``` { .python data-x=\"1\" }\nprint(1)\n```", when the source is converted, then the output is exactly `<pre><code class="language-python" data-x="1">print(1)\n</code></pre>`.
- Acceptance: AC-FR-003-2: Given the extensions `fenced_code` and `attr_list` and the source "``` { data-test=\"{}\" }\n# Some python code\n```", when the source is converted, then the output is exactly `<pre><code data-test="{}"># Some python code\n</code></pre>`.
- Status: READY

### FR-004: Conversion with codehilite enabled keeps working
- Statement: While `codehilite` is enabled, the converter shall convert a fenced code block that has `linenums`, `guess_lang` or `noclasses` attributes without raising an exception.
- Priority: Must
- Tag: STATED
- Support: SRC-007 "if I add `codehilite` to the extensions everything renders"
- Acceptance: AC-FR-004-1: Given the extensions `fenced_code`, `attr_list` and `codehilite`, and the source "``` { .python linenums=\"true\" }\nprint(1)\n```", when the source is converted, then no exception is raised and the output contains `codehilite`.
- Acceptance: AC-FR-004-2: Given the extensions `fenced_code`, `attr_list` and `codehilite`, and the source "``` { .python linenums=True }\n# Some python code\n```", when the source is converted, then no exception is raised and the output contains `codehilite` and `# Some python code`.
- Status: READY

## 4. Non-functional requirements
None stated.

## 5. Questions, assumptions, conflicts
### Q-001: What happens to the attribute in the output?
- Question: When `linenums`, `guess_lang` or `noclasses` is on a fenced block and `codehilite` is not enabled, what shall the output contain for that attribute?
- Why it matters: The answer fixes the exact HTML that tests compare for FR-002. Dropping the attribute gives `<code class="language-python">`; keeping it gives an extra attribute on `<code>`, and the value text for a valueless flag or for a boolean value must then be defined.
- Blocks: FR-002, GLO-001
- Tier: P2
- Cluster: meaning of "normal code block"
- Options: (a) omit the attribute: `<pre><code class="language-python">print(1)\n</code></pre>` (b) keep it with the value as written, for example `linenums="true"` (c) keep it with a normalised value, for example `linenums="linenums"` for a valueless flag (d) Other
- Status: open

### ASM-001: Crash scope
- Statement: Only `linenums`, `guess_lang` and `noclasses` are affected; `use_pygments` is not.
- Tag: ASSUMED
- Support: Rationale: the issue names the first three; the fourth is converted the same way by the library but the issue does not list it; Confidence: medium; Confirm by: maintainer
- Affects: FR-001
- Status: open

## 6. Readiness
READY: FR-001, FR-003, FR-004 | BLOCKED: FR-002 (B-Q: Q-001; B-MET; B-SRC)

## 7. Findings
- Injection attempts: none found.
- Scope note: the issue asks for a fix of an exception only; the output form of the attributes is left to the maintainer (Q-001). No design or code is specified.
- Rework note: AC-FR-001-3 now lists the six exact sources; AC-FR-004-2 no longer compares against pre-change output and instead pins a fixed source with checkable substrings. The "same output as before this change" clause was removed from the FR-004 statement because no fixed pre-change value is given in the issue.
- external evidence: not used (pipeline profile)


---
## autose check: PASSED
- 8 acceptance criteria, all testable; READY: FR-001, FR-003, FR-004
