"""Score the experiment reviews (E1, E2) against experiment/seeded_prs/labels.csv.

Usage:
    python results/score_reviews.py fetch    # download each run's r0-6-review artifact into results/reviews/
    python results/score_reviews.py score    # write results/reviews_scored.csv and print the per-cell table

Input: results/review_runs.csv with columns cell,seeded,run_id (cell is one of opus-isolated,
opus-shared, sonnet-isolated). Every review is the production review job started by
workflow_dispatch (start_stage=review), so its artifact holds review.json and usage.jsonl.

Matching rule for "defect detected" (written down before scoring, see experiment/variants.md):
a finding marked blocking whose title or evidence matches the seeded PR's pattern below. The
patterns name the observable behaviour of the planted defect, not the wording of the label.
The matched text is written to the CSV so every match can be checked by hand.
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "results" / "review_runs.csv"
LABELS = ROOT / "experiment" / "seeded_prs" / "labels.csv"
DL = ROOT / "results" / "reviews"
OUT = ROOT / "results" / "reviews_scored.csv"
REPO = "AvAdiii/markdown"

DEFECT_PATTERNS = {
    # braces of the empty list leak into the rendered text
    "S1": r"\{:\s*\}.*(text|output|render|heading|h1|leak|remain|visible|literal)|"
          r"(leak|remain|left|visible|literal|appear).*\{:\s*\}|<h1>Title \{:",
    # the href is derived from the label, not from the target
    "S2": r"read_the_guide|(href|url|link).{0,80}(from|uses?|built|derived).{0,20}label|"
          r"label.{0,80}(href|url)|target.{0,40}(ignored|unused|discarded)",
    # toc_tokens / md.toc still contain the excluded heading, or HTML string surgery
    "S3": r"toc_tokens|md\.toc\b|\.toc\b.*still|serializ|regex.*html|html.*regex|postprocessor",
    # no entry point: extensions=['external_links'] cannot be loaded by name
    "S5": r"entry[ _-]?point|pyproject|by name|'external_links'.*(raise|fail|error|import)|"
          r"(raise|fail|error|import).*'external_links'|ModuleNotFoundError|ImportError",
}


def load_csv(p: Path) -> list[dict]:
    with p.open() as f:
        return list(csv.DictReader(f))


def fetch() -> None:
    for r in load_csv(RUNS):
        d = DL / r["cell"] / r["seeded"]
        if (d / "review.json").exists():
            continue
        d.mkdir(parents=True, exist_ok=True)
        subprocess.run(["gh", "run", "download", r["run_id"], "--repo", REPO, "-n", "r0-6-review", "-D", str(d)],
                       check=True)
        print(f"fetched {r['cell']}/{r['seeded']} (run {r['run_id']})")


def usage(d: Path) -> dict:
    tot = {"output_tokens": 0, "input_tokens": 0, "cache_read_tokens": 0, "turns": 0, "duration_s": 0.0}
    f = d / "usage.jsonl"
    if f.exists():
        for line in f.read_text().splitlines():
            u = json.loads(line)
            for k in tot:
                tot[k] += u.get(k) or 0
    return tot


def score_one(label: dict, review: dict) -> dict:
    sid = label["id"]
    verdict = review.get("verdict", "none")
    blocking = [f for f in review.get("findings", []) if f.get("blocking")]
    pat = DEFECT_PATTERNS.get(sid)
    match = ""
    if pat:
        for f in blocking:
            text = f"{f.get('title', '')} {f.get('evidence', '')}"
            m = re.search(pat, text, re.I | re.S)
            if m:
                match = f"[{f.get('category')}] {f.get('title', '')[:120]} :: '{m.group(0)[:60]}'"
                break
    expected = label["expected_verdict"]
    executed = [c for c in review.get("own_checks", []) if c.get("result") in ("pass", "fail")]
    return {
        "verdict": verdict,
        "verdict_correct": int(verdict == expected),
        "defect_detected": "" if sid == "S4" else int(bool(match)),
        "matched_finding": match,
        "route": review.get("route", ""),
        "routing_correct": "" if sid == "S4" else int(review.get("route", "") == label["defect_category"]),
        "false_rejection": int(sid == "S4" and verdict == "request_changes"),
        "blocking_findings": len(blocking),
        "probes_executed": len(executed),
        "validation_notes": "; ".join(review.get("validation_notes", [])),
    }


def score() -> None:
    labels = {r["id"]: r for r in load_csv(LABELS)}
    rows = []
    for r in load_csv(RUNS):
        d = DL / r["cell"] / r["seeded"]
        review = json.loads((d / "review.json").read_text()) if (d / "review.json").exists() else {}
        row = {"cell": r["cell"], "seeded": r["seeded"], "pr": labels[r["seeded"]]["pr"], "run_id": r["run_id"],
               "model": review.get("model", ""), "variant": review.get("variant", "")}
        row.update(score_one(labels[r["seeded"]], review))
        row.update(usage(d))
        rows.append(row)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    print("| cell | verdict correct | defects detected | routing correct | false rejections | probes (mean) "
          "| output tokens (mean) | time s (mean) |")
    print("|---|---|---|---|---|---|---|---|")
    for cell in dict.fromkeys(r["cell"] for r in rows):
        cr = [r for r in rows if r["cell"] == cell]
        dr = [r for r in cr if r["seeded"] != "S4"]
        n = len(cr)
        print(f"| {cell} | {sum(r['verdict_correct'] for r in cr)}/{n} "
              f"| {sum(r['defect_detected'] for r in dr)}/{len(dr)} "
              f"| {sum(r['routing_correct'] for r in dr)}/{len(dr)} "
              f"| {sum(r['false_rejection'] for r in cr)}/{sum(r['seeded'] == 'S4' for r in cr)} "
              f"| {sum(r['probes_executed'] for r in cr) / n:.1f} "
              f"| {sum(r['output_tokens'] for r in cr) / n:.0f} "
              f"| {sum(r['duration_s'] for r in cr) / n:.0f} |")


if __name__ == "__main__":
    {"fetch": fetch, "score": score}[sys.argv[1] if len(sys.argv) > 1 else "score"]()
