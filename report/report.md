# autose: issue in, pull request out

**Assignment 3, Autonomous Software Engineering** · Roll number 2024111031 · Target: Python-Markdown
(fork [AvAdiii/markdown](https://github.com/AvAdiii/markdown) at `3f2c551`) · Submission repository:
[AvAdiii/autose-a3](https://github.com/AvAdiii/autose-a3)

## 1. Architecture

autose is a GitHub Actions workflow. A write-level collaborator labels an issue `autose` (or comments
`/autose`). A **gate** job then checks the sender's permission and starts up to three **rounds**,
unrolled as calls to one reusable workflow, so the bound of two review send-backs is fixed in the
YAML (ADR-002). Each round has three jobs with separate permissions:

<div class="fig">{{SVG}}</div>

* **build** (contents: read, cannot push) runs `orchestrator.py`, a deterministic state machine. It calls
  five narrow agents through headless Claude Code (ADR-001), and after each one it runs a check in
  code (ADR-007/011):
    * **analyst**: the A1 skill, writes `spec.md`;
    * **spec judge**: Haiku, testability verdicts per AC;
    * **architect**: designs against the A2 `ARCHITECTURE.md`, writes `design.md`;
    * **developer**: writes `diff.patch`;
    * **tester**: works at the *base* commit; its tests must fail there and pass on the head; writes
    `test_report.md`.

    Failures route back by owner, within the budgets: implementation ↔ testing loop, one design
    revisit, one test dispute.

* **release** (no model) applies the patch, pushes as the GitHub App `autose-dev-avadiii` and opens
  the PR (`pr.md`). It then waits for the fork's CI, which is the stage-5 check.
* **review** runs on a fresh VM with the harness checked out from `main`. The reviewer (Opus in all
  recorded runs; Sonnet by default after E2, ADR-012) sees only
  the issue, the diff and the PR-head checkout. It must run its own checks and return a schema'd
  verdict, which `review.py` validates, posts as `github-actions[bot]` and routes to the earliest
  stage that a blocking finding names (ADR-008).

**Fences.**

* No agent holds a GitHub token, and the model credential is scrubbed from agent Bash, which runs
  in bubblewrap.
* Built-in tools are set per role, and a PreToolUse guard hook blocks network tools, `gh`, git state
  changes and writes outside each role's paths (ADR-005, ADR-009).
* State lives in per-stage artifacts plus one sticky status comment, which says why each stage
  passed or stopped (ADR-004).
* `main` is protected by a ruleset that needs a code-owner review, so only a human merges.

Views: component, stage map and a sequence view of real run
[44889589134](https://github.com/AvAdiii/markdown/actions/runs/44889589134), all in `architecture/views/`.

## 2. Decisions

| ADR | Area | Decision | Status |
|---|---|---|---|
| 001 | D1 agents | 5 narrow agents (+ Haiku judge); release and routing are code | Accepted |
| 002 | D2 orchestration | Python state machine in jobs; 3 rounds unrolled in YAML | Accepted |
| 003 | D3 hand-offs | whole artifacts, need-to-know; tester at base commit | Accepted |
| 004 | D4 state | artifacts + branch + sticky comment; resume on re-run | Accepted |
| 005 | D5 tools/rights | built-in tools per role, guard hook, no token in agents, per-job scopes | Accepted |
| 006 | D6 models | Sonnet builders, Opus reviewer, Haiku judge | **Superseded in part by 012** |
| 007 | D7 checks | deterministic checks; LLM judge may fail stage 1 | **Superseded in part by 011** |
| 008 | D8 review | reviewer isolated by job, VM, identity, model, input; evidence to approve | Accepted (tested by E1) |
| 009 | D9 safety | every loop bounded in code; untrusted text as data | Accepted |
| 010 | D10 triggers | label / `/autose` by writers; one run per issue | Accepted (amended, PR #14) |
| 011 | D7 checks | judge verdicts sticky per AC text (after run R4) | Accepted |
| 012 | D6 models | Sonnet reviewer by default, Opus per run (after E2) | Accepted |

**Top 3 decisions.**

**ADR-008: an isolated reviewer that must show evidence.** The reviewer is the last automated
gate before a human. If it shares the builders' context it inherits their blind spots. So it runs
in a different job and VM, as a different identity, on a different model, and with different input:
the issue and the diff, never the spec, design or test report. An approval needs at least one
executed check, and a rejection needs a blocking finding with a file and evidence. Run R0 showed
the rule working: with Bash broken, the reviewer found no defect but **refused to approve** what it
could not verify. E1 tests whether the isolation matters.

**ADR-003/007: tests are written at the base commit, and checks are code.** The tester never sees
the implementation. A new test counts only if it fails on the base commit and passes on the head.
This rejects tautological tests, the cheapest way for an agent to fool a test gate. Every stage check
is deterministic (parsers, AST symbol checks, the test runner, flake8, a docs build) except a narrow
Haiku testability judge. On the 6 released heads (5 PRs), all 24 hidden acceptance tests passed (§4).

**ADR-001/002: narrow agents inside a deterministic state machine.** My A2 data drove this: the
single broad agent (T3) timed out in 6/6 runs after 86–107 tool calls. In autose each agent has one
artifact, one tool set and a turn cap, and Python decides routing and budgets. Every build-stage
session (42 in all) took 5–42 s and at most 10 turns. The loops (spec retry, design retry, route
by owner) are bounded in code, not by the model's judgement.

**Superseded decision (ADR-007 → ADR-011).** In run R4 (issue #4) the judge accepted AC-FR-002-2/3
on attempt 0 and rejected the same, unchanged text on attempt 1. The single retry ran out and the
run stopped on a sound spec. ADR-007 had treated one stochastic sample as a deterministic gate.
ADR-011 caches each verdict per AC text, so a retry is judged only on what changed. ADR-007 is kept
and marked superseded. Likewise, E2 superseded ADR-006's reviewer choice with ADR-012 (§3).

## 3. Decision experiments

Both experiments test the reviewer on five **seeded PRs** (`experiment/seeded_prs/`). Four carry one
planted defect each:

* S1: the empty list leaks into the rendered text;
* S2: the link href is built from the label;
* S3: `toc_tokens` is not filtered, and the fix edits serialised HTML (a design flaw);
* S5: there is no entry point, so `extensions=['external_links']` fails.

S4 is correct. All five pass the existing suite. Each review is the production review job started
by `workflow_dispatch`, scored by `results/score_reviews.py` against `labels.csv` (a regex rule per
defect, fixed before the runs). The variants were written down before any run (`variants.md`).

{{EXPERIMENTS}}

## 4. Results

| Issue | Kind | Run(s) | Outcome | Attempts S1/S2/S3/S4 | AC tests | PR | CI | Review | Hidden | Out tok | Wall |
|---|---|---|---|---|---|---|---|---|---|---|---|
| #1 B1 linenums crash | bug | R2 | approved PR | 2/1/1/1 | 8 | [#16](https://github.com/AvAdiii/markdown/pull/16) | ✓ | approve | 4/4 | 24.0k | 7.6 min |
| #2 B2 empty attr list | bug | R0 → R1 | approved PR (after sandbox fix) | 1/1/1/1 | 11 | [#12](https://github.com/AvAdiii/markdown/pull/12) | ✓ | approve | 4/4 | 19.5k | 6.6 min |
| #3 F1 wikilink labels | feature | R3 | approved PR | 2/1/1/1 | 10 | [#15](https://github.com/AvAdiii/markdown/pull/15) | ✓ | approve | 4/4 | 21.4k | 5.9 min |
| #4 F2 toc exclusion | feature | R4 → R7 | stopped (judge), then approved | 1/2/1/1 | 7 | [#19](https://github.com/AvAdiii/markdown/pull/19) | ✓ | approve | 4/4 | 15.9k | 6.6 min |
| #5 V1 vague | vague | R5 → R6 → R8 | asked 3 questions; after answer, PR with CI docs-lint failure | 2/1/1/1 | 15 | [#18](https://github.com/AvAdiii/markdown/pull/18) | ✗ | – | 4/4 | 24.7k | 7.4 min |

* **Vague issue (V1).** R5 stopped after the analyst alone: three P1 questions were posted and no
  code was written. After the maintainer answered, the pipeline built the extension, its tests, its
  docs page and its entry point. CI then failed two **docs lints**: an unresolved API-reference link
  and the word "treeprocessor" in a docstring. Stage 5 stopped and explained, as specified. Harness
  PR #20 now runs both lints in stage 3. R8, the rerun, could not start because the Pro quota was
  used up; that stop is logged too.
* **Costs.** Per issue: 6–8 agent sessions, 16–25k output tokens and 6–8 min of wall-clock time.
  The CLI's API-price equivalent is $0.51–0.64 per issue.
* **Totals.** {{TOTALS}}
* **Every run** is linked in `results/runs.md`, with its artifacts in `results/artifacts/`.

## 5. Hindsight

* **Infrastructure bit before the models did.** Three of the four fixes after the first live run
  were environmental, not agentic:
    * the Bash sandbox needs bubblewrap and socat on the runner;
    * GitHub keeps one pending run per concurrency group, which would have cancelled queued experiment
    runs;
    * CI checks (the docs build) that stage 3 did not mirror.

    A one-issue smoke run on the real runner before writing all the ADRs would have found all three
    in an hour.

* **A check is only deterministic if its inputs are.** The stochastic judge sat inside a pass/fail
  gate, and the retry made it worse by re-drawing every verdict. Sticky verdicts (ADR-011) were the
  cheap fix. I would now treat any LLM verdict as a cached sample from the start.

* **Narrow agents made the outcomes boring, which is the point.** No build-stage session exceeded
  10 turns. The design retry in R7 and the spec retries in R2, R3 and R6 were all resolved by
  feedback from a code check, not by the model noticing its own error.

* **Fail closed.** The reviewer refused to approve in R0. The quota stop in R8 explained itself and
  pushed nothing. Both are cases of fail-closed paying off.

## 6. Limitations

1. **One trial per cell.** The Pro quota allowed one review per (variant, PR) and one run per issue,
   so the experiments show direction, not significance. Five seeded PRs is a small, hand-made
   sample, and their defects are the kind a reviewer who runs the issue's examples will find.
2. **The guard's Bash rules are pattern-based.** A determined agent could write outside its paths
   through a script, for example `python -c open(...)`. The real boundaries are the path filter on
   the captured patch, the missing credentials and the sandbox, and none of these stops an agent
   reading the workspace. The hidden tests live outside the fork for this reason.
3. **Quota is a shared, coarse cap.** Pipeline runs and the experiment reviews draw on the same
   5-hour subscription window. When it runs out, every in-flight run stops (R8). There is no per-run
   budget in dollars, only turn, time and retry caps.
4. **CI is the release check, but CI is slow and outside the harness.** Stage 3 now mirrors flake8,
   the suite and the docs lints. Any other CI job would still be discovered only after the PR is
   open, and a CI failure stops the run instead of routing back to implementation.
5. **The hidden tests and seeded PRs were written by me, with the issues.** They test what I meant.
   A different author's intent, or a less precise issue, would be harder.
