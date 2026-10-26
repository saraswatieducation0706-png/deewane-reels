#!/usr/bin/env python3
"""Render a Deewane job-notification VIDEO in 16:9 (1920x1080, 30 fps) for YouTube, from a JSON spec.

Usage:  python3 render_job_landscape.py spec.json [--no-tts]

Same spec format and voice pipeline as render_reel.py (see references/scene_kinds.md), plus:
  * scene kinds `job` and `index` for the Sunday apprentice/contract roundup,
  * optional "chapter": "<label>" on any scene -> YouTube chapters written to <out>.chapters.txt
    (first chapter "Intro" at 0:00 is automatic; chapters shorter than 10 s are merged).
The WELCOME scene and the website/QR END scene are added automatically.
Prints JSON: {"out", "duration_s", "scenes", "chapters": [...]}
"""
import subprocess, os, sys, json, math, shutil
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_reel as rr  # tts(), dur(), F(), colours, config, QR list

A, CFG, F = rr.A, rr.CFG, rr.F
W, H, FPS = 1920, 1080, 30
RED, DRED, WHITE, INK, SOFT = rr.RED, rr.DRED, rr.WHITE, rr.INK, rr.SOFT
GOLD = (255, 214, 0)
CHANNEL = rr.CHANNEL
SETTLE = 4.2   # seconds after which every scene's entry animation is finished -> layer is cached

WELCOME = dict(rr.WELCOME)
END = dict(kind="end", voice="For test series and study material, visit web dot D. I. G. career thrust dot com. "
           "Scan the codes to get our app and join our Telegram. Subscribe and press the bell icon for daily "
           "government job updates!", min_dur=8.0)

ease = rr.ease
def back(t):
    t = min(max(t, 0), 1); c = 1.70158
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def al(c, a): return c + (int(255 * max(0, min(a, 1))),)
def fit(d, txt, w, s, maxw, mn=22):
    while s > mn and d.textlength(txt, font=F(w, s)) > maxw: s -= 2
    return F(w, s)
def ctext(d, y, txt, font, fill, a=1.0, cx=W / 2):
    d.text((cx - d.textlength(txt, font=font) / 2, y), txt, font=font, fill=al(fill, a))
def ftext(d, y, txt, w, s, fill, a, maxw=W - 240, cx=W / 2):
    ctext(d, y, txt, fit(d, txt, w, s, maxw), fill, a, cx)
def wrap(d, txt, font, maxw):
    out, cur = [], ""
    for wd in str(txt).split():
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else:
            if cur: out.append(cur)
            cur = wd
    if cur: out.append(cur)
    return out
def wrapfit(d, txt, w, s, maxw, maxlines, mn=22):
    while True:
        lines = wrap(d, txt, F(w, s), maxw)
        if (len(lines) <= maxlines and all(d.textlength(l, font=F(w, s)) <= maxw for l in lines)) or s <= mn:
            return lines, F(w, s)
        s -= 2

def title(d, s, t, y=150):
    a = ease(t / 0.45); sl = (1 - a) * 70
    ftext(d, y + sl, s["title"], "ExtraBold", 66, WHITE, a, W - 300)
    d.rounded_rectangle([W / 2 - 120 * a, y + 96, W / 2 + 120 * a, y + 105], 5, fill=al(WHITE, 0.9 * a))
    return a

