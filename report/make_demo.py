"""Build demo.mp4: slides + screenshots of the real runs, narrated with an offline TTS voice (piper).
Usage: python report/make_demo.py <workdir> <piper-voice.onnx>
Needs: playwright (chromium), piper-tts, ffmpeg."""
import csv
import subprocess
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = Path(sys.argv[1])
VOICE = sys.argv[2]
W, H = 1600, 900
GH = "https://github.com/AvAdiii/markdown"


def exp_rows():
    p = ROOT / "results/reviews_scored.csv"
    rows = list(csv.DictReader(p.open())) if p.exists() else []
    out = []
    for cell in dict.fromkeys(r["cell"] for r in rows):
        cr = [r for r in rows if r["cell"] == cell]
        dr = [r for r in cr if r["seeded"] != "S4"]
        out.append((cell, sum(int(r["verdict_correct"]) for r in cr), len(cr),
                    sum(int(r["defect_detected"] or 0) for r in dr), len(dr),
                    sum(int(r["routing_correct"] or 0) for r in dr),
                    sum(int(r["false_rejection"]) for r in cr)))
    return out


def slide(title, body):
    return f"""<html><body style="margin:0;width:{W}px;height:{H}px;background:#0f1720;color:#e8edf3;
font-family:Helvetica,Arial,sans-serif;display:flex;flex-direction:column;justify-content:center;padding:0 110px;box-sizing:border-box">
<div style="font-size:30px;color:#7fb3ff;letter-spacing:1px;margin-bottom:18px">autose · issue in, pull request out</div>
<div style="font-size:58px;font-weight:bold;margin-bottom:34px">{title}</div><div style="font-size:31px;line-height:1.5">{body}</div>
</body></html>"""


def table(rows, head):
    th = "".join(f"<th style='text-align:left;padding:8px 22px;border-bottom:2px solid #7fb3ff'>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td style='padding:8px 22px;border-bottom:1px solid #334'>{c}</td>" for c in r) + "</tr>"
                 for r in rows)
    return f"<table style='border-collapse:collapse;font-size:29px'><tr>{th}</tr>{tr}</table>"


E = exp_rows()
exp_table = table([(c, f"{v}/{n}", f"{d}/{dn}", f"{rt}/{dn}", f"{fr}") for c, v, n, d, dn, rt, fr in E],
                  ["reviewer cell", "verdict right", "defect found", "routing right", "false reject"])

