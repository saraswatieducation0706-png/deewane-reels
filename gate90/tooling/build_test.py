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
