"""YouTube thumbnail (1280x720) for a long video.
python3 make_thumb.py out.jpg <scene> "Big text" ["small line"] [seed]
"""
import sys
from PIL import Image, ImageDraw
import cb_common as cb

out, scene, big = sys.argv[1], sys.argv[2], sys.argv[3]
small = sys.argv[4] if len(sys.argv) > 4 else ""
seed = int(sys.argv[5]) if len(sys.argv) > 5 else 1
W, H = 1280, 720
img = cb.paint(scene, W, H, seed=seed)
if scene == "candle":
    cb.flame(img, 0.3, W, H)
img = img.convert("RGBA")
t = cb.text_block(W, big, "serif_bold", 150, (255, 255, 255), W - 140, max_lines=2)
img.alpha_composite(t, (0, int(H * 0.36 - t.height / 2)))
if small:
    s = cb.text_block(W, small, "body_italic", 44, (255, 236, 200), W - 200)
    img.alpha_composite(s, (0, int(H * 0.36 + t.height / 2 - 10)))
d = ImageDraw.Draw(img)
f = cb.font("serif", 34)
label = "Christ's Blessings"
tw = d.textlength(label, font=f)
d.text((W - tw - 40, H - 62), label, font=f, fill=(255, 245, 225, 230))
img.convert("RGB").save(out, quality=92)
