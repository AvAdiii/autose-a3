# Test report: issue #4, round 0

Base commit `1038c85`. New tests are run on the base commit (they must fail there) and on the head (they must pass). The full existing suite is run on the head.

| Acceptance criterion | Test | Base | Head |
|---|---|---|---|
| AC-FR-001-1 | `test_ac_fr_001_1_hrefs` | fail | pass |
| AC-FR-001-2 | `test_ac_fr_001_2_md_toc` | fail | pass |
| AC-FR-001-3 | `test_ac_fr_001_3_multiple_classes` | fail | pass |
| AC-FR-002-1 | `test_ac_fr_002_1_heading_keeps_id` | pass | pass |
| AC-FR-002-2 | `test_ac_fr_002_2_unique_ids` | pass | pass |
| AC-FR-003-1 | `test_ac_fr_003_1_toc_tokens` | fail | pass |
| AC-FR-003-2 | `test_ac_fr_003_2_no_contents_token` | fail | pass |

Full suite, base before the change: {'pass': 1114, 'skip': 52}
Full suite, head: {'pass': 1121, 'skip': 52}

## autose check: PASSED

