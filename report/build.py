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
<text x="597" y="148" text-anchor="middle">fresh VM, Opus</text><text x="597" y="162" text-anchor="middle">issue+diff only</text>
<rect class="b" x="665" y="80" width="88" height="44" rx="5"/><text x="709" y="98" text-anchor="middle" class="t">Human</text>
<text x="709" y="113" text-anchor="middle">merges</text>
<line x1="85" y1="102" x2="104" y2="102"/><line x1="175" y1="102" x2="194" y2="102"/>
<line x1="530" y1="70" x2="549" y2="70"/><line x1="597" y1="92" x2="597" y2="117"/>
<line x1="645" y1="140" x2="664" y2="112"/>
<path class="l" d="M597,172 L597,190 L235,190 L235,83"/><text x="300" y="185">request_changes → earliest stage named (≤2 rounds)</text>
</svg>"""

CSS = """@page{size:A4;margin:16mm 15mm 15mm 15mm;@bottom-center{content:counter(page);font-size:9pt;color:#666}}
body{font-family:Helvetica,Arial,sans-serif;font-size:9.6pt;line-height:1.36;color:#111}
h1{font-size:17pt;margin:0 0 4pt}h2{font-size:12.5pt;margin:12pt 0 4pt;border-bottom:1px solid #ccd;padding-bottom:2pt}
h3{font-size:10.5pt;margin:8pt 0 2pt}p{margin:3pt 0 5pt}ul,ol{margin:2pt 0 5pt;padding-left:16pt}li{margin:1pt 0}
table{border-collapse:collapse;width:100%;margin:4pt 0 6pt;font-size:8.3pt}th,td{border:1px solid #bbc;padding:2pt 3pt;vertical-align:top}
th{background:#eef1f6}code{font-family:Menlo,Consolas,monospace;font-size:8.4pt;background:#f3f3f3;padding:0 1.5pt}
a{color:#1a4fa0;text-decoration:none}.fig svg{width:100%;height:auto;margin:2pt 0 4pt}"""


def totals() -> str:
    rows = list(csv.DictReader((ROOT / "results/results.csv").open()))
    out = sum(int(r["output_tokens"] or 0) for r in rows)
    cr = sum(int(r["cache_read_tokens"] or 0) for r in rows)
    usd = sum(float(r["cost_usd"] or 0) for r in rows)
    n = sum(int(r["sessions"] or 0) for r in rows)
    s = (f"{len(rows)} pipeline runs, {n} agent sessions, {out:,} output tokens, {cr:,} cache-read tokens, "
         f"${usd:.2f} API-price equivalent")
    rv = ROOT / "results/reviews_scored.csv"
    if rv.exists():
        rr = list(csv.DictReader(rv.open()))
        s += (f"; experiment reviews: {len(rr)} sessions, "
              f"{sum(int(r['output_tokens'] or 0) for r in rr):,} output tokens")
    return s + "."


def main() -> None:
    md = (R / "report.md").read_text()
    exp = (R / "experiments.md").read_text() if (R / "experiments.md").exists() else "*(pending)*"
    md = md.replace("{{EXPERIMENTS}}", exp).replace("{{TOTALS}}", totals())
    html = markdown.markdown(md, extensions=["tables", "sane_lists"]).replace("{{SVG}}", SVG)
    doc = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{html}</body></html>"
    pdf = HTML(string=doc).write_pdf(ROOT / "report.pdf")
    import subprocess
    pages = subprocess.run(["python3", "-c", "print(open('report.pdf','rb').read().count(b'/Type /Page'))"],
                           cwd=ROOT, capture_output=True, text=True).stdout.strip()
    print("wrote report.pdf, pages (approx):", pages)


if __name__ == "__main__":
    main()
