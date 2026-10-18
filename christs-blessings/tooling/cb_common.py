"""Shared helpers for Christ's Blessings videos: TTS, music, scenery, captions.

All visuals are drawn procedurally (no stock footage, no film stills) and the
music is synthesised here, so every video is original and copyright-clean.
"""
import base64, hashlib, json, math, os, random, subprocess, urllib.request, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
CFG = json.load(open(os.path.join(HERE, "config.json")))
CACHE = os.path.expanduser("~/.cache/cb_tts")
os.makedirs(CACHE, exist_ok=True)


def font(name, size):
    files = {
        "serif": "cormorant-garamond-latin-600-normal.ttf",
        "serif_bold": "cormorant-garamond-latin-700-normal.ttf",
        "serif_italic": "cormorant-garamond-latin-500-italic.ttf",
        "body": "lora-latin-400-normal.ttf",
        "body_italic": "lora-latin-500-italic.ttf",
        "body_bold": "lora-latin-600-normal.ttf",
    }
    return ImageFont.truetype(os.path.join(FONTS, files[name]), size)


# ---------------------------------------------------------------- TTS
def spoken(text):
    """Same-length substitutions so caption char indices still line up."""
    return text.replace("LORD", "Lord")


def tts(text, speed=None):
    """Return (mp3_path, chars, starts, ends) for the spoken version of text."""
    key = os.environ["XI"]
    speed = speed or CFG["speed"]
    say = spoken(text)
    h = hashlib.sha1(f"{CFG['voice_id']}|{CFG['tts_model']}|{speed}|{say}".encode()).hexdigest()[:16]
    mp3, js = os.path.join(CACHE, h + ".mp3"), os.path.join(CACHE, h + ".json")
    if not os.path.exists(mp3):
        body = json.dumps({
            "text": say, "model_id": CFG["tts_model"],
            "voice_settings": {"stability": 0.62, "similarity_boost": 0.8, "style": 0.12,
                               "use_speaker_boost": True, "speed": speed},
        }).encode()
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{CFG['voice_id']}/with-timestamps"
            "?output_format=mp3_44100_128",
            data=body, headers={"xi-api-key": key, "Content-Type": "application/json"})
        for attempt in range(3):
            try:
                d = json.load(urllib.request.urlopen(req, timeout=180))
                break
            except Exception:
                if attempt == 2:
                    raise
        open(mp3, "wb").write(base64.b64decode(d["audio_base64"]))
        json.dump(d["alignment"], open(js, "w"))
    a = json.load(open(js))
    return mp3, a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]


def decode(path, sr=44100):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(sr), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def write_wav(path, x, sr=44100):
    x = np.clip(x, -1, 1)
    if x.ndim == 1:
        x = x[:, None]
    with wave.open(path, "wb") as w:
        w.setnchannels(x.shape[1]); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def chunks(display, starts, ends, max_words=9):
    """Split display text into caption chunks timed from char alignment."""
    words, i = [], 0
    for part in display.split(" "):
        if part:
            words.append((part, i, i + len(part) - 1))
        i += len(part) + 1
    out, cur = [], []
    for w in words:
        cur.append(w)
        end_punct = w[0][-1] in ".!?;:" or w[0].endswith('."') or w[0].endswith('?"')
        if len(cur) >= max_words or (end_punct and len(cur) >= 3) or (w[0][-1] == "," and len(cur) >= max_words - 3):
            out.append(cur); cur = []
    if cur:
        if out and len(cur) <= 2:
            out[-1] += cur
        else:
            out.append(cur)
    res = []
    n = len(starts)
    for c in out:
        a, b = min(c[0][1], n - 1), min(c[-1][2], n - 1)
        res.append({"text": " ".join(x[0] for x in c), "t0": starts[a], "t1": ends[b]})
    return res


# ---------------------------------------------------------------- music
NOTE = {"C": 261.63, "D": 293.66, "Eb": 311.13, "E": 329.63, "F": 349.23, "G": 392.0, "A": 440.0, "Bb": 466.16}
PROGS = [[0, 9, 5, 7], [0, 5, 9, 7], [9, 5, 0, 7], [0, 7, 9, 5]]  # semitone roots: I vi IV V etc.


