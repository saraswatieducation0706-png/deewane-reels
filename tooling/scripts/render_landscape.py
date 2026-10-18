#!/usr/bin/env python3
"""Render a 16:9 (1920x1080, 30 fps) promo / explainer video in the Deewane reel style from a JSON spec.

Usage:  python3 render_landscape.py spec.json [--no-tts]

Same voice pipeline as render_challenge.py (ElevenLabs, one clip per scene, cached).
Scene kinds: hook, punch, big, versus, card, steps, grid, chips, table, qr, end.
"""
import subprocess, os, sys, json, math
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_challenge as rc  # reuse tts(), dur(), fonts, colours, config

A, CFG = rc.A, rc.CFG
W, H, FPS = 1920, 1080, 30
RED, DRED, WHITE, INK, SOFT = rc.RED, rc.DRED, rc.WHITE, rc.INK, rc.SOFT
GOLD, GREEN, GREY = (255, 196, 0), (22, 163, 74), (120, 120, 128)
F = rc.F
ease = rc.ease
def back(t):  # overshoot ease for "pop"
    t = min(max(t, 0), 1); c = 1.70158
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2

def fit(d, txt, weight, size, maxw, minsize=22):
    s = size
    while s > minsize and d.textlength(txt, font=F(weight, s)) > maxw: s -= 2
    return F(weight, s)
def ctext(d, y, txt, font, fill, alpha=1.0, cx=W / 2):
    w = d.textlength(txt, font=font)
    d.text((cx - w / 2, y), txt, font=font, fill=fill + (int(255 * max(0, min(alpha, 1))),))
def ftext(d, y, txt, weight, size, fill, alpha, maxw=W - 300, cx=W / 2):
    ctext(d, y, txt, fit(d, txt, weight, size, maxw), fill, alpha, cx)
def col(c, a): return c + (int(255 * max(0, min(a, 1))),)

def title(d, s, t, y=150):
    a = ease(t / 0.4); sl = (1 - a) * 80
    ftext(d, y + sl, s["title"], "ExtraBold", 72, WHITE, a, W - 300)
    d.rounded_rectangle([W / 2 - 120 * a, y + 104, W / 2 + 120 * a, y + 113], 5, fill=col(WHITE, 0.9 * a))
    return a

