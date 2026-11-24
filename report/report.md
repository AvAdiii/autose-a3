# autose: issue in, pull request out

**Assignment 3, Autonomous Software Engineering** · Roll number 2024111031 · Target: Python-Markdown
(fork [AvAdiii/markdown](https://github.com/AvAdiii/markdown) at `3f2c551`) · Submission repository:
[AvAdiii/autose-a3](https://github.com/AvAdiii/autose-a3)

## 1. Architecture

autose is a GitHub Actions workflow. A write-level collaborator labels an issue `autose` (or comments
`/autose`). A **gate** job checks the sender's permission and starts up to three **rounds**,
unrolled as calls to one reusable workflow, so the bound of two review send-backs is fixed in the
YAML (ADR-002). Each round has three jobs with separate permissions.

### 1.1 Component view

<div class="fig">{{SVG}}</div>

* **build** (contents: read, **cannot push**) runs `orchestrator.py`, a deterministic state machine.
  It calls five narrow agents through headless Claude Code (ADR-001) and, after each one, a check
  written in code (ADR-007/011). Failures route back by owner within code-enforced budgets: the
  implementation ↔ testing loop (3 attempts), one design revisit, one test dispute.
* **release** (no model) applies the patch, pushes as the GitHub App `autose-dev-avadiii`, opens
  the PR (`pr.md`) and waits for the fork's CI, which is the stage-5 check.
* **review** runs on a fresh VM with the harness checked out from `main`. The reviewer sees only
  the issue, the diff and the PR-head checkout, must run its own checks and returns a schema'd
  verdict. `review.py` validates it, posts it as `github-actions[bot]` and routes a
  `request_changes` to the earliest stage a blocking finding names (ADR-008).

**Fences (ADR-005, ADR-009).** No agent holds a GitHub token; the model credential is scrubbed
from agent Bash, which runs in bubblewrap. Built-in tools are set per role and a PreToolUse guard
hook blocks network tools, `gh`, git state changes and writes outside each role's paths. Issue
text reaches agents only inside a nonce-tagged `<untrusted-issue>` block. State lives in per-stage
workflow artifacts plus one sticky status comment (ADR-004). `main` is protected by a ruleset that
needs a code-owner review, so only a human merges.

### 1.2 Stage map: agent, artifact and check per stage

| # | Stage | Agent (model) | Job | Artifact | Check (decided by code) | On failure |
|---|---|---|---|---|---|---|
| 1 | Requirements | analyst (Sonnet) + A1 skill; spec judge (Haiku) | build | `spec.md` | every AC is Given/When/Then, no A1 weak word, unique ID, judged testable (verdict sticky per AC text) | 1 retry; open P1 questions → post them, stop `needs-clarification` |
| 2 | Design | architect (Sonnet) + A2 `ARCHITECTURE.md` | build | `design.md` | names ≥1 file and function; every `modify` file/symbol exists (AST); every AC mapped; changelog row | 1 retry, then stop |
| 3 | Implementation | developer (Sonnet) | build | `diff.patch` | non-empty, no `tests/`/`.github/` edits, `compileall`, `pip install -e`, import, flake8, docs build + spelling | retry inside the 3-attempt 3/4 budget |
| 4 | Testing | tester (Sonnet), **at the base commit** | build | `test_report.md` | every AC has a test; new tests **fail on base, pass on head**; full suite passes | back to 3; after 2 failures back to 2 once |
| 5 | Release | none (`release.py`) | release | `pr.md` + PR link | PR open, every CI check on the head `success` | stop; `pr.md` names the failing check |
| 6 | Review | reviewer (Opus in R0–R10; Sonnet from ADR-012) | review | `review.md` + `review.json` | `approve` (needs ≥1 executed check) or rounds used up | earliest stage named by a blocking finding; ≤2 rework rounds |

### 1.3 Sequence view: real run [44889589134](https://github.com/AvAdiii/markdown/actions/runs/44889589134) (issue #2, PR #12)

<div class="fig">{{SEQ}}</div>

All times (UTC) and numbers come from the run's job logs and artifacts. The full Mermaid version,
with every message, is `architecture/views/sequence_view.md`.

## 2. Design decisions

| ADR | Decision | Chosen option | Main option rejected | Main reason | Status |
|---|---|---|---|---|---|
| 001 | D1 splitting work | 5 narrow agents (+ Haiku judge); release and routing in code | one agent for everything | a single agent grades its own work; A2's broad agent timed out 6/6 | Accepted |
| 002 | D2 control flow | Python state machine in jobs; 3 rounds unrolled in YAML | LLM planner choosing the next stage | every routing rule is a function of check results; a planner can skip a check | Accepted |
| 003 | D3 hand-offs | whole artifacts on need-to-know; tester at the base commit | summaries / shared transcript | summaries are lossy and untraceable; a shared transcript shares assumptions | Accepted |
| 004 | D4 state | workflow artifacts + PR branch + sticky comment; resume from `state.json` | artifacts committed on the PR branch | the reviewer would read the builders' reasoning in its checkout | Accepted |
| 005 | D5 tools | built-in tools per role + guard hook; GitHub only via code | GitHub MCP server for agents | puts a write token next to untrusted text | Accepted |
| 006 | D6 models | Sonnet builders, Opus reviewer, Haiku judge | Opus everywhere | ~5× quota; the 5-hour limit after 1–2 issues | **Superseded in part by 012** |
| 007 | D7 checks | deterministic checks; a Haiku judge may fail stage 1 | LLM judge for every stage | non-deterministic and gameable where a test can decide | **Superseded in part by 011** |
| 008 | D8 reviewer | separate job, VM, identity, prompt, input; evidence to approve | reviewer sees spec + design | shared context inherits blind spots (tested: E1) | Accepted, model row amended by 012 |
| 009 | D9 safety | every loop bounded in code; untrusted text as data, no credential | filtering "ignore instructions" text | brittle; removing credentials and tools is enforceable | Accepted |
| 010 | D10 triggers | label / `/autose` by write-level users; one run per issue, queued | any issue author; `cancel-in-progress` | quota and push abuse; a relabel would kill a nearly finished run | Accepted (amended, PR #14) |
| 011 | D7 checks | judge verdicts sticky per AC text (after run R4) | majority vote of 3 judge samples | 3× cost and can still flip on retry | Accepted |
| 012 | D6 models | Sonnet reviewer by default, Opus per run (after E2) | keep Opus | pre-stated rule: a tie supersedes ADR-006; ~40 % less quota | Accepted |

**The three decisions that mattered most.**

**ADR-008: an isolated reviewer that must show evidence.** The reviewer is the last automated gate
before a human; if it shares the builders' context it inherits their blind spots. It runs in a
different job and VM, as a different identity, with a different prompt and different input (the
issue and the diff, never the spec, design or test report). To stop it approving everything, an
approval needs at least one *executed* check, and a rejection needs a blocking finding with a file
and evidence; `review.py` enforces both. Run R0 showed the rule working: with Bash broken, the
reviewer found no defect but **refused to approve** what it could not verify. On the seeded PRs it
rejected 12/12 planted defects and approved 3/3 correct PRs (§3), so it is not a rubber stamp.

**ADR-003/007: tests at the base commit, checks in code.** The tester never sees the
implementation, and a new test counts only if it fails on the base commit and passes on the head.
This rejects tautological tests, the cheapest way for an agent to fool a test gate. Every stage
check is deterministic (parsers, AST symbol checks, the test runner, flake8, docs build) except a
narrow Haiku testability judge. The gates were not decorative: a code check stopped or sent back
work in 7 of the 9 runs that reached an agent, CI caught one more (§4), and every released head
passed all its hidden tests.

**ADR-001/002: narrow agents inside a deterministic state machine.** My A2 data drove this: the
single broad agent there (Qwen3.5-9B, local) timed out in 6/6 runs after 86–107 tool calls. In
autose each agent has one artifact, one tool set and a turn cap, and Python decides routing and
budgets. Every build-stage session (42 in all) took 5–42 s and at most 10 turns.

**Superseded decisions.** In run R4 the judge accepted AC-FR-002-2/3 on attempt 0 and rejected the
same, unchanged text on attempt 1; the single retry ran out and the run stopped on a sound spec.
ADR-007 had treated one stochastic sample as a deterministic gate. ADR-011 caches each verdict per
AC text, so a retry is judged only on what changed; R7 then passed. ADR-007 is kept and marked
superseded. Likewise, experiment E2 superseded ADR-006's reviewer row with ADR-012 (§3).

## 3. Decision experiments

Both experiments test the reviewer on five **seeded PRs** (`experiment/seeded_prs/`, PRs #6–#10).
Four carry one planted defect each: S1 the empty list leaks into the output; S2 the link href is
built from the label; S3 `toc_tokens` is not filtered and the fix edits serialised HTML (a design
flaw); S5 there is no entry point, so `extensions=['external_links']` fails. S4 is correct. All
five pass the existing suite. Each review is the production review job started by
`workflow_dispatch` and scored by `results/score_reviews.py` against `labels.csv` (a regex rule per
defect, fixed before the runs). The variants and hypotheses were written down before any run
(`experiment/variants.md`): **E1 tests ADR-008** (H1: giving the reviewer the PR description, spec
and design rationale lowers detection) and **E2 tests ADR-006** (H2: Sonnet misses defects Opus
finds; a tie supersedes ADR-006).

{{EXPERIMENTS}}

**What changed in the design.** E2 → ADR-012: Sonnet became the default reviewer (harness PR #23),
Opus stays a per-run input. E1 → no change to ADR-008, but its justification is now stated as
"cheap insurance" rather than a measured gain. Giving up model diversity (ADR-012) leaves input
isolation as the main guard against correlated blind spots, which is one more reason to keep it.

## 4. Results

| Issue | Kind | Run(s) | Outcome | Attempts S1/S2/S3/S4 | AC tests | PR | CI | Review | Hidden | Out tok | Wall |
|---|---|---|---|---|---|---|---|---|---|---|---|
| #1 B1 linenums crash | bug | R2 | approved PR | 2/1/1/1 | 8 | [#16](https://github.com/AvAdiii/markdown/pull/16) | ✓ | approve | 4/4 | 24.0k | 7.6 min |
| #2 B2 empty attr list | bug | R0 → R1 | comment (sandbox broken), then approved | 1/1/1/1 | 11 | [#12](https://github.com/AvAdiii/markdown/pull/12) | ✓ | approve | 4/4 | 19.5k | 6.6 min |
| #3 F1 wikilink labels | feature | R3 | approved PR | 2/1/1/1 | 10 | [#15](https://github.com/AvAdiii/markdown/pull/15) | ✓ | approve | 4/4 | 21.4k | 5.9 min |
| #4 F2 toc exclusion | feature | R4 → R7 | stopped (judge flip), then approved | 1/2/1/1 | 7 | [#19](https://github.com/AvAdiii/markdown/pull/19) | ✓ | approve | 4/4 | 15.9k | 6.6 min |
| #5 V1 vague | vague | R5 → R6 → R10 | questions; CI docs fail; approved | 1/1/2/2 | 17 | [#18](https://github.com/AvAdiii/markdown/pull/18) | ✓ | approve | 4/4 | 28.3k | 9.6 min |

**Pass rate per stage** (all 11 runs; R8/R9 stopped on the subscription quota before any agent
output and are excluded; "first try" = passed its check on attempt 1).

| Stage | Entered | Passed (eventually) | Passed first try | What stopped or retried it |
|---|---|---|---|---|
| 1 Requirements | 9 | 7 (78 %) | 4 (44 %) | R2, R3, R6 judge-driven retries (fixed); R4 judge flip (stop, → ADR-011); R5 vague issue (stop with questions, intended) |
| 2 Design | 7 | 7 (100 %) | 6 (86 %) | R7: `add` row for a file that exists (AST/path check), fixed on retry |
| 3 Implementation | 7 | 7 (100 %) | 7 (100 %) | built every time; R10 re-entered stage 3 once from stage 4 |
| 4 Testing | 7 | 7 (100 %) | 6 (86 %) | R10: a test asserted an attribute order the serializer cannot produce; the developer filed a `TEST_DISPUTE`, the tester rewrote it (the dispute path, live) |
| 5 Release (CI) | 7 | 6 (86 %) | 6 (86 %) | R6: CI docs lints (`checklinks`, spelling) → stage 3 now runs both (PR #20) |
| 6 Review | 6 | 5 approve (83 %) | 5 | R0: reviewer could not execute anything and refused to approve |

**Hidden tests.** 4 per issue, kept outside the fork and run on the exact head each run released:
**28/28 on 7 released heads (5 PRs)**, including the R6 head that failed CI on docs only. Each
hidden test was validated to fail on the base and pass with my reference fix.

**What the reviewer caught, and where it was wrong.**

* *Caught, blocking:* 12/12 planted defects across the three cells, each with executed evidence and
  the right route (design for S3, implementation for the rest); 0/3 false rejections of S4.
* *Caught, non-blocking (useful to the human):* R2 found the docs still say only `use_pygments` is
  dropped; R1 found a pre-existing greedy `}` capture in `BASE_RE`; R3 noted `[[P|l]]` inside a
  table row splits at the pipe; R10 noted the scheme check is case-sensitive (`HTTPS://`).
* *Wrong or weak:* (1) **too lenient on docs.** R7 approved a new user-visible option (`no-toc`)
  with no documentation, and R2 approved with stale docs, listing both only as notes. A human
  maintainer would have asked for docs. (2) **It could not verify the tests itself.** In R7 my guard
  blocked git, so it could not check out the base and re-run the new tests there; it reported this
  honestly but approved on the tester's evidence. In R10 the guard blocked literal URLs, so it built
  probes indirectly. (3) In R0 it was right not to approve but for an infrastructure reason; it
  produced no finding. (4) It never sent a real pipeline PR back: every builder head was correct
  (28/28 hidden), so the **send-back loop was exercised only on seeded PRs with `rework=false`**.

**Why the numbers look so clean, and what that does and does not show.** In A2 I used a local
9B model (Qwen3.5-9B), which failed often enough that the interesting result was the failure itself. Claude
Sonnet/Opus solved all five issues, so the model is not the bottleneck here and the 100 % rows
should not be read as "the architecture makes agents correct". The issues are small, single-module
changes in a well-tested library. The evidence for the *architecture* is elsewhere: the checks
fired in 7 of 9 runs and each time it was a code check, not the model, that noticed the problem; and
every real failure (sandbox, CI drift, judge flip, quota, concurrency) was a harness or
infrastructure failure that the design stopped and explained instead of hiding. The one live
model error was the *tester's* (R10), and it was caught because the developer may dispute a test
but not edit it.

**Tokens and cost.** {{TOTALS}} A successful run takes 6–10 agent sessions, 16–28k output tokens and
6–10 min. The hard spending cap is the Claude Pro subscription itself (no API key); when its
5-hour quota ran out, R8/R9 stopped at the first agent call and said so.

## 5. Hindsight

**The decision I would change first is the reviewer's tool fence in ADR-005.** I fenced every agent
with the same guard rules, so the reviewer, the one agent whose job is to distrust the others, could
not run `git` to check out the base commit and re-run the new tests there (R7), and could not put a
URL in a shell command (R10). It therefore approved partly on the tester's word, which is exactly
the dependence ADR-008 was meant to remove. Tomorrow I would have `review.py` prepare a read-only
base worktree next to the PR checkout and give the reviewer a role-specific allow-list, and I would
make "the new tests fail on base" a check the reviewer reproduces. This is cheap and directly
strengthens the decision that mattered most.

Two smaller lessons. **Infrastructure bit before the models did:** three of the four fixes after the
first live run (bubblewrap/socat on the runner, GitHub's single pending-run slot per concurrency
group, CI docs checks stage 3 did not mirror) were environmental. A one-issue smoke run on the real
runner before writing all the ADRs would have found them in an hour. **A check is only deterministic
if its inputs are:** I would treat any LLM verdict as a cached sample from day one (ADR-011), not
discover it from a flip.

## 6. Limitations and threats to validity

1. **Ceiling effect and one trial per cell.** All three reviewer cells scored the maximum, and every
   issue was solved. The quota allowed one review per (variant, PR) and one run per issue, so the
   experiments show direction, not significance, and cannot separate the variants.
2. **Easy, self-authored ground truth.** I wrote the issues, hidden tests and seeded PRs, with help
   from Claude Code (README). They test what I meant, and the seeded defects are all findable by
   running the issue's own examples. Using the same model family to build the benchmark and to run
   the agents risks correlated blind spots that would inflate every number here.
3. **The review send-back loop was never exercised end-to-end.** Routing to design/implementation
   is implemented in `review.py` and the seeded reviews chose the right routes, but no pipeline run
   reached round 2 because every builder output was approved.
4. **The guard's Bash rules are pattern-based.** A determined agent could write outside its paths
   through a script (`python -c open(...)`). The real boundaries are the path filter on the captured
   patch, the missing credentials and the sandbox; none stops an agent *reading* the workspace, which
   is why the hidden tests live outside the fork.
5. **Same vendor everywhere, shared quota.** Builders and reviewer are now both Sonnet (ADR-012), and
   everything draws on one 5-hour subscription window; when it ran out every in-flight run stopped
   (R8, R9). There is no per-run dollar budget, only turn, time and retry caps.
6. **CI is outside the harness.** Stage 3 now mirrors flake8, the suite and the docs lints, but any
   other CI job is discovered only after the PR is open, and a CI failure stops the run rather than
   routing back to implementation.
