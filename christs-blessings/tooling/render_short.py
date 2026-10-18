"""Render one Christ's Blessings Short (1080x1920) from a spec JSON.

Spec:
{
  "out": "/abs/short.mp4", "template": "A", "scene": "dawn_lake", "seed": 1, "music_key": "D",
  "cover": ["Read this", "slowly"],
  "segments": [
    {"role": "hook", "text": "..."},            # spoken while the cover title shows
    {"role": "ref", "text": "Philippians 4, verses 6 and 7.", "label": "Philippians 4:6-7"},
    {"role": "verse", "text": "Be careful for nothing; ...", "label": "Philippians 4:6-7"},
    {"role": "reflection", "text": "..."},
    {"role": "prayer", "text": "..."},
    {"role": "close", "text": "..."}
  ]
}
Templates: A nature (lake), B illustrated scene, C kinetic gold text on dark, D candle, E "pray with me" parchment.
"""
import json, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw
import cb_common as cb

W, H, FPS = 1080, 1920, 30
STYLE = {
    "A": dict(txt=(255, 255, 255), verse=(255, 232, 180), sub=(255, 240, 214), parts=(40, (255, 236, 196))),
    "B": dict(txt=(255, 255, 255), verse=(255, 230, 176), sub=(255, 236, 210), parts=(26, (255, 226, 180))),
    "C": dict(txt=(244, 222, 170), verse=(255, 214, 140), sub=(214, 196, 160), parts=(55, (230, 190, 120))),
    "D": dict(txt=(255, 244, 228), verse=(255, 214, 150), sub=(240, 210, 170), parts=(18, (255, 180, 100))),
    "E": dict(txt=(58, 44, 30), verse=(122, 84, 30), sub=(110, 86, 56), parts=(20, (255, 250, 230))),
}
GAP = {"verse": 0.55, "ref": 0.3, "prayer": 0.5}


