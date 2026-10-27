#!/usr/bin/env python3
"""Build a GATE ME 2027 Test Series formula-notes PDF (A4 portrait, xelatex).

Usage: python3 build_notes.py <notes.json> <figs_dir> <out.pdf> [--keep-tex]

notes.json (paid content: keep it in the vault, never in plain form in the repo):
{
  "code": "SOM", "name": "Strength of Materials",
  "intro": "one-line LaTeX text under the cover title (optional)",
  "sections": [                                   # one per syllabus block, appears in the contents
    {"title": "Stress, strain and elastic constants",
     "appendix": false,                           # true -> numbered A, B ... after the main sections
     "cards": [{
        "title": "Generalised Hooke's law",       # LaTeX text
        "formula": ["\\varepsilon_x=\\frac{1}{E}[\\sigma_x-\\nu(\\sigma_y+\\sigma_z)]", "..."],
                                                  # display-math lines (one gather* row each, no &)
        "symbols": [["$\\sigma_x$", "normal stress along x", "Pa (N/m$^2$)"], ...],
        "units": "what to substitute / conversions that catch students (LaTeX text)",
        "assumptions": "assumptions of the derivation",
        "valid": "valid when ...", "not_valid": "not valid when ...",
        "traps": ["common trap 1", "common trap 2"],
        "fig": "hooke"                            # optional: <figs_dir>/hooke.png (drawn with gate90 figlib)
        "fig_w": 0.34                             # optional: figure column width as fraction of card width
     }, ...]}
  ]
}
Every text field is LaTeX (use $...$ for inline maths, \\% for percent).
The PDF has a cover, a contents page, the cards (2-3 per page) and a QR-codes page last."""
import json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "..", "tooling", "assets")
WEB = "https://web.digcareerthrust.com/login"
APP = "https://play.google.com/store/apps/details?id=co.jack.iurlk"


def qr(url, path):
    import qrcode
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=12, border=2)
    q.add_data(url); q.make(fit=True); q.make_image(fill_color="black", back_color="white").save(path)


PRE = r"""\documentclass[9pt]{extarticle}
\usepackage[a4paper,top=20mm,bottom=17mm,left=13mm,right=13mm,headheight=12mm,headsep=4mm,footskip=8mm]{geometry}
\usepackage{fontspec}
\usepackage{amsmath,amssymb,mathtools,bm}
\usepackage{graphicx,xcolor,tabularx,array,booktabs,enumitem,fancyhdr,lastpage,titlesec,needspace}
\usepackage[most]{tcolorbox}
\usepackage[hidelinks]{hyperref}
\usepackage{etoolbox}
\setmainfont{Latin Modern Roman}
\newfontfamily\pop[Path=./,UprightFont=Poppins-Medium.ttf,BoldFont=Poppins-Bold.ttf]{Poppins}
\newfontfamily\popx[Path=./]{Poppins-ExtraBold.ttf}
\newfontfamily\popsb[Path=./]{Poppins-SemiBold.ttf}
\definecolor{dig}{HTML}{D7191F}\definecolor{ink}{HTML}{1A1A1A}\definecolor{soft}{HTML}{FBEDED}
\definecolor{grey}{HTML}{6B6B6B}\definecolor{rule}{HTML}{E4B4B5}
\raggedbottom\setlength{\parindent}{0pt}\setlength{\parskip}{0pt}
\renewcommand{\arraystretch}{1.12}
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\pagestyle{fancy}\fancyhf{}
\renewcommand{\headrulewidth}{0.6pt}\renewcommand{\headrule}{{\color{dig}\hrule height 0.6pt}}
\fancyhead[L]{\raisebox{-0.35\height}{\includegraphics[height=7mm]{logo_red.png}}\hspace{2mm}{\pop\fontsize{7.5}{9}\selectfont\color{grey}GATE ME 2027 Test Series \,|\, Formula Notes \,|\, @@SUBJ@@}}
\fancyhead[R]{{\popsb\fontsize{8}{9}\selectfont\color{dig}Dig Career Thrust}}
\fancyfoot[L]{{\pop\fontsize{7}{9}\selectfont\color{grey}web.digcareerthrust.com \,|\, Dig Career Thrust app on Google Play}}
\fancyfoot[R]{{\pop\fontsize{7}{9}\selectfont\color{grey}Page \thepage\ of \pageref{LastPage}}}
\fancypagestyle{plain}{\fancyhf{}\renewcommand{\headrulewidth}{0pt}\renewcommand{\headrule}{}}
\titleformat{\section}{\pop\fontsize{12.5}{15}\selectfont\color{dig}}{\thesection}{0.6em}{}[{\color{dig}\titlerule[0.8pt]}]
\titlespacing*{\section}{0pt}{4pt}{5pt}
\setcounter{tocdepth}{2}
\makeatletter
\renewcommand{\l@section}[2]{\addpenalty{-\@highpenalty}\vskip 3pt{\pop\fontsize{9.5}{12}\selectfont\leavevmode\color{dig}\def\numberline##1{##1\quad}#1\hfill #2\par}}
\renewcommand{\l@subsection}[2]{{\fontsize{8.6}{10.2}\selectfont\leftskip 1.6em\leavevmode\color{ink}#1\nobreak\leaders\hbox to 0.6em{\hss.\hss}\hfill\nobreak #2\par}}
\makeatother
\newcounter{card}
\newtcolorbox{fcard}[1]{enhanced,breakable=false,colback=white,colframe=dig,boxrule=0.7pt,arc=1.2mm,
  left=2.2mm,right=2.2mm,top=1.4mm,bottom=1.6mm,before skip=2.2mm,after skip=2.2mm,
  title={\pop\fontsize{9.5}{11}\selectfont #1},coltitle=white,colbacktitle=dig,toptitle=0.6mm,bottomtitle=0.6mm}
\newcommand{\formulabox}[1]{\begin{tcolorbox}[enhanced,colback=soft,colframe=soft,boxrule=0pt,arc=0.8mm,left=1mm,right=1mm,top=0mm,bottom=0.6mm,before skip=0.5mm,after skip=1.2mm]#1\end{tcolorbox}}
\newcommand{\lab}[1]{\leavevmode{\popsb\fontsize{7.4}{9}\selectfont\color{dig}#1}}
\newcommand{\symhead}{\lab{Symbol} & \lab{Meaning} & \lab{SI unit}\\[-1pt]\midrule}
\setlength{\abovedisplayskip}{2pt}\setlength{\belowdisplayskip}{2pt}
\setlength{\abovedisplayshortskip}{1pt}\setlength{\belowdisplayshortskip}{1pt}
\setlength{\jot}{3pt}
\begin{document}
"""


