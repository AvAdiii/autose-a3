"""Collect every pipeline run into results/results.csv and archive its artifacts.

Usage:
    python results/collect_runs.py fetch     # download the stage artifacts of each run into results/artifacts/<label>/
    python results/collect_runs.py hidden    # run the hidden tests on each run's released head (needs REF_CLONE)
    python results/collect_runs.py csv       # write results/results.csv

Input: results/pipeline_runs.csv (label,issue_id,issue,run_id,note). Everything else is read from
the run (GitHub API) and its artifacts; hidden-test results are cached in results/hidden_results.csv.
REF_CLONE: a local clone of the fork with a remote `gh` (hidden tests are run on a worktree of it).
"""
from __future__ import annotations

import csv
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
ART = RES / "artifacts"
RUNS = RES / "pipeline_runs.csv"
HIDDEN = RES / "hidden_results.csv"
REPO = "AvAdiii/markdown"
SKIP = {"baseline.json", "tests-head-all.json"}  # large raw suite dumps; summarised in test_report.md


def rows(p: Path) -> list[dict]:
    with p.open() as f:
        return list(csv.DictReader(f))


def gh_json(*args: str):
    return json.loads(subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout)


def fetch() -> None:
    for r in rows(RUNS):
        d = ART / r["label"]
        if d.exists():
            continue
        names = [a["name"] for a in gh_json("api", f"repos/{REPO}/actions/runs/{r['run_id']}/artifacts",
                                            "--jq", "[.artifacts[]|{name}]")]
        for n in names:
            if not re.match(r"r\d-(build|5-release|6-review)$", n):
                continue
            subprocess.run(["gh", "run", "download", r["run_id"], "--repo", REPO, "-n", n, "-D", str(d / n)],
                           check=True)
            for f in (d / n).rglob("*"):
                if f.name in SKIP:
                    f.unlink()
        print(f"fetched {r['label']}: {sorted(p.name for p in d.iterdir()) if d.exists() else 'no artifacts'}")


def last(d: Path, pattern: str) -> Path | None:
    found = sorted(d.glob(pattern))
    return found[-1] if found else None


def released_head(d: Path) -> tuple[str, str, str]:
    rel = last(d, "r*-5-release/release.json")
    if not rel:
        return "", "", ""
    j = json.loads(rel.read_text())
    return str(j.get("pr", "")), j.get("head", ""), "pass" if j.get("ci_ok") else "fail"


def hidden() -> None:
    clone = Path(os.environ["REF_CLONE"])
    py = os.environ.get("HIDDEN_PY", sys.executable)
    cache = {h["label"]: h for h in rows(HIDDEN)} if HIDDEN.exists() else {}
    for r in rows(RUNS):
        pr, head, _ = released_head(ART / r["label"])
        if not head or r["label"] in cache:
            continue
        subprocess.run(["git", "-C", str(clone), "fetch", "-q", "gh", head], check=True)
        wt = clone.parent / f"hidden-{r['label']}"
        shutil.rmtree(wt, ignore_errors=True)
        subprocess.run(["git", "-C", str(clone), "worktree", "prune"], check=True)
        subprocess.run(["git", "-C", str(clone), "worktree", "add", "-q", "-f", "--detach", str(wt), head], check=True)
        out = subprocess.run(["bash", str(ROOT / "experiment/hidden_tests/run_hidden.sh"), str(wt), r["issue_id"], py],
                             capture_output=True, text=True)
        text = out.stdout + out.stderr
        total = int(m.group(1)) if (m := re.search(r"Ran (\d+) test", text)) else 0
        failed = sum(int(x) for x in re.findall(r"(?:failures|errors)=(\d+)", text))
        cache[r["label"]] = {"label": r["label"], "head": head, "hidden_pass": total - failed, "hidden_total": total}
        print(f"{r['label']} {head[:7]}: hidden {total - failed}/{total}")
    with HIDDEN.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["label", "head", "hidden_pass", "hidden_total"])
        w.writeheader()
        w.writerows(cache.values())


