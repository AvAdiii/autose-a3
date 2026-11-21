# Stage map

One row per stage: who does the work, what it leaves behind, and what decides that the stage
passed. "Decided by" is always deterministic code; a model can only feed it evidence.

| # | Stage | Agent (model) | Job | Artifact | Check before moving on | Decided by | On failure |
|---|---|---|---|---|---|---|---|
| 1 | Requirements | Analyst (`claude-sonnet-5-5`) with the A1 `requirements-specifier` skill in pipeline profile | build | `spec.md` | Every acceptance criterion parses as Given/When/Then, contains no A1 weak word, has a unique `AC-` ID, and is judged testable by the spec judge (`claude-haiku-5-5`). At least one Must FR is READY. | `checks.check_spec` (lint) AND judge verdict | 1 retry with the failing ACs. If READY is empty because P1 questions are open: post the questions on the issue, stop with `needs-clarification`. |
| 2 | Design | Architect (`claude-sonnet-5-5`) + A2 `ARCHITECTURE.md` | build | `design.md` | The change table names at least one file and one function/class; every `modify` row exists in the repo (file on disk, symbol found by AST); every READY AC maps to a row; a `docs/changelog.md` row exists when `markdown/` changes (the fork's CI enforces it). | `checks.check_design` | 1 retry with the failures, then stop. |
| 3 | Implementation | Developer (`claude-sonnet-5-5`) | build | `diff.patch` | The diff is non-empty and touches no `tests/`, `.github/` or `.autose/` path; `compileall` passes; `pip install -e .` and `import markdown` work; `flake8` (CI config) is clean on changed files. | `checks.check_build` | Retry inside the stage-3/4 budget (3 attempts). |
| 4 | Testing | Tester (`claude-sonnet-5-5`) in a worktree **at the base commit** | build | `test_report.md` (+ `tests.patch`) | Every READY AC has at least one test that names it; the new tests fail on the base commit (they detect the change) and pass on the head; the full existing suite passes on the head. | `checks.check_tests` | Back to stage 3 with the failing tests. After 2 failed fix attempts in a row, back to stage 2 once. A developer `TEST_DISPUTE` sends the test back to the tester once. |
| 5 | Release | none (`release.py`) | release | `pr.md` + PR link | The PR is open from `autose/issue-N` and every CI check on its head commit has concluded `success` (15 min limit). | `release.wait_for_ci` | Stop; `pr.md` records the failing check and log link. |
| 6 | Review | Reviewer (`claude-opus-5-5`), separate job and VM | review | `review.md` (+ `review.json`) | Verdict is `approve`, or the round limit is used up. A `request_changes` verdict must carry at least one blocking finding with a file and evidence. | `post_review.route` | Earliest stage named by a blocking finding (`requirements`, `design`, `implementation`, `testing`) is re-entered in the next round; at most 2 rework rounds. |

**Budgets** (all enforced in code): 3 implementation attempts per round, 1 design revisit per
round, 1 retry for stages 1 and 2, 2 rework rounds after the first review, `--max-turns` per agent
(analyst 40, architect 40, developer 60, tester 50, reviewer 50), a wall-clock limit per agent call
(20 min), `timeout-minutes` per job (build 75, release 25, review 30).
