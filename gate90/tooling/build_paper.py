#!/usr/bin/env python3
"""
build_paper.py — Build IOCL full-length test papers as two Word files
(Section A and Section B) in the exact MCQ-table format the website ingests.

Input : a JSON file describing the questions (see schema below).
Output: "Section A - Test N.docx" and "Section B - Test N.docx"

Each MCQ becomes one 8-row / 3-column table, styled identically to the
bundled template (assets/template.docx): grid 1680/3285/4180 DXA, light
blue-grey cell fill (CED7E7), black inner cell borders, white outer border,
pStyle "BodyA".

Rich content in any field (question / option / solution):
  * Math   -> wrap LaTeX in  \\( ... \\)   -> converted to native Word equation.
  * Image  -> write  [[IMG:filename.png]]  -> the PNG (from --images-dir) is
              embedded inline as a Word picture, sized to fit the cell.
Text, math and images may be freely interleaved and appear in written order.

JSON schema
-----------
{
  "test_number": 1,
  "questions": [
    {
      "section": "A",                       # "A" or "B"
      "group": "Quantitative Aptitude",     # A: QA / LR / VA ; B: "Mechanical"
      "topic": "Data interpretation - bar graphs",
      "question": "Study the chart. [[IMG:q3_sales.png]] Which year was highest?",
      "options": ["2019", "2020", "2021", "2022"],
      "answer": 2,
      "solution": "The tallest bar is 2021, as the figure shows.",
      "marks": 1,                           # optional (default 1)
      "negative": 0.25                      # optional (default 0.25)
    }
  ]
}

Correct-option positions are re-shuffled with a per-test seed so the answer
key is not predictable, regardless of where the author placed it.
"""

import argparse
import html
import json
import os
import random
import re
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template.docx")

# ---- fixed geometry / styling cloned from the sample -----------------------
COL1, COL2, COL3 = 1680, 3285, 4180
MERGED = COL2 + COL3
TABLE_W = COL1 + COL2 + COL3

EMU_PER_IN = 914400
IMG_DPI = 150                      # figures are authored/saved at this DPI
WIDE_MAX = (4.3, 3.2)             # (max_w_in, max_h_in) for merged Q/Solution cells
OPT_MAX = (2.0, 1.6)             # for the narrower Option cell

# Author-facing tokens.  \( ... \) = math ; [[IMG:name]] = image.
MATH_RE = re.compile(r'\\\((.+?)\\\)', re.S)
IMG_TOKEN_RE = re.compile(r'\[\[IMG:([^\]]+)\]\]')
SEG_RE = re.compile(r'(\\\(.+?\\\)|\[\[IMG:[^\]]+\]\])', re.S)

TBL_PR = (
    '<w:tblPr>'
    f'<w:tblW w:w="{TABLE_W}" w:type="dxa"/>'
    '<w:tblInd w:w="216" w:type="dxa"/>'
    '<w:tblBorders>'
    '<w:top w:val="single" w:sz="8" w:space="0" w:color="FFFFFF"/>'
    '<w:left w:val="single" w:sz="8" w:space="0" w:color="FFFFFF"/>'
    '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="FFFFFF"/>'
    '<w:right w:val="single" w:sz="8" w:space="0" w:color="FFFFFF"/>'
    '<w:insideH w:val="single" w:sz="8" w:space="0" w:color="FFFFFF"/>'
    '<w:insideV w:val="single" w:sz="8" w:space="0" w:color="FFFFFF"/>'
    '</w:tblBorders>'
    '<w:shd w:val="clear" w:color="auto" w:fill="CED7E7"/>'
    '<w:tblLayout w:type="fixed"/>'
    '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" '
    'w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'
    '</w:tblPr>'
)
TBL_GRID = (
    '<w:tblGrid>'
    f'<w:gridCol w:w="{COL1}"/><w:gridCol w:w="{COL2}"/><w:gridCol w:w="{COL3}"/>'
    '</w:tblGrid>'
)
BLACK_BORDERS = (
    '<w:tcBorders>'
    '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    '</w:tcBorders>'
)
TC_MAR = (
    '<w:tcMar>'
    '<w:top w:w="80" w:type="dxa"/><w:left w:w="80" w:type="dxa"/>'
    '<w:bottom w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/>'
    '</w:tcMar>'
)
SPACER_P = '<w:p><w:pPr><w:pStyle w:val="BodyA"/></w:pPr></w:p>'
SECT_PR = (
    '<w:p><w:pPr><w:pStyle w:val="BodyA"/></w:pPr></w:p>'
    '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
    '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
    'w:header="708" w:footer="708" w:gutter="0"/>'
    '<w:cols w:space="708"/><w:docGrid w:linePitch="360"/></w:sectPr>'
)


