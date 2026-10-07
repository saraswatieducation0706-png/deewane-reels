#!/usr/bin/env python3
"""Render a GATE ME 90 Days Challenge daily reel (adapted from render_reel.py) (1080x1920, 30 fps) from a JSON spec.

Usage:  python3 render_reel.py spec.json [--no-tts]

The fixed WELCOME scene (signature line) and END scene (website + 3 QR codes) are added
automatically - the spec contains only the job scenes (first one must be kind "hook").
See references/scene_kinds.md for every scene kind and its fields.
Voice: ElevenLabs (config.json), one clip per scene, scene = clip + gap. Clips are cached
by text so the welcome/end lines are only billed once.
"""
import subprocess, os, sys, json, hashlib, urllib.request, shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets")
CFG = json.load(open(os.path.join(ROOT, "config.json")))
W, H, FPS = 1080, 1920, 30
RED, DRED, WHITE, INK, SOFT = (237, 27, 36), (168, 10, 18), (255, 255, 255), (28, 28, 30), (255, 225, 226)
CHANNEL = "Deewane: IES & GATE Point"
_fc = {}
def F(w, s):
    k = (w, int(s))
    if k not in _fc: _fc[k] = ImageFont.truetype(os.path.join(A, f"Poppins-{w}.ttf"), int(s))
    return _fc[k]

WELCOME = dict(kind="welcome", voice="Hello Everyone, I hope your preparations for the exam are going well.",
               title="Hello Everyone!", sub="Hope your preparation is going well")
END = dict(kind="end", voice="Comment GATE ninety to get all the links. For test series and study material, visit web dot D. I. G. career thrust dot com. "
           "Scan the codes to get our app and join our Telegram.", min_dur=7.0)
QRS = [("Mobile App", "qr_playstore_app.jpeg"), ("Telegram", "qr_telegram.jpeg"), ("Website", "qr_website.jpeg")]

# ---------------- TTS ----------------
def tts(text, out, cache, use_api=True):
    key = os.environ.get("XI") or CFG.get("elevenlabs_api_key")
    voice = os.environ.get("VOICE_ID") or CFG["voice_id"]
    speed = float(os.environ.get("SPEED") or CFG.get("speed", 1.1))
    h = hashlib.sha1(f"{voice}|{speed}|{CFG['tts_model']}|{text}".encode()).hexdigest()[:16]
    cp = os.path.join(cache, h + ".wav")
    if not os.path.exists(cp):
        if use_api and key:
            body = {"text": text, "model_id": CFG["tts_model"],
                    "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "speed": speed}}
            req = urllib.request.Request(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128",
                data=json.dumps(body).encode(), headers={"xi-api-key": key, "Content-Type": "application/json"})
            try:
                data = urllib.request.urlopen(req, timeout=120).read()
            except urllib.error.HTTPError as e:
                sys.exit(f"ElevenLabs error {e.code}: {e.read()[:300]}")
            open(cp + ".mp3", "wb").write(data)
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", cp + ".mp3", cp], check=True)
        else:  # silent placeholder for layout tests (~13 chars/sec)
            d = max(1.5, len(text) / 15)
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
                            "-t", str(d), cp], check=True)
    shutil.copy(cp, out)

dur = lambda p: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                                "-of", "csv=p=0", p]))

# ---------------- drawing helpers ----------------
ease = lambda t: 1 - (1 - min(max(t, 0), 1)) ** 3
def fit(d, txt, weight, size, maxw, minsize=26):
    s = size
    while s > minsize and d.textlength(txt, font=F(weight, s)) > maxw: s -= 2
    return F(weight, s)
def ctext(d, y, txt, font, fill, alpha=1.0, x=None):
    w = d.textlength(txt, font=font)
    d.text(((W - w) / 2 if x is None else x, y), txt, font=font, fill=fill + (int(255 * max(0, min(alpha, 1))),))
def ftext(d, y, txt, weight, size, fill, alpha, maxw=W - 160):
    ctext(d, y, txt, fit(d, txt, weight, size, maxw), fill, alpha)
def title(d, s, t):
    a = ease(t / 0.45); sl = (1 - a) * 110
    ftext(d, 330 + sl, s["title"], "ExtraBold", 80, WHITE, a, W - 120)
    d.rounded_rectangle([W/2 - 110*a, 455, W/2 + 110*a, 465], 5, fill=WHITE + (int(230*a),))
    return a

