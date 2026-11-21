# Sequence view: one real run

Run [44889589134](https://github.com/AvAdiii/markdown/actions/runs/44889589134), issue
[#2](https://github.com/AvAdiii/markdown/issues/2) (B2, empty attribute list), started by the
maintainer comment `/autose` on 2026-11-21. Times are UTC from the job logs (`[autose hh:mm:ss]`
lines). Every value below is taken from the run's logs and artifacts (`r0-build`, `r0-5-release`,
`r0-6-review`); nothing is illustrative.

```mermaid
sequenceDiagram
    autonumber
    actor M as Maintainer (AvAdiii)
    participant GH as GitHub (issue #2, PR #12)
    participant G as gate job
    participant O as build job: orchestrator.py
    participant A as analyst (Sonnet)
    participant J as spec judge (Haiku)
    participant AR as architect (Sonnet)
    participant D as developer (Sonnet)
    participant T as tester (Sonnet)
    participant R as release job: release.py (App token)
    participant CI as fork CI (ci.yml etc.)
    participant RV as review job: reviewer (Opus) + review.py

    M->>GH: comment "/autose" (09:26:22)
    GH->>G: issue_comment event
    G->>GH: collaborator permission = admin ✓, 👀 reaction, status comment
    G-->>O: trigger.json (issue 2, start_stage=requirements), 09:26:30
    Note over O: sandbox ok (bubblewrap + socat), pip install -e, Claude Code 2.1.323
    O->>A: issue as <untrusted-issue nonce>, SKILL.md + analyst.md
    A-->>O: spec.md: FR-001..FR-004, 11 ACs (41.3 s, 8 turns)
    O->>J: ACs only
    J-->>O: 11/11 testable (4.9 s)
    Note over O: check_spec PASSED: 4 Must READY, 0 open P1 (09:28:04)
    O->>AR: spec.md + ARCHITECTURE.md
    AR-->>O: design.md: Changes table (BASE_RE modify, tests, changelog), AC→test map (30.2 s)
    Note over O: check_design PASSED: symbol AttrListTreeprocessor.BASE_RE exists, all ACs covered, changelog row
    O->>D: spec + design (tests/ is read-only for D)
    D-->>O: edits attr_list.py, changelog.md; ran the suite and flake8 itself (12.4 s)
    Note over O: check_build PASSED: compileall, pip install, import, no new flake8 errors
    O->>T: spec + design, at the BASE commit (tests/** only)
    T-->>O: 11 test methods named after the ACs (13.3 s)
    Note over O: check_tests PASSED: new tests fail on base, pass on head, suite 1114 → 1125, 0 regressions (09:29:21)
    O->>GH: status comment: stages 1-4 passed
    O-->>R: r0-build artifact (diff.patch, spec, design, test_report)
    R->>GH: push 30f9655 to autose/issue-2 as autose-dev-avadiii[bot] (09:29:39)
    R->>GH: update PR #12 body from pr.md (09:29:42)
    GH->>CI: pull_request synchronize
    CI-->>R: 13 check runs green (polled until 09:31:46)
    R-->>RV: pr=12, ci_ok=true
    Note over RV: fresh VM, harness from main, PR head checkout, no build artifacts
    RV->>RV: reviewer gets issue + diff only; runs 6 own checks (incl. 24-input regex comparison) (39.8 s)
    RV->>GH: APPROVED review by github-actions[bot] (09:32:54)
    RV->>GH: status comment: approved; round1/round2 skipped
    M->>GH: reads PR #12 and decides whether to merge (the workflow never merges)
```

## What the run shows

| Property | Evidence in this run |
|---|---|
| Fixed stage order, each with an artifact and a check | `spec.md` → `checks/spec-0.json`, `design.md` → `design-1.json`, `diff.patch` → `build-1.json`, `test_report.md` → `tests-0.json`, `pr.md`/`release.json`, `review.md`/`review.json` |
| The model never holds a GitHub token | pushes and PR edits by `release.py` with the App token; review posted by `review.py` after the agent process exited |
| Tests written against the base | `tests-0.json` `base_new`: the new AC tests fail on the base `bb9e8d8`, pass on head |
| Independent review | different job, VM, model (Opus vs Sonnet), identity (`github-actions` vs the App) and input (no spec/design/test report) |
| Human merges | the run ends with an approved PR; PR #12 stays open until the maintainer merges it |

Total: 6 min 38 s wall-clock, 6 agent sessions, 19,459 output tokens.
