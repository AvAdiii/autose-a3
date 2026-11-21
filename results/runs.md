# Runs

Every run is a real GitHub Actions run on [AvAdiii/markdown](https://github.com/AvAdiii/markdown)
(fork of Python-Markdown at `3f2c551`). Token counts come from each job's `usage.jsonl`
(the `result` event of every Claude Code session); `$ equiv` is the CLI's API-price estimate, the
runs themselves were billed to a Claude Pro subscription quota. Hidden tests were run by me,
after the run, with `experiment/hidden_tests/run_hidden.sh` on the PR head.

## R0: first real run, issue #2 (B2): infrastructure fault found

- Run: [44887224113](https://github.com/AvAdiii/markdown/actions/runs/44887224113), trigger:
  label `autose` on [#2](https://github.com/AvAdiii/markdown/issues/2), 08:56:47 to 09:03:21 UTC
  (6 min 34 s: gate 27 s, build 2 min 11 s, release 2 min 31 s incl. CI wait, review 1 min 11 s).
- PR: [#12](https://github.com/AvAdiii/markdown/pull/12), opened by `autose-dev-avadiii[bot]`; CI
  green (13 checks).
- Stages: requirements, design, implementation, testing all passed at the first attempt; 10 new
  tests (6 fail on base, all pass on head), suite 1114 → 1124 passing.
- Hidden tests (B2): **4/4 pass**.
- Review (Opus, isolated): **no approval**. Every Bash call of every agent failed with
  `Sandbox is required but failed to initialize: socat not installed`. The builders fell back to
  Read/Edit; the reviewer could run none of its six checks, traced them statically, found no
  defect, and returned `request_changes` *because nothing was verified*. `review.py` downgraded it
  to a comment review (no blocking finding with evidence). This is the behaviour ADR-008 asks for:
  no unverified approval.
- Cause: `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` (ADR-005) makes Claude Code run Bash inside
  bubblewrap, which needs `bubblewrap` + `socat` and unprivileged user namespaces; the runner has
  none. Fixed in harness PR [#13](https://github.com/AvAdiii/markdown/pull/13): install and
  smoke-test the sandbox in the build and review jobs, and stop the run with
  `error_kind=sandbox` instead of continuing without Bash.
- Tokens: output 20,188; input 58 + cache read 396,356 + cache write 99,704; $0.76 equiv;
  agent time 146 s (analyst 22.5 s, judge 6.1 s, architect 32.3 s, developer 14.8 s, tester
  19.2 s, reviewer 51.0 s).

## R1: issue #2 (B2) again, after the sandbox fix

- Run: [44889589134](https://github.com/AvAdiii/markdown/actions/runs/44889589134), trigger: a
  maintainer comment `/autose` on #2 (the comment trigger). Sandbox step: `sandbox ok`; zero
  sandbox failures in any transcript; the developer ran the full suite and flake8 itself.
- PR [#12](https://github.com/AvAdiii/markdown/pull/12) force-updated to `30f9655` (round 0 rebuilds
  the branch from base); CI green.
- All four build stages passed at the first attempt; 11 new tests, suite 1114 → 1125.
- Hidden tests (B2): **4/4 pass**.
- Review (Opus, isolated): **approve**, 6/6 own checks executed and passing (including a
  24-input comparison of the old and new regex), posted by `github-actions` as an APPROVED review
  on a PR authored by `autose-dev-avadiii[bot]`.
- Time 09:26:22 to 09:33:00 UTC (6 min 38 s). Tokens: output 19,459; input 50 + cache read
  368,687 + cache write 58,002; $0.53 equiv; agent time 142 s.
