# Component view

What runs where, which tools each agent has, and who calls whom. Solid arrows are calls or
data flow; dashed arrows are what an agent may read. Nothing an agent runs holds a GitHub
credential: every GitHub write is made by deterministic Python (`gh` CLI), never by a model.

```mermaid
flowchart TB
  subgraph GH["GitHub: AvAdiii/markdown (fork, main pinned at 3f2c551)"]
    ISSUE[(Issue + label 'autose'<br/>or '/autose' comment)]
    STATUS[(Sticky status comment<br/>on the issue)]
    BR[(Branch autose/issue-N)]
    PR[(Pull request)]
    CI[[Repo CI: tox.yml,<br/>changelog-enforcer]]
    ART[(Workflow artifacts<br/>r&lt;k&gt;-spec, -design, -diff,<br/>-tests, -release, -review)]
  end

  subgraph WF["autose.yml (caller workflow)"]
    GATE["gate job<br/>permissions: issues:write<br/>trigger + permission check,<br/>input sanitising"]
    R0["round 0<br/>(autose-round.yml)"]
    R1["round 1 (rework)"]
    R2["round 2 (rework)"]
  end

  subgraph ROUND["autose-round.yml (one review round, called 1-3 times)"]
    direction TB
    subgraph BUILD["build job · contents:read, issues:write · no push rights"]
      ORCH{{"orchestrator.py<br/>deterministic state machine<br/>budgets, routing, checks"}}
      AN["Analyst agent<br/>Sonnet · Read Grep Glob Write*<br/>+ A1 requirements-specifier skill"]
      AR["Architect agent<br/>Sonnet · Read Grep Glob Write* Bash*<br/>+ A2 ARCHITECTURE.md"]
      DEV["Developer agent<br/>Sonnet · Read Grep Glob Edit Write Bash*<br/>source files only"]
      TE["Tester agent<br/>Sonnet · Read Grep Glob Edit Write Bash*<br/>tests/ only, base-commit worktree"]
      JUDGE["Spec judge<br/>Haiku · no tools · JSON verdict"]
      CHK["checks.py<br/>parse, AST, compileall, flake8,<br/>unittest base vs head"]
      GUARD["guard.py<br/>PreToolUse hook:<br/>path + command policy per role"]
    end
    subgraph REL["release job · App token (contents, PRs) · no model"]
      RELPY["release.py<br/>apply diff.patch, push branch,<br/>open/update PR, wait for CI"]
    end
    subgraph REV["review job · contents:read, pull-requests:write, issues:write · fresh runner"]
      RVA["Reviewer agent<br/>Sonnet (Opus on request) · Read Grep Glob Bash<br/>no Edit/Write, no token in env"]
      POST["review.py (after the agent exits)<br/>schema check, post PR review,<br/>route: approve | design | implementation | ..."]
    end
  end

  ISSUE -->|issues.labeled / issue_comment| GATE
  GATE --> R0 -->|verdict = request_changes| R1 -->|verdict = request_changes| R2
  R0 & R1 & R2 -. "approve or rounds used up" .-> HUMAN([Maintainer merges or closes])

  ORCH --> AN & AR & DEV & TE
  ORCH --> JUDGE
  ORCH --> CHK
  AN & AR & DEV & TE -. every tool call .-> GUARD
  ORCH -->|stage artifacts| ART
  ORCH -->|progress| STATUS
  ART -->|diff.patch, spec, design, tests| RELPY
  RELPY --> BR --> PR --> CI
  RELPY -->|pr.md| PR
  PR -->|issue + diff + checkout at head only| RVA
  RVA -->|review.json| POST -->|review.md as PR review| PR
  POST -->|route + findings| ART
```

## Components

| Component | Kind | Runs in | Tools / rights | Calls |
|---|---|---|---|---|
| `autose.yml` | caller workflow | GitHub Actions | `permissions: {}` at top; each job widens only what it needs | gate job, then `autose-round.yml` up to 3 times |
| gate job | deterministic | `ubuntu-latest` | `issues: write` (reaction + status comment), API read of collaborator permission | decides start stage and issue number, writes `trigger.json` |
| `autose-round.yml` | reusable workflow | GitHub Actions | build → release → review jobs | `orchestrator.py`, `release.py`, reviewer + `review.py` |
| `orchestrator.py` | deterministic state machine (Python) | build job | `GITHUB_TOKEN` (issues: write) kept in its own process; spawns agents with a scrubbed environment | the four builder agents, the spec judge, `checks.py` |
| Analyst | Claude Code headless, `claude-sonnet-5-5` | build job | `Read Grep Glob Write`; Write only to `spec.md` | none |
| Architect | Claude Code headless, `claude-sonnet-5-5` | build job | `Read Grep Glob Write Bash`; Write only to `design.md`; Bash for read-only probes, tree reset afterwards | none |
| Developer | Claude Code headless, `claude-sonnet-5-5` | build job, head worktree | `Read Grep Glob Edit Write Bash`; edits only `markdown/**`, `docs/**`, `pyproject.toml`; no `git push/commit`, no network commands | none |
| Tester | Claude Code headless, `claude-sonnet-5-5` | build job, **base-commit** worktree | `Read Grep Glob Edit Write Bash`; edits only `tests/**` | none |
| Spec judge | Claude Code headless, `claude-haiku-5-5`, no tools, `--json-schema` | build job | none | none |
| `checks.py` | deterministic | build job | Python AST, `compileall`, `flake8`, `unittest` | none |
| `guard.py` | PreToolUse hook | every agent | denies tool calls outside the role's policy and logs them | none |
| `release.py` | deterministic | release job | short-lived GitHub App token (`autose-dev-avadiii`: contents + pull requests write, **no workflows permission**) | `git push`, `gh pr create/edit`, `gh pr checks` |
| Reviewer | Claude Code headless, `claude-sonnet-5-5` by default (ADR-012; Opus per run via `reviewer_model`; all recorded runs used Opus), `--json-schema` | review job (fresh VM) | `Read Grep Glob Bash`; no Edit/Write; environment has no GitHub token; `persist-credentials: false` | none |
| `review.py` (posting half) | deterministic | review job | `GITHUB_TOKEN` (pull-requests: write, issues: write for the status comment), used only after the reviewer process has exited | validates the verdict, posts the PR review, emits the route |

## Information each agent receives

| Agent | Gets | Deliberately does not get |
|---|---|---|
| Analyst | issue title + body, later comments by maintainers only (as untrusted data), repository (read), A1 skill | comments by non-maintainers, any GitHub token |
| Architect | `spec.md`, `ARCHITECTURE.md`, repository (read); in rework: test failures or reviewer findings tagged `design` | the raw issue text |
| Developer | `spec.md`, `design.md`, repository; on retry: failing test names + assertion output | the raw issue text, the tester's reasoning, the hidden tests |
| Tester | `spec.md`, `design.md` (interface), repository **at the base commit** | the implementation diff, the developer's reasoning |
| Reviewer | issue title + body, `git diff base...head`, repository at PR head; may run anything locally | `spec.md`, `design.md`, `test_report.md`, `pr.md`, every agent transcript |
