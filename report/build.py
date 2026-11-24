"""Build report.pdf from report/report.md (+ report/experiments.md). Needs: markdown, weasyprint.
    python report/build.py"""
import csv
from pathlib import Path

import markdown
from weasyprint import HTML

R = Path(__file__).resolve().parent
ROOT = R.parent

SVG = """<svg viewBox="0 0 760 210" xmlns="http://www.w3.org/2000/svg" font-family="Helvetica" font-size="11">
<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
<path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs>
<style>.b{fill:#f4f6fa;stroke:#334;stroke-width:1}.j{fill:none;stroke:#889;stroke-dasharray:4 3}.t{font-weight:bold}
line,path.l{stroke:#333;stroke-width:1.2;marker-end:url(#a);fill:none}</style>
<rect class="b" x="5" y="80" width="80" height="44" rx="5"/><text x="45" y="98" text-anchor="middle" class="t">Issue</text>
<text x="45" y="113" text-anchor="middle">label / /autose</text>
<rect class="b" x="105" y="80" width="70" height="44" rx="5"/><text x="140" y="98" text-anchor="middle" class="t">gate</text>
<text x="140" y="113" text-anchor="middle">write access?</text>
<rect class="j" x="195" y="8" width="335" height="194" rx="6"/><text x="205" y="22" class="t">build job (no push)</text>
<text x="205" y="36">orchestrator.py: state machine, checks in code</text>
<rect class="b" x="205" y="48" width="100" height="34" rx="4"/><text x="255" y="63" text-anchor="middle">1 analyst+judge</text><text x="255" y="76" text-anchor="middle">spec.md</text>
<rect class="b" x="315" y="48" width="100" height="34" rx="4"/><text x="365" y="63" text-anchor="middle">2 architect</text><text x="365" y="76" text-anchor="middle">design.md</text>
<rect class="b" x="425" y="48" width="95" height="34" rx="4"/><text x="472" y="63" text-anchor="middle">3 developer</text><text x="472" y="76" text-anchor="middle">diff.patch</text>
<rect class="b" x="425" y="118" width="95" height="34" rx="4"/><text x="472" y="133" text-anchor="middle">4 tester @base</text><text x="472" y="146" text-anchor="middle">test_report.md</text>
<line x1="305" y1="65" x2="314" y2="65"/><line x1="415" y1="65" x2="424" y2="65"/>
<path class="l" d="M460,82 L460,117"/><path class="l" d="M485,117 L485,83"/>
<text x="262" y="112" font-size="10">each stage: artifact + code check</text><text x="262" y="126" font-size="10">fail → retry / route by owner</text>
<text x="262" y="140" font-size="10">budgets in config.json</text><text x="262" y="154" font-size="10">stop → STOPPED.md + status</text>
<rect class="b" x="550" y="48" width="95" height="44" rx="4"/><text x="597" y="64" text-anchor="middle" class="t">5 release</text>
<text x="597" y="78" text-anchor="middle">App push, PR, CI</text>
<rect class="b" x="550" y="118" width="95" height="54" rx="4"/><text x="597" y="134" text-anchor="middle" class="t">6 review</text>
<text x="597" y="148" text-anchor="middle">fresh VM, no push</text><text x="597" y="162" text-anchor="middle">issue+diff only</text>
<rect class="b" x="665" y="80" width="88" height="44" rx="5"/><text x="709" y="98" text-anchor="middle" class="t">Human</text>
<text x="709" y="113" text-anchor="middle">merges</text>
<line x1="85" y1="102" x2="104" y2="102"/><line x1="175" y1="102" x2="194" y2="102"/>
<line x1="530" y1="70" x2="549" y2="70"/><line x1="597" y1="92" x2="597" y2="117"/>
<line x1="645" y1="140" x2="664" y2="112"/>
<path class="l" d="M597,172 L597,190 L235,190 L235,83"/><text x="300" y="185">request_changes → earliest stage named (≤2 rounds)</text>
</svg>"""

LANES = ["Maintainer", "gate", "build: orchestrator", "agents (Sonnet/Haiku)", "release (App)", "fork CI", "review job"]
MSGS = [  # (from, to, label, time)
    (0, 1, "/autose on issue #2", "09:26:22"),
    (1, 2, "permission=admin; trigger.json", "09:26:30"),
    (2, 3, "analyst: issue in <untrusted-issue>", ""),
    (3, 2, "spec.md 11 ACs; judge 11/11 testable", "09:28:04"),
    (2, 3, "architect: spec + ARCHITECTURE.md", ""),
    (3, 2, "design.md; AST check passed", ""),
    (2, 3, "developer: spec + design", ""),
    (3, 2, "diff.patch; build check passed", ""),
    (2, 3, "tester at base bb9e8d8", ""),
    (3, 2, "fail on base, pass on head; 1114→1125", "09:29:21"),
    (2, 4, "artifact r0-build", ""),
    (4, 5, "push 30f9655, PR #12", "09:29:39"),
    (5, 4, "13 checks green", "09:31:46"),
    (4, 6, "pr=12, ci_ok", ""),
    (6, 6, "issue + diff only; 6 own checks", ""),
    (6, 0, "APPROVED review on PR #12", "09:32:54"),
]


