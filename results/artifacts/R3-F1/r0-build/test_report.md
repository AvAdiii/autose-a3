# Test report: issue #3, round 0

Base commit `bb9e8d8`. New tests are run on the base commit (they must fail there) and on the head (they must pass). The full existing suite is run on the head.

| Acceptance criterion | Test | Base | Head |
|---|---|---|---|
| AC-FR-001-1 | `test_ac_fr_001_1_label` | fail | pass |
| AC-FR-001-2 | `test_ac_fr_001_2_same_href` | fail | pass |
| AC-FR-001-3 | `test_ac_fr_001_3_no_syntax_left` | fail | pass |
| AC-FR-002-1 | `test_ac_fr_002_1_spaces_around_pipe` | fail | pass |
| AC-FR-002-2 | `test_ac_fr_002_2_label_padding` | fail | pass |
| AC-FR-003-1 | `test_ac_fr_003_1_options` | fail | pass |
| AC-FR-003-2 | `test_ac_fr_003_2_empty_class` | fail | pass |
| AC-FR-003-3 | `test_ac_fr_003_3_custom_build_url` | fail | pass |
| AC-FR-004-1 | `test_ac_fr_004_1_unlabelled` | pass | pass |
| AC-FR-004-2 | `test_ac_fr_004_2_blank_wikilink` | pass | pass |

Full suite, base before the change: {'pass': 1114, 'skip': 52}
Full suite, head: {'pass': 1124, 'skip': 52}

## autose check: PASSED

