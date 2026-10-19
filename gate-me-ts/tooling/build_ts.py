#!/usr/bin/env python3
"""Build GATE ME 2027 Test Series Word files in the Dig Career Thrust website's table format.

Usage
  Topic / subject test (one file):
    python3 build_ts.py test.json "<out.docx>" <figures_dir> <seed>
  Full-length mock (two files: Section A = General Aptitude, Section B = Technical):
    python3 build_ts.py mock.json "<out_section_A.docx>" <figures_dir> <seed> --mock "<out_section_B.docx>"

test.json = {"questions": [...]} — each question:
  qtype "mcq"      {question, options[4], answer (0-based index of correct option), solution, marks 1|2, negative 0.33|0.67}
  qtype "integer"  {question, answer (int), solution, marks}
  qtype "fill_ups" {question, range [lo, hi], solution, marks}
  mocks also need "section": "A" (General Aptitude) or "B" (Technical) on every question.
Math as \\(...\\) with NO space right inside the delimiters; figures as [[IMG:name.png]] from figures_dir.
Options are shuffled per seed so the key is not predictable.
"""
import sys, os, json, io, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "gate90", "tooling"))
import build_paper as bp
from PIL import Image


def _shrink(path):
    zin = zipfile.ZipFile(path); buf = io.BytesIO(); zout = zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED)
    for it in zin.infolist():
        data = zin.read(it.filename)
        if it.filename.startswith("word/media/") and it.filename.endswith(".png"):
            im = Image.open(io.BytesIO(data)).convert("L").point(lambda v: 255 if v > 200 else (0 if v < 60 else v))
            b = io.BytesIO(); im.quantize(8).save(b, "PNG", optimize=True); data = b.getvalue()
        zout.writestr(it, data)
    zout.close(); zin.close(); open(path, "wb").write(buf.getvalue())


def build(qs, out, img, seed):
    for q in qs:
        q.setdefault("group", "Mechanical")
        q["section"] = "B"  # build_paper needs a section; one file per call
        if q.get("qtype", "mcq") == "mcq":
            q.setdefault("negative", 0.33 if q.get("marks", 1) == 1 else 0.67)
    # 1-mark questions first, then 2-mark, as on the GATE screen (stable within each group)
    qs = sorted(qs, key=lambda q: q.get("marks", 1))
    tpl = bp.DEFAULT_TEMPLATE
    res = bp.resolve(qs, seed)
    math = bp.latex_to_omml(bp.collect_math(res))
    bp.build_docx(res, out, tpl, bp.body_open_tag(tpl), math, img)
    _shrink(out)
    print("wrote", out, len(qs), "questions,", os.path.getsize(out), "bytes")


if __name__ == "__main__":
    a = sys.argv[1:]
    inp, out, img, seed = a[:4]
    qs = json.load(open(inp))["questions"]
    if "--mock" in a:
        out_b = a[a.index("--mock") + 1]
        sa = [q for q in qs if q.get("section") == "A"]
        sb = [q for q in qs if q.get("section") == "B"]
        assert len(sa) == 10 and len(sb) == 55, (len(sa), len(sb))
        build(sa, out, img, seed + ":A")
        build(sb, out_b, img, seed + ":B")
    else:
        build(qs, out, img, seed)
