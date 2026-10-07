#!/usr/bin/env python3
"""Make a YouTube thumbnail (1280x720) and a 9:16 reel cover (1080x1920) in the channel's red/white style.

Usage: python3 thumbnail.py OUT_PREFIX --org "ONGC" --big "2,500 POSTS" --line "Graduate Trainee 2026" \
                            --badge "Freshers Can Apply" [--badge2 "Last Date: 30 Oct"]
Writes OUT_PREFIX_thumb.jpg and OUT_PREFIX_cover.jpg
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); A = os.path.join(ROOT, "assets")
RED, DRED, WHITE, INK, YEL = (237, 27, 36), (150, 8, 15), (255, 255, 255), (28, 28, 30), (255, 214, 0)
F = lambda w, s: ImageFont.truetype(os.path.join(A, f"Poppins-{w}.ttf"), int(s))

def fit(d, t, w, s, maxw, mn=24):
    while s > mn and d.textlength(t, font=F(w, s)) > maxw: s -= 2
    return F(w, s)

def bg(W, H):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for x in range(W):
        k = x / W; d.line([(x, 0), (x, H)], fill=tuple(int(RED[c] * (1 - k * .5) + DRED[c] * k * .5) for c in range(3)))
    im = im.convert("RGBA"); ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for k in range(-6, 20):
        x = k * 200; od.polygon([(x, 0), (x + 60, 0), (x + 60 - H // 2, H), (x - H // 2, H)], fill=(255, 255, 255, 16))
    im.alpha_composite(ov); return im

def pill(d, xy, text, fill, tcol, size, maxw):
    f = fit(d, text, "ExtraBold", size, maxw); x, y = xy
    w = d.textlength(text, font=f); h = int(f.size * 1.5)
    d.rounded_rectangle([x, y, x + w + 60, y + h], h // 2, fill=fill)
    d.text((x + 30, y + (h - f.size * 1.3) / 2), text, font=f, fill=tcol); return y + h

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("out")
    for k in ["org", "big", "line", "badge", "badge2"]: ap.add_argument("--" + k, default="")
    a = ap.parse_args()
    logo = Image.open(os.path.join(A, "logo_white.png")).convert("RGBA")

    # 16:9 thumbnail
    W, H = 1280, 720; im = bg(W, H); d = ImageDraw.Draw(im)
    im.alpha_composite(logo.resize((110, 103)), (40, 34))
    d.text((165, 50), "Deewane: IES & GATE Point", font=F("Bold", 38), fill=WHITE)
    d.text((60, 175), a.org.upper(), font=fit(d, a.org.upper(), "ExtraBold", 120, W - 120), fill=WHITE)
    d.text((60, 330), a.big, font=fit(d, a.big, "ExtraBold", 110, W - 120), fill=YEL)
    if a.line: d.text((62, 470), a.line, font=fit(d, a.line, "Bold", 54, W - 120), fill=WHITE)
    y = 575
    if a.badge: pill(d, (60, y), a.badge, WHITE, RED, 46, 560)
    if a.badge2: pill(d, (680, y), a.badge2, INK, WHITE, 46, 470)
    im.convert("RGB").save(a.out + "_thumb.jpg", quality=92)

    # 9:16 cover
    W, H = 1080, 1920; im = bg(W, H); d = ImageDraw.Draw(im)
    im.alpha_composite(logo.resize((150, 140)), (465, 120))
    def c(y, t, f, col): d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=col)
    c(300, "NEW GOVT JOB", F("ExtraBold", 90), WHITE)
    c(560, a.org.upper(), fit(d, a.org.upper(), "ExtraBold", 150, W - 100), WHITE)
    c(800, a.big, fit(d, a.big, "ExtraBold", 130, W - 100), YEL)
    if a.line: c(1010, a.line, fit(d, a.line, "Bold", 60, W - 100), WHITE)
    y = 1200
    for b, fl, tc in [(a.badge, WHITE, RED), (a.badge2, INK, WHITE)]:
        if b:
            f = fit(d, b, "ExtraBold", 60, W - 220); w = d.textlength(b, font=f); h = int(f.size * 1.6)
            d.rounded_rectangle([(W - w) / 2 - 40, y, (W + w) / 2 + 40, y + h], h // 2, fill=fl)
            c(y + (h - f.size * 1.3) / 2, b, f, tc); y += h + 50
    c(1720, "Deewane: IES & GATE Point", F("Bold", 50), WHITE)
    im.convert("RGB").save(a.out + "_cover.jpg", quality=92)
    print(a.out + "_thumb.jpg", a.out + "_cover.jpg")

if __name__ == "__main__":
    main()
