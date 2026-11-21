# Test report: issue #2, round 0

Base commit `bb9e8d8`. New tests are run on the base commit (they must fail there) and on the head (they must pass). The full existing suite is run on the head.

| Acceptance criterion | Test | Base | Head |
|---|---|---|---|
| AC-FR-001-1 | `test_ac_fr_001_1_empty_list_heading` | fail | pass |
| AC-FR-001-2 | `test_ac_fr_001_2_empty_list_no_space_and_many_spaces` | fail | pass |
| AC-FR-001-3 | `test_ac_fr_001_3_nonempty_list_heading` | pass | pass |
| AC-FR-002-1 | `test_ac_fr_002_1_empty_list_block_no_space` | fail | pass |
| AC-FR-002-2 | `test_ac_fr_002_2_empty_list_block_space` | fail | pass |
| AC-FR-002-3 | `test_ac_fr_002_3_nonempty_list_block` | pass | pass |
| AC-FR-003-1 | `test_ac_fr_003_1_empty_list_inline_space` | fail | pass |
| AC-FR-003-2 | `test_ac_fr_003_2_empty_list_inline_no_space` | fail | pass |
| AC-FR-003-3 | `test_ac_fr_003_3_nonempty_list_inline` | pass | pass |
| AC-FR-004-1 | `test_ac_fr_004_1_id_heading` | pass | pass |
| AC-FR-004-2 | `test_ac_fr_004_2_multiple_classes_heading` | pass | pass |

Full suite, base before the change: {'pass': 1114, 'skip': 52}
Full suite, head: {'pass': 1125, 'skip': 52}

## autose check: PASSED

