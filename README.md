# autose: issue in, pull request out

A GitHub Actions workflow that turns a labelled issue into a reviewed pull request in six fixed
stages: requirements → design → implementation → testing → release → independent review. A human
always merges.

- **Target repository (fork):** [AvAdiii/markdown](https://github.com/AvAdiii/markdown), Python-Markdown
  forked at upstream commit `3f2c551` (the same project as Assignment 2; its `ARCHITECTURE.md` is in
  the fork root and is what the architect agent designs against).
- **Workflow:** [`.github/workflows/autose.yml`](https://github.com/AvAdiii/markdown/blob/main/.github/workflows/autose.yml)
  + [`autose-round.yml`](https://github.com/AvAdiii/markdown/blob/main/.github/workflows/autose-round.yml),
  harness in [`.github/autose/`](https://github.com/AvAdiii/markdown/tree/main/.github/autose). A copy is in
  [`workflow/`](workflow/).
- **Report:** [`report.pdf`](report.pdf). **Demo:** [`demo.mp4`](demo.mp4).
- **All runs, PRs and reviews:** [`results/runs.md`](results/runs.md); one row per run in
  [`results/results.csv`](results/results.csv).

## How it works (one paragraph)

Labelling an issue `autose` (or commenting `/autose`) by a user with write access starts a *gate* job,
then up to three *rounds*. Each round is three jobs: **build** (a deterministic Python state machine
runs the analyst, spec judge, architect, developer and tester agents, each followed by a code check),
**release** (no model: applies the patch, pushes the branch as the `autose-dev-avadiii` GitHub App,
opens the PR, waits for CI) and **review** (a fresh VM: an Opus reviewer that sees only the issue, the
diff and the checkout, runs its own checks, and returns a structured verdict). `request_changes`
sends the run back to the earliest stage the blocking findings name, at most twice. Every stage
writes its artifact (`spec.md`, `design.md`, `diff.patch`, `test_report.md`, `pr.md`, `review.md`), a
sticky status comment on the issue explains each pass or stop, and nothing ever merges.
Details: [`architecture/views/component_view.md`](architecture/views/component_view.md),
[`stage_map.md`](architecture/views/stage_map.md), [`sequence_view.md`](architecture/views/sequence_view.md)
(one real run), and the ADRs in [`architecture/decisions/`](architecture/decisions/).

## Repository layout

```
README.md, report.pdf, demo.mp4
architecture/views/        component view, stage map, sequence view of run 44889589134
architecture/decisions/    ADR-001 … ADR-011 (Nygard format; ADR-007 superseded in part by ADR-011)
workflow/                  copy of .github/workflows/ and .github/autose/ (agents, prompts, checks, A1 skill)
experiment/issues/         B1 B2 (bugs), F1 F2 (features), V1 (vague) + the maintainer's V1 answer
experiment/hidden_tests/   4 hidden acceptance tests per issue + run_hidden.sh (never in the fork)
experiment/reference_solutions/  my patches used to validate every hidden test (fail on base, pass with fix)
experiment/seeded_prs/     S1–S5 diffs, author context, labels.csv (ground truth)
experiment/variants.md     E1 (reviewer isolation) and E2 (reviewer model), written before any run
results/                   results.csv, runs.md, reviews_scored.csv, per-run artifacts, scripts
```

## Running it on the fork

1. **Secrets** (Settings → Secrets → Actions), set by the owner only:
   - `CLAUDE_CODE_OAUTH_TOKEN`: from `claude setup-token` (Claude Pro subscription; no API key is used);
   - `AUTOSE_APP_ID`, `AUTOSE_APP_PRIVATE_KEY`: the GitHub App `autose-dev-avadiii`, permissions
     contents/pull-requests/issues write, **no workflows permission**, installed on the fork only.
2. **Branch protection:** a ruleset on `main` requires a PR and a code-owner review (`CODEOWNERS: * @AvAdiii`),
   blocks force pushes and deletion. The App cannot satisfy it, so it cannot merge.
3. **Start a run:** add the label `autose` to an issue, or comment `/autose` (a later `/autose` restarts
   it, e.g. after answering the clarification questions). `/autose` on an autose PR re-runs only the
   review. Experiments use *Run workflow* (`workflow_dispatch`): `start_stage=review`, `pr`,
   `reviewer_variant`, `reviewer_model`, `rework=false` (see `results/dispatch_reviews.sh`).
4. **Models:** analyst, architect, developer, tester `claude-sonnet-5-5`; spec judge `claude-haiku-5-5`;
   reviewer `claude-opus-5-5` (ADR-006), Claude Code CLI 2.1.323 headless.

## Cost, quota and the spending cap

The workflow runs on a Claude Pro subscription (`CLAUDE_CODE_OAUTH_TOKEN`), so the hard spending cap is
the plan itself: no API key, no pay-as-you-go billing, and when the 5-hour quota is used up the agents
get a provider error and the run **stops with an explanation** instead of continuing (this happened
once, run R8 in `runs.md`). Inside a run, ADR-009 caps each agent (`--max-turns`, a 20-minute timeout),
the retries per stage, and the rounds (three, fixed in the YAML). Every agent session's tokens are
logged to `usage.jsonl` and summed per run in `results/results.csv` (`output_tokens`,
`input_tokens`, `cache_*`, and `cost_usd`, the CLI's API-price equivalent, for comparison).

## Safety rules, and where each is enforced

| Rule | Enforcement |
|---|---|
| Acts only on its own fork | workflow lives in the fork; App installed on the fork only |
| Never merges | no merge call anywhere; ruleset needs a code-owner review the bot cannot give |
| Secrets only in repo secrets | agents get a whitelisted environment without GitHub tokens; `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` keeps the model credential out of agent Bash, which runs in a bubblewrap sandbox (ADR-005) |
| Least privilege per job | `permissions: {}` at workflow level; per-job scopes in ADR-005 (the build job cannot push) |
| Issue text is untrusted | gate accepts write-level users only; issue text is wrapped in a nonce-tagged `<untrusted-issue>` block; the guard hook blocks network tools, `gh`, git state changes and writes outside each role's paths (ADR-009) |
| Design before agent code | submission commit `6c3d6a5` (views + ADRs, 12:43 IST) precedes the fork's harness commit `66a9ee4` (13:00) |
| Wrong ADRs are kept | ADR-007 is marked *Superseded in part* by ADR-011, with the run that proved it wrong |

## Use of AI (disclosure)

I used Claude Code (Claude Opus 5.5) as an assistant throughout this assignment: to draft and
debug the harness code, prompts and workflow YAML, to draft the ADRs and views from my decisions, to
write the hidden tests, reference fixes and seeded PRs, to analyse the run artifacts, and to draft
this README and the report. I reviewed and decided every design choice, checked every claim against
the run logs and artifacts, and ran all experiments on the real workflow. The agents *inside* the
workflow are Claude models by design (see Models above). The requirements agent reuses my A1 skill
(`workflow/autose/skills/requirements-specifier/SKILL.md`), and the architect designs against my A2
`ARCHITECTURE.md`.
