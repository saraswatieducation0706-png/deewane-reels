#!/usr/bin/env python3
"""Build one GATE ME 90 Days Challenge test as a single Word file in the Dig Career Thrust
website's MCQ-table format.
Usage: python3 build_test.py test.json "<out.docx>" <figures_dir> <seed>
test.json = {"questions":[{question, options[4], answer(0-based), solution, marks(1|2), negative(0.33|0.67)}...]}
Math in \\( ... \\); figures as [[IMG:name.png]] (see build_paper.py)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_paper as bp
inp, out, img, seed = sys.argv[1:5]
qs = json.load(open(inp))["questions"]
for q in qs: q.setdefault("section", "B"); q.setdefault("group", "Mechanical")
tpl = bp.DEFAULT_TEMPLATE
res = bp.resolve(qs, seed)
math = bp.latex_to_omml(bp.collect_math(res))
bp.build_docx(res, out, tpl, bp.body_open_tag(tpl), math, img)
print("wrote", out, len(qs), "questions")

# shrink figures so the .docx is small enough to upload to Google Drive through the connector
import zipfile, io
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
_shrink(out)
print("shrunk to", os.path.getsize(out), "bytes")