def card_tex(c):
    lines = c["formula"] if isinstance(c["formula"], list) else [c["formula"]]
    form = r"\formulabox{\vspace{-3pt}\begin{gather*}" + r"\\".join(lines) + r"\end{gather*}}"
    sym = ""
    if c.get("symbols"):
        rows = "".join(f"{s[0]} & {s[1]} & {s[2]}\\\\" for s in c["symbols"])
        sym = (r"{\fontsize{8}{9.4}\selectfont\begin{tabularx}{\linewidth}{@{}l Y >{\raggedright\arraybackslash}p{0.2\linewidth}@{}}"
               + r"\symhead" + rows + r"\bottomrule\end{tabularx}}")
    top = form + sym
    if c.get("fig"):
        w = float(c.get("fig_w", 0.34))
        top = (r"\begin{minipage}[t]{" + f"{1 - w - 0.03:.3f}" + r"\linewidth}\vspace{0pt}" + top + r"\end{minipage}\hfill"
               r"\begin{minipage}[t]{" + f"{w:.3f}" + r"\linewidth}\vspace{2pt}\centering\includegraphics[width=\linewidth,height=46mm,keepaspectratio]{"
               + c["fig"] + r".png}\end{minipage}")
    rows = []
    for key, lab in (("units", "Units"), ("assumptions", "Assumptions"), ("valid", "Valid when"), ("not_valid", "Not valid when")):
        if c.get(key):
            rows.append(f"\\lab{{{lab}}} & {c[key]}\\\\")
    if c.get("traps"):
        tr = c["traps"] if isinstance(c["traps"], list) else [c["traps"]]
        items = r"\newline ".join(r"\textcolor{dig}{\textbullet}\,~" + x for x in tr)
        rows.append(r"\lab{Traps} & " + items + r"\\")
    notes = (r"\par\vspace{2pt}{\fontsize{8.3}{9.8}\selectfont\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{19.5mm}Y@{}}"
             + "".join(rows) + r"\end{tabularx}}")
    title = c["title"]
    return (r"\stepcounter{card}\phantomsection\addcontentsline{toc}{subsection}{" + title + "}"
            + r"\begin{fcard}{" + title + "}" + top + notes + r"\end{fcard}" + "\n")