def seq_svg() -> str:
    W, top, dy = 760, 30, 17
    xs = [45, 135, 235, 450, 560, 645, 712]  # wide gap where the agent hand-offs are labelled
    H = top + dy * (len(MSGS) + 1) + 10
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Helvetica" font-size="9.5">',
         '<defs><marker id="s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
         '<path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs>']
    for x, n in zip(xs, LANES):
        o.append(f'<rect x="{x-52}" y="4" width="104" height="18" rx="3" fill="#eef1f6" stroke="#334"/>'
                 f'<text x="{x}" y="16" text-anchor="middle" font-weight="bold">{n}</text>'
                 f'<line x1="{x}" y1="22" x2="{x}" y2="{H-4}" stroke="#bbb" stroke-dasharray="3 3"/>')
    for i, (a, b, lab, t) in enumerate(MSGS):
        y = top + dy * (i + 1)
        if a == b:
            x = xs[a]
            o.append(f'<path d="M{x},{y-6} h18 v8 h-16" fill="none" stroke="#333" marker-end="url(#s)"/>'
                     f'<text x="{x-6}" y="{y-8}" text-anchor="end">{lab}</text>')
        else:
            x1, x2 = xs[a], xs[b]
            o.append(f'<line x1="{x1}" y1="{y}" x2="{x2 + (-3 if x2 > x1 else 3)}" y2="{y}" stroke="#333" '
                     f'marker-end="url(#s)"{" stroke-dasharray=\"4 2\"" if b < a else ""}/>'
                     f'<text x="{(x1+x2)/2}" y="{y-3}" text-anchor="middle">{lab}</text>')
        if t:
            o.append(f'<text x="{W-2}" y="{y-3}" text-anchor="end" fill="#666" font-size="8.5">{t}</text>')
    o.append("</svg>")
    return "".join(o)


CSS = """@page{size:A4;margin:16mm 15mm 15mm 15mm;@bottom-center{content:counter(page);font-size:9pt;color:#666}}
body{font-family:Helvetica,Arial,sans-serif;font-size:9.6pt;line-height:1.36;color:#111}
h1{font-size:17pt;margin:0 0 4pt}h2{font-size:12.5pt;margin:12pt 0 4pt;border-bottom:1px solid #ccd;padding-bottom:2pt}
h3{font-size:10.5pt;margin:8pt 0 2pt}p{margin:3pt 0 5pt}ul,ol{margin:2pt 0 5pt;padding-left:16pt}li{margin:1pt 0}
table{border-collapse:collapse;width:100%;margin:4pt 0 6pt;font-size:8.3pt}th,td{border:1px solid #bbc;padding:2pt 3pt;vertical-align:top}
th{background:#eef1f6}code{font-family:Menlo,Consolas,monospace;font-size:8.4pt;background:#f3f3f3;padding:0 1.5pt}
a{color:#1a4fa0;text-decoration:none}.fig svg{width:100%;height:auto;margin:2pt 0 4pt}"""


def totals() -> str:
    rows = list(csv.DictReader((ROOT / "results/results.csv").open()))
    k = lambda rs, c: sum(int(r.get(c) or 0) for r in rs)
    out, inp, cr, cc = (k(rows, c) for c in ("output_tokens", "input_tokens", "cache_read_tokens",
                                              "cache_creation_tokens"))
    usd = sum(float(r["cost_usd"] or 0) for r in rows)
    s = (f"Pipeline: {len(rows)} runs, {k(rows, 'sessions')} agent sessions, {out:,} output, {inp:,} "
         f"uncached input, {cc:,} cache-write and {cr:,} cache-read tokens "
         f"(**{out + inp + cc + cr:,} in total**), ${usd:.2f} at API prices")
    rv = ROOT / "results/reviews_scored.csv"
    if rv.exists():
        rr = list(csv.DictReader(rv.open()))
        ro, ri, rc = k(rr, "output_tokens"), k(rr, "input_tokens"), k(rr, "cache_read_tokens")
        s += (f". Experiment reviews: {len(rr)} sessions, {ro:,} output, {ri:,} input and {rc:,} "
              f"cache-read tokens (**{ro + ri + rc:,}**)")
    return s + "."


def main() -> None:
    md = (R / "report.md").read_text()
    exp = (R / "experiments.md").read_text() if (R / "experiments.md").exists() else "*(pending)*"
    md = md.replace("{{EXPERIMENTS}}", exp).replace("{{TOTALS}}", totals())
    html = markdown.markdown(md, extensions=["tables", "sane_lists"]).replace("{{SVG}}", SVG).replace("{{SEQ}}", seq_svg())
    doc = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{html}</body></html>"
    pdf = HTML(string=doc).write_pdf(ROOT / "report.pdf")
    import subprocess
    pages = subprocess.run(["python3", "-c", "print(open('report.pdf','rb').read().count(b'/Type /Page'))"],
                           cwd=ROOT, capture_output=True, text=True).stdout.strip()
    print("wrote report.pdf, pages (approx):", pages)


if __name__ == "__main__":
    main()
