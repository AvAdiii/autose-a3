# Test report: issue #5, round 0

Base commit `65eb770`. New tests are run on the base commit (they must fail there) and on the head (they must pass). The full existing suite is run on the head.

| Acceptance criterion | Test | Base | Head |
|---|---|---|---|
| AC-FR-001-1 | `test_ac_fr_001_1_loads_by_name` | error | pass |
| AC-FR-001-2 | `test_ac_fr_001_2_construct` | error | pass |
| AC-FR-002-1 | `test_ac_fr_002_1_disabled_inline` | pass | pass |
| AC-FR-002-2 | `test_ac_fr_002_2_disabled_autolink` | pass | pass |
| AC-FR-003-1 | `test_ac_fr_003_1_https` | error | pass |
| AC-FR-003-2 | `test_ac_fr_003_2_http` | error | pass |
| AC-FR-003-3 | `test_ac_fr_003_3_reference_link` | error | pass |
| AC-FR-004-1 | `test_ac_fr_004_1_autolink` | error | pass |
| AC-FR-005-1 | `test_ac_fr_005_1_relative` | error | pass |
| AC-FR-005-2 | `test_ac_fr_005_2_anchor` | error | pass |
| AC-FR-005-3 | `test_ac_fr_005_3_mailto` | error | pass |
| AC-FR-006-1 | `test_ac_fr_006_1_image` | error | pass |
| AC-FR-006-2 | `test_ac_fr_006_2_linked_image` | error | pass |
| AC-FR-007-1 | `test_ac_fr_007_1_no_configs` | error | pass |
| AC-FR-007-2 | `test_ac_fr_007_2_unknown_option` | error | pass |

Full suite, base before the change: {'pass': 1114, 'skip': 52}
Full suite, head: {'pass': 1129, 'skip': 52}

## autose check: PASSED

