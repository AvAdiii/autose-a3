# Seeded reviewer-check PRs

Five pull requests opened by hand on the fork (label `seeded-pr`, PRs #6-#10), each answering one of the
five experiment issues. Four contain one planted defect, one is correct. `labels.csv` is the ground
truth, written before any review ran. `S*.diff` is each PR's diff against `main`;
`S*_author_context.md` is the PR description, written the way the pipeline's `pr.md` reads (spec,
design rationale, test report). That description is what the **shared** reviewer variant of
experiment E1 sees in addition to the issue and diff; the **isolated** reviewer never sees it.

All five PRs pass the repository's existing test suite and their own new tests; the defects are only
visible against the issue (and, for S1-S3 and S5, the hidden acceptance tests fail).
