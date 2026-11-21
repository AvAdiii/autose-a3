# Test report: issue #5, round 0

Base commit `10be0dd`. New tests are run on the base commit (they must fail there) and on the head (they must pass). The full existing suite is run on the head.

| Acceptance criterion | Test | Base | Head |
|---|---|---|---|
| AC-FR-001-1 | `test_ac_fr_001_1_loads_by_name` | error | pass |
| AC-FR-001-2 | `test_ac_fr_001_2_plain_text_unchanged` | error | pass |
| AC-FR-002-1 | `test_ac_fr_002_1_disabled_inline_link` | pass | pass |
| AC-FR-002-2 | `test_ac_fr_002_2_disabled_autolink` | pass | pass |
| AC-FR-003-1 | `test_ac_fr_003_1_https_inline_link` | error | pass |
| AC-FR-003-2 | `test_ac_fr_003_2_http_link_with_query` | error | pass |
| AC-FR-003-3 | `test_ac_fr_003_3_text_and_href_unchanged` | error | pass |
| AC-FR-004-1 | `test_ac_fr_004_1_autolink` | error | pass |
| AC-FR-004-2 | `test_ac_fr_004_2_mailto_autolinks` | error | pass |
| AC-FR-005-1 | `test_ac_fr_005_1_reference_link` | error | pass |
| AC-FR-006-1 | `test_ac_fr_006_1_relative_absolute_path` | error | pass |
| AC-FR-006-2 | `test_ac_fr_006_2_anchor` | error | pass |
| AC-FR-006-3 | `test_ac_fr_006_3_mailto_link` | error | pass |
| AC-FR-006-4 | `test_ac_fr_006_4_relative_file` | error | pass |
| AC-FR-007-1 | `test_ac_fr_007_1_image_only` | error | pass |
| AC-FR-007-2 | `test_ac_fr_007_2_linked_image` | error | pass |
| AC-FR-008-1 | `test_ac_fr_008_1_no_config_needed` | error | pass |

Full suite, base before the change: {'pass': 1055, 'skip': 111}
Full suite, head: {'pass': 1072, 'skip': 111}

## autose check: PASSED


## History
- 11:03:12 testing: developer disputes a test
