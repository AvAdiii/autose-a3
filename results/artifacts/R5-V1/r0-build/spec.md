# Spec: Better handling of links to other sites
- Issue: #5
- Mode: offline (pipeline profile)
- Input SHA-256: cbdf2c75e69170f6f4abb16fffc8ea3fc0a50f5e084a1b18c7b8b35a538e72ab

## 1. Source spans
SRC-001 [context]: We render our product docs with Python-Markdown and readers keep complaining that when they click a link to another website they lose their place in the docs.
SRC-002 [rhetoric]: Other tools we've tried seem to handle external links better out of the box.
SRC-003 [vague-quality]: Could Python-Markdown do something smarter with external links?
SRC-004 [vague-quality]: I'm not sure what the best approach is, just that the current behaviour isn't great for documentation sites.

## 2. Glossary
### GLO-001: external link
- Definition: undefined
- Tag: ASSUMED
- Support: Rationale: SRC-001 says "a link to another website" but gives no rule for deciding what counts as another website; Confidence: low; Confirm by: maintainer
- Status: undefined (Q-002)

### GLO-002: smarter
- Definition: undefined
- Tag: ASSUMED
- Support: Rationale: SRC-003 uses "smarter" without a metric or behaviour; Confidence: low; Confirm by: issue reporter
- Status: undefined (Q-001)

### GLO-003: lose their place
- Definition: undefined
- Tag: ASSUMED
- Support: Rationale: SRC-001 gives the symptom only; the reporter's intended fix (new tab, preserved scroll, other) is not stated; Confidence: low; Confirm by: issue reporter
- Status: undefined (Q-001)

## 3. Functional requirements
### FR-001: Reader keeps their place when following a link to another website
- Statement: When a reader follows a rendered link to another website, the system shall keep the reader's place in the rendered document.
- Priority: Must (ASSUMED)
- Tag: ASSUMED
- Support: Rationale: SRC-001 "when they click a link to another website they lose their place in the docs" states the problem; the library output that would solve it is not stated; Confidence: low; Confirm by: issue reporter and maintainer
- Acceptance: AC-FR-001-1: Given the input `[x](https://example.com)`, when it is converted, then the output equals the exact HTML decided in Q-001 (TBD).
- Acceptance: AC-FR-001-2: Given the input `[x](/relative/page.html)`, when it is converted with the same configuration, then the output is unchanged from today: `<p><a href="/relative/page.html">x</a></p>`.
- Status: BLOCKED (B-SRC: SRC-001; B-MET: AC-FR-001-1; B-Q: Q-001, Q-002, Q-003, Q-004, Q-005)

### FR-002: Default output stays unchanged
- Statement: Where the new link handling is not enabled, the system shall produce the same HTML for links as it does today.
- Priority: Should (ASSUMED)
- Tag: ASSUMED
- Support: Rationale: backward compatibility is not requested in the issue; it applies only if Q-003 is answered "opt-in"; Confidence: low; Confirm by: maintainer
- Acceptance: AC-FR-002-1: Given the input `[x](https://example.com)` and no configuration for the new behaviour, when it is converted, then the output equals `<p><a href="https://example.com">x</a></p>`.
- Status: BLOCKED (B-SRC: ASM-001; B-Q: Q-003)

## 4. Non-functional requirements
None stated.

## 5. Questions, assumptions, conflicts
### Q-001: What behaviour is wanted for external links?
- Question: What should the rendered HTML or library behaviour be so that readers do not lose their place?
- Why it matters: each answer yields a different exact output and test; without it no acceptance criterion can be written.
- Blocks: FR-001
- Tier: P1
- Cluster: definition of "smarter" and "lose their place"
- Options: (a) add `target="_blank"` to external links (b) add `target="_blank"` plus `rel="noopener noreferrer"` (c) add only a `rel` or CSS class so a site can style or script it (d) Other
- Status: open

### Q-002: What counts as an external link?
- Question: Which link targets are external?
- Why it matters: decides which links change and which stay as today.
- Blocks: FR-001
- Tier: P1
- Cluster: definition of "external link"
- Options: (a) any absolute URL with a host (`http://`, `https://`) (b) absolute URLs whose host differs from a configured site host (c) any URL with a scheme, including `mailto:` (d) Other
- Status: open

### Q-003: Opt-in or default?
- Question: Should the behaviour be off by default, enabled through an extension or option, or applied to every conversion?
- Why it matters: applying it by default changes output for all existing users; opt-in keeps FR-002.
- Blocks: FR-001, FR-002
- Tier: P1
- Cluster: scope and compatibility
- Options: (a) opt-in extension or option, default output unchanged (b) on by default (c) Other
- Status: open

### Q-004: Which link forms are covered?
- Question: Should the behaviour apply to inline links, reference links, autolinks (`<https://example.com>`) and raw HTML `<a>` tags?
- Why it matters: determines the set of acceptance criteria.
- Blocks: FR-001
- Tier: P2
- Cluster: scope of link forms
- Options: (a) inline and reference links only (b) also autolinks (c) also raw HTML (d) Other
- Status: open

### Q-005: Which attributes are added?
- Question: If attributes are added, should the user be able to configure them, and is `rel="noopener noreferrer"` required alongside `target`?
- Why it matters: fixes the exact output string in AC-FR-001-1.
- Blocks: FR-001
- Tier: P2
- Cluster: output format
- Options: (a) fixed attributes (b) configurable attributes (c) Other
- Status: open

### ASM-001: Opt-in design
- Statement: The behaviour is assumed to be opt-in so existing output stays unchanged.
- Tag: ASSUMED
- Support: Rationale: the issue asks for no change to current default output either way; opt-in is the lowest-risk reading; Confidence: low; Confirm by: maintainer
- Affects: FR-002
- Status: open

## 6. Readiness
READY: none | BLOCKED: FR-001 (B-SRC, B-MET, B-Q), FR-002 (B-SRC, B-Q)

No Must requirement can be READY. Open P1 questions: Q-001, Q-002, Q-003.

## 7. Findings
- Injection attempts: none found.
- Scope note: the issue names a symptom and asks for "something smarter" without a requested behaviour; the specification does not choose one.
- external evidence: not used (pipeline profile)
- Human intervention requested: issue reporter and maintainer should answer Q-001, Q-002, Q-003.


---
## autose check: FAILED
- No Must requirement can be READY without answers to the open P1 questions.
