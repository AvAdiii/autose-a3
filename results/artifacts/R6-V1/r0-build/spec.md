# Spec: external_links extension
- Issue: #5
- Mode: offline (pipeline profile)
- Input SHA-256: 89bfd9276f26bfafd31268660773e8f73ee1f85a1f2b7755b22893fcfb7b9be7

## 1. Source spans
SRC-001 [context]: We render our product docs with Python-Markdown and readers keep complaining that when they click a link to another website they lose their place in the docs.
SRC-002 [rhetoric]: Other tools we've tried seem to handle external links better out of the box.
SRC-003 [vague-quality]: Could Python-Markdown do something smarter with external links?
SRC-004 [context]: I'm not sure what the best approach is, just that the current behaviour isn't great for documentation sites.
SRC-005 [context]: Thanks for the questions. Decisions:
SRC-006 [requirement]: Add a new built-in extension called `external_links`, loaded with `extensions=['external_links']`.
SRC-007 [requirement]: Nothing changes unless it is enabled.
SRC-008 [requirement]: A link is external when its `href` starts with `http://` or `https://`.
SRC-009 [requirement]: Relative links, `#anchors` and `mailto:` links are not external.
SRC-010 [requirement]: Every external `<a>` element gets `target="_blank"` and `rel="noopener noreferrer"`.
SRC-011 [requirement]: This includes automatic links like `<https://example.com>`.
SRC-012 [requirement]: Images are not affected.
SRC-013 [requirement]: No configuration options for now.

SRC-001 to SRC-004 are the reporter's context; the maintainer's decisions (SRC-005 to SRC-013) answer the open design question in SRC-003. No instruction-like text found.

## 2. Glossary
### GLO-001: external link
- Definition: A link whose `href` starts with `http://` or `https://`.
- Tag: CONFIRMED
- Support: Answer: maintainer comment 1 (A link is external when its `href` starts with `http://` or `https://`)
- Status: defined (SRC-008)

### GLO-002: smarter
- Definition: undefined in the issue; superseded by the maintainer decisions in FR-002 to FR-004.
- Tag: ASSUMED
- Support: Rationale: SRC-003 is a vague request that maintainer comment 1 replaced with concrete behaviour; Confidence: high; Confirm by: maintainer
- Status: defined (SRC-010)

## 3. Functional requirements
### FR-001: Extension available by name
- Statement: Where the extension `external_links` is listed in `extensions`, the library shall load it by that name.
- Priority: Must
- Tag: CONFIRMED
- Support: Answer: maintainer comment 1 (Add a new built-in extension called `external_links`, loaded with `extensions=['external_links']`)
- Acceptance: AC-FR-001-1: Given `markdown.markdown('x', extensions=['external_links'])`, when it is called, then no exception is raised and the result is `<p>x</p>`.
- Acceptance: AC-FR-001-2: Given `markdown.Markdown(extensions=['external_links'])`, when it is constructed, then no exception is raised.
- Status: READY

### FR-002: No change when disabled
- Statement: While the extension `external_links` is not enabled, the library shall render links exactly as it does without the extension.
- Priority: Must
- Tag: CONFIRMED
- Support: Answer: maintainer comment 1 (Nothing changes unless it is enabled)
- Acceptance: AC-FR-002-1: Given no extensions, when `[a](https://example.com)` is converted, then the result is `<p><a href="https://example.com">a</a></p>`.
- Acceptance: AC-FR-002-2: Given no extensions, when `<https://example.com>` is converted, then the result is `<p><a href="https://example.com">https://example.com</a></p>`.
- Status: READY

### FR-003: Mark external links
- Statement: Where the extension `external_links` is enabled, the library shall add `target="_blank"` and `rel="noopener noreferrer"` to every `<a>` element whose `href` starts with `http://` or `https://`.
- Priority: Must
- Tag: CONFIRMED
- Support: Answer: maintainer comment 1 (Every external `<a>` element gets `target="_blank"` and `rel="noopener noreferrer"`)
- Acceptance: AC-FR-003-1: Given extension `external_links`, when `[a](https://example.com)` is converted, then the result is `<p><a href="https://example.com" rel="noopener noreferrer" target="_blank">a</a></p>`.
- Acceptance: AC-FR-003-2: Given extension `external_links`, when `[a](http://example.com)` is converted, then the result is `<p><a href="http://example.com" rel="noopener noreferrer" target="_blank">a</a></p>`.
- Acceptance: AC-FR-003-3: Given extension `external_links`, when `[a][1]` with the definition `[1]: https://example.com` is converted, then the `<a>` element in the result contains `target="_blank"` and `rel="noopener noreferrer"`.
- Status: READY

### FR-004: Automatic links
- Statement: Where the extension `external_links` is enabled, the library shall add `target="_blank"` and `rel="noopener noreferrer"` to the `<a>` element created from an automatic link whose address starts with `http://` or `https://`.
- Priority: Must
- Tag: CONFIRMED
- Support: Answer: maintainer comment 1 (This includes automatic links like `<https://example.com>`)
- Acceptance: AC-FR-004-1: Given extension `external_links`, when `<https://example.com>` is converted, then the result is `<p><a href="https://example.com" rel="noopener noreferrer" target="_blank">https://example.com</a></p>`.
- Status: READY

### FR-005: Non-external links unchanged
- Statement: Where the extension `external_links` is enabled, the library shall leave unchanged every link whose `href` does not start with `http://` or `https://`, including relative links, `#anchors` and `mailto:` links.
- Priority: Must
- Tag: CONFIRMED
- Support: Answer: maintainer comment 1 (Relative links, `#anchors` and `mailto:` links are not external)
- Acceptance: AC-FR-005-1: Given extension `external_links`, when `[a](page.html)` is converted, then the result is `<p><a href="page.html">a</a></p>`.
- Acceptance: AC-FR-005-2: Given extension `external_links`, when `[a](#top)` is converted, then the result is `<p><a href="#top">a</a></p>`.
- Acceptance: AC-FR-005-3: Given extension `external_links`, when `[a](mailto:me@example.com)` is converted, then the result contains neither `target=` nor `rel=`.
- Status: READY