def scene(s, t, d, lay):
    k = s["kind"]
    if k == "welcome":
        p0 = ease(t / 0.5); r = 175 * p0
        d.ellipse([W / 2 - r, 420 - r, W / 2 + r, 420 + r], fill=al(WHITE, p0))
        if p0 > 0.05:
            lg = LOGO_R.copy(); lg.putalpha(lg.getchannel("A").point(lambda v: int(v * p0)))
            lay.alpha_composite(lg, (int(W / 2 - 115), int(420 - 107)))
        p1 = ease((t - 0.4) / 0.4); ctext(d, 630 + (1 - p1) * 50, s["title"], F("ExtraBold", 92), WHITE, p1)
        p2 = ease((t - 0.8) / 0.4)
        d.rounded_rectangle([W / 2 - 560, 780, W / 2 + 560, 870], 45, fill=al(WHITE, p2))
        ctext(d, 798, s["sub"], F("Bold", 40), RED, p2)
        return
    if k == "hook":
        lines = s["title"]; n = len(lines); y0 = 300 if n > 1 else 380
        for j, ln in enumerate(lines):
            p = back((t - 0.3 * j) / 0.45); a = ease((t - 0.3 * j) / 0.3)
            ftext(d, y0 + j * 165, ln, "ExtraBold", 140 * (0.6 + 0.4 * p), GOLD if j == 1 else WHITE, a, W - 200)
        if s.get("sub"):
            p2 = ease((t - 0.8) / 0.4); y = y0 + n * 165 + 40
            d.rounded_rectangle([W / 2 - 700, y, W / 2 + 700, y + 104], 52, fill=al(WHITE, p2))
            ftext(d, y + 24, s["sub"], "Bold", 48, RED, p2, 1300)
        return
    if k == "end":
        p = ease((t - 0.3) / 0.5)
        d.rounded_rectangle([90, 190, W - 90, 930], 48, fill=al(WHITE, p))
        ctext(d, 250, "DIG Career Thrust", F("ExtraBold", 76), RED, p, cx=520)
        ctext(d, 360, "Test Series  •  Study Material", F("SemiBold", 40), INK, p, cx=520)
        ctext(d, 430, "web.digcareerthrust.com", F("Bold", 44), INK, p, cx=520)
        pf = ease((t - 2.2) / 0.4)
        d.rounded_rectangle([170, 600, 870, 700], 50, fill=al(RED, pf))
        ctext(d, 622, "SUBSCRIBE & PRESS THE BELL", fit(d, "SUBSCRIBE & PRESS THE BELL", "ExtraBold", 44, 640), WHITE, pf, cx=520)
        ctext(d, 730, "Daily government job updates", F("SemiBold", 36), INK, pf, cx=520)
        for j, (lab, _) in enumerate(rr.QRS):
            q = ease((t - 0.8 - 0.35 * j) / 0.4); x = 980 + j * 290
            if q > 0:
                qi = QR_IMGS[j].copy(); qi.putalpha(int(255 * q)); lay.alpha_composite(qi, (int(x), 300))
                d.rounded_rectangle([x, 570, x + 260, 636], 20, fill=al(RED, q))
                ctext(d, 580, lab, F("Bold", 36), WHITE, q, cx=x + 130)
        return

    a = title(d, s, t)
    if k == "card":   # 1-5 lines
        ln = s["lines"]; n = len(ln); hh = 112 if n <= 4 else 100; gap = 26
        y0 = 300 + (5 - n) * (hh + gap) / 2 * 0.8
        for j, txt in enumerate(ln):
            p = ease((t - 0.4 - 0.4 * j) / 0.4); y = y0 + j * (hh + gap); dx = (1 - p) * 500
            d.rounded_rectangle([210 + dx, y, W - 210 + dx, y + hh], 32, fill=al(WHITE, p))
            d.rounded_rectangle([210 + dx, y, 236 + dx, y + hh], 12, fill=al(DRED, p))
            f = fit(d, txt, "Bold", 54, W - 520, 28)
            d.text(((W - d.textlength(txt, font=f)) / 2 + dx, y + (hh - f.size * 1.25) / 2), txt, font=f, fill=al(INK, p))
    elif k == "count":
        cx, cy, R = 600, 600, 270
        d.ellipse([cx - R * a, cy - R * a, cx + R * a, cy + R * a], fill=al(WHITE, a))
        n = int(s["num"] * ease((t - 0.3) / 1.5))
        ctext(d, cy - 150, f"{n:,}", fit(d, f"{s['num']:,}", "ExtraBold", 170, 440), RED, a, cx=cx)
        ctext(d, cy + 60, s.get("label", "POSTS"), fit(d, s.get("label", "POSTS"), "Bold", 50, 420), INK, a, cx=cx)
        notes = s.get("notes") or ([s["note"]] if s.get("note") else [])
        for j, nt in enumerate(notes[:3]):
            p = ease((t - 1.0 - 0.4 * j) / 0.4); y = 430 + j * 130 + (3 - len(notes)) * 65
            d.rounded_rectangle([1000, y, 1760, y + 104], 52, fill=al(WHITE if j == 0 else DRED, p))
            ftext(d, y + 26, nt, "Bold", 44, RED if j == 0 else WHITE, p, 680, cx=1380)
    elif k == "table":  # rows [[label, value]] up to 7
        rows = s["rows"]; n = len(rows); rh = 84 if n > 5 else 100; gap = 12 if n > 5 else 18
        y0 = 300 + (7 - n) * (rh + gap) / 2 * 0.6
        for j, (l, r) in enumerate(rows):
            p = ease((t - 0.35 - 0.3 * j) / 0.35); y = y0 + j * (rh + gap); dx = (1 - p) * 400
            d.rounded_rectangle([210 + dx, y, W - 210 + dx, y + rh], 28, fill=al(WHITE, p))
            d.rounded_rectangle([W - 650 + dx, y, W - 210 + dx, y + rh], 28, fill=al(RED, p))
            fl = fit(d, l, "Bold", 44, W - 950, 24); fr = fit(d, str(r), "ExtraBold", 50, 400, 24)
            d.text((250 + dx, y + (rh - fl.size * 1.25) / 2), l, font=fl, fill=al(INK, p))
            ctext(d, y + (rh - fr.size * 1.25) / 2, str(r), fr, WHITE, p, cx=W - 430 + dx)
        if s.get("note"):
            p = ease((t - 0.5 - 0.3 * n) / 0.4); yn = y0 + n * (rh + gap) + 14
            ftext(d, yn, s["note"], "SemiBold", 36, SOFT, p)
    elif k == "pattern":
        hd = s.get("header", ["Section", "Qs", "Marks"]); rows = s["rows"]; cw = [620, 240, 240]
        x0 = 140; xs = [x0, x0 + cw[0], x0 + cw[0] + cw[1]]; y0 = 290; rh = 84
        d.rounded_rectangle([x0 - 10, y0, x0 + sum(cw) + 10, y0 + rh], 24, fill=al(INK, a))
        for c in range(3):
            f = fit(d, hd[c], "Bold", 38, cw[c] - 30)
            ctext(d, y0 + 22, hd[c], f, WHITE, a, cx=xs[c] + cw[c] / 2)
        for j, row in enumerate(rows):
            p = ease((t - 0.4 - 0.25 * j) / 0.35); y = y0 + (j + 1) * (rh + 10)
            d.rounded_rectangle([x0 - 10, y, x0 + sum(cw) + 10, y + rh], 24, fill=al(WHITE, p))
            for c in range(3):
                txt = str(row[c]); f = fit(d, txt, "Bold" if c == 0 else "ExtraBold", 40, cw[c] - 30, 22)
                ctext(d, y + (rh - f.size * 1.25) / 2, txt, f, INK if c == 0 else RED, p, cx=xs[c] + cw[c] / 2)
        for j, ch in enumerate(s.get("chips", [])):
            p = ease((t - 0.6 - 0.25 * len(rows) - 0.3 * j) / 0.35); y = 330 + j * 150
            d.rounded_rectangle([1300, y, 1800, y + 120], 40, fill=al(DRED, p))
            lines, f = wrapfit(d, ch, "Bold", 38, 440, 2)
            for i, l in enumerate(lines):
                ctext(d, y + 60 - len(lines) * f.size * 0.62 + i * f.size * 1.2, l, f, WHITE, p, cx=1550)
    elif k == "steps":  # 2-5 steps, horizontal flow
        st = s["steps"]; n = len(st); gap = 70; bw = (W - 240 - gap * (n - 1)) / n; y = 380; bh = 270
        for j, label in enumerate(st):
            p = ease((t - 0.4 - 0.5 * j) / 0.4); x = 120 + j * (bw + gap); dy = (1 - p) * 80
            d.rounded_rectangle([x, y + dy, x + bw, y + bh + dy], 34, fill=al(WHITE, p))
            d.ellipse([x + bw / 2 - 55, y - 55 + dy, x + bw / 2 + 55, y + 55 + dy], fill=al(INK, p))
            ctext(d, y - 42 + dy, str(j + 1), F("ExtraBold", 64), WHITE, p, cx=x + bw / 2)
            lines, f = wrapfit(d, label, "Bold", 44, bw - 50, 3)
            th = len(lines) * f.size * 1.25
            for i, l in enumerate(lines):
                ctext(d, y + 40 + (bh - 40 - th) / 2 + i * f.size * 1.25 + dy, l, f, INK, p, cx=x + bw / 2)
            if j < n - 1:
                pa = ease((t - 0.7 - 0.5 * j) / 0.3); ax = x + bw + 12
                d.polygon([(ax, y + bh / 2 - 22), (ax, y + bh / 2 + 22), (ax + gap - 24, y + bh / 2)], fill=al(WHITE, pa))
        if s.get("note"):
            p = ease((t - 0.6 - 0.5 * n) / 0.4)
            d.rounded_rectangle([W / 2 - 650, 760, W / 2 + 650, 860], 50, fill=al(DRED, p))
            ftext(d, 784, s["note"], "Bold", 42, WHITE, p, 1220)
    elif k == "dates":  # [[label, value]] 2-4, last one highlighted
        ln = s["lines"]; n = len(ln); gap = 40; bw = (W - 240 - gap * (n - 1)) / n; y = 360; bh = 330
        for j, (lab, val) in enumerate(ln):
            p = ease((t - 0.4 - 0.5 * j) / 0.4); x = 120 + j * (bw + gap); dy = (1 - p) * 60
            d.rounded_rectangle([x, y + dy, x + bw, y + bh + dy], 36, fill=al(WHITE, p))
            d.rounded_rectangle([x, y + dy, x + bw, y + 96 + dy], 36, fill=al(INK, p))
            d.rectangle([x, y + 60 + dy, x + bw, y + 96 + dy], fill=al(INK, p))
            ftext(d, y + 22 + dy, lab.upper(), "Bold", 40, WHITE, p, bw - 40, cx=x + bw / 2)
            lines, f = wrapfit(d, val, "ExtraBold", 76, bw - 50, 2, 30)
            th = len(lines) * f.size * 1.2
            for i, l in enumerate(lines):
                ctext(d, y + 96 + (bh - 96 - th) / 2 + i * f.size * 1.2 + dy, l, f, RED if j == n - 1 else INK, p, cx=x + bw / 2)
    elif k == "job":  # roundup: one job per scene
        pl = ease((t - 0.3) / 0.45); dx = (1 - pl) * -300
        d.rounded_rectangle([120 + dx, 290, 820 + dx, 930], 40, fill=al(WHITE, pl))
        lines, f = wrapfit(d, s["org"], "ExtraBold", 64, 600, 3, 32)
        yy = 340
        for l in lines:
            ctext(d, yy, l, f, RED, pl, cx=470 + dx); yy += f.size * 1.18
        yy += 18
        pl2, f2 = wrapfit(d, s["post"], "Bold", 44, 600, 3, 24)
        for l in pl2:
            ctext(d, yy, l, f2, INK, pl, cx=470 + dx); yy += f2.size * 1.22
        if s.get("type"):
            ft = F("Bold", 36); tw = d.textlength(s["type"], font=ft)
            d.rounded_rectangle([470 - tw / 2 - 30 + dx, 760, 470 + tw / 2 + 30 + dx, 820], 30, fill=al(INK, pl))
            ctext(d, 768, s["type"], ft, WHITE, pl, cx=470 + dx)
        if s.get("posts"):
            ctext(d, 845, s["posts"], fit(d, s["posts"], "ExtraBold", 50, 600), RED, pl, cx=470 + dx)
        rows = s.get("rows", [])[:5]
        for j, (lab, val) in enumerate(rows):
            p = ease((t - 0.6 - 0.35 * j) / 0.35); y = 290 + j * 108; ddx = (1 - p) * 400
            d.rounded_rectangle([880 + ddx, y, W - 120 + ddx, y + 94], 26, fill=al(WHITE, p))
            d.text((910 + ddx, y + 10), lab.upper(), font=F("Bold", 28), fill=al(DRED, p))
            fv = fit(d, str(val), "Bold", 36, W - 120 - 910 - 30, 20)
            d.text((910 + ddx, y + 44), str(val), font=fv, fill=al(INK, p))
        p = ease((t - 0.8 - 0.35 * len(rows)) / 0.4)
        if s.get("last_date"):
            yl = 290 + len(rows) * 108 + 10
            d.rounded_rectangle([880, yl, W - 120, yl + 96], 48, fill=al(DRED, p))
            ftext(d, yl + 22, f"Last date: {s['last_date']}", "ExtraBold", 46, WHITE, p, W - 1100, cx=(880 + W - 120) / 2)
    elif k == "index":  # roundup overview, rows [[name, last date]] up to 10 (two columns)
        rows = s["rows"][:10]; half = (len(rows) + 1) // 2
        for j, (nm, ld) in enumerate(rows):
            col, r = (0, j) if j < half else (1, j - half)
            p = ease((t - 0.4 - 0.22 * j) / 0.35); x = 120 + col * 860; y = 300 + r * 124
            d.rounded_rectangle([x, y, x + 820, y + 106], 28, fill=al(WHITE, p))
            ctext(d, y + 18, str(j + 1), F("ExtraBold", 50), RED, p, cx=x + 50)
            fn = fit(d, nm, "Bold", 38, 520, 22); d.text((x + 100, y + (106 - fn.size * 1.25) / 2), nm, font=fn, fill=al(INK, p))
            d.rounded_rectangle([x + 630, y + 20, x + 800, y + 86], 33, fill=al(DRED, p))
            fl = fit(d, ld, "Bold", 30, 150, 18); ctext(d, y + 53 - fl.size * 0.65, ld, fl, WHITE, p, cx=x + 715)
    else:
        raise ValueError(f"unknown scene kind {k}")