def scene(s, t, d, lay):
    k = s["kind"]
    if k == "welcome":
        p0 = ease(t / 0.5); r = 230 * p0
        d.ellipse([W/2 - r, 800 - r, W/2 + r, 800 + r], fill=WHITE + (int(255 * p0),))
        if p0 > 0.05:
            lg = LOGO_R.copy(); lg.putalpha(lg.getchannel("A").point(lambda v: int(v * p0)))
            lay.alpha_composite(lg, (int(W/2 - 150), int(800 - 140)))
        p1 = ease((t - 0.4) / 0.4); ctext(d, 1090 + (1-p1)*60, s["title"], F("ExtraBold", 104), WHITE, p1)
        p2 = ease((t - 0.8) / 0.4)
        d.rounded_rectangle([110, 1250, W - 110, 1350], 50, fill=WHITE + (int(255 * p2),))
        ctext(d, 1272, s["sub"], F("Bold", 40), RED, p2)
        return
    if k == "hook":
        p0 = ease(t / 0.35); sc = 0.55 + 0.45 * p0
        ftext(d, 560, s["title"][0], "ExtraBold", 120 * sc, WHITE, p0, W - 100)
        p1 = ease((t - 0.3) / 0.35)
        if len(s["title"]) > 1: ftext(d, 720 + (1-p1)*60, s["title"][1], "ExtraBold", 120, WHITE, p1, W - 100)
        p2 = ease((t - 0.7) / 0.4)
        d.rounded_rectangle([70, 960, W - 70, 1080], 60, fill=WHITE + (int(255 * p2),))
        ftext(d, 988, s.get("sub", ""), "Bold", 44, RED, p2, W - 200)
        return
    if k == "end":
        p = ease((t - 0.3) / 0.5)
        d.rounded_rectangle([60, 560, W - 60, 1300], 44, fill=WHITE + (int(255 * p),))
        ctext(d, 600, "DIG Career Thrust", F("ExtraBold", 66), RED, p)
        ctext(d, 690, "Test Series  •  Study Material", F("SemiBold", 40), INK, p)
        for j, (lab, _) in enumerate(QRS):
            q = ease((t - 0.8 - 0.35 * j) / 0.4); x = 90 + j * 310
            if q > 0:
                qi = QR_IMGS[j].copy(); qi.putalpha(int(255 * q)); lay.alpha_composite(qi, (int(x), 790))
                d.rounded_rectangle([x, 1080, x + 270, 1150], 20, fill=RED + (int(255 * q),))
                w = d.textlength(lab, font=F("Bold", 38))
                d.text((x + (270 - w) / 2, 1088), lab, font=F("Bold", 38), fill=WHITE + (int(255*q),))
        ctext(d, 1190, "web.digcareerthrust.com", F("SemiBold", 44), INK, p)
        pf = ease((t - 2.2) / 0.4)
        d.rounded_rectangle([170, 1380, W - 170, 1490], 55, fill=INK + (int(255 * pf),))
        ctext(d, 1400, "Comment GATE90 for links", F("Bold", 46), WHITE, pf)
        return

    a = title(d, s, t)
    if k == "card":  # 1-4 short lines
        n = len(s["lines"]); hh = 160 if n <= 3 else 140; gap = hh + 45; y0 = 560 + (4 - n) * 50
        for j, ln in enumerate(s["lines"]):
            p = ease((t - 0.4 - 0.45 * j) / 0.4); y = y0 + j * gap; dx = (1 - p) * 400
            d.rounded_rectangle([80 + dx, y, W - 80 + dx, y + hh], 34, fill=WHITE + (int(255 * p),))
            d.rounded_rectangle([80 + dx, y, 104 + dx, y + hh], 12, fill=DRED + (int(255 * p),))
            f = fit(d, ln, "Bold", 52, W - 240, 30)
            d.text(((W - d.textlength(ln, font=f)) / 2 + dx, y + (hh - f.size * 1.25) / 2), ln, font=f, fill=INK + (int(255*p),))
    elif k == "count":
        d.ellipse([W/2 - 330*a, 960 - 330*a, W/2 + 330*a, 960 + 330*a], fill=WHITE + (int(255*a),))
        n = int(s["num"] * ease((t - 0.3) / 1.5))
        ftext(d, 820, f"{n:,}", "ExtraBold", 190, RED, a, 600)
        ctext(d, 1060, s.get("label", "POSTS"), F("Bold", 56), INK, a)
        if s.get("note"):
            p = ease((t - 1.2) / 0.4)
            d.rounded_rectangle([120, 1360, W - 120, 1460], 50, fill=WHITE + (int(255 * p),))
            ftext(d, 1382, s["note"], "Bold", 42, RED, p, W - 300)
    elif k == "table":  # rows [[left, right]] up to 7
        rows = s["rows"]; n = len(rows); rh = 118 if n > 5 else 140; y0 = 540
        for j, (l, r) in enumerate(rows):
            p = ease((t - 0.35 - 0.3 * j) / 0.35); y = y0 + j * (rh + 22); dx = (1 - p) * 300
            d.rounded_rectangle([70 + dx, y, W - 70 + dx, y + rh], 30, fill=WHITE + (int(255 * p),))
            d.rounded_rectangle([W - 320 + dx, y, W - 70 + dx, y + rh], 30, fill=RED + (int(255 * p),))
            fl = fit(d, l, "Bold", 46, W - 470, 26); fr = fit(d, str(r), "ExtraBold", 54, 220, 26)
            d.text((105 + dx, y + (rh - fl.size * 1.25) / 2), l, font=fl, fill=INK + (int(255*p),))
            wr = d.textlength(str(r), font=fr)
            d.text((W - 195 - wr / 2 + dx, y + (rh - fr.size * 1.25) / 2), str(r), font=fr, fill=WHITE + (int(255*p),))
        if s.get("note"):
            p = ease((t - 0.5 - 0.3 * n) / 0.4); yn = y0 + n * (rh + 22) + 20
            ftext(d, yn, s["note"], "SemiBold", 38, SOFT, p)
    elif k == "pattern":  # header [3], rows [[3]] up to 6, chips up to 3
        hd = s.get("header", ["Section", "Qs", "Marks"]); rows = s["rows"]; cw = [500, 200, 200]
        xs = [80, 80 + cw[0], 80 + cw[0] + cw[1]]; y0 = 540; rh = 100
        d.rounded_rectangle([70, y0, W - 70, y0 + rh], 26, fill=INK + (int(255 * a),))
        for c in range(3):
            f = fit(d, hd[c], "Bold", 40, cw[c] - 30)
            d.text((xs[c] + (cw[c] - d.textlength(hd[c], font=f)) / 2, y0 + 26), hd[c], font=f, fill=WHITE + (int(255*a),))
        for j, row in enumerate(rows):
            p = ease((t - 0.4 - 0.25 * j) / 0.35); y = y0 + (j + 1) * (rh + 12)
            d.rounded_rectangle([70, y, W - 70, y + rh], 26, fill=WHITE + (int(255 * p),))
            for c in range(3):
                txt = str(row[c]); f = fit(d, txt, "Bold" if c == 0 else "ExtraBold", 42, cw[c] - 30, 24)
                d.text((xs[c] + (cw[c] - d.textlength(txt, font=f)) / 2, y + (rh - f.size * 1.25) / 2), txt,
                       font=f, fill=(INK if c == 0 else RED) + (int(255*p),))
        chips = s.get("chips", []); yc = y0 + (len(rows) + 1) * (rh + 12) + 40
        for j, ch in enumerate(chips):
            p = ease((t - 0.6 - 0.25 * len(rows) - 0.3 * j) / 0.35); y = yc + j * 110
            d.rounded_rectangle([140, y, W - 140, y + 90], 45, fill=DRED + (int(255 * p),))
            ftext(d, y + 18, ch, "Bold", 42, WHITE, p, W - 340)
    elif k == "steps":  # selection process, 2-5 steps
        st = s["steps"]; n = len(st); bh = 120; gap = 70; y0 = 560 + (5 - n) * 40
        for j, label in enumerate(st):
            p = ease((t - 0.4 - 0.5 * j) / 0.4); y = y0 + j * (bh + gap)
            d.rounded_rectangle([150, y, W - 90, y + bh], 60, fill=WHITE + (int(255 * p),))
            d.ellipse([80, y - 5, 210, y + bh + 5], fill=INK + (int(255 * p),))
            num = str(j + 1); fn = F("ExtraBold", 64)
            d.text((145 - d.textlength(num, font=fn) / 2, y + 12), num, font=fn, fill=WHITE + (int(255*p),))
            f = fit(d, label, "Bold", 48, W - 360, 26)
            d.text((240, y + (bh - f.size * 1.25) / 2), label, font=f, fill=INK + (int(255*p),))
            if j < n - 1:
                pa = ease((t - 0.7 - 0.5 * j) / 0.3)
                d.polygon([(130, y + bh + 15), (160, y + bh + 15), (145, y + bh + gap - 12)], fill=WHITE + (int(220*pa),))
        if s.get("note"):
            p = ease((t - 0.6 - 0.5 * n) / 0.4); yn = y0 + n * (bh + gap) + 10
            d.rounded_rectangle([90, yn, W - 90, yn + 100], 50, fill=DRED + (int(255 * p),))
            ftext(d, yn + 24, s["note"], "Bold", 40, WHITE, p, W - 260)
    elif k == "dates":  # lines [[label, value]] 2-4
        ln = s["lines"]; n = len(ln); bh = 290 if n <= 2 else (230 if n == 3 else 190); gap = bh + 50
        for j, (lab, val) in enumerate(ln):
            p = ease((t - 0.4 - 0.6 * j) / 0.4); y = 560 + j * gap
            hb = 80 if n <= 2 else 66
            d.rounded_rectangle([110, y, W - 110, y + bh], 40, fill=WHITE + (int(255 * p),))
            d.rounded_rectangle([110, y, W - 110, y + hb], 40, fill=INK + (int(255 * p),))
            d.rectangle([110, y + hb - 36, W - 110, y + hb], fill=INK + (int(255 * p),))
            ftext(d, y + (hb - 52) / 2, lab.upper(), "Bold", 42 if n <= 2 else 36, WHITE, p, W - 300)
            vs = 96 if n <= 2 else (78 if n == 3 else 64)
            ftext(d, y + hb + (bh - hb - vs * 1.3) / 2, val, "ExtraBold", vs, RED if j == n - 1 else INK, p, W - 300)
    elif k == "toppers":  # entries [{rank, name, marks, photo?}] 1-5 (ties allowed)
        en = s["entries"]; n = len(en); rh = 190 if n <= 3 else 150; gap = rh + 34; y0 = 540 + (3 - min(n, 3)) * 60
        for j, e in enumerate(en):
            p = ease((t - 0.4 - 0.5 * j) / 0.4); y = y0 + j * gap; dx = (1 - p) * 400
            d.rounded_rectangle([70 + dx, y, W - 70 + dx, y + rh], 40, fill=WHITE + (int(255 * p),))
            cr = rh * 0.32; cx = 140 + dx; cy = y + rh / 2
            d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=RED + (int(255 * p),))
            rk = f"#{e['rank']}"; fr = F("ExtraBold", int(cr * 0.9))
            d.text((cx - d.textlength(rk, font=fr) / 2, cy - fr.size * 0.62), rk, font=fr, fill=WHITE + (int(255*p),))
            ps = int(rh * 0.74); px = int(215 + dx); py = int(cy - ps / 2)
            ph = e.get("photo")
            if ph and os.path.exists(ph) and p > 0.02:
                im = Image.open(ph).convert("RGB"); m = min(im.size)
                im = im.crop(((im.width - m) // 2, (im.height - m) // 2, (im.width + m) // 2, (im.height + m) // 2)).resize((ps, ps))
                mk = Image.new("L", (ps, ps), 0); ImageDraw.Draw(mk).ellipse([0, 0, ps - 1, ps - 1], fill=int(255 * p))
                im = im.convert("RGBA"); im.putalpha(mk); lay.alpha_composite(im, (px, py))
                tx = px + ps + 28
            else:
                tx = int(215 + dx)
            mk_txt = str(e["marks"]); fm = fit(d, mk_txt, "ExtraBold", 50, 230, 26)
            mw = d.textlength(mk_txt, font=fm) + 50
            d.rounded_rectangle([W - 90 - mw + dx, cy - 45, W - 90 + dx, cy + 45], 45, fill=RED + (int(255 * p),))
            d.text((W - 90 - mw + 25 + dx, cy - fm.size * 0.62), mk_txt, font=fm, fill=WHITE + (int(255*p),))
            fn = fit(d, e["name"], "Bold", 50, (W - 110 - mw + dx) - tx - 10, 26)
            d.text((tx, cy - fn.size * 0.62), e["name"], font=fn, fill=INK + (int(255*p),))
        if s.get("note"):
            p = ease((t - 0.6 - 0.5 * n) / 0.4); yn = y0 + n * gap + 10
            ftext(d, yn, s["note"], "SemiBold", 38, SOFT, p)
    else:
        raise ValueError(f"unknown scene kind {k}")

def min_dur(s):
    k = s["kind"]
    if k == "card": return 0.9 + 0.45 * len(s["lines"])
    if k == "table": return 0.9 + 0.3 * len(s["rows"])
    if k == "pattern": return 1.2 + 0.25 * len(s["rows"]) + 0.3 * len(s.get("chips", []))
    if k == "steps": return 1.2 + 0.5 * len(s["steps"])
    if k == "toppers": return 1.2 + 0.6 * len(s["entries"])
    if k == "dates": return 0.9 + 0.6 * len(s["lines"])
    return s.get("min_dur", 2.0)

# ---------------- main ----------------
def main():
    global LOGO_R, QR_IMGS
    spec_path = sys.argv[1]; use_api = "--no-tts" not in sys.argv
    spec = json.load(open(spec_path))
    scenes = [dict(WELCOME)] + spec["scenes"] + [dict(END)]
    out = spec["out"]; work = out + ".work"; os.makedirs(work, exist_ok=True)
    cache = os.path.join(os.path.dirname(os.path.abspath(out)), ".tts_cache"); os.makedirs(cache, exist_ok=True)
    gap = CFG.get("scene_gap_s", 0.4)
    for i, s in enumerate(scenes):
        p = f"{work}/s{i}.wav"; tts(s["voice"], p, cache, use_api)
        s["dur"] = max(dur(p) + gap, min_dur(s), s.get("min_dur", 0))
    ins = sum((["-i", f"{work}/s{i}.wav"] for i in range(len(scenes))), [])
    flt = "".join(f"[{i}]aresample=44100,aformat=channel_layouts=mono,apad=whole_dur={s['dur']}[a{i}];" for i, s in enumerate(scenes))
    flt += "".join(f"[a{i}]" for i in range(len(scenes))) + \
        f"concat=n={len(scenes)}:v=0:a=1,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[out]"
    subprocess.run(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", flt, "-map", "[out]", f"{work}/voice.wav"], check=True)

    LOGO_R = Image.open(os.path.join(A, "logo_red.png")).convert("RGBA").resize((300, 280), Image.LANCZOS)
    logo_w = Image.open(os.path.join(A, "logo_white.png")).convert("RGBA").resize((120, 112), Image.LANCZOS)
    QR_IMGS = [Image.open(os.path.join(A, p)).convert("RGBA").resize((270, 270), Image.NEAREST) for _, p in QRS]
    base = Image.new("RGB", (W, H)); bd = ImageDraw.Draw(base)
    for y in range(H):
        k = y / H
        bd.line([(0, y), (W, y)], fill=tuple(int(RED[c] * (1 - k * 0.45) + DRED[c] * k * 0.45) for c in range(3)))
    base = base.convert("RGBA")
    src = spec.get("source", "")
    # wide striped background (stripes repeat every 220 px) - each frame is just a crop + header paste
    grad = base.resize((W + 220, H))
    wd = ImageDraw.Draw(stripes := Image.new("RGBA", (W + 220, H), (0, 0, 0, 0)))
    for k in range(-5, 17):
        x = k * 220
        wd.polygon([(x, 0), (x + 70, 0), (x + 70 - 900, H), (x - 900, H)], fill=(255, 255, 255, 14))
    grad.alpha_composite(stripes)
    top = Image.new("RGBA", (W, 190), (0, 0, 0, 40)); top.alpha_composite(logo_w, (50, 50))
    total = sum(s["dur"] for s in scenes)

    def background(tg):
        off = int((tg * 40) % 220)
        im = grad.crop((220 - off, 0, 220 - off + W, H))
        hdr_bg = im.crop((0, 0, W, 190)); hdr_bg.alpha_composite(top); im.paste(hdr_bg, (0, 0))
        d = ImageDraw.Draw(im)
        d.text((190, 62), CHANNEL, font=F("Bold", 46), fill=WHITE)
        d.text((192, 120), "GATE ME 90 Days Challenge", font=F("Medium", 30), fill=SOFT)
        if spec.get("footer"):
            lab = spec["footer"]
            f = fit(d, lab, "Medium", 30, W - 100, 20)
            d.text(((W - d.textlength(lab, font=f)) / 2, 1790), lab, font=f, fill=SOFT)
        d.rectangle([0, H - 16, W, H], fill=DRED)
        d.rectangle([0, H - 16, W * tg / total, H], fill=WHITE)
        return im

    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-i", f"{work}/voice.wav", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                           "-preset", "fast", "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-shortest",
                           "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    st = 0
    for s in scenes:
        for fr in range(int(round(s["dur"] * FPS))):
            t = fr / FPS
            im = background(st + t)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); scene(s, t, ImageDraw.Draw(lay), lay)
            im.alpha_composite(lay); ff.stdin.write(im.convert("RGB").tobytes())
        st += s["dur"]
    ff.stdin.close(); ff.wait()
    shutil.rmtree(work, ignore_errors=True)
    print(json.dumps({"out": out, "duration_s": round(total, 1), "scenes": len(scenes)}))

if __name__ == "__main__":
    main()