# ---- images ----------------------------------------------------------------
def png_size(data):
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError("Embedded images must be PNG (author figures with "
                         "matplotlib savefig('...png')).")
    w = int.from_bytes(data[16:20], "big")
    h = int.from_bytes(data[20:24], "big")
    return w, h


class ImageContext:
    """Accumulates media parts + relationships and emits inline picture XML."""

    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.media = []     # list[(arcname, bytes)]
        self.rels = []      # list[(rId, target)]
        self._n = 0

    def add(self, spec, max_w_in, max_h_in):
        path = spec if os.path.isabs(spec) else os.path.join(self.base_dir, spec)
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Image not found: {path} (referenced as [[IMG:{spec}]]). "
                f"Generate it into --images-dir before building.")
        data = open(path, "rb").read()
        w, h = png_size(data)
        self._n += 1
        arc = f"word/media/img{self._n}.png"
        rid = f"rIdImg{self._n + 1000}"
        pid = self._n + 1000
        self.media.append((arc, data))
        self.rels.append((rid, f"media/img{self._n}.png"))
        # natural inch size at IMG_DPI, scaled DOWN (never up) to fit the box.
        win, hin = w / IMG_DPI, h / IMG_DPI
        s = min(max_w_in / win, max_h_in / hin, 1.0)
        cx, cy = int(win * s * EMU_PER_IN), int(hin * s * EMU_PER_IN)
        return self._drawing(rid, cx, cy, pid)

    @staticmethod
    def _drawing(rid, cx, cy, pid):
        A = "http://schemas.openxmlformats.org/drawingml/2006/main"
        PIC = "http://schemas.openxmlformats.org/drawingml/2006/picture"
        return (
            '<w:r><w:drawing>'
            '<wp:inline distT="0" distB="0" distL="0" distR="0">'
            f'<wp:extent cx="{cx}" cy="{cy}"/>'
            '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
            f'<wp:docPr id="{pid}" name="Picture {pid}"/>'
            '<wp:cNvGraphicFramePr>'
            f'<a:graphicFrameLocks xmlns:a="{A}" noChangeAspect="1"/>'
            '</wp:cNvGraphicFramePr>'
            f'<a:graphic xmlns:a="{A}">'
            f'<a:graphicData uri="{PIC}">'
            f'<pic:pic xmlns:pic="{PIC}">'
            '<pic:nvPicPr>'
            f'<pic:cNvPr id="{pid}" name="img{pid}.png"/>'
            '<pic:cNvPicPr/>'
            '</pic:nvPicPr>'
            '<pic:blipFill>'
            f'<a:blip r:embed="{rid}"/>'
            '<a:stretch><a:fillRect/></a:stretch>'
            '</pic:blipFill>'
            '<pic:spPr>'
            f'<a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
            '</pic:spPr>'
            '</pic:pic>'
            '</a:graphicData>'
            '</a:graphic>'
            '</wp:inline>'
            '</w:drawing></w:r>'
        )


# ---- math conversion (LaTeX -> OMML via pandoc, batched) --------------------
def latex_to_omml(snippets):
    if not snippets:
        return []
    md = "\n\n".join(f"${s}$" for s in snippets)
    with tempfile.TemporaryDirectory() as td:
        mdp, dxp = os.path.join(td, "m.md"), os.path.join(td, "m.docx")
        open(mdp, "w", encoding="utf-8").write(md)
        subprocess.run(["pandoc", mdp, "-o", dxp], check=True,
                       capture_output=True, text=True)
        with zipfile.ZipFile(dxp) as z:
            xml = z.read("word/document.xml").decode("utf-8")
    omaths = re.findall(r'<m:oMath>.*?</m:oMath>', xml, re.S)
    if len(omaths) != len(snippets):
        raise RuntimeError(
            f"Math conversion mismatch: {len(snippets)} snippets in, "
            f"{len(omaths)} out. Check the \\(...\\) LaTeX in the questions.")
    return omaths


# ---- shuffle resolution & math collection (identical order) -----------------
def resolve(questions, seed_prefix):
    out = []
    for i, q in enumerate(questions):
        opts = list(q["options"])
        if len(opts) != 4:
            raise ValueError(f"Every question needs exactly 4 options; got "
                             f"{len(opts)} for topic '{q.get('topic','?')}'.")
        correct = opts[q["answer"]]
        rng = random.Random(f"{seed_prefix}:{i}")
        rng.shuffle(opts)
        out.append({**q, "_opts": opts, "_correct": correct})
    return out


