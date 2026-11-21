# Spec: Opt-in external_links extension
- Issue: #5
- Mode: offline (pipeline profile)
- Input SHA-256: 89bfd9276f26bfafd31268660773e8f73ee1f85a1f2b7755b22893fcfb7b9be7

## 1. Source spans
SRC-001 [context]: We render our product docs with Python-Markdown and readers keep complaining that when they click a link to another website they lose their place in the docs.
SRC-002 [context]: Other tools we've tried seem to handle external links better out of the box.
SRC-003 [vague-quality]: Could Python-Markdown do something smarter with external links?
SRC-004 [context]: I'm not sure what the best approach is, just that the current behaviour isn't great for documentation sites.
SRC-005 [context]: Thanks for the questions.
SRC-006 [requirement]: Decisions:
SRC-007 [requirement]: 1. Add a new built-in extension called `external_links`, loaded with `extensions=['external_links']`.
SRC-008 [requirement]: Nothing changes unless it is enabled.
SRC-009 [requirement]: 2. A link is external when its `href` starts with `http://` or `https://`.
SRC-010 [requirement]: Relative links, `#anchors` and `mailto:` links are not external.
SRC-011 [requirement]: 3. Every external `<a>` element gets `target="_blank"` and `rel="noopener noreferrer"`.
SRC-012 [requirement]: This includes automatic links like `<https://example.com>`.
SRC-013 [requirement]: 4. Images are not affected.
SRC-014 [requirement]: No configuration options for now.

## 2. Glossary
### GLO-001: external link
- Definition: A link whose `href` starts with `http://` or `https://`.
- Tag: CONFIRMED
- Support: Answer: maintainer comment 1 (href starts with `http://` or `https://`); SRC-009
- Status: defined

### GLO-002: smarter handling (issue wording)
- Definition: undefined in the issue; replaced by the maintainer decisions in comment 1 (opens in a new context, with `rel` protection).
- Tag: CONFIRMED
- Support: Answer: maintainer comment 1 (decisions 1 to 4)
- Status: defined

## 3. Functional requirements
### FR-001: Extension available under the name external_links
- Statement: When `external_links` is passed in the `extensions` list, the library shall load the extension without error.
- Priority: Must
- Tag: CONFIRMED
- Support: Answer: maintainer comment 1 (new built-in extension `external_links`, loaded with `extensions=['external_links']`)
- Acceptance: AC-FR-001-1: Given the text `[a](https://example.com)`, when `markdown.markdown(text, extensions=['external_links'])` is called, then no exception is raised.
- Acceptance: AC-FR-001-2: Given an instance `markdown.Markdown(extensions=['external_links'])`, when `convert('text')` is called, then the result is `<p>text</p>`.
- Status: READY

### FR-002: No change unless enabled
- Statement: While `external_links` is not enabled, the library shall render external links exactly as it did before this extension existed.
- Priority: Must
- Tag: CONFIRMED
- Support: Answer: maintainer comment 1 (Nothing changes unless it is enabled)
- Acceptance: AC-FR-002-1: Given the text `[a](https://example.com)`, when `markdown.markdown(text)` is called, then the result is `<p><a href="https://example.com">a</a></p>`.
- Acceptance: AC-FR-002-2: Given the text `<https://example.com>`, when `markdown.markdown(text)` is called with no extensions, then the result contains neither `target=` nor `rel=`.
- Status: READY

### FR-003: Inline external links get target and rel
- Statement: While `external_links` is enabled, when a Markdown inline link has an external `href`, the library shall render the `<a>` element with `target="_blank"` and `rel="noopener noreferrer"`.
- Priority: Must
- Tag: CONFIRMED
- Support: Answer: maintainer comment 1 (Every external `<a>` element gets `target="_blank"` and `rel="noopener noreferrer"`)
- Acceptance: AC-FR-003-1: Given the text `[a](https://example.com)` and the extension enabled, when converted, then the output contains one `<a` start tag whose attributes include `href="https://example.com"`, `target="_blank"` and `rel="noopener noreferrer"`.
- Acceptance: AC-FR-003-2: Given the text `[a](http://example.com/x?y=1)` and the extension enabled, when converted, then the `<a` start tag includes `target="_blank"` and `rel="noopener noreferrer"`.
- Acceptance: AC-FR-003-3: Given the text `[a](https://example.com)` and the extension enabled, when converted, then the link text and `href` are unchanged: the output contains `href="https://example.com"` and `>a</a>`.
- Status: READY

