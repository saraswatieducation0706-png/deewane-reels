#!/usr/bin/env python3
"""Build the branded GATE ME 90 Days Challenge practice-set PDF.
Usage: python3 build_practice_pdf.py practice.json <figures_dir> <out.pdf>
practice.json: day, subject, topic, days_to_gate, summary, minutes, test_qs, test_minutes, test_marking,
next_day ("" on the last day), questions[{type: MCQ|NAT, text, fig?, opts?[4], ans, solution[paragraphs], sfig?}]
HTML allowed in text (sub/sup/b). Figures are PNGs in <figures_dir>."""
import html, json, os, sys, shutil, tempfile
inp, figdir, out = sys.argv[1:4]
D = json.load(open(inp)); Q = D["questions"]
for x in Q: x["t"]=x["type"]; x["sol"]=x["solution"]; x.setdefault("fig",None); x.setdefault("opts",None); x.setdefault("sfig",None)
RED = "#D7191F"
work = tempfile.mkdtemp()
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "tooling", "assets")
for f in os.listdir(ASSETS): shutil.copy(os.path.join(ASSETS, f), work)
for f in os.listdir(figdir):
    if f.endswith(".png"): shutil.copy(os.path.join(figdir, f), work)
win = "7 to 10 PM" if int(D.get("test_minutes", 60)) > 60 else "7 to 8 PM"
nm = sum(1 for x in Q if x["t"] == "MCQ"); nn = len(Q) - nm
nxt = (f'<b>Next, Day {D["day"]+1}/90:</b> {html.escape(D["next_day"])}.' if D.get("next_day") else "<b>That's the final day of the challenge. All the best for GATE!</b>")
def opts_html(o):
    return '<div class="opts">'+"".join(f'<div class="opt"><b>({chr(65+i)})</b> {x}</div>' for i,x in enumerate(o))+'</div>'
qs="".join(f'''<div class="q"><div class="qh"><span class="qn">Q{i+1}</span><span class="tag {'nat' if x['t']=='NAT' else ''}">{x['t']}</span></div>
<div class="qt">{x['text']}</div>{f'<img class="fig" src="{x["fig"]}">' if x['fig'] else ''}{opts_html(x['opts']) if x['opts'] else ''}</div>''' for i,x in enumerate(Q))
key="".join(f'<tr><td>Q{i+1}</td><td>{x["t"]}</td><td>{x["ans"]}</td></tr>' for i,x in enumerate(Q))
sols="".join(f'''<div class="s"><div class="sh"><span class="qn">Q{i+1}</span> <span class="ans">Answer: {x['ans']}</span></div>
{''.join(f'<p>{p}</p>' for p in x['sol'])}{f'<img class="sfig" src="{x["sfig"]}">' if x['sfig'] else ''}</div>''' for i,x in enumerate(Q))

