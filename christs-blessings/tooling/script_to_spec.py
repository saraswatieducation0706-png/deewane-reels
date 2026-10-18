"""Convert a long-video script (.txt) into a render_long spec.

Format:
  ## Chapter title | scene [| music_only=SECONDS | dim=0.45 | card=Text | rain]
  Spoken paragraph ... [pause] more ... [long pause]
  A paragraph ending with "| scene" switches scenery from that paragraph on (no new chapter).
Usage: python3 script_to_spec.py script.txt out.mp4 '<extra json>' > spec.json
"""
import json, re, sys
PAUSE = {"[pause]": 6, "[long pause]": 10}
src, out = sys.argv[1], sys.argv[2]
extra = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
chapters = []
for line in open(src, encoding="utf-8"):
    line = line.strip()
    if not line:
        continue
    if line.startswith("## "):
        parts = [p.strip() for p in line[3:].split("|")]
        ch = {"title": parts[0], "scene": parts[1], "items": []}
        for p in parts[2:]:
            if p == "rain":
                ch["rain"] = True
            elif "=" in p:
                k, v = p.split("=", 1)
                ch[k] = float(v) if k in ("music_only", "dim") else v
        if ch.get("scene") == "storm":
            ch["rain"] = True
        chapters.append(ch)
        continue
    m = re.search(r"\|\s*([a-z_]+)\s*$", line)
    if m:
        line = line[:m.start()].strip()
        scene = m.group(1)
        chapters.append({"title": None, "scene": scene, "items": [], "rain": scene == "storm"})
    for tok in re.split(r"(\[pause\]|\[long pause\])", line):
        tok = tok.strip()
        if not tok:
            continue
        if tok in PAUSE:
            chapters[-1]["items"].append({"pause": PAUSE[tok]})
        else:
            chapters[-1]["items"].append({"say": tok})
for ch in chapters:
    if "music_only" in ch:
        del ch["items"]
spec = dict({"out": out, "fps": 24, "seed": 11, "music_key": "D", "chapters": chapters}, **extra)
print(json.dumps(spec, indent=1, ensure_ascii=False))