def main(spec_path):
    spec = json.load(open(spec_path))
    st = STYLE[spec["template"]]
    work = tempfile.mkdtemp(prefix="cbs_")
    sr = 44100
    # ---- voice timeline
    t = 0.35
    voice = np.zeros(int(sr * 120), np.float32)
    caps, labels = [], []
    for seg in spec["segments"]:
        mp3, chars, s0, s1 = cb.tts(seg["text"])
        x = cb.decode(mp3)
        i0 = int(t * sr)
        voice[i0:i0 + len(x)] += x
        dur = len(x) / sr
        if seg["role"] != "hook":
            for c in cb.chunks(seg["text"], s0, s1, max_words=8 if seg["role"] != "verse" else 9):
                caps.append(dict(c, t0=t + c["t0"], t1=t + c["t1"], role=seg["role"]))
        if seg.get("label"):
            labels.append((t, t + dur, seg["label"]))
        if seg["role"] == "hook":
            hook_end = t + dur
        t += dur + GAP.get(seg["role"], 0.35)
    total = t + 2.6
    voice = voice[:int(total * sr)]
    # caption end = next caption start (or own end + 0.4)
    for a, b in zip(caps, caps[1:]):
        a["t1"] = b["t0"] if b["t0"] - a["t1"] < 1.6 else a["t1"] + 0.3
    caps[-1]["t1"] += 0.5
    json.dump(caps, open(spec["out"].replace(".mp4", "_caps.json"), "w"), indent=0)
    vw = os.path.join(work, "voice.wav"); cb.write_wav(vw, voice)
    mus = cb.music_loop(os.path.join(cb.CACHE, f"loop_{spec['music_key']}_{spec['seed']}.wav"),
                        seed=spec["seed"], key=spec["music_key"])
    audio = os.path.join(work, "mix.m4a")
    cb.mix(vw, mus, audio, total, music_db=-19, lufs=-15)

    # ---- visuals
    BW, BH = int(W * 1.06), int(H * 1.06)
    base = cb.paint(spec["scene"], BW, BH, seed=spec["seed"])
    parts = cb.Particles(W, H, st["parts"][0], spec["seed"], color=st["parts"][1],
                         size=(3, 9) if spec["template"] == "C" else (4, 14))
    # header
    hdr = Image.new("RGBA", (W, 120), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hdr)
    hf = cb.font("serif", 46)
    label = "Christ's Blessings"
    tw = hd.textlength(label, font=hf)
    x0 = (W - tw) / 2 + 18
    col = st["sub"] + (230,)
    hd.line([(x0 - 34, 30), (x0 - 34, 82)], fill=col, width=4)
    hd.line([(x0 - 50, 46), (x0 - 18, 46)], fill=col, width=4)
    hd.text((x0, 26), label, font=hf, fill=col)
    hdr = cb.Faded(hdr)
    SH = spec["template"] != "E"
    # cover title
    cover = cb.text_block(W, " ".join(spec["cover"]), "serif_bold", 150, st["txt"], W - 160, max_lines=3, shadow=SH)
    cover = cb.Faded(cover)
    cap_imgs = []

    for c in caps:
        if c["role"] == "verse":
            im = cb.text_block(W, c["text"], "serif_italic", 82, st["verse"], W - 170, max_lines=4, shadow=SH)
        else:
            im = cb.text_block(W, c["text"], "serif", 80, st["txt"], W - 170, max_lines=4, shadow=SH)
        cap_imgs.append(cb.Faded(im))
    lab_imgs = {l[2]: cb.Faded(cb.text_block(W, "— " + l[2] + " (KJV) —", "body_italic", 40, st["sub"], W - 200, shadow=SH))
                for l in labels}
    end1 = cb.Faded(cb.text_block(W, "Christ's Blessings", "serif_bold", 96, st["txt"], W - 160, shadow=SH))
    end2 = cb.Faded(cb.text_block(W, "A new prayer every morning", "body_italic", 44, st["sub"], W - 160, shadow=SH))

    def fade(t, a, b, f=0.35):
        if t < a or t > b:
            return 0.0
        return min(1, (t - a) / f, (b - t) / f)

    out = spec["out"]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    p = subprocess.Popen(cb.encode_cmd(out, W, H, FPS, audio, crf=20, preset="veryfast"), stdin=subprocess.PIPE)
    n = int(total * FPS)
    for fi in range(n):
        tt = fi / FPS
        k = tt / total
        ox, oy = int((BW - W) * (0.2 + 0.6 * k)), int((BH - H) * (0.7 - 0.5 * k))
        fr = base.crop((ox, oy, ox + W, oy + H))
        parts.draw(fr, tt)
        if spec["scene"] == "candle":
            cb.flame(fr, tt, W, H)
        hh = hdr.at(1.0); fr.paste(hh, (0, 70), hh)
        a = fade(tt, -1, hook_end + 0.25, 0.4)
        if a > 0:
            im = cover.at(a)
            fr.paste(im, (0, int(H * 0.40 - im.height / 2)), im)
        for c, im in zip(caps, cap_imgs):
            a = fade(tt, c["t0"] - 0.08, c["t1"], 0.18)
            if a > 0:
                ii = im.at(a)
                fr.paste(ii, (0, int(H * 0.47 - ii.height / 2)), ii)
        for l0, l1, lab in labels:
            a = fade(tt, l0, l1 + 0.3, 0.3)
            if a > 0:
                ii = lab_imgs[lab].at(a)
                fr.paste(ii, (0, int(H * 0.66)), ii)
        a = fade(tt, total - 2.4, total + 1, 0.5)
        if a > 0:
            fr.paste(end1.at(a), (0, int(H * 0.40)), end1.at(a))
            fr.paste(end2.at(a), (0, int(H * 0.40) + 130), end2.at(a))
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()
    print(json.dumps({"out": out, "duration": round(total, 2)}))


if __name__ == "__main__":
    main(sys.argv[1])