def music_loop(path, seed=1, key="D", chord_s=12.0, sr=44100, brightness=1.0):
    """Seamless ambient pad loop (original, synthesised). Writes stereo wav."""
    if os.path.exists(path):
        return path
    rng = np.random.default_rng(seed)
    prog = PROGS[seed % len(PROGS)]
    L = int(sr * chord_s * len(prog))
    t = np.arange(L) / sr
    out = np.zeros((L, 2), np.float32)
    base = NOTE[key] / 2
    for ci, r in enumerate(prog):
        minor = r == 9
        tones = [0, 3 if minor else 4, 7, 12, 14 if not minor else 15]
        center = ci * chord_s + chord_s / 2
        # periodic raised-cosine window of width 2*chord_s, wrapped
        d = ((t - center + L / sr / 2) % (L / sr)) - L / sr / 2
        env = np.where(np.abs(d) < chord_s, 0.5 * (1 + np.cos(np.pi * d / chord_s)), 0).astype(np.float32)
        for k, semi in enumerate(tones):
            f = base * 2 ** ((r + semi) / 12)
            amp = [0.55, 0.38, 0.4, 0.22, 0.12 * brightness][k]
            for ch, det in ((0, 0.9985), (1, 1.0015)):
                ph = rng.uniform(0, 2 * np.pi)
                s = np.sin(2 * np.pi * f * det * t + ph) + 0.18 * np.sin(4 * np.pi * f * det * t + ph)
                out[:, ch] += (amp * env * s).astype(np.float32)
        fb = base / 2 * 2 ** (r / 12)  # soft bass
        out += (0.35 * env * np.sin(2 * np.pi * fb * t))[:, None].astype(np.float32)
    # gentle chimes (pentatonic), periodic placement
    penta = [0, 2, 4, 7, 9]
    for _ in range(int(len(prog) * 1.5)):
        st = rng.uniform(0, L / sr)
        f = NOTE[key] * 2 * 2 ** (penta[rng.integers(5)] / 12)
        dt = (t - st) % (L / sr)
        e = np.exp(-dt / 1.6) * (dt < 8)
        out[:, int(rng.integers(2))] += (0.09 * brightness * e * np.sin(2 * np.pi * f * dt)).astype(np.float32)
    # circular reverb via FFT convolution with decaying noise
    ir_len = int(sr * 2.2)
    for ch in range(2):
        ir = np.zeros(L, np.float32)
        ir[:ir_len] = rng.standard_normal(ir_len) * np.exp(-np.arange(ir_len) / (sr * 0.55))
        ir[0] = 6.0
        wet = np.fft.irfft(np.fft.rfft(out[:, ch]) * np.fft.rfft(ir), L)
        out[:, ch] = 0.55 * out[:, ch] + 0.45 * wet / (np.abs(wet).max() + 1e-9) * np.abs(out[:, ch]).max()
    # one-pole lowpass for warmth
    a = math.exp(-2 * math.pi * 2600 / sr)
    from scipy.signal import lfilter  # noqa
    out = lfilter([1 - a], [1, -a], out, axis=0).astype(np.float32)
    out /= np.abs(out).max() + 1e-9
    write_wav(path, out * 0.8, sr)
    return path


def mix(voice_wav, music_wav, out_m4a, duration, music_db=-21, fade_out=2.5, lufs=-16):
    """Loop music under voice with ducking, fade, loudness-normalise."""
    fc = (f"[1:a]volume={music_db}dB,atrim=0:{duration:.3f},afade=t=in:d=2,"
          f"afade=t=out:st={max(0, duration - fade_out):.3f}:d={fade_out}[m];"
          f"[0:a]aformat=channel_layouts=stereo,asplit[v][sc];"
          f"[m][sc]sidechaincompress=threshold=0.03:ratio=4:attack=60:release=900[md];"
          f"[v][md]amix=inputs=2:duration=longest:normalize=0,"
          f"atrim=0:{duration:.3f},loudnorm=I={lufs}:TP=-1.5:LRA=11[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", voice_wav, "-stream_loop", "-1", "-i", music_wav,
                    "-filter_complex", fc, "-map", "[a]", "-ar", "44100", "-c:a", "aac", "-b:a", "160k",
                    out_m4a], check=True)