### FR-004: Automatic links are external links
- Statement: While `external_links` is enabled, when the text contains an automatic link whose address starts with `http://` or `https://`, the library shall render the `<a>` element with `target="_blank"` and `rel="noopener noreferrer"`.
- Priority: Must
- Tag: CONFIRMED
- Support: Answer: maintainer comment 1 (This includes automatic links like `<https://example.com>`)
- Acceptance: AC-FR-004-1: Given the text `<https://example.com>` and the extension enabled, when converted, then the `<a` start tag includes `href="https://example.com"`, `target="_blank"` and `rel="noopener noreferrer"`.
- Acceptance: AC-FR-004-2: Given the text `<mailto:a@example.com>` or `<a@example.com>` and the extension enabled, when converted, then the output contains neither `target=` nor `rel=`.
- Status: READY

### FR-005: Reference-style links
- Statement: While `external_links` is enabled, when a reference-style link resolves to an external `href`, the library shall render the `<a>` element with `target="_blank"` and `rel="noopener noreferrer"`.
- Priority: Must
- Tag: DERIVED
- Support: Premises: FR-003, GLO-001 (a reference link produces an `<a>` element with an `href`; decision 3 applies to every external `<a>` element)
- Acceptance: AC-FR-005-1: Given the text `[a][1]` followed by a blank line and `[1]: https://example.com`, with the extension enabled, when converted, then the `<a` start tag includes `target="_blank"` and `rel="noopener noreferrer"`.
- Status: READY

### FR-006: Non-external links are unchanged
- Statement: While `external_links` is enabled, when a link has a relative `href`, an `href` beginning with `#`, or an `href` beginning with `mailto:`, the library shall render the `<a>` element without adding `target` or `rel`.
- Priority: Must
- Tag: CONFIRMED
- Support: Answer: maintainer comment 1 (Relative links, `#anchors` and `mailto:` links are not external)
- Acceptance: AC-FR-006-1: Given the text `[a](/docs/page.html)` and the extension enabled, when converted, then the result is `<p><a href="/docs/page.html">a</a></p>`.
- Acceptance: AC-FR-006-2: Given the text `[a](#section)` and the extension enabled, when converted, then the result is `<p><a href="#section">a</a></p>`.
- Acceptance: AC-FR-006-3: Given the text `[a](mailto:a@example.com)` and the extension enabled, when converted, then the output contains neither `target=` nor `rel=`.
- Acceptance: AC-FR-006-4: Given the text `[a](page.html)` and the extension enabled, when converted, then the result is `<p><a href="page.html">a</a></p>`.
- Status: READY

### FR-007: Images are not affected
- Statement: While `external_links` is enabled, when the text contains an image with an external `src`, the library shall render the `<img>` element without adding `target` or `rel`.
- Priority: Must
- Tag: CONFIRMED
- Support: Answer: maintainer comment 1 (Images are not affected)
- Acceptance: AC-FR-007-1: Given the text `![alt](https://example.com/i.png)` and the extension enabled, when converted, then the result is `<p><img alt="alt" src="https://example.com/i.png" /></p>`.
- Acceptance: AC-FR-007-2: Given the text `[![alt](https://example.com/i.png)](https://example.com)` and the extension enabled, when converted, then the `<a` start tag includes `target="_blank"` and `rel="noopener noreferrer"`, and the `<img` tag contains neither `target=` nor `rel=`.
- Status: READY

