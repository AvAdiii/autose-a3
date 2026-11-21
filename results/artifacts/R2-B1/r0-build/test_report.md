# Test report: issue #1, round 0

Base commit `bb9e8d8`. New tests are run on the base commit (they must fail there) and on the head (they must pass). The full existing suite is run on the head.

| Acceptance criterion | Test | Base | Head |
|---|---|---|---|
| AC-FR-001-1 | `test_ac_fr_001_1_linenums_flag` | error | pass |
| AC-FR-001-2 | `test_ac_fr_001_2_linenums_value` | error | pass |
| AC-FR-001-3 | `test_ac_fr_001_3_guess_lang_noclasses` | - | pass |
| AC-FR-001-4 | `test_ac_fr_001_4_plain_python` | pass | pass |
| AC-FR-003-1 | `test_ac_fr_003_1_data_attr` | pass | pass |
| AC-FR-003-2 | `test_ac_fr_003_2_data_test_braces` | pass | pass |
| AC-FR-004-1 | `test_ac_fr_004_1_codehilite_linenums` | pass | pass |
| AC-FR-004-2 | `test_ac_fr_004_2_codehilite_linenums_true` | pass | pass |

Full suite, base before the change: {'pass': 1114, 'skip': 52}
Full suite, head: {'pass': 1122, 'skip': 52}

## autose check: PASSED