def collect_math(resolved):
    """Ordered list of LaTeX snippets, in the order build_table consumes them:
    question -> each (shuffled) option -> solution."""
    snippets = []
    for q in resolved:
        snippets.extend(MATH_RE.findall(q["question"] or ""))
        for o in q["_opts"]:
            snippets.extend(MATH_RE.findall(o or ""))
        snippets.extend(MATH_RE.findall(q["solution"] or ""))
    return snippets


# ---- run/paragraph builders ------------------------------------------------
def text_run(text):
    return (f'<w:r><w:t xml:space="preserve">{html.escape(text)}</w:t></w:r>'
            if text else "")


def bold_run(text):
    return ('<w:r><w:rPr><w:b/><w:bCs/><w:lang w:val="en-US"/></w:rPr>'
            f'<w:t xml:space="preserve">{html.escape(text)}</w:t></w:r>')


def content_runs(field, math_iter, imgctx, box):
    """Interleave text, math (OMML) and images in written order."""
    out = []
    for part in SEG_RE.split(field or ""):
        if not part:
            continue
        if part.startswith('\\(') and part.endswith('\\)'):
            out.append(next(math_iter))
        elif part.startswith('[[IMG:'):
            spec = IMG_TOKEN_RE.match(part).group(1).strip()
            out.append(imgctx.add(spec, *box))
        else:
            out.append(text_run(part))
    return "".join(out)


def para(inner, bold_ppr=False):
    ppr = '<w:pPr><w:pStyle w:val="BodyA"/>'
    if bold_ppr:
        ppr += '<w:rPr><w:b/><w:bCs/></w:rPr>'
    ppr += '</w:pPr>'
    return f'<w:p>{ppr}{inner}</w:p>'


def cell(width, inner_para, gridspan=1):
    span = f'<w:gridSpan w:val="{gridspan}"/>' if gridspan > 1 else ""
    return (f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{span}'
            f'{BLACK_BORDERS}{TC_MAR}</w:tcPr>{inner_para}</w:tc>')


def label_row(label, content_field, math_iter, imgctx):
    c1 = cell(COL1, para(bold_run(label), bold_ppr=True))
    c2 = cell(MERGED, para(content_runs(content_field, math_iter, imgctx, WIDE_MAX)),
              gridspan=2)
    return f'<w:tr>{c1}{c2}</w:tr>'


def type_row():
    c1 = cell(COL1, para(bold_run("Type"), bold_ppr=True))
    c2 = cell(MERGED, para(bold_run("multiple_choice")), gridspan=2)
    return f'<w:tr>{c1}{c2}</w:tr>'


def option_row(opt_field, is_correct, math_iter, imgctx):
    c1 = cell(COL1, para(bold_run("Option"), bold_ppr=True))
    c2 = cell(COL2, para(content_runs(opt_field, math_iter, imgctx, OPT_MAX)))
    c3 = cell(COL3, para(text_run("correct" if is_correct else "incorrect")))
    return f'<w:tr>{c1}{c2}{c3}</w:tr>'


def marks_row(marks, negative):
    c1 = cell(COL1, para(bold_run("Marks"), bold_ppr=True))
    c2 = cell(COL2, para(bold_run(_num(marks))))
    c3 = cell(COL3, para(bold_run(_num(negative))))
    return f'<w:tr>{c1}{c2}{c3}</w:tr>'


def _num(v):
    return str(int(v)) if float(v) == int(v) else str(v)


def build_table(q, math_iter, imgctx):
    rows = [
        label_row("Question", q["question"], math_iter, imgctx),
        type_row(),
    ]
    for o in q["_opts"]:
        rows.append(option_row(o, o == q["_correct"], math_iter, imgctx))
    rows.append(label_row("Solution", q["solution"], math_iter, imgctx))
    rows.append(marks_row(q.get("marks", 1), q.get("negative", 0.25)))
    return f'<w:tbl>{TBL_PR}{TBL_GRID}{"".join(rows)}</w:tbl>'


# ---- document assembly -----------------------------------------------------
def body_open_tag(template):
    with zipfile.ZipFile(template) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    return xml[:xml.index("<w:body>") + len("<w:body>")]


