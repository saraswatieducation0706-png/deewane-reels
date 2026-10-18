"""Render a Christ's Blessings long video (1920x1080) from a spec JSON.

Spec:
{
  "out": "/abs/long.mp4", "fps": 24, "seed": 11, "music_key": "D", "music_db": -20, "lufs": -18,
  "intro": "Fall Asleep in God's Peace",            # title card for the first seconds
  "subtitles": "normal" | "dim",
  "chapters": [
    {"title": "Settling in", "scene": "night_lake",
     "items": [{"say": "Hello, and welcome..."}, {"pause": 6}, ...]},
    {"title": null, "scene": "night_lake", "music_only": 780, "dim": 0.55, "card": "Rest now"}
  ]
}
Writes <out>, plus <out>_chapters.txt with YouTube chapter timestamps.
"""
import json, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image
import cb_common as cb

W, H = 1920, 1080


def ts(sec):
    sec = int(sec)
    return f"{sec // 3600}:{sec % 3600 // 60:02d}:{sec % 60:02d}" if sec >= 3600 else f"{sec // 60}:{sec % 60:02d}"


def main(spec_path):
    spec = json.load(open(spec_path))
    fps, sr = spec.get("fps", 24), 44100
    speed = cb.CFG.get("speed_long", 0.9)
    work = tempfile.mkdtemp(prefix="cbl_")
    # ---- audio timeline
    clips, caps, chap = [], [], []
    t = 4.0  # intro card
    for ci, ch in enumerate(spec["chapters"]):
        c0 = t if ci else 0.0
        chap.append({"t0": c0, "title": ch.get("title"), "scene": ch["scene"], "dim": ch.get("dim", 0),
                     "card": ch.get("card"), "rain": ch.get("rain", False)})
        if ch.get("title") and ci:
            t += 2.5
        if "music_only" in ch:
            t += ch["music_only"]
            continue
        for it in ch["items"]:
            if "pause" in it:
                t += it["pause"]
                continue
            mp3, chars, s0, s1 = cb.tts(it["say"], speed=speed)
            x = cb.decode(mp3)
            clips.append((t, x))
            for c in cb.chunks(it["say"], s0, s1, max_words=12):
                caps.append(dict(c, t0=t + c["t0"], t1=t + c["t1"]))
            t += len(x) / sr + 0.9
    total = t + 4.0
    for i, ch in enumerate(chap):
        ch["t1"] = chap[i + 1]["t0"] if i + 1 < len(chap) else total
    for a, b in zip(caps, caps[1:]):
        a["t1"] = b["t0"] if b["t0"] - a["t1"] < 1.2 else a["t1"] + 0.5
    caps[-1]["t1"] += 0.6
    voice = np.zeros(int(total * sr) + 1, np.float32)
    for t0, x in clips:
        i0 = int(t0 * sr); voice[i0:i0 + len(x)] += x[:len(voice) - i0]
    vw = os.path.join(work, "voice.wav"); cb.write_wav(vw, voice)
    mus = cb.music_loop(os.path.join(cb.CACHE, f"loop_{spec['music_key']}_{spec['seed']}_long.wav"),
                        seed=spec["seed"], key=spec["music_key"], chord_s=14.0, brightness=0.8)
    audio = os.path.join(work, "mix.m4a")
    cb.mix(vw, mus, audio, total, music_db=spec.get("music_db", -20), fade_out=8, lufs=spec.get("lufs", -18), abr="112k")

    # chapters file for the description
    out = spec["out"]; os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out.replace(".mp4", "_chapters.txt"), "w") as f:
        for ch in chap:
            if ch["title"]:
                f.write(f"{ts(ch['t0'])} {ch['title']}\n")

    # ---- visuals
    BW, BH = int(W * 1.05), int(H * 1.05)
    bases = {}
    for ch in chap:
        k = (ch["scene"], ch["dim"])
        if k not in bases:
            im = cb.paint(ch["scene"], BW, BH, seed=spec["seed"])
            if ch["dim"]:
                im = Image.blend(im, Image.new("RGB", im.size, (0, 0, 0)), ch["dim"])
            bases[k] = im
    dim_sub = spec.get("subtitles") == "dim"
    col = (236, 232, 222) if dim_sub else (255, 255, 255)
    cap_imgs = [cb.Faded(cb.text_block(W, c["text"], "serif", 50 if dim_sub else 58, col, W - 420, max_lines=2))
                for c in caps]
    intro = cb.Faded(cb.text_block(W, spec["intro"], "serif_bold", 104, (255, 255, 255), W - 360, max_lines=2))
    brand = cb.Faded(cb.text_block(W, "Christ's Blessings", "body_italic", 38, (240, 228, 200), W - 300))
    titles = {ch["title"]: cb.Faded(cb.text_block(W, ch["title"], "serif_italic", 84, (255, 240, 214), W - 360))
              for ch in chap if ch["title"]}
    cards = {ch["card"]: cb.Faded(cb.text_block(W, ch["card"], "serif_italic", 72, (230, 226, 240), W - 360))
             for ch in chap if ch["card"]}
    stars = cb.Particles(W, H, 16, spec["seed"], color=(255, 240, 210), rise=False, size=(3, 7))
    rain = cb.Rain(W, H)

    def fade(t, a, b, f=0.6):
        if t < a or t > b:
            return 0.0
        return min(1, (t - a) / f, (b - t) / f)

    def frame_for(ch, tt):
        b = bases[(ch["scene"], ch["dim"])]
        ox, oy = int((BW - W) * 0.5), int((BH - H) * 0.5)
        return b.crop((ox, oy, ox + W, oy + H))

    p = subprocess.Popen(cb.encode_cmd(out, W, H, fps, audio, crf=27, preset="veryfast", tune="stillimage",
                                       maxrate="1500k"), stdin=subprocess.PIPE)
    n = int(total * fps)
    ci = 0
    for fi in range(n):
        tt = fi / fps
        while ci + 1 < len(chap) and tt >= chap[ci + 1]["t0"]:
            ci += 1
        ch = chap[ci]
        fr = frame_for(ch, tt)
        if ci and tt - ch["t0"] < 2.0 and (chap[ci - 1]["scene"], chap[ci - 1]["dim"]) != (ch["scene"], ch["dim"]):
            fr = Image.blend(frame_for(chap[ci - 1], tt), fr, (tt - ch["t0"]) / 2.0)
        stars.draw(fr, tt)
        if ch["rain"]:
            rain.draw(fr, tt)
        a = fade(tt, -1, 4.6, 0.8)
        if a:
            im = intro.at(a); fr.paste(im, (0, int(H * 0.38 - im.height / 2)), im)
            im = brand.at(a); fr.paste(im, (0, int(H * 0.38 + 90)), im)
        if ch["title"] and ci:
            a = fade(tt, ch["t0"], ch["t0"] + 3.2, 0.6)
            if a:
                im = titles[ch["title"]].at(a); fr.paste(im, (0, int(H * 0.42 - im.height / 2)), im)
        if ch["card"]:
            a = fade(tt, ch["t0"] + 1, ch["t0"] + 12, 1.5)
            if a:
                im = cards[ch["card"]].at(a); fr.paste(im, (0, int(H * 0.42 - im.height / 2)), im)
        for c, im in zip(caps, cap_imgs):
            if c["t0"] - 0.2 <= tt <= c["t1"] + 0.3:
                a = fade(tt, c["t0"] - 0.15, c["t1"], 0.25) * (0.85 if dim_sub else 1)
                if a:
                    ii = im.at(a); fr.paste(ii, (0, int(H * 0.80 - ii.height / 2)), ii)
        a = fade(tt, total - 3.5, total + 1, 1.0)
        if a:
            im = brand.at(a); fr.paste(im, (0, int(H * 0.45)), im)
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()
    print(json.dumps({"out": out, "duration": round(total, 1)}))


if __name__ == "__main__":
    main(sys.argv[1])