def build(D, figdir, out, keep=False):
    work = tempfile.mkdtemp()
    for f in os.listdir(ASSETS):
        shutil.copy(os.path.join(ASSETS, f), work)
    if figdir and os.path.isdir(figdir):
        for f in os.listdir(figdir):
            if f.endswith(".png"):
                shutil.copy(os.path.join(figdir, f), work)
    qr(WEB, os.path.join(work, "qr_web.png")); qr(APP, os.path.join(work, "qr_app.png"))
    subj = D["name"]
    ncards = sum(len(s["cards"]) for s in D["sections"])
    t = PRE.replace("@@SUBJ@@", subj)
    # cover
    t += (r"\thispagestyle{plain}\begin{tikzpicture}[remember picture,overlay]\fill[dig] (current page.north west) rectangle ([yshift=-95mm]current page.north east);\end{tikzpicture}"
          r"\vspace*{-6mm}{\color{white}\includegraphics[height=22mm]{logo_white.png}\par\vspace{8mm}"
          r"{\popx\fontsize{30}{34}\selectfont GATE ME 2027\par}\vspace{2mm}{\pop\fontsize{15}{18}\selectfont Test Series \,|\, Formula Notes\par}}"
          r"\vspace{30mm}{\popx\fontsize{24}{29}\selectfont\color{ink}" + subj + r"\par}\vspace{4mm}"
          r"{\pop\fontsize{10.5}{14}\selectfont\color{grey}" + D.get("intro", "") + r"\par}\vspace{8mm}"
          r"{\fontsize{10}{14}\selectfont " + f"{ncards} formula cards" + r" \,---\, every card gives the formula, a symbol table with SI units, the unit conversions that catch students, the assumptions behind it, when it holds and when it does not, a figure where it helps, and the traps that cost marks.\par}"
          r"\vfill{\pop\fontsize{9}{12}\selectfont\color{grey}Dig Career Thrust \,|\, web.digcareerthrust.com\par For the enrolled students of the GATE ME 2027 Test Series. Please do not share or resell.\par}\newpage")
    t = t.replace(r"\usepackage{etoolbox}", r"\usepackage{etoolbox}\usepackage{tikz}")
    # contents
    t += r"{\pop\fontsize{16}{20}\selectfont\color{dig}Contents\par}\vspace{2mm}{\color{dig}\hrule height 0.8pt}\vspace{3mm}\begingroup\tableofcontents\endgroup\newpage"
    t = t.replace(r"\begin{document}", r"\begin{document}\makeatletter\renewcommand{\tableofcontents}{\@starttoc{toc}}\makeatother")
    app = False
    for s in D["sections"]:
        if s.get("appendix") and not app:
            app = True; t += r"\appendix\renewcommand{\thesection}{\Alph{section}}"
        t += r"\Needspace*{90mm}\section{" + s["title"] + "}\n"
        for c in s["cards"]:
            t += card_tex(c)
    # QR page
    t += (r"\newpage\thispagestyle{fancy}\vspace*{8mm}\begin{center}{\popx\fontsize{20}{24}\selectfont\color{dig}Keep practising with Dig Career Thrust\par}\vspace{4mm}"
          r"{\pop\fontsize{10.5}{14}\selectfont\color{grey}Topic tests, subject tests and full-length mocks of the GATE ME 2027 Test Series\par}\vspace{16mm}"
          r"\begin{tabular}{c@{\hspace{22mm}}c}\includegraphics[width=55mm]{qr_web.png} & \includegraphics[width=55mm]{qr_app.png}\\[3mm]"
          r"{\pop\fontsize{12}{14}\selectfont Website} & {\pop\fontsize{12}{14}\selectfont Android app}\\[1mm]"
          r"{\fontsize{9}{11}\selectfont\url{web.digcareerthrust.com/login}} & {\fontsize{9}{11}\selectfont Google Play: Dig Career Thrust}\\\end{tabular}"
          r"\vspace{18mm}\par\includegraphics[height=20mm]{logo_red.png}\par\vspace{3mm}{\popsb\fontsize{12}{14}\selectfont\color{dig}Dig Career Thrust}\end{center}")
    t += r"\end{document}" + "\n"
    tex = os.path.join(work, "notes.tex"); open(tex, "w").write(t)
    for _ in range(3):
        r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", "notes.tex"], cwd=work,
                           capture_output=True, text=True)
        if r.returncode:
            log = r.stdout[-4000:]
            sys.exit("xelatex failed:\n" + log + "\n(work dir " + work + ")")
    log = open(os.path.join(work, "notes.log"), errors="ignore").read()
    bad = re.findall(r"Overfull \\hbox \((\d+\.\d+)pt", log)
    big = [float(b) for b in bad if float(b) > 3]
    if big:
        print("WARN overfull boxes (pt):", big[:20])
    shutil.copy(os.path.join(work, "notes.pdf"), out)
    if keep:
        shutil.copy(tex, os.path.splitext(out)[0] + ".tex")
    shutil.rmtree(work, ignore_errors=True)
    print("OK", out, ncards, "cards")


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    build(json.load(open(a[0])), a[1], a[2], keep="--keep-tex" in sys.argv)