# ---------------------------------------------------------------- scenery
def lerp(a, b, x):
    return a + (b - a) * x


def vgrad(W, H, stops):
    y = np.linspace(0, 1, H)[:, None]
    img = np.zeros((H, 1, 3), np.float32)
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        m = (y >= p0) & (y <= p1)
        x = np.clip((y - p0) / max(p1 - p0, 1e-6), 0, 1)
        x = x * x * (3 - 2 * x)
        for k in range(3):
            img[:, :, k] = np.where(m, lerp(c0[k], c1[k], x), img[:, :, k])
    return np.repeat(img, W, axis=1)


def glow(arr, cx, cy, r, color, strength=1.0, power=2.0):
    H, W, _ = arr.shape
    yy, xx = np.ogrid[:H, :W]
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
    g = np.clip(1 - d, 0, 1) ** power * strength
    for k in range(3):
        arr[:, :, k] = arr[:, :, k] + (color[k] - arr[:, :, k]) * np.clip(g, 0, 1)
    return arr


def ridge(W, rng, base, amp, octaves=4):
    x = np.linspace(0, 1, W)
    y = np.full(W, base, np.float32)
    for o in range(octaves):
        f = 1.5 * 2 ** o
        y += amp / (1.8 ** o) * np.sin(2 * np.pi * (f * x + rng.uniform(0, 1)))
    return y


def fill_below(arr, ys, color, alpha=1.0):
    H, W, _ = arr.shape
    yy = np.arange(H)[:, None]
    m = (yy >= ys[None, :]).astype(np.float32) * alpha
    for k in range(3):
        arr[:, :, k] = arr[:, :, k] * (1 - m) + color[k] * m
    return arr