SCENES = [
    ("slide", slide("Issue in, pull request out",
                    "A GitHub Actions workflow on a fork of Python-Markdown.<br>Six fixed stages, five narrow agents, "
                    "checks in code,<br>an independent reviewer, and a human who merges."),
     "This is autose. It turns a GitHub issue into a reviewed pull request on my fork of Python Markdown. "
     "There are six fixed stages, five narrow agents, a check in code after every stage, an independent reviewer, "
     "and a human who always merges."),
    ("svg", None,
     "A maintainer labels an issue, or comments slash autose. A gate job checks that they have write access. "
     "The build job cannot push. A Python state machine runs the analyst with my assignment one skill, the "
     "architect against my assignment two architecture document, the developer, and the tester, who writes tests "
     "at the base commit that must fail there and pass after the change. The release job has no model: it pushes "
     "as a GitHub App and waits for CI. The reviewer runs on a fresh machine, on Opus, and sees only the issue and the diff. "
     "If it requests changes, the run goes back to the earliest stage it names, at most twice."),
    ("shot", (f"{GH}/issues/5", "Updated by the autose workflow"),
     "The workflow keeps one status comment on each issue and updates it after every stage, with the reason for "
     "each pass or stop. A stop always says why, and nothing is pushed after it."),
    ("shot", (f"{GH}/actions/runs/44889589134", None),
     "Here is a real run on issue two, an attribute list bug. This is its Actions run: a gate job, then build, release and review, with the later rounds skipped because "
     "the reviewer approved. Every stage uploads its artifact: the spec, the design, the diff, the test report, "
     "the PR text and the review."),
    ("shot", (f"{GH}/pull/12", None),
     "The pull request is opened by the autose dev bot, CI is green, and the review is posted by a different "
     "identity, GitHub Actions. Main is protected, so only I can merge."),
    ("shot", (f"{GH}/pull/19", "independent review: APPROVE"),
     "The reviewer must run its own checks to approve. This is its approval on the table of contents feature, with "
     "the checks it derived from the issue and ran itself. On the attribute list fix it compared the old and new "
     "regular expression on twenty four inputs. In the very first run, the Bash sandbox was missing on the runner, "
     "and the reviewer refused to approve what it could not verify. That is the fail closed behaviour I wanted."),
    ("shot", (f"{GH}/issues/5", "Q-001"),
     "For the vague issue, the analyst did not guess. It posted three questions and stopped before any code. "
     "After I answered on the issue, the pipeline built the extension, its tests and docs. CI then failed on a docs "
     "spelling lint, so stage five stopped and said why. I added the docs checks to stage three, and the next run "
     "passed CI and was approved."),
    ("slide", slide("A decision that was wrong",
                    "ADR-007 let the Haiku spec judge fail stage 1.<br>Issue #4: the judge accepted two criteria, then "
                    "rejected<br>the <i>same, unchanged text</i> on the retry. Run stopped.<br><br>ADR-011: verdicts are "
                    "sticky per criterion text.<br>ADR-007 is kept and marked superseded."),
     "One decision was wrong. The spec judge could fail stage one, and on issue four it accepted two criteria, then "
     "rejected the same unchanged text on the retry. A single random sample was being treated as a deterministic gate. "
     "ADR eleven caches each verdict by its text, so a retry is judged only on what changed. The old ADR is kept and "
     "marked superseded."),
    ("slide", slide("Reviewer experiments (5 seeded PRs each)",
                    exp_table + "<br><span style='font-size:25px'>Four PRs carry one planted defect, one is correct. "
                    "E1: isolated vs shared author context. E2: Opus vs Sonnet.</span>"),
     "Two experiments test the reviewer on five seeded pull requests: four with one planted defect, one correct. "
     "Experiment one gives the reviewer the authors' context or not. Experiment two swaps Opus for Sonnet. "
     "All three cells scored perfectly, a ceiling effect, so neither hypothesis was supported. Isolation stays because "
     "it costs nothing, and since Sonnet matched Opus at about sixty percent of the tokens, I superseded the reviewer "
     "model decision with ADR twelve, as the rule I wrote before the experiment required."),
    ("slide", slide("Results on the five issues",
                    table([("#1 B1 bug", "approved PR #16", "4/4"), ("#2 B2 bug", "approved PR #12", "4/4"),
                           ("#3 F1 feature", "approved PR #15", "4/4"), ("#4 F2 feature", "judge stop, then approved #19", "4/4"),
                           ("#5 V1 vague", "questions, CI docs fail, then approved #18", "4/4")],
                          ["issue", "outcome", "hidden tests"])
                    + "<br><span style='font-size:25px'>Per issue: 6 to 10 agent sessions, 16k to 28k output tokens, "
                      "6 to 10 minutes.</span>"),
     "Across the five issues, every released change passed all of its hidden acceptance tests, which the agents never "
     "saw, and all five pull requests ended approved by the reviewer, waiting for me to merge. A successful run took "
     "six to ten agent sessions and six to ten minutes."),
    ("slide", slide("Limits",
                    "One trial per cell: direction, not significance.<br>Guard rules for Bash are patterns; the real "
                    "fences are<br>the path filter, missing credentials and the sandbox.<br>The subscription quota is a "
                    "shared, coarse cap.<br><br>Every run, PR and review: results/runs.md"),
     "The limits: one trial per experiment cell, so these are directions rather than significant results. The Bash "
     "guard is pattern based, and the real fences are the path filter, the missing credentials and the sandbox. "
     "And the subscription quota is a shared, coarse cap: when it ran out, a run stopped and explained why. "
     "Every run, pull request and review is linked in results slash runs dot md."),
]


def tts(text, out):
    subprocess.run([sys.executable, "-m", "piper", "-m", VOICE, "-f", str(out), "--length-scale", "0.95"],
                   input=text, text=True, check=True, capture_output=True)
    with wave.open(str(out)) as w:
        return w.getnframes() / w.getframerate()


def main():
    from playwright.sync_api import sync_playwright
    sys.path.insert(0, str(ROOT / "report"))
    from build import SVG
    WORK.mkdir(parents=True, exist_ok=True)
    parts = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        for i, (kind, src, text) in enumerate(SCENES):
            img = WORK / f"s{i:02d}.png"
            if kind == "slide":
                pg.set_content(src)
            elif kind == "svg":
                pg.set_content(f"<html><body style='margin:0;background:#fff;display:flex;align-items:center;"
                               f"justify-content:center;width:{W}px;height:{H}px'><div style='width:1500px'>{SVG}"
                               f"</div></body></html>")
            else:
                url, anchor = src
                pg.goto(url, wait_until="networkidle", timeout=60000)
                if anchor:
                    try:
                        pg.get_by_text(anchor).first.scroll_into_view_if_needed(timeout=8000)
                        pg.mouse.wheel(0, -450)
                        pg.wait_for_timeout(500)
                    except Exception:
                        pass
                pg.wait_for_timeout(3000)
            pg.screenshot(path=str(img))
            wav = WORK / f"s{i:02d}.wav"
            dur = tts(text, wav) + 0.8
            mp4 = WORK / f"s{i:02d}.mp4"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(img), "-i", str(wav),
                            "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p", "-r", "25",
                            "-vf", f"scale={W}:{H}", "-c:a", "aac", "-b:a", "128k", "-af", "apad=pad_dur=0.8",
                            "-t", f"{dur:.2f}", str(mp4)], check=True)
            parts.append(mp4)
            print(f"scene {i}: {dur:.1f}s")
        b.close()
    lst = WORK / "list.txt"
    lst.write_text("".join(f"file '{m}'\n" for m in parts))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                    str(ROOT / "demo.mp4")], check=True)
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                          str(ROOT / "demo.mp4")], capture_output=True, text=True).stdout.strip()
    print("demo.mp4 duration:", out)


if __name__ == "__main__":
    main()