HTML=f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:P;src:url(Poppins-Medium.ttf);font-weight:400}}
@font-face{{font-family:P;src:url(Poppins-SemiBold.ttf);font-weight:600}}
@font-face{{font-family:P;src:url(Poppins-Bold.ttf);font-weight:700}}
@font-face{{font-family:P;src:url(Poppins-ExtraBold.ttf);font-weight:800}}
@page{{size:A4;margin:16mm 15mm 16mm 15mm;
 @top-left{{content:"GATE ME 90 Days Challenge  |  Day {D["day"]}/90  |  Practice Set";font-family:P;font-size:7.5pt;color:#777}}
 @top-right{{content:"Deewane: IES & GATE Point";font-family:P;font-size:7.5pt;color:{RED}}}
 @bottom-left{{content:"web.digcareerthrust.com  |  t.me/digcareerthrust";font-family:P;font-size:7.5pt;color:#777}}
 @bottom-right{{content:"Page " counter(page) " of " counter(pages);font-family:P;font-size:7.5pt;color:#777}}}}
@page:first{{@top-left{{content:none}} @top-right{{content:none}}}}
body{{font-family:"DejaVu Sans",P,sans-serif;font-size:9.6pt;line-height:1.45;color:#1a1a1a}}
h1,h2,.qn,.tag,.band,.ans,th{{font-family:P,sans-serif}}
.cover{{background:{RED};color:#fff;border-radius:10px;padding:16px 20px;display:flex;align-items:center;gap:16px}}
.cover img{{width:62px;height:auto;background:#fff;border-radius:50%;padding:6px}}
.cover .t1{{font-family:P;font-weight:800;font-size:20pt;line-height:1.1}}
.cover .t2{{font-family:P;font-weight:600;font-size:11pt;opacity:.95}}
.meta{{display:flex;gap:8px;margin:12px 0 4px}}
.chip{{flex:1;border:1.2px solid {RED};border-radius:8px;padding:7px 10px}}
.chip .k{{font-family:P;font-size:7.5pt;color:#777;text-transform:uppercase;letter-spacing:.5px}}
.chip .v{{font-family:P;font-weight:700;font-size:11pt;color:{RED}}}
.inst{{background:#FBEAEA;border-radius:8px;padding:9px 12px;font-size:8.8pt;margin:10px 0 6px}}
h2{{font-weight:800;color:{RED};font-size:13pt;border-bottom:2px solid {RED};padding-bottom:3px;margin:16px 0 8px}}
.q{{break-inside:avoid;border-bottom:1px solid #e6e6e6;padding:8px 0}}
.qh{{margin-bottom:3px}}
.qn{{font-weight:800;color:{RED};font-size:10.5pt;margin-right:6px}}
.tag{{font-size:7pt;font-weight:600;border:1px solid #999;color:#555;border-radius:4px;padding:0 5px}}
.tag.nat{{border-color:{RED};color:{RED}}}
.fig{{display:block;max-width:62%;max-height:58mm;margin:6px auto}}
.sfig{{display:block;max-width:45%;max-height:52mm;margin:6px auto}}
.opts{{display:grid;grid-template-columns:1fr 1fr;gap:2px 16px;margin-top:4px}}
table{{width:100%;border-collapse:collapse;font-size:9pt}}
th{{background:{RED};color:#fff;text-align:left;padding:5px 8px;font-weight:600}}
td{{border-bottom:1px solid #e3e3e3;padding:4px 8px}}
.s{{break-inside:avoid;margin:0 0 10px;padding:8px 12px;border-left:3px solid {RED};background:#FAFAFA}}
.s p{{margin:3px 0}}
.ans{{font-weight:700;color:#1a1a1a;font-size:9.5pt}}
.end{{break-before:page}}
.cta{{background:{RED};color:#fff;border-radius:10px;padding:14px 18px;margin-top:6px}}
.cta .big{{font-family:P;font-weight:800;font-size:16pt}}
.qr{{display:flex;justify-content:space-around;margin:16px 0 6px;text-align:center;font-family:P;font-size:9pt;font-weight:600}}
.qr img{{width:34mm;height:34mm;border:1px solid #ddd;border-radius:6px;padding:4px;background:#fff}}
</style></head><body>
<div class="cover"><img src="logo_red.png"><div><div class="t1">GATE ME 90 Days Challenge</div><div class="t2">Day {D["day"]}/90 · Practice Set with Detailed Solutions</div></div></div>
<div class="meta">
<div class="chip"><div class="k">Subject</div><div class="v">{D["subject"]}</div></div>
<div class="chip"><div class="k">Today's topic</div><div class="v">{html.escape(D["topic"])}</div></div>
<div class="chip"><div class="k">Countdown</div><div class="v">{D["days_to_gate"]} days to GATE</div></div></div>
<div class="inst"><b>How to use this set:</b> {len(Q)} questions ({nm} MCQ, {nn} NAT) on {D["summary"]}. Try them in <b>{D["minutes"]} minutes</b> without looking at the solutions, then check the answer key and the step-by-step solutions. For NAT questions, enter the number; there is no negative marking for NAT in GATE.<br><b>Today's test:</b> open {win} in the <b>GATE ME 90 Days Challenge</b> course on our app and website (enrol once for ₹1), {D["test_qs"]} new questions on the same topic. Top scorers are announced in the next 8 AM challenge reel.</div>
<h2>Questions</h2>{qs}
<h2 style="break-before:page">Answer Key</h2>
<table><tr><th style="width:12%">Q</th><th style="width:12%">Type</th><th>Answer</th></tr>{key}</table>
<h2>Detailed Solutions</h2>{sols}
<div class="end"><h2>What next?</h2>
<div class="cta"><div class="big">Day {D["day"]} test tonight, {win}</div>{D["test_qs"]} questions · {D["test_minutes"]} minutes · {D["test_marking"]}. Top 3 scorers are announced with name, marks and photo (if shared) in the next 8 AM challenge reel. Not enrolled yet? Join the ₹1 challenge course: comment GATE90 on our reel for the link.</div>
<div class="qr"><div><img src="qr_website.jpeg"><br>Website test series</div><div><img src="qr_playstore_app.jpeg"><br>Dig Career Thrust app</div><div><img src="qr_telegram.jpeg"><br>Telegram: daily PDFs</div></div>
<div class="inst">{nxt} Comment <b>GATE90</b> on our reel to get all links.<br>Want concise revision notes? The GATE ME handwritten short notes of an AIR 16 topper are available in the Dig Career Thrust app.</div></div>
</body></html>'''
open(os.path.join(work,"practice.html"),"w").write(HTML)
from weasyprint import HTML as W
W(os.path.join(work,"practice.html"),base_url=work).write_pdf(out)
print("wrote",out)