def noise_field(W, H, rng, scale=8, blur=3):
    small = Image.fromarray((rng.random((max(2, H // scale), max(2, W // scale))) * 255).astype(np.uint8))
    return np.asarray(small.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(blur)), np.float32) / 255


def to_img(arr):
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def vignette(arr, strength=0.45):
    H, W, _ = arr.shape
    yy, xx = np.ogrid[:H, :W]
    d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 1.4142
    arr *= (1 - strength * np.clip(d, 0, 1) ** 2)[:, :, None]
    return arr


def boat(d, cx, cy, s, color):
    d.polygon([(cx - 1.0 * s, cy), (cx + 1.0 * s, cy), (cx + 0.75 * s, cy + 0.28 * s), (cx - 0.75 * s, cy + 0.28 * s)], fill=color)
    d.line([(cx, cy), (cx, cy - 1.3 * s)], fill=color, width=max(2, int(s * 0.05)))
    d.polygon([(cx + 0.03 * s, cy - 1.25 * s), (cx + 0.03 * s, cy - 0.12 * s), (cx + 0.7 * s, cy - 0.12 * s)], fill=color)


def paint(scene, W, H, seed=0, warm=0.0):
    """Return a PIL RGB background for a named scene."""
    rng = np.random.default_rng(seed)
    hz = int(H * (0.58 if H > W else 0.6))
    if scene in ("dawn_lake", "sunrise_lake", "calm_dawn", "galilee_dusk", "night_lake"):
        if scene == "night_lake":
            sky = [(0, (8, 12, 32)), (0.45, (18, 28, 62)), (hz / H, (38, 52, 92))]
        elif scene == "galilee_dusk":
            sky = [(0, (34, 38, 78)), (0.35, (92, 72, 118)), (0.5, (196, 120, 110)), (hz / H, (238, 170, 120))]
        elif scene == "sunrise_lake":
            sky = [(0, (70, 110, 170)), (0.3, (150, 160, 190)), (0.48, (245, 196, 150)), (hz / H, (255, 214, 150))]
        else:
            sky = [(0, (52, 74, 128)), (0.32, (128, 132, 172)), (0.48, (232, 178, 160)), (hz / H, (252, 206, 158))]
        a = vgrad(W, H, sky + [(1.0, sky[-1][1])])
        sun_c = (255, 236, 190) if scene != "night_lake" else (230, 236, 255)
        sx, sy = W * 0.5, hz - H * 0.035
        a = glow(a, sx, sy, W * (0.9 if scene != "night_lake" else 0.25), sun_c, 0.55 if scene != "night_lake" else 0.25)
        a = glow(a, sx, sy, W * 0.08, sun_c, 1.0, 1.2)
        if scene == "night_lake":
            for _ in range(int(W * H / 2600)):
                x, y = rng.integers(0, W), rng.integers(0, int(hz * 0.95))
                b = rng.uniform(120, 255)
                a[y, x] = (b, b, min(255, b + 20))
        hills = (40, 44, 70) if scene != "night_lake" else (10, 14, 30)
        if scene == "galilee_dusk":
            hills = (58, 44, 70)
        a = fill_below(a, ridge(W, rng, hz - H * 0.03, H * 0.018), [c * 1.25 for c in hills], 1.0)
        a = fill_below(a, ridge(W, rng, hz - H * 0.012, H * 0.01), hills, 1.0)
        # water: mirrored sky, darker, with streaks
        refl = a[max(0, 2 * hz - H):hz][::-1]
        water = refl * 0.62 + np.array([10, 18, 34]) * 0.38
        hh = H - hz
        if water.shape[0] < hh:
            water = np.concatenate([water, np.repeat(water[-1:], hh - water.shape[0], 0)], 0)
        a[hz:] = water[:hh]
        small = rng.random((max(2, hh // 3), max(2, W // 60)))
        streak = np.asarray(Image.fromarray((small * 255).astype(np.uint8)).resize((W, hh), Image.BICUBIC), np.float32) / 255
        depth = np.linspace(0.6, 1.0, hh)[:, None]
        a[hz:] *= (0.94 + 0.12 * streak * depth)[:, :, None]
        a = glow(a, sx, hz + hh * 0.25, W * 0.12, sun_c, 0.55, 1.5)
        img = to_img(vignette(a, 0.35))
        if scene in ("galilee_dusk", "calm_dawn"):
            d = ImageDraw.Draw(img)
            boat(d, W * 0.36, hz + hh * 0.12, W * 0.06, (28, 24, 40))
        return img
    if scene == "storm":
        a = vgrad(W, H, [(0, (22, 26, 34)), (0.5, (48, 56, 66)), (1, (20, 26, 32))])
        n = noise_field(W, H, rng, scale=40, blur=18)
        a = a * (0.75 + 0.5 * n[:, :, None])
        img = to_img(a)
        d = ImageDraw.Draw(img)
        for i, (base, amp, col) in enumerate([(0.6, 0.014, (40, 52, 62)), (0.68, 0.02, (28, 38, 48)), (0.8, 0.028, (16, 22, 30))]):
            x = np.linspace(0, 1, W)
            ys = H * base + sum(H * amp / (1.6 ** o) * np.sin(2 * np.pi * ((6 + 5 * o) * x + rng.uniform(0, 1))) for o in range(5))
            ys = ys - H * amp * 0.8 * np.abs(np.sin(2 * np.pi * (9 * x + rng.uniform(0, 1))))
            pts = [(x, ys[x]) for x in range(0, W, 4)] + [(W, H), (0, H)]
            d.polygon(pts, fill=col)
            if i == 1:
                boat(d, W * 0.48, ys[int(W * 0.48)] - W * 0.02, W * 0.07, (8, 10, 14))
        return img.filter(ImageFilter.GaussianBlur(1.2))
    if scene in ("hills_sunset", "forest_fork"):
        if scene == "hills_sunset":
            a = vgrad(W, H, [(0, (70, 56, 110)), (0.3, (176, 104, 128)), (0.5, (246, 170, 112)), (1, (246, 190, 130))])
            a = glow(a, W * 0.5, H * 0.46, W * 0.9, (255, 224, 170), 0.5)
            a = glow(a, W * 0.5, H * 0.46, W * 0.09, (255, 240, 200), 1.0, 1.2)
            cols = [(160, 96, 120), (118, 70, 104), (80, 48, 84), (48, 30, 58)]
            for i, c in enumerate(cols):
                a = fill_below(a, ridge(W, rng, H * (0.5 + 0.09 * i), H * 0.03, 3), c)
            img = to_img(vignette(a, 0.3))
            d = ImageDraw.Draw(img, "RGBA")
            pts_l, pts_r = [], []
            for k in range(60):
                y = H * 0.56 + (H * 0.44) * (k / 59) ** 1.6
                w = 4 + (W * 0.32) * (k / 59) ** 1.8
                x = W * 0.5 + W * 0.12 * math.sin(k / 59 * 4.2) * (k / 59)
                pts_l.append((x - w / 2, y)); pts_r.append((x + w / 2, y))
            d.polygon(pts_l + pts_r[::-1], fill=(250, 200, 150, 120))
            return img
        a = vgrad(W, H, [(0, (120, 150, 160)), (0.45, (186, 200, 196)), (1, (60, 80, 78))])
        a = glow(a, W * 0.28, H * 0.42, W * 0.7, (255, 226, 170), 0.6)
        a = fill_below(a, np.full(W, H * 0.6), (52, 66, 60))
        a[int(H * 0.6):] *= np.linspace(1.0, 0.7, H - int(H * 0.6))[:, None, None]
        img = to_img(a)
        d = ImageDraw.Draw(img, "RGBA")
        for layer in range(4):
            col = [(96, 120, 120, 150), (70, 92, 92, 190), (46, 64, 64, 230), (26, 38, 38, 255)][layer]
            y0 = H * (0.48 + 0.08 * layer)
            for _ in range(10 + layer * 3):
                x = rng.uniform(-50, W + 50)
                h = H * (0.12 + 0.06 * layer) * rng.uniform(0.8, 1.2)
                w = h * 0.28
                for tier in range(4):
                    ty = y0 - h + tier * h * 0.22
                    d.polygon([(x, ty), (x - w * (0.5 + tier * 0.18), ty + h * 0.35), (x + w * (0.5 + tier * 0.18), ty + h * 0.35)], fill=col)
                d.rectangle([x - w * 0.05, y0 - h * 0.1, x + w * 0.05, y0 + h * 0.04], fill=col)
            fog = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            fd = ImageDraw.Draw(fog)
            fd.rectangle([0, int(y0 - H * 0.04), W, int(y0 + H * 0.06)], fill=(220, 226, 220, 70))
            img = Image.alpha_composite(img.convert("RGBA"), fog.filter(ImageFilter.GaussianBlur(H * 0.02))).convert("RGB")
            d = ImageDraw.Draw(img, "RGBA")
        # forked path
        cx, top = W * 0.5, H * 0.66
        d.polygon([(cx - W * 0.3, H), (cx + W * 0.3, H), (cx + W * 0.03, H * 0.8), (cx - W * 0.03, H * 0.8)], fill=(200, 184, 150, 200))
        d.polygon([(cx - W * 0.04, H * 0.8), (cx - W * 0.005, H * 0.8), (cx - W * 0.2, top), (cx - W * 0.22, top)], fill=(240, 214, 160, 210))
        d.polygon([(cx + W * 0.005, H * 0.8), (cx + W * 0.04, H * 0.8), (cx + W * 0.2, top), (cx + W * 0.18, top)], fill=(150, 150, 136, 170))
        return img.filter(ImageFilter.GaussianBlur(0.8))
    if scene == "dark_gold":
        a = vgrad(W, H, [(0, (10, 12, 24)), (1, (16, 14, 22))])
        a = glow(a, W * 0.5, H * 0.45, max(W, H) * 0.55, (70, 54, 30), 0.8, 1.6)
        return to_img(vignette(a, 0.5))
    if scene == "candle":
        a = vgrad(W, H, [(0, (18, 12, 10)), (1, (34, 22, 16))])
        a = glow(a, W * 0.5, H * 0.7, max(W, H) * 0.6, (120, 70, 30), 0.7, 1.5)
        img = to_img(vignette(a, 0.5))
        bok = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        bd = ImageDraw.Draw(bok)
        for _ in range(22):
            r = rng.uniform(W * 0.02, W * 0.07)
            x, y = rng.uniform(0, W), rng.uniform(0, H * 0.6)
            bd.ellipse([x - r, y - r, x + r, y + r], fill=(255, 190, 110, int(rng.uniform(18, 45))))
        img = Image.alpha_composite(img.convert("RGBA"), bok.filter(ImageFilter.GaussianBlur(W * 0.006))).convert("RGB")
        d = ImageDraw.Draw(img)
        cw, ch = W * 0.11, H * 0.16 if H > W else H * 0.24
        cx, cy = W * 0.5, H * (0.78 if H > W else 0.72)
        d.rounded_rectangle([cx - cw / 2, cy, cx + cw / 2, cy + ch], radius=int(cw * 0.08), fill=(236, 222, 200))
        d.rectangle([cx - cw / 2, cy, cx - cw / 2 + cw * 0.18, cy + ch], fill=(214, 198, 176))
        d.line([(cx, cy), (cx, cy - cw * 0.15)], fill=(40, 30, 24), width=max(2, int(cw * 0.03)))
        return img
    if scene == "parchment":
        a = vgrad(W, H, [(0, (246, 238, 222)), (1, (232, 218, 192))])
        n = noise_field(W, H, rng, scale=3, blur=1)
        a = a * (0.96 + 0.06 * n[:, :, None])
        a = glow(a, W * 0.5, 0, max(W, H) * 0.8, (255, 250, 236), 0.6)
        img = to_img(vignette(a, 0.28))
        d = ImageDraw.Draw(img, "RGBA")
        cx, cy, s = W * 0.5, H * (0.25 if H > W else 0.2), min(W, H) * 0.08
        for k in range(9):  # light rays
            ang = math.radians(-90 + (k - 4) * 14)
            d.polygon([(cx, cy), (cx + math.cos(ang - 0.05) * W, cy + math.sin(ang - 0.05) * W * -1 * -1 + W),
                       (cx + math.cos(ang + 0.05) * W, cy + W)], fill=(255, 236, 190, 14))
        gold = (176, 138, 72)
        lw = max(3, int(s * 0.07))
        d.line([(cx, cy - s), (cx, cy + s * 1.15)], fill=gold, width=lw)
        d.line([(cx - s * 0.62, cy - s * 0.35), (cx + s * 0.62, cy - s * 0.35)], fill=gold, width=lw)
        return img
    raise ValueError(scene)


# ---------------------------------------------------------------- animation
class Particles:
    def __init__(self, W, H, n, seed, color=(255, 236, 196), rise=True, size=(4, 16)):
        rng = np.random.default_rng(seed)
        self.W, self.H, self.rise = W, H, rise
        self.p = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(*size), rng.uniform(8, 30), rng.uniform(0, 6.28))
                  for _ in range(n)]
        self.sprites = {}
        for r in sorted({int(x[2]) for x in self.p}):
            m = Image.new("L", (r * 6, r * 6), 0)
            ImageDraw.Draw(m).ellipse([r * 2, r * 2, r * 4, r * 4], fill=200)
            s = Image.new("RGBA", m.size, color + (0,))
            s.putalpha(m.filter(ImageFilter.GaussianBlur(r * 0.8)))
            self.sprites[r] = s

    def draw(self, img, t):
        for x, y, r, v, ph in self.p:
            yy = (y - v * t) % (self.H + 60) - 30 if self.rise else y
            xx = x + 14 * math.sin(t * 0.4 + ph)
            tw = 0.5 + 0.5 * math.sin(t * 1.3 + ph)
            if tw < 0.15:
                continue
            s = self.sprites[int(r)]
            if tw < 0.9:
                s = s.copy(); s.putalpha(s.getchannel("A").point(lambda a, k=tw: int(a * k)))
            img.paste(s, (int(xx - s.width / 2), int(yy - s.height / 2)), s)


class Rain:
    def __init__(self, W, H, n=260, seed=3):
        rng = np.random.default_rng(seed)
        self.W, self.H = W, H
        self.d = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(700, 1100), rng.uniform(20, 50)) for _ in range(n)]

    def draw(self, img, t):
        dr = ImageDraw.Draw(img, "RGBA")
        for x, y, v, l in self.d:
            yy = (y + v * t) % self.H
            xx = (x - 0.25 * v * t) % self.W
            dr.line([(xx, yy), (xx - l * 0.25, yy - l)], fill=(190, 205, 220, 70), width=2)
        if (t % 23) < 0.12 or (t % 37) < 0.08:
            dr.rectangle([0, 0, self.W, self.H], fill=(220, 230, 255, 40))


def flame(img, t, W, H):
    cx, cy = W * 0.5, H * (0.78 if H > W else 0.72)
    cw = W * 0.11
    f = 1 + 0.08 * math.sin(t * 9.1) + 0.05 * math.sin(t * 13.7)
    g = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(g)
    r = cw * 1.6 * f
    d.ellipse([cx - r, cy - cw * 0.5 - r, cx + r, cy - cw * 0.5 + r], fill=(255, 170, 70, 46))
    fw, fh = cw * 0.16, cw * 0.55 * f
    d.ellipse([cx - fw, cy - cw * 0.12 - fh, cx + fw, cy - cw * 0.08], fill=(255, 214, 130, 235))
    d.ellipse([cx - fw * 0.45, cy - cw * 0.12 - fh * 0.55, cx + fw * 0.45, cy - cw * 0.1], fill=(255, 250, 225, 250))
    g = g.filter(ImageFilter.GaussianBlur(cw * 0.04))
    img.paste(g, (0, 0), g)


# ---------------------------------------------------------------- text
def wrap(text, fnt, maxw, draw):
    lines, cur = [], ""
    for w in text.split():
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(W, text, fname, size, color, maxw, shadow=True, align="center", line_gap=1.18, min_size=30, max_lines=5):
    """RGBA image with wrapped, shadowed text; shrinks to fit max_lines."""
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    while True:
        fnt = font(fname, size)
        lines = wrap(text, fnt, maxw, tmp)
        if len(lines) <= max_lines or size <= min_size:
            break
        size = int(size * 0.92)
    lh = int(size * line_gap)
    h = lh * len(lines) + int(size * 0.5)
    img = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=fnt)
        x = (W - tw) / 2 if align == "center" else (W - maxw) / 2
        d.text((x, i * lh), ln, font=fnt, fill=color)
    if shadow:
        pad = int(size * 0.9)
        big = Image.new("RGBA", (W, h + 2 * pad), (0, 0, 0, 0))
        big.paste(img, (0, pad))
        A = big.getchannel("A")
        veil = A.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(size * 0.55)).point(lambda a: min(255, int(a * 1.6)))
        tight = A.filter(ImageFilter.GaussianBlur(size * 0.1))
        sh = Image.fromarray(np.maximum(np.asarray(veil, np.float32) * 0.55, np.asarray(tight, np.float32) * 0.9).astype(np.uint8))
        out = Image.new("RGBA", big.size, (8, 10, 22, 0))
        out.putalpha(sh)
        out.alpha_composite(big)
        return out
    return img


class Faded:
    """Caches alpha-scaled copies of an RGBA overlay."""
    def __init__(self, img):
        self.img, self.cache = img, {}

    def at(self, a):
        k = round(max(0, min(1, a)) * 10)
        if k not in self.cache:
            im = self.img.copy()
            im.putalpha(im.getchannel("A").point(lambda v: int(v * k / 10)))
            self.cache[k] = im
        return self.cache[k]


def encode_cmd(out, W, H, fps, audio, crf=21, preset="medium", tune=None, maxrate=None):
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps),
           "-i", "-", "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
           "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", "-shortest"]
    if tune:
        cmd += ["-tune", tune]
    if maxrate:
        cmd += ["-maxrate", maxrate, "-bufsize", str(int(maxrate[:-1]) * 2) + "k"]
    return cmd + [out]
