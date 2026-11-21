# Test report: issue #2, round 0

Base commit `66a9ee4`. New tests are run on the base commit (they must fail there) and on the head (they must pass). The full existing suite is run on the head.

| Acceptance criterion | Test | Base | Head |
|---|---|---|---|
| AC-FR-001-1 | `test_ac_fr_001_1_empty_list_header_space` | fail | pass |
| AC-FR-001-2 | `test_ac_fr_001_2_empty_list_header_no_space` | fail | pass |
| AC-FR-002-1 | `test_ac_fr_002_1_empty_list_block_no_space` | fail | pass |
| AC-FR-002-2 | `test_ac_fr_002_2_empty_list_block_space` | fail | pass |
| AC-FR-003-1 | `test_ac_fr_003_1_empty_list_inline_space` | fail | pass |
| AC-FR-003-2 | `test_ac_fr_003_2_empty_list_inline_no_space` | fail | pass |
| AC-FR-004-1 | `test_ac_fr_004_1_nonempty_header` | pass | pass |
| AC-FR-004-2 | `test_ac_fr_004_2_nonempty_inline` | pass | pass |
| AC-FR-004-3 | `test_ac_fr_004_3_nonempty_block` | pass | pass |
| AC-FR-005-1 | `test_ac_fr_005_1_braces_without_colon_unchanged` | pass | pass |

Full suite, base before the change: {'pass': 1114, 'skip': 52}
Full suite, head: {'pass': 1124, 'skip': 52}

## autose check: PASSED