def wrap(d, txt, font, maxw):
    words, lines, cur = txt.split(), [], ""
    for w_ in words:
        tst = (cur + " " + w_).strip()
        if d.textlength(tst, font=font) <= maxw: cur = tst
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def scene(s, t, d, lay, T):
    k = s["kind"]
    if k == "hook":  # title lines (1-3) popping in, optional sub pill, optional "shake"
        n = len(s["title"]); y0 = 300 - (n - 1) * 70
        for j, ln in enumerate(s["title"]):
            p = back((t - 0.25 * j) / 0.45); a = ease((t - 0.25 * j) / 0.3)
            size = s.get("size", 120) * (0.6 + 0.4 * p)
            jit = math.sin(t * 40) * 6 * max(0, 1 - t) if s.get("shake") else 0
            ftext(d, y0 + j * 150, ln, "ExtraBold", size, GOLD if j == s.get("gold", -1) else WHITE, a, W - 200, W / 2 + jit)
        if s.get("sub"):
            p = ease((t - 0.3 * n - 0.2) / 0.4)
            f = fit(d, s["sub"], "Bold", 50, W - 500); w = d.textlength(s["sub"], font=f) + 100
            y = y0 + n * 150 + 40
            d.rounded_rectangle([W / 2 - w / 2, y, W / 2 + w / 2, y + 100], 50, fill=col(WHITE, p))
            ctext(d, y + (100 - f.size * 1.3) / 2, s["sub"], f, RED, p)
        return
    if k == "punch":  # tilted dark band with a funny line + small caption
        p = back(t / 0.45); a = ease(t / 0.3)
        band = Image.new("RGBA", (W + 400, 260), (0, 0, 0, 0)); bd = ImageDraw.Draw(band)
        bd.rectangle([0, 0, W + 400, 260], fill=col(INK, 0.92 * a))
        f = fit(bd, s["text"], "ExtraBold", 84, W - 260)
        bd.text(((W + 400 - bd.textlength(s["text"], font=f)) / 2, (260 - f.size * 1.3) / 2), s["text"], font=f, fill=col(GOLD, a))
        band = band.rotate(-4 * p, resample=Image.BICUBIC, expand=True)
        sc = 0.7 + 0.3 * p; band = band.resize((int(band.width * sc), int(band.height * sc)))
        lay.alpha_composite(band, (int((W - band.width) / 2), int(470 - band.height / 2)))
        if s.get("cap"):
            q = ease((t - 0.6) / 0.4); ftext(d, 700, s["cap"], "SemiBold", 46, WHITE, q, W - 300)
        if s.get("top"):
            q = ease(t / 0.4); ftext(d, 200, s["top"], "Bold", 60, WHITE, q, W - 300)
        return
    if k == "big":  # giant number counting up (prefix/suffix), label, optional note
        a = ease(t / 0.4)
        if s.get("title"): title(d, s, t, 120)
        r = 300 * back(t / 0.5)
        d.ellipse([W / 2 - r, 560 - r, W / 2 + r, 560 + r], fill=col(WHITE, a))
        num = s["num"]; v = num * ease((t - 0.2) / 1.4)
        txt = s.get("prefix", "") + (f"{v:,.1f}" if isinstance(num, float) else f"{int(v):,}") + s.get("suffix", "")
        ftext(d, 420, txt, "ExtraBold", 170, RED, a, 520)
        ftext(d, 640, s.get("label", ""), "Bold", 46, INK, a, 500)
        if s.get("note"):
            p = ease((t - 1.0) / 0.4); f = fit(d, s["note"], "Bold", 44, W - 400)
            w = d.textlength(s["note"], font=f) + 90
            d.rounded_rectangle([W / 2 - w / 2, 900, W / 2 + w / 2, 990], 45, fill=col(INK, p))
            ctext(d, 900 + (90 - f.size * 1.3) / 2, s["note"], f, WHITE, p)
        return
    if k == "versus":  # two panels: left (bad, grey) vs right (good, white) with bullet lines
        title(d, s, t, 110)
        for side, (hd, lines) in enumerate([(s["left"], s["lt"]), (s["right"], s["rt"])]):
            p = ease((t - 0.4 - 0.6 * side) / 0.45); x0 = 160 + side * 840; dx = (1 - p) * (-300 if side == 0 else 300)
            d.rounded_rectangle([x0 + dx, 300, x0 + 760 + dx, 960], 40, fill=col((235, 235, 238) if side == 0 else WHITE, p))
            d.rounded_rectangle([x0 + dx, 300, x0 + 760 + dx, 400], 40, fill=col(GREY if side == 0 else GREEN, p))
            d.rectangle([x0 + dx, 360, x0 + 760 + dx, 400], fill=col(GREY if side == 0 else GREEN, p))
            ftext(d, 318, hd, "ExtraBold", 50, WHITE, p, 700, x0 + 380 + dx)
            for j, ln in enumerate(lines):
                q = ease((t - 0.7 - 0.6 * side - 0.3 * j) / 0.35); y = 440 + j * 120
                mark = "✗" if side == 0 else "✓"
                f = fit(d, ln, "Bold", 42, 600)
                d.text((x0 + 50 + dx, y), "•", font=F("ExtraBold", 50), fill=col(GREY if side == 0 else GREEN, q))
                d.text((x0 + 95 + dx, y + 4), ln, font=f, fill=col(INK, q))
        return
    if k == "qr":  # 2-4 QR codes with labels, optional bottom line
        title(d, s, t, 110)
        items = s["items"]; n = len(items); size = 330 if n <= 3 else 300; gap = 90
        x0 = (W - (n * size + (n - 1) * gap)) / 2
        for j, it in enumerate(items):
            q = back((t - 0.4 - 0.3 * j) / 0.45); a = ease((t - 0.4 - 0.3 * j) / 0.3); x = x0 + j * (size + gap)
            if a <= 0: continue
            pad = 18
            d.rounded_rectangle([x - pad, 290 - pad, x + size + pad, 290 + size + 110], 30, fill=col(WHITE, a))
            im = QR[it["img"]].resize((int(size * (0.8 + 0.2 * q)),) * 2, Image.NEAREST); im.putalpha(int(255 * a))
            lay.alpha_composite(im, (int(x + (size - im.width) / 2), int(290 + (size - im.height) / 2)))
            d.rounded_rectangle([x, 290 + size + 15, x + size, 290 + size + 85], 20, fill=col(RED, a))
            ftext(d, 290 + size + 22, it["label"], "Bold", 40, WHITE, a, size - 30, x + size / 2)
        if s.get("note"):
            p = ease((t - 0.6 - 0.3 * n) / 0.4); ftext(d, 880, s["note"], "Bold", 46, WHITE, p, W - 300)
        return
    if k == "end":
        p = ease((t - 0.2) / 0.5)
        d.rounded_rectangle([200, 130, W - 200, 990], 50, fill=col(WHITE, p))
        lay.alpha_composite(_alpha(LOGO_R, p), (int(W / 2 - 110), 170))
        ctext(d, 380, "DIG Career Thrust", F("ExtraBold", 70), RED, p)
        ctext(d, 470, s.get("line", "GATE ME 90 Days Challenge  •  Enrol once for ₹1"), F("SemiBold", 42), INK, p)
        items = s["items"]; n = len(items); size = 220; gap = 90; x0 = (W - (n * size + (n - 1) * gap)) / 2
        for j, it in enumerate(items):
            q = ease((t - 0.6 - 0.25 * j) / 0.4); x = x0 + j * (size + gap)
            if q <= 0: continue
            im = QR[it["img"]].resize((size, size), Image.NEAREST); im.putalpha(int(255 * q))
            lay.alpha_composite(im, (int(x), 550))
            d.rounded_rectangle([x, 785, x + size, 845], 18, fill=col(RED, q))
            ftext(d, 790, it["label"], "Bold", 34, WHITE, q, size - 20, x + size / 2)
        pf = ease((t - 1.8) / 0.4)
        d.rounded_rectangle([W / 2 - 520, 870, W / 2 + 520, 960], 45, fill=col(INK, pf))
        ctext(d, 885, s.get("cta", "All links are in the description below"), F("Bold", 44), WHITE, pf)
        return

    a = title(d, s, t)
    if k == "card":  # 1-5 lines
        n = len(s["lines"]); hh = 120 if n <= 4 else 104; gap = hh + 30; y0 = 330 + (5 - n) * 45
        for j, ln in enumerate(s["lines"]):
            p = ease((t - 0.4 - 0.45 * j) / 0.4); y = y0 + j * gap; dx = (1 - p) * 500
            d.rounded_rectangle([260 + dx, y, W - 260 + dx, y + hh], 30, fill=col(WHITE, p))
            d.rounded_rectangle([260 + dx, y, 284 + dx, y + hh], 12, fill=col(DRED, p))
            f = fit(d, ln, "Bold", 50, W - 640, 26)
            d.text(((W - d.textlength(ln, font=f)) / 2 + dx, y + (hh - f.size * 1.3) / 2), ln, font=f, fill=col(INK, p))
    elif k == "steps":  # horizontal timeline, 3-5 steps: [time, label]
        st = s["steps"]; n = len(st); bw = 300 if n == 5 else 360; gap = (W - 160 - n * bw) / max(n - 1, 1)
        for j, (tm, lab) in enumerate(st):
            p = back((t - 0.4 - 0.5 * j) / 0.45); a2 = ease((t - 0.4 - 0.5 * j) / 0.3); x = 80 + j * (bw + gap)
            cy = 470
            d.ellipse([x + bw / 2 - 90 * p, cy - 90 * p, x + bw / 2 + 90 * p, cy + 90 * p], fill=col(WHITE, a2))
            ftext(d, cy - 40, tm, "ExtraBold", 54, RED, a2, 160, x + bw / 2)
            d.rounded_rectangle([x, 600, x + bw, 820], 30, fill=col(WHITE, a2))
            f = F("Bold", 40); ls = wrap(d, lab, f, bw - 40)
            if len(ls) > 3: f = F("Bold", 34); ls = wrap(d, lab, f, bw - 40)
            yy = 600 + (220 - len(ls) * f.size * 1.25) / 2
            for ln in ls: ctext(d, yy, ln, f, INK, a2, x + bw / 2); yy += f.size * 1.25
            if j < n - 1:
                pa = ease((t - 0.7 - 0.5 * j) / 0.3)
                ax = x + bw / 2 + 110; bx = x + bw + gap + bw / 2 - 110
                d.line([ax, cy, ax + (bx - ax) * pa, cy], fill=col(WHITE, 0.85), width=8)
        if s.get("note"):
            p = ease((t - 0.6 - 0.5 * n) / 0.4); ftext(d, 880, s["note"], "Bold", 46, WHITE, p, W - 300)
    elif k == "grid":  # tiles [head, sub] 2-8 (2 rows max)
        tl = s["tiles"]; n = len(tl); cols = n if n <= 4 else math.ceil(n / 2); rows = 1 if n <= 4 else 2
        tw = (W - 200 - (cols - 1) * 40) / cols; th = 300 if rows == 1 else 250; y0 = 380 if rows == 1 else 300
        for j, (hd, sb) in enumerate(tl):
            r_, c_ = divmod(j, cols); x = 100 + c_ * (tw + 40); y = y0 + r_ * (th + 40)
            p = back((t - 0.35 - 0.25 * j) / 0.45); a2 = ease((t - 0.35 - 0.25 * j) / 0.3)
            sc = 0.7 + 0.3 * p; cx_, cy_ = x + tw / 2, y + th / 2; w2, h2 = tw * sc / 2, th * sc / 2
            d.rounded_rectangle([cx_ - w2, cy_ - h2, cx_ + w2, cy_ + h2], 34, fill=col(WHITE, a2))
            d.rounded_rectangle([cx_ - w2, cy_ - h2, cx_ + w2, cy_ - h2 + 16], 8, fill=col(RED, a2))
            fh = fit(d, hd, "ExtraBold", 50, tw - 50, 26)
            ctext(d, y + 50, hd, fh, RED, a2, cx_)
            f = F("SemiBold", 38); ls = wrap(d, sb, f, tw - 60)
            yy = y + 70 + fh.size * 1.3
            for ln in ls[:4]: ctext(d, yy, ln, f, INK, a2, cx_); yy += 48
    elif k == "chips":  # popping pills (e.g. organisations), optional note
        ch = s["chips"]; f = F("ExtraBold", 54); rows, cur, wsum = [], [], 0
        for c in ch:
            w_ = d.textlength(c, font=f) + 110
            if wsum + w_ > W - 300 and cur: rows.append(cur); cur, wsum = [], 0
            cur.append((c, w_)); wsum += w_ + 30
        if cur: rows.append(cur)
        k_ = 0; y0 = 380 if len(rows) <= 2 else 320
        for ri, row in enumerate(rows):
            tot = sum(w_ for _, w_ in row) + 30 * (len(row) - 1); x = (W - tot) / 2
            for c, w_ in row:
                p = back((t - 0.4 - 0.2 * k_) / 0.4); a2 = ease((t - 0.4 - 0.2 * k_) / 0.25)
                cx_, cy_ = x + w_ / 2, y0 + ri * 150 + 55; ww, hh = w_ * (0.6 + 0.4 * p) / 2, 55 * (0.6 + 0.4 * p)
                d.rounded_rectangle([cx_ - ww, cy_ - hh, cx_ + ww, cy_ + hh], 55, fill=col(WHITE, a2))
                ctext(d, cy_ - 38, c, f, RED, a2, cx_)
                x += w_ + 30; k_ += 1
        if s.get("note"):
            p = ease((t - 0.5 - 0.2 * len(ch)) / 0.4)
            nf = fit(d, s["note"], "Bold", 46, W - 400); w_ = d.textlength(s["note"], font=nf) + 100
            d.rounded_rectangle([W / 2 - w_ / 2, 820, W / 2 + w_ / 2, 920], 50, fill=col(INK, p))
            ctext(d, 820 + (100 - nf.size * 1.3) / 2, s["note"], nf, WHITE, p)
    elif k == "table":  # rows [[left, right]] up to 6
        rows = s["rows"]; n = len(rows); rh = 96 if n > 5 else 110; y0 = 310
        for j, (l, r) in enumerate(rows):
            p = ease((t - 0.35 - 0.3 * j) / 0.35); y = y0 + j * (rh + 18); dx = (1 - p) * 400
            d.rounded_rectangle([280 + dx, y, W - 280 + dx, y + rh], 28, fill=col(WHITE, p))
            d.rounded_rectangle([W - 700 + dx, y, W - 280 + dx, y + rh], 28, fill=col(INK, p))
            fl = fit(d, l, "Bold", 44, W - 1060, 24); fr = fit(d, str(r), "ExtraBold", 48, 380, 24)
            d.text((320 + dx, y + (rh - fl.size * 1.3) / 2), l, font=fl, fill=col(INK, p))
            ctext(d, y + (rh - fr.size * 1.3) / 2, str(r), fr, WHITE, p, W - 490 + dx)
        if s.get("note"):
            p = ease((t - 0.5 - 0.3 * n) / 0.4); ftext(d, y0 + n * (rh + 18) + 30, s["note"], "SemiBold", 36, SOFT, p, W - 400)
    else:
        raise ValueError(f"unknown scene kind {k}")