def usage(d: Path) -> dict:
    tot = {"sessions": 0, "output_tokens": 0, "input_tokens": 0, "cache_read_tokens": 0, "cache_creation_tokens": 0,
           "cost_usd": 0.0, "agent_s": 0.0}
    for f in d.rglob("usage.jsonl"):
        for line in f.read_text().splitlines():
            u = json.loads(line)
            tot["sessions"] += 1
            for k in ("output_tokens", "input_tokens", "cache_read_tokens", "cache_creation_tokens"):
                tot[k] += u.get(k) or 0
            tot["cost_usd"] += u.get("cost_usd") or 0
            tot["agent_s"] += u.get("duration_s") or 0
    tot["cost_usd"] = round(tot["cost_usd"], 2)
    tot["agent_s"] = round(tot["agent_s"])
    return tot


def ts(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def csv_out() -> None:
    hid = {h["label"]: h for h in rows(HIDDEN)} if HIDDEN.exists() else {}
    out = []
    for r in rows(RUNS):
        d = ART / r["label"]
        run = gh_json("run", "view", r["run_id"], "--repo", REPO, "--json", "createdAt,updatedAt,event,jobs")
        jobs = [j for j in run["jobs"] if j.get("startedAt") and j.get("completedAt")]
        wall = int((ts(max(j["completedAt"] for j in jobs)) - ts(run["createdAt"])).total_seconds()) if jobs else ""
        rounds = sorted({p.name[:2] for p in d.glob("r*-*")}) if d.exists() else []
        st_file = last(d, "r*-build/state.json")
        st = json.loads(st_file.read_text()) if st_file else {}
        stages = st.get("stages", {})
        stop = d / (st_file.parent.name if st_file else "") / "STOPPED.md"
        rep = last(d, "r*-build/test_report.md")
        suite = re.findall(r"\{'pass': (\d+)", rep.read_text()) if rep else []
        new_tests = len(re.findall(r"^\| AC-", rep.read_text(), re.M)) if rep else ""
        pr, head, ci = released_head(d)
        rv = last(d, "r*-6-review/review.json")
        review = json.loads(rv.read_text()) if rv else {}
        h = hid.get(r["label"], {})
        if review.get("verdict") == "approve":
            outcome = "approved PR"
        elif review.get("verdict"):
            outcome = f"review: {review['verdict']}"
        elif ci == "fail":
            outcome = "stopped: CI failed"
        elif st.get("final", {}).get("status") == "stopped" or stop.exists():
            outcome = "stopped: " + st.get("final", {}).get("kind", "") + " at " + st.get("final", {}).get("stage", "")
        else:
            outcome = st.get("final", {}).get("status", "")
        row = {
            "label": r["label"], "issue_id": r["issue_id"], "kind": {"B": "bug", "F": "feature", "V": "vague"}[r["issue_id"][0]],
            "issue": r["issue"], "run_id": r["run_id"], "run_url": f"https://github.com/{REPO}/actions/runs/{r['run_id']}",
            "trigger": run["event"], "rounds": len(rounds),
            "req_attempts": stages.get("requirements", {}).get("attempts", ""),
            "design_attempts": stages.get("design", {}).get("attempts", ""),
            "impl_attempts": stages.get("implementation", {}).get("attempts", ""),
            "test_attempts": stages.get("testing", {}).get("attempts", ""),
            "ac_tests": new_tests, "suite_before": suite[0] if suite else "", "suite_after": suite[1] if len(suite) > 1 else "",
            "pr": pr, "ci": ci, "review_verdict": review.get("verdict", ""), "review_route": review.get("route", ""),
            "reviewer_checks_run": len([c for c in review.get("own_checks", []) if c.get("result") in ("pass", "fail")]),
            "hidden_pass": h.get("hidden_pass", ""), "hidden_total": h.get("hidden_total", ""),
            "outcome": outcome, "wall_s": wall, **usage(d), "note": r["note"],
        }
        out.append(row)
    with (RES / "results.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    for o in out:
        print(o["label"], o["issue_id"], o["outcome"], f"hidden {o['hidden_pass']}/{o['hidden_total']}",
              f"out_tok {o['output_tokens']}", f"{o['wall_s']}s")


if __name__ == "__main__":
    {"fetch": fetch, "hidden": hidden, "csv": csv_out}[sys.argv[1]]()
