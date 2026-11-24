# Test report: issue #3, round 0

Base commit `77387dd`. New tests are run on the base commit (they must fail there) and on the head (they must pass). The full existing suite is run on the head.

| Acceptance criterion | Test | Base | Head |
|---|---|---|---|
| AC-FR-001-1 | `test_ac_fr_001_1_label` | fail | pass |
| AC-FR-001-2 | `test_ac_fr_001_2_label_in_text` | fail | pass |
| AC-FR-001-3 | `test_ac_fr_001_3_no_brackets_or_pipe` | fail | pass |
| AC-FR-002-1 | `test_ac_fr_002_1_space_around_pipe` | fail | pass |
| AC-FR-002-2 | `test_ac_fr_002_2_extra_space_equal` | fail | pass |
| AC-FR-003-1 | `test_ac_fr_003_1_base_end_class` | fail | pass |
| AC-FR-003-2 | `test_ac_fr_003_2_empty_class` | fail | pass |
| AC-FR-003-3 | `test_ac_fr_003_3_build_url_args` | fail | pass |
| AC-FR-004-1 | `test_ac_fr_004_1_no_pipe` | pass | pass |
| AC-FR-004-2 | `test_ac_fr_004_2_whitespace_no_pipe` | pass | pass |
| AC-FR-004-3 | `test_ac_fr_004_3_blank_removed` | pass | pass |

Full suite, base before the change: {'pass': 1055, 'skip': 111}
Full suite, head: {'pass': 1066, 'skip': 111}

## autose check: PASSED