def patch_rels(rels_xml, imgctx):
    if not imgctx.rels:
        return rels_xml
    IMG_TYPE = ("http://schemas.openxmlformats.org/officeDocument/2006/"
                "relationships/image")
    add = "".join(
        f'<Relationship Id="{rid}" Type="{IMG_TYPE}" Target="{tgt}"/>'
        for rid, tgt in imgctx.rels)
    return rels_xml.replace("</Relationships>", add + "</Relationships>")


def patch_content_types(ct_xml, imgctx):
    if not imgctx.media or 'Extension="png"' in ct_xml:
        return ct_xml
    add = '<Default Extension="png" ContentType="image/png"/>'
    return ct_xml.replace("</Types>", add + "</Types>")


def build_docx(resolved, out_path, template, open_tag, math_pool, images_dir):
    imgctx = ImageContext(images_dir)
    math_iter = iter(math_pool)
    tables = [build_table(q, math_iter, imgctx) for q in resolved]
    document_xml = open_tag + SPACER_P.join(tables) + SECT_PR + "</w:body></w:document>"

    tmp = out_path + ".tmp"
    with zipfile.ZipFile(template) as zin, \
         zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.namelist():
            data = zin.read(item)
            if item == "word/document.xml":
                zout.writestr(item, document_xml)
            elif item == "word/_rels/document.xml.rels":
                zout.writestr(item, patch_rels(data.decode("utf-8"), imgctx))
            elif item == "[Content_Types].xml":
                zout.writestr(item, patch_content_types(data.decode("utf-8"), imgctx))
            else:
                zout.writestr(item, data)
        for arc, blob in imgctx.media:
            zout.writestr(arc, blob)
    os.replace(tmp, out_path)


A_ORDER = ["Quantitative Aptitude", "Logical Reasoning", "Verbal Ability"]


def order_section_a(qs):
    def key(q):
        g = q.get("group", "")
        for i, name in enumerate(A_ORDER):
            if name.lower() in g.lower():
                return i
        return 99
    return sorted(qs, key=key)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="questions JSON")
    ap.add_argument("--test-number", type=int, default=None)
    ap.add_argument("--output-dir", default=".")
    ap.add_argument("--images-dir", default=None,
                    help="folder holding PNGs referenced by [[IMG:...]] "
                         "(default: the input JSON's directory)")
    ap.add_argument("--template", default=DEFAULT_TEMPLATE)
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as fh:
        data = json.load(fh)
    qs = data["questions"]
    n = args.test_number if args.test_number is not None else data.get("test_number", 1)
    images_dir = args.images_dir or os.path.dirname(os.path.abspath(args.input))

    sec_a = order_section_a([q for q in qs if q.get("section") == "A"])
    sec_b = [q for q in qs if q.get("section") == "B"]

    problems = []
    if len(sec_a) != 50:
        problems.append(f"Section A must have 50 questions, found {len(sec_a)}.")
    if len(sec_b) != 50:
        problems.append(f"Section B must have 50 questions, found {len(sec_b)}.")
    ga = [q for q in sec_a if "quantitative" in q.get("group", "").lower()]
    gl = [q for q in sec_a if "logical" in q.get("group", "").lower()]
    gv = [q for q in sec_a if "verbal" in q.get("group", "").lower()]
    if len(ga) != 20: problems.append(f"Quantitative Aptitude must be 20, found {len(ga)}.")
    if len(gl) != 15: problems.append(f"Logical Reasoning must be 15, found {len(gl)}.")
    if len(gv) != 15: problems.append(f"Verbal Ability must be 15, found {len(gv)}.")
    if problems:
        print("VALIDATION ERRORS:\n - " + "\n - ".join(problems), file=sys.stderr)
        sys.exit(1)

    template = os.path.abspath(args.template)
    open_tag = body_open_tag(template)

    a_res = resolve(sec_a, f"A:{n}")
    b_res = resolve(sec_b, f"B:{n}")
    a_math = latex_to_omml(collect_math(a_res))
    b_math = latex_to_omml(collect_math(b_res))

    os.makedirs(args.output_dir, exist_ok=True)
    a_path = os.path.join(args.output_dir, f"Section A - Test {n}.docx")
    b_path = os.path.join(args.output_dir, f"Section B - Test {n}.docx")
    build_docx(a_res, a_path, template, open_tag, a_math, images_dir)
    build_docx(b_res, b_path, template, open_tag, b_math, images_dir)
    print(f"Wrote:\n  {a_path}\n  {b_path}")


if __name__ == "__main__":
    main()
