# Decision experiments: variants (written before any experiment run)

Both experiments test the reviewer, because the reviewer is the last automated line before a human
and the two decisions about it (what it sees, which model it is) are the ones I was least sure of.
Both use the five seeded PRs in `seeded_prs/` (four with one planted defect, one correct; ground
truth in `seeded_prs/labels.csv`), so every variant reviews exactly the same diffs against the same
issues. Runs are started with `workflow_dispatch` (`start_stage=review`, `pr=<n>`,
`rework=false`), so the review job, its permissions and its prompt are the production ones; only
the input named below changes.

## E1: does isolating the reviewer from the authors' context matter? (tests ADR-008)

| Variant | Reviewer sees | Everything else |
|---|---|---|
| `isolated` (production) | the issue, the diff, the repository at the PR head | `claude-opus-5-5`, `prompts/reviewer.md`, same schema |
| `shared` | the same **plus** the authors' context: the PR description (spec summary, design rationale, test report), given as `<author-context>` | identical |

The shared context is realistic, not adversarial: each description is what the pipeline's `pr.md`
looks like, states the authors' intent honestly, and says the tests pass (they do). For S1, S3 and S5
the rationale makes the defective choice sound deliberate, which is exactly the situation in which
shared context could anchor a reviewer.

**Hypothesis (H1).** The isolated reviewer detects at least as many planted defects as the shared
one, and the difference shows on the PRs whose rationale explains the defect away (S1, S3).

## E2: does the reviewer need the strongest model? (tests ADR-006)

| Variant | Model | Everything else |
|---|---|---|
| `opus` (production) | `claude-opus-5-5` | isolated input, same prompt and schema |
| `sonnet` | `claude-sonnet-5-5` (the builders' model) | identical |

**Hypothesis (H2).** Opus detects more planted defects than Sonnet. If Sonnet matches Opus, ADR-006
is superseded (use Sonnet, cheaper per review and less quota), at the cost of reviewer/builder
model diversity.

## Measures (same for both)

Per review, scored against `labels.csv` by `results/score_reviews.py` (no judgement calls by me
beyond the matching rule below):

- **verdict correct**: `request_changes` for S1, S2, S3, S5; `approve` for S4;
- **defect detected**: a *blocking* finding whose title or evidence describes the planted defect
  (matching rule: it names the behaviour in the `planted_defect` column, e.g. the leaked braces,
  the wrong href, `toc_tokens`, the missing entry point). Recorded with the finding text so the
  match can be checked;
- **routing correct**: the earliest blocking category equals `defect_category`;
- **false rejection**: `request_changes` on S4;
- **own probes executed**: number of `own_checks` with an executed command;
- cost: output tokens, turns, wall-clock time (from the review job's `usage.jsonl`).

The `opus`/`isolated` cell is shared by both experiments (same five runs). Total: 15 reviews,
one trial per cell (the subscription quota allows no more; see Limitations in the report).