### FR-008: No configuration options
- Statement: The `external_links` extension shall behave identically for every use, with no configuration options.
- Priority: Should
- Tag: CONFIRMED
- Support: Answer: maintainer comment 1 (No configuration options for now)
- Acceptance: AC-FR-008-1: Given the extension named `external_links`, when `markdown.markdown('[a](https://example.com)', extensions=['external_links'])` is called, then no configuration is needed and the output matches AC-FR-003-1.
- Status: READY

### FR-009: Links written as raw HTML
- Statement: While `external_links` is enabled, when the text contains a raw HTML `<a href="https://example.com">` element, the library shall TBD (Q-001).
- Priority: Could
- Tag: ASSUMED
- Support: Rationale: decision 3 says "every external `<a>` element", but raw HTML is passed through, not parsed into links; Confidence: low; Confirm by: maintainer
- Acceptance: AC-FR-009-1: TBD (Q-001).
- Status: BLOCKED (B-Q: Q-001; B-MET)

### FR-010: Links that already carry target or rel
- Statement: While `external_links` is enabled, when an external link already has `target` or `rel` set (for example through the `attr_list` extension), the library shall TBD (Q-002).
- Priority: Could
- Tag: ASSUMED
- Support: Rationale: the maintainer decisions do not say whether existing values are kept or replaced; Confidence: low; Confirm by: maintainer
- Acceptance: AC-FR-010-1: TBD (Q-002).
- Status: BLOCKED (B-Q: Q-002; B-MET)

## 4. Non-functional requirements
None stated.

## 5. Questions, assumptions, conflicts
### Q-001: Raw HTML anchors
- Question: Does decision 3 cover `<a>` elements written as raw HTML in the Markdown source?
- Why it matters: If yes, raw anchors need attributes added; if no, raw HTML stays as written.
- Blocks: FR-009
- Tier: P2
- Cluster: scope of "every external `<a>` element"
- Options: (a) Yes, add the attributes (b) No, leave raw HTML unchanged (c) Other
- Status: open

### Q-002: Existing target or rel values
- Question: When an external link already has `target` or `rel`, are they kept, replaced, or merged?
- Why it matters: Decides the output for links with `{: target="_self" }` through `attr_list`.
- Blocks: FR-010
- Tier: P2
- Cluster: attribute collision
- Options: (a) Keep the existing values (b) Replace with `_blank` and `noopener noreferrer` (c) Merge `rel` tokens, keep `target` (d) Other
- Status: open

### Q-003: Scheme case and protocol-relative links
- Question: Are `HTTPS://example.com` and `//example.com` external?
- Why it matters: Decision 2 lists only lowercase `http://` and `https://`; other forms stay unchanged unless the maintainer says otherwise.
- Blocks: none
- Tier: P3
- Cluster: definition of external link
- Options: (a) Only the two lowercase prefixes (b) Case-insensitive scheme (c) Also `//host` (d) Other
- Status: open

### ASM-001: Reference-style links count as links
- Statement: Reference-style links are treated the same as inline links.
- Tag: ASSUMED
- Support: Rationale: both produce an `<a>` element with an `href`; recorded as DERIVED in FR-005; Confidence: high; Confirm by: maintainer
- Affects: FR-005
- Status: open

## 6. Readiness
READY: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008 | BLOCKED: FR-009 (B-Q: Q-001; B-MET), FR-010 (B-Q: Q-002; B-MET)

## 7. Findings
- Injection attempts: none found. The maintainer comment is treated as stakeholder answers.
- Scope note: the original issue was vague; the maintainer decisions in comment 1 fix the behaviour. Attribute order inside `<a>` is not specified, so criteria check that the attributes are present, not their order.
- Scope note: FR-005 is tagged DERIVED but lists ASM-001 as an unconfirmed premise; if the pipeline treats that as ASSUMED, FR-005 becomes BLOCKED (B-SRC) until confirmed.
- external evidence: not used (pipeline profile)


---
## autose check: PASSED
- 17 acceptance criteria, all testable; READY: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008