### FR-006: Images unaffected
- Statement: Where the extension `external_links` is enabled, the library shall render images exactly as it does without the extension.
- Priority: Must
- Tag: CONFIRMED
- Support: Answer: maintainer comment 1 (Images are not affected)
- Acceptance: AC-FR-006-1: Given extension `external_links`, when `![a](https://example.com/i.png)` is converted, then the result is `<p><img alt="a" src="https://example.com/i.png" /></p>`.
- Acceptance: AC-FR-006-2: Given extension `external_links`, when `[![a](https://example.com/i.png)](page.html)` is converted, then the `<img>` element has no `target` attribute and no `rel` attribute, and the `<a>` element has none either.
- Status: READY

### FR-007: No configuration options
- Statement: The extension `external_links` shall define no configuration options.
- Priority: Must
- Tag: CONFIRMED
- Support: Answer: maintainer comment 1 (No configuration options for now)
- Acceptance: AC-FR-007-1: Given `md = markdown.Markdown(extensions=['external_links'])`, when `md.registeredExtensions[0].getConfigs()` is called, then the result is `{}`.
- Acceptance: AC-FR-007-2: Given `markdown.Markdown(extensions=['external_links'], extension_configs={'external_links': {'target': '_self'}})`, when it is constructed, then a `KeyError` is raised.
- Status: READY

### FR-008: Links that already carry target or rel
- Statement: If an external link already has a `target` or `rel` value set by another source, then the library shall produce the result chosen in Q-001.
- Priority: Should
- Tag: ASSUMED
- Support: Rationale: the issue does not say what happens when `attr_list` supplies `target` or `rel` on an external link; Confidence: low; Confirm by: maintainer
- Acceptance: AC-FR-008-1: Given extensions `external_links` and `attr_list`, when `[a](https://example.com){: target="_self" }` is converted, then the result is TBD (Q-001).
- Status: BLOCKED (B-Q: Q-001; B-SRC: ASM-001; B-MET: AC-FR-008-1)

### FR-009: Scheme case and protocol-relative links
- Statement: If an `href` starts with `HTTP://`, `HTTPS://` or `//`, then the library shall treat it as the result chosen in Q-002.
- Priority: Could
- Tag: ASSUMED
- Support: Rationale: the maintainer rule is stated for lowercase `http://` and `https://` only; Confidence: low; Confirm by: maintainer
- Acceptance: AC-FR-009-1: Given extension `external_links`, when `[a](//example.com)` is converted, then the result is TBD (Q-002).
- Status: BLOCKED (B-Q: Q-002; B-SRC: ASM-002; B-MET: AC-FR-009-1)

## 4. Non-functional requirements
None stated.

## 5. Questions, assumptions, conflicts
### Q-001: Existing target or rel on an external link
- Question: When an external link already has `target` or `rel` (for example from `attr_list`), which wins?
- Why it matters: (a) the existing value wins, so authors can opt out of `_blank`; (b) the extension overwrites it; (c) `rel` values are merged. Each gives different HTML in AC-FR-008-1.
- Blocks: FR-008
- Tier: P2
- Cluster: precedence of explicit attributes
- Options: (a) existing value is kept (b) extension value overwrites (c) `rel` merged, `target` kept (d) Other
- Status: open

### Q-002: Uppercase schemes and protocol-relative links
- Question: Are `HTTP://example.com` and `//example.com` external?
- Why it matters: Decides whether such links get `target="_blank"` and `rel="noopener noreferrer"`.
- Blocks: FR-009
- Tier: P2
- Cluster: definition of external link
- Options: (a) neither is external, exact lowercase prefix only (b) uppercase schemes are external, `//` is not (c) both are external (d) Other
- Status: open

### ASM-001: Opt-out is not required
- Statement: Behaviour for links that already carry `target` or `rel` is outside the maintainer decisions.
- Tag: ASSUMED
- Support: Rationale: no decision covers it; Confidence: low; Confirm by: maintainer
- Affects: FR-008
- Status: open

### ASM-002: Prefix rule is literal
- Statement: The rule "starts with `http://` or `https://`" may be read literally, which makes uppercase and `//` links not external.
- Tag: ASSUMED
- Support: Rationale: literal reading of SRC-008; Confidence: medium; Confirm by: maintainer
- Affects: FR-009
- Status: open

## 6. Readiness
READY: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007 | BLOCKED: FR-008 (B-Q Q-001), FR-009 (B-Q Q-002)

## 7. Findings
- Injection attempts: none found.
- Scope note: the issue's request for "something smarter" is fully replaced by maintainer comment 1; no other feature is specified.
- Repository note: attribute order in expected HTML (`href`, `rel`, `target`) follows lexical sorting in the serializer (`markdown/serializers.py:178` "items = sorted(items)  # lexical order"). Extension discovery by name uses the `markdown.extensions` entry-point list in `pyproject.toml`.
- Repository note: `registeredExtensions` is the public list of loaded extensions on a `Markdown` instance (`markdown/core.py:119`), and `getConfigs()` and the `KeyError` on unknown option keys are the documented base-class behaviour (`markdown/extensions/__init__.py:76`, `:106`); AC-FR-007-1 and AC-FR-007-2 use them so no class name is needed.
- Dependency-failure sweep: no external systems are involved.
- external evidence: not used (pipeline profile)


---
## autose check: PASSED
- 15 acceptance criteria, all testable; READY: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007