def _alpha(im, a):
    im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * a))); return im

def min_dur(s):
    k = s["kind"]
    if k == "card": return 1.0 + 0.45 * len(s["lines"])
    if k == "table": return 1.0 + 0.3 * len(s["rows"])
    if k == "steps": return 1.5 + 0.5 * len(s["steps"])
    if k == "grid": return 1.5 + 0.25 * len(s["tiles"])
    if k == "chips": return 1.5 + 0.2 * len(s["chips"])
    if k == "qr": return 2.5
    return s.get("min_dur", 2.0)

def main():
    global LOGO_R, QR
    spec_path = sys.argv[1]; use_api = "--no-tts" not in sys.argv
    spec = json.load(open(spec_path)); scenes = spec["scenes"]
    out = spec["out"]; work = out + ".work"; os.makedirs(work, exist_ok=True)
    cache = os.path.join(os.path.dirname(os.path.abspath(out)), ".tts_cache"); os.makedirs(cache, exist_ok=True)
    gap = CFG.get("scene_gap_s", 0.4)
    for i, s in enumerate(scenes):
        p = f"{work}/s{i}.wav"; rc.tts(s["voice"], p, cache, use_api)
        s["dur"] = max(rc.dur(p) + gap, min_dur(s), s.get("min_dur", 0))
    ins = sum((["-i", f"{work}/s{i}.wav"] for i in range(len(scenes))), [])
    flt = "".join(f"[{i}]aresample=44100,aformat=channel_layouts=mono,apad=whole_dur={s['dur']}[a{i}];" for i, s in enumerate(scenes))
    flt += "".join(f"[a{i}]" for i in range(len(scenes))) + \
        f"concat=n={len(scenes)}:v=0:a=1,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[out]"
    subprocess.run(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", flt, "-map", "[out]", f"{work}/voice.wav"], check=True)

    LOGO_R = Image.open(os.path.join(A, "logo_red.png")).convert("RGBA").resize((220, 205), Image.LANCZOS)
    logo_w = Image.open(os.path.join(A, "logo_white.png")).convert("RGBA").resize((86, 80), Image.LANCZOS)
    QR = {}
    for name, path in spec.get("qrs", {}).items():
        QR[name] = Image.open(path).convert("RGBA")
    grad = Image.new("RGB", (W + 240, H)); gd = ImageDraw.Draw(grad)
    for y in range(H):
        k = y / H; gd.line([(0, y), (W + 240, y)], fill=tuple(int(RED[c] * (1 - k * 0.45) + DRED[c] * k * 0.45) for c in range(3)))
    grad = grad.convert("RGBA"); stripes = Image.new("RGBA", (W + 240, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(stripes)
    for k in range(-6, 16):
        x = k * 240; sd.polygon([(x, 0), (x + 80, 0), (x + 80 - 700, H), (x - 700, H)], fill=(255, 255, 255, 14))
    grad.alpha_composite(stripes)
    total = sum(s["dur"] for s in scenes)

    def background(tg):
        off = int((tg * 40) % 240); im = grad.crop((240 - off, 0, 240 - off + W, H))
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, W, 104], fill=(0, 0, 0, 50))
        im.alpha_composite(logo_w, (40, 12))
        d.text((140, 18), rc.CHANNEL, font=F("Bold", 36), fill=WHITE)
        d.text((142, 62), spec.get("header_sub", "GATE ME 90 Days Challenge"), font=F("Medium", 24), fill=SOFT)
        if spec.get("footer"):
            f = fit(d, spec["footer"], "Medium", 26, W - 200); ctext(d, H - 62, spec["footer"], f, SOFT)
        d.rectangle([0, H - 12, W, H], fill=DRED); d.rectangle([0, H - 12, W * tg / total, H], fill=WHITE)
        return im

    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-i", f"{work}/voice.wav", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                           "-preset", "fast", "-crf", "21", "-c:a", "aac", "-b:a", "160k", "-shortest",
                           "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    st = 0; only = os.environ.get("ONLY")  # ONLY=3 renders a 1-frame-per-scene preview strip
    for i, s in enumerate(scenes):
        nfr = int(round(s["dur"] * FPS))
        for fr in range(nfr):
            t = fr / FPS
            im = background(st + t)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); scene(s, t, ImageDraw.Draw(lay), lay, total)
            im.alpha_composite(lay); ff.stdin.write(im.convert("RGB").tobytes())
        st += s["dur"]
    ff.stdin.close(); ff.wait()
    print(json.dumps({"out": out, "duration_s": round(total, 1), "scenes": len(scenes)}))

if __name__ == "__main__":
    main()
