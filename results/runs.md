# Runs

Every run is a real GitHub Actions run on [AvAdiii/markdown](https://github.com/AvAdiii/markdown)
(Python-Markdown forked at `3f2c551`). Columns as in `results.csv`, which `collect_runs.py` builds
from each run's API record and artifacts. The artifacts are archived in `artifacts/<label>/`:
`r0-build` holds spec, design, diff, test report, checks, transcripts and guard log; `r0-5-release`
holds `pr.md` and `release.json`; `r0-6-review` holds `review.md`, `review.json` and the reviewer
transcript.
* **Tokens** come from each agent session's `usage.jsonl`. The runs were billed to a Claude Pro
  subscription. `cost_usd` in the CSV is the CLI's API-price equivalent, for comparison only.
* **Hidden tests** (`experiment/hidden_tests/`, never in the fork) were run by `collect_runs.py
  hidden` on the exact head each run released.

## Pipeline runs (issues #1 to #5)

| Run | Issue | Actions run | Trigger | Attempts S1/S2/S3/S4 | PR | CI | Review | Hidden | Outcome | Output tokens | Wall |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R0-B2 | #2 B2 | [44887224113](https://github.com/AvAdiii/markdown/actions/runs/44887224113) | label | 1/1/1/1 | [#12](https://github.com/AvAdiii/markdown/pull/12) | pass | comment | 4/4 | no approval: agent Bash broken (see below) | 20,188 | 394 s |
| R1-B2 | #2 B2 | [44889589134](https://github.com/AvAdiii/markdown/actions/runs/44889589134) | `/autose` | 1/1/1/1 | [#12](https://github.com/AvAdiii/markdown/pull/12) | pass | approve | 4/4 | approved PR | 19,459 | 397 s |
| R2-B1 | #1 B1 | [44890133094](https://github.com/AvAdiii/markdown/actions/runs/44890133094) | label | 2/1/1/1 | [#16](https://github.com/AvAdiii/markdown/pull/16) | pass | approve | 4/4 | approved PR | 24,007 | 454 s |
| R3-F1 | #3 F1 | [44890136597](https://github.com/AvAdiii/markdown/actions/runs/44890136597) | label | 2/1/1/1 | [#15](https://github.com/AvAdiii/markdown/pull/15) | pass | approve | 4/4 | approved PR | 21,440 | 356 s |
| R4-F2 | #4 F2 | [44890139146](https://github.com/AvAdiii/markdown/actions/runs/44890139146) | label | 2/–/–/– | – | – | – | – | stopped at requirements: spec judge | 13,215 | 156 s |
| R5-V1 | #5 V1 | [44890142013](https://github.com/AvAdiii/markdown/actions/runs/44890142013) | label | 1/–/–/– | – | – | – | – | stopped: needs clarification (3 questions posted) | 3,411 | 67 s |
| R6-V1 | #5 V1 | [44890315260](https://github.com/AvAdiii/markdown/actions/runs/44890315260) | `/autose` after answer | 2/1/1/1 | [#18](https://github.com/AvAdiii/markdown/pull/18) | **fail** | – | 4/4 | stopped at release: CI docs lints | 24,679 | 444 s |
| R7-F2 | #4 F2 | [44890548514](https://github.com/AvAdiii/markdown/actions/runs/44890548514) | `/autose` | 1/2/1/1 | [#19](https://github.com/AvAdiii/markdown/pull/19) | pass | approve | 4/4 | approved PR | 15,859 | 398 s |
| R8-V1 | #5 V1 | [44893689623](https://github.com/AvAdiii/markdown/actions/runs/44893689623) | `/autose` | 1/–/–/– | – | – | – | – | stopped: Claude Pro 5-hour limit | 0 | 124 s |
| R9-V1 | #5 V1 | [44895471619](https://github.com/AvAdiii/markdown/actions/runs/44895471619) | `/autose` | 1/–/–/– | – | – | – | – | stopped: Claude Pro 5-hour limit | 0 | 155 s |
| R10-V1 | #5 V1 | [44896794171](https://github.com/AvAdiii/markdown/actions/runs/44896794171) | `/autose` (new token) | 1/1/2/2 | [#18](https://github.com/AvAdiii/markdown/pull/18) | pass | approve | 4/4 | approved PR (docs checks in stage 3 passed CI) | 28,310 | 573 s |
| R11-F1 | #3 F1 | [45405624215](https://github.com/AvAdiii/markdown/actions/runs/45405624215) | `/autose` (recorded for `demo.mp4`) | 1/1/1/1 | [#15](https://github.com/AvAdiii/markdown/pull/15) | pass | approve (Sonnet reviewer, ADR-012) | 4/4 | approved PR | 15,834 | 391 s |

Reviews by the reviewer on the pipeline PRs are on the PRs themselves, posted by
`github-actions[bot]`: [#12](https://github.com/AvAdiii/markdown/pull/12),
[#15](https://github.com/AvAdiii/markdown/pull/15), [#16](https://github.com/AvAdiii/markdown/pull/16),
[#19](https://github.com/AvAdiii/markdown/pull/19). R11 is the run recorded in `demo.mp4` and the first pipeline run with the Sonnet reviewer of ADR-012. R10 used a new `CLAUDE_CODE_OAUTH_TOKEN` (the same subscription plan, a second account's quota window). Every PR is still open for the maintainer to
merge or close; the workflow never merges.

## What each incident taught, and the harness PR that fixed it

| Run | What happened | Fix |
|---|---|---|
| R0 | `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` runs agent Bash in bubblewrap, and the runner has neither bubblewrap nor socat, so every Bash call failed. The builders fell back to Read/Edit. The reviewer could run none of its six checks, found no defect by reading, and **refused to approve** unverified work: `request_changes` without a blocking finding, which `review.py` downgraded to a comment. | [#13](https://github.com/AvAdiii/markdown/pull/13): install and smoke-test the sandbox; stop with `error_kind=sandbox` if it breaks |
| R2, R3 | The judge rejected ACs whose expected output was "the same as before this change" (no literal value) or named unspecified variants; the analyst made them concrete on the single retry. The judge doing its job. | none |
| R4 | The Haiku judge accepted AC-FR-002-2/3 on attempt 0 and rejected the **identical text** on attempt 1, so the run stopped on a sound spec. | [#17](https://github.com/AvAdiii/markdown/pull/17), ADR-011 (supersedes the stage-1 rule of ADR-007): verdicts sticky per AC text |
| R5 | Vague issue: the analyst posted three P1 questions (behaviour, what is external, opt-in) and no code was written. The maintainer answered with `experiment/issues/V1_clarification.md`, written before any run. | none (intended) |
| R6 | A correct implementation (hidden tests 4/4) failed CI `checklinks` (unresolved API autoref) and `checkspelling` (`treeprocessor` in a docstring). Stage 5 stopped and explained. | [#20](https://github.com/AvAdiii/markdown/pull/20): stage 3 runs both docs checks; the developer may edit `mkdocs.yml` |
| R7 | Design check failed once: the Changes table listed `tests/test_syntax/extensions/test_toc.py` as *add* although it exists (AST/path check); the architect fixed it on the retry. | none |
| R8, R9 | The Claude Pro 5-hour limit was reached by the experiment reviews running in parallel. Each run stopped at its first agent call and said why; the status comment showed raw JSON. | [#21](https://github.com/AvAdiii/markdown/pull/21): the CLI's message ("You've hit your 5-hour limit · resets …") comes first |
| E runs | The experiment reviews of seeded PRs (linked to issues #1–#5) **overwrote each issue's sticky status comment** with their own review status. The earlier versions remain in each comment's edit history. | [#22](https://github.com/AvAdiii/markdown/pull/22): only `autose/issue-N` PRs update the issue status |
| — | The 15 experiment review dispatches over 5 issues would have cancelled one another in GitHub's single pending-run slot per concurrency group. | [#14](https://github.com/AvAdiii/markdown/pull/14), ADR-010 amendment |

Harness PRs [#11](https://github.com/AvAdiii/markdown/pull/11), [#13](https://github.com/AvAdiii/markdown/pull/13),
[#14](https://github.com/AvAdiii/markdown/pull/14), [#17](https://github.com/AvAdiii/markdown/pull/17),
[#20](https://github.com/AvAdiii/markdown/pull/20), [#21](https://github.com/AvAdiii/markdown/pull/21),
[#22](https://github.com/AvAdiii/markdown/pull/22) were opened on `harness/*` branches and merged by the
maintainer with an admin bypass of the code-owner rule. #11 makes the lint check report only the
flake8 errors a change introduces; upstream already had some on Python 3.12.

## Experiment reviews (E1, E2)

Started by `results/dispatch_reviews.sh` (production review job, `workflow_dispatch`,
`start_stage=review`, `rework=false`) and scored by `results/score_reviews.py`. Each review is
also posted on its seeded PR ([#6](https://github.com/AvAdiii/markdown/pull/6)–[#10](https://github.com/AvAdiii/markdown/pull/10)).

| Cell | Seeded | PR | Run | Verdict | Route | Defect found | Own checks run | Output tokens |
|---|---|---|---|---|---|---|---|---|
| opus-isolated | S1 | [#6](https://github.com/AvAdiii/markdown/pull/6) | [44890809280](https://github.com/AvAdiii/markdown/actions/runs/44890809280) | request_changes | implementation | yes | 6 | 2,868 |
| opus-isolated | S2 | [#7](https://github.com/AvAdiii/markdown/pull/7) | [44890825281](https://github.com/AvAdiii/markdown/actions/runs/44890825281) | request_changes | implementation | yes | 5 | 1,880 |
| opus-isolated | S3 | [#8](https://github.com/AvAdiii/markdown/pull/8) | [44890841473](https://github.com/AvAdiii/markdown/actions/runs/44890841473) | request_changes | design | yes | 7 | 2,727 |
| opus-isolated | S4 | [#9](https://github.com/AvAdiii/markdown/pull/9) | [44890851656](https://github.com/AvAdiii/markdown/actions/runs/44890851656) | approve | – | n/a | 7 | 4,427 |
| opus-isolated | S5 | [#10](https://github.com/AvAdiii/markdown/pull/10) | [44890867863](https://github.com/AvAdiii/markdown/actions/runs/44890867863) | request_changes | implementation | yes | 7 | 2,527 |
| opus-shared | S1 | [#6](https://github.com/AvAdiii/markdown/pull/6) | [44896794659](https://github.com/AvAdiii/markdown/actions/runs/44896794659) | request_changes | implementation | yes | 6 | 2,905 |
| opus-shared | S2 | [#7](https://github.com/AvAdiii/markdown/pull/7) | [44896830144](https://github.com/AvAdiii/markdown/actions/runs/44896830144) | request_changes | implementation | yes | 6 | 2,100 |
| opus-shared | S3 | [#8](https://github.com/AvAdiii/markdown/pull/8) | [44896839711](https://github.com/AvAdiii/markdown/actions/runs/44896839711) | request_changes | design | yes | 8 | 3,015 |
| opus-shared | S4 | [#9](https://github.com/AvAdiii/markdown/pull/9) | [44896854333](https://github.com/AvAdiii/markdown/actions/runs/44896854333) | approve | – | n/a | 6 | 5,453 |
| opus-shared | S5 | [#10](https://github.com/AvAdiii/markdown/pull/10) | [44896874565](https://github.com/AvAdiii/markdown/actions/runs/44896874565) | request_changes | implementation | yes | 5 | 2,338 |
| sonnet-isolated | S1 | [#6](https://github.com/AvAdiii/markdown/pull/6) | [44896915224](https://github.com/AvAdiii/markdown/actions/runs/44896915224) | request_changes | implementation | yes | 3 | 1,512 |
| sonnet-isolated | S2 | [#7](https://github.com/AvAdiii/markdown/pull/7) | [44896933378](https://github.com/AvAdiii/markdown/actions/runs/44896933378) | request_changes | implementation | yes | 3 | 1,393 |
| sonnet-isolated | S3 | [#8](https://github.com/AvAdiii/markdown/pull/8) | [44896946310](https://github.com/AvAdiii/markdown/actions/runs/44896946310) | request_changes | design | yes | 5 | 2,154 |
| sonnet-isolated | S4 | [#9](https://github.com/AvAdiii/markdown/pull/9) | [44896965636](https://github.com/AvAdiii/markdown/actions/runs/44896965636) | approve | – | n/a | 5 | 1,443 |
| sonnet-isolated | S5 | [#10](https://github.com/AvAdiii/markdown/pull/10) | [44896984226](https://github.com/AvAdiii/markdown/actions/runs/44896984226) | request_changes | implementation | yes | 3 | 1,933 |

Ten earlier dispatches of the `opus-shared` and `sonnet-isolated` cells
(`review_runs_quota_failed.csv`) hit the Claude Pro 5-hour limit and produced no verdict. They were
re-dispatched after the window reset and are not scored.
