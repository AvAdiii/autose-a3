#!/usr/bin/env bash
# Start the experiment reviews (E1, E2) as production review-only runs and record their run ids in
# results/review_runs.csv. Usage: results/dispatch_reviews.sh [cell ...]
# Cells: opus-isolated (production; shared by E1 and E2), opus-shared (E1), sonnet-isolated (E2).
set -euo pipefail
repo=AvAdiii/markdown
here=$(cd "$(dirname "$0")" && pwd)
csv=$here/review_runs.csv
[ -f "$csv" ] || echo "cell,seeded,run_id" > "$csv"
cells=("${@:-opus-isolated opus-shared sonnet-isolated}")
# seeded id -> PR, issue (experiment/seeded_prs/labels.csv)
declare -A PR=([S1]=6 [S2]=7 [S3]=8 [S4]=9 [S5]=10) ISSUE=([S1]=2 [S2]=3 [S3]=4 [S4]=1 [S5]=5)
for cell in ${cells[@]}; do
  case $cell in
    opus-isolated)   variant=isolated model='' ;;
    opus-shared)     variant=shared   model='' ;;
    sonnet-isolated) variant=isolated model=claude-sonnet-5-5 ;;
    *) echo "unknown cell $cell" >&2; exit 1 ;;
  esac
  for s in S1 S2 S3 S4 S5; do
    grep -q "^$cell,$s," "$csv" && { echo "skip $cell/$s (already dispatched)"; continue; }
    before=$(gh run list --repo $repo --workflow autose.yml --event workflow_dispatch --limit 1 --json databaseId --jq '.[0].databaseId // 0')
    gh workflow run autose.yml --repo $repo -f issue=${ISSUE[$s]} -f start_stage=review -f pr=${PR[$s]} \
      -f reviewer_variant=$variant -f reviewer_model="$model" -f rework=false
    for _ in $(seq 30); do
      sleep 3
      id=$(gh run list --repo $repo --workflow autose.yml --event workflow_dispatch --limit 1 --json databaseId --jq '.[0].databaseId // 0')
      [ "$id" != "$before" ] && break
    done
    [ "$id" = "$before" ] && { echo "no run appeared for $cell/$s" >&2; exit 1; }
    echo "$cell,$s,$id" >> "$csv"
    echo "dispatched $cell/$s -> run $id"
  done
done
