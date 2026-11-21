| Cell | Model | Input | Verdict right | Defect found | Routing right | False reject | Probes/PR | Out tokens (5 PRs) | Agent time |
|---|---|---|---|---|---|---|---|---|---|
| production | Opus | isolated: issue + diff | 5/5 | 4/4 | 4/4 | 0/1 | 6.4 | 14,429 | 137 s |
| E1 variant | Opus | + PR description, spec, design rationale | 5/5 | 4/4 | 4/4 | 0/1 | 6.2 | 15,811 | 158 s |
| E2 variant | Sonnet | isolated | 5/5 | 4/4 | 4/4 | 0/1 | 3.8 | 8,435 | 80 s |

**E1 (ADR-008, isolation). H1 not supported.** The shared-context reviewer was as accurate as the
isolated one. This held even on S1 and S3, whose author rationale presents the defect as deliberate.
Like the isolated reviewer, it found the leaked braces and the unfiltered `toc_tokens` by running
the issue's examples, whatever the description said. The shared context cost 10 % more tokens and
bought nothing. ADR-008 stays: the experiment shows isolation is cheap, not that it is necessary.
Its case rests on cases that this set does not contain, such as a rationale that changes what the
reviewer thinks the issue asks for.

**E2 (ADR-006, reviewer model). H2 not supported.** Sonnet matched Opus on every measure at 58 % of
the tokens and the time. It ran fewer probes (3.8 against 6.4), but every rejection carried
executed evidence that named the planted defect. The rule written before the run said that a tie
supersedes ADR-006, so **ADR-012** makes Sonnet the default reviewer and keeps Opus available per
run.

**Reading both.** All three cells scored the maximum, so this is a ceiling effect. The planted
defects are found by running the issue's own examples, and the reviewer prompt requires exactly
that. These negative results are still informative. They show that *executed* evidence, not the
model or the context, is what the reviewer's accuracy rests on here. They also show that the
cheaper configuration is safe for defects of this kind. Separating the variants needs subtler
defects, such as performance regressions, concurrency bugs or a misread requirement, and more
than one trial per cell.