def min_dur(s):
    k = s["kind"]
    if k == "job": return 2.5 + 0.35 * len(s.get("rows", []))
    if k == "index": return 1.5 + 0.22 * len(s["rows"])
    return rr.min_dur(s)

def fmt(sec):
    sec = int(sec); return f"{sec // 3600}:{sec % 3600 // 60:02d}:{sec % 60:02d}" if sec >= 3600 else f"{sec // 60}:{sec % 60:02d}"

def main():
    global LOGO_R, QR_IMGS
    spec_path = sys.argv[1]; use_api = "--no-tts" not in sys.argv
    spec = json.load(open(spec_path))
    assert spec["scenes"][0]["kind"] == "hook", "first spec scene must be the hook"
    scenes = [dict(WELCOME)] + spec["scenes"] + [dict(END)]
    out = spec["out"]; work = out + ".work"; os.makedirs(work, exist_ok=True)
    cache = os.path.join(os.path.dirname(os.path.abspath(out)), ".tts_cache"); os.makedirs(cache, exist_ok=True)
    gap = CFG.get("scene_gap_s", 0.4)
    for i, s in enumerate(scenes):
        p = f"{work}/s{i}.wav"; rr.tts(s["voice"], p, cache, use_api)
        s["dur"] = max(rr.dur(p) + gap, min_dur(s), s.get("min_dur", 0))
    ins = sum((["-i", f"{work}/s{i}.wav"] for i in range(len(scenes))), [])
    flt = "".join(f"[{i}]aresample=44100,aformat=channel_layouts=mono,apad=whole_dur={s['dur']}[a{i}];" for i, s in enumerate(scenes))
    flt += "".join(f"[a{i}]" for i in range(len(scenes))) + \
        f"concat=n={len(scenes)}:v=0:a=1,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[out]"
    subprocess.run(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", flt, "-map", "[out]", f"{work}/voice.wav"], check=True)

    # chapters
    chapters, tcur = [("0:00", "Intro")], 0.0; last = 0.0
    for s in scenes:
        if s.get("chapter") and tcur - last >= 10 and tcur > 0:
            chapters.append((fmt(tcur), s["chapter"])); last = tcur
        tcur += s["dur"]
    if len(chapters) >= 2 and tcur - last < 10: chapters.pop()
    if len(chapters) < 3: chapters = []
    if chapters:
        open(out + ".chapters.txt", "w").write("\n".join(f"{a} {b}" for a, b in chapters) + "\n")

    LOGO_R = Image.open(os.path.join(A, "logo_red.png")).convert("RGBA").resize((230, 214), Image.LANCZOS)
    logo_w = Image.open(os.path.join(A, "logo_white.png")).convert("RGBA").resize((86, 80), Image.LANCZOS)
    QR_IMGS = [Image.open(os.path.join(A, p)).convert("RGBA").resize((260, 260), Image.NEAREST) for _, p in rr.QRS]
    grad = Image.new("RGB", (W + 240, H)); gd = ImageDraw.Draw(grad)
    for x in range(W + 240):
        k = x / (W + 240)
        gd.line([(x, 0), (x, H)], fill=tuple(int(RED[c] * (1 - k * 0.45) + DRED[c] * k * 0.45) for c in range(3)))
    grad = grad.convert("RGBA")
    stripes = Image.new("RGBA", (W + 240, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(stripes)
    for k in range(-6, 16):
        x = k * 240
        sd.polygon([(x, 0), (x + 80, 0), (x + 80 - 600, H), (x - 600, H)], fill=(255, 255, 255, 14))
    grad.alpha_composite(stripes)
    top = Image.new("RGBA", (W, 128), (0, 0, 0, 40)); top.alpha_composite(logo_w, (44, 24))
    src = spec.get("source", "")
    total = sum(s["dur"] for s in scenes)
    lab = ""
    if src:
        lab = (f"Verified from official source: {src}" if spec.get("verified", True)
               else f"Official site: {src} — check notification before applying")

    def background(tg):
        off = int((tg * 40) % 240)
        im = grad.crop((240 - off, 0, 240 - off + W, H))
        hb = im.crop((0, 0, W, 128)); hb.alpha_composite(top); im.paste(hb, (0, 0))
        d = ImageDraw.Draw(im)
        d.text((150, 24), CHANNEL, font=F("Bold", 42), fill=WHITE)
        d.text((152, 76), "Daily Govt Job Updates", font=F("Medium", 28), fill=SOFT)
        if lab:
            f = fit(d, lab, "Medium", 28, W - 200, 18)
            d.text(((W - d.textlength(lab, font=f)) / 2, 1010), lab, font=f, fill=SOFT)
        d.rectangle([0, H - 12, W, H], fill=DRED)
        d.rectangle([0, H - 12, W * tg / total, H], fill=WHITE)
        return im

    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-i", f"{work}/voice.wav", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                           "-preset", "fast", "-crf", "21", "-c:a", "aac", "-b:a", "160k", "-shortest",
                           "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    st = 0
    for s in scenes:
        cached = None
        for fr in range(int(round(s["dur"] * FPS))):
            t = fr / FPS
            im = background(st + t)
            if t >= SETTLE and s["kind"] != "end" or (s["kind"] == "end" and t >= 3.5):
                if cached is None:
                    cached = Image.new("RGBA", (W, H), (0, 0, 0, 0)); scene(s, t, ImageDraw.Draw(cached), cached)
                lay = cached
            else:
                lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); scene(s, t, ImageDraw.Draw(lay), lay)
            im.alpha_composite(lay); ff.stdin.write(im.convert("RGB").tobytes())
        st += s["dur"]
    ff.stdin.close(); ff.wait()
    shutil.rmtree(work, ignore_errors=True)
    print(json.dumps({"out": out, "duration_s": round(total, 1), "scenes": len(scenes),
                      "chapters": [f"{a} {b}" for a, b in chapters]}))

if __name__ == "__main__":
    main()
