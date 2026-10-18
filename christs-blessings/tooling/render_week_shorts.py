"""Render Shorts listed in a week's shorts.json: python3 render_week_shorts.py <week_dir> [id ...]"""
import json, os, sys, subprocess
wk = os.path.abspath(sys.argv[1]); only = set(sys.argv[2:])
for s in json.load(open(os.path.join(wk, "shorts.json"))):
    if only and s["id"] not in only:
        continue
    s = dict(s, out=os.path.join(wk, "out", f"{s['date']}_{s['id']}.mp4"))
    sp = os.path.join(wk, "out", f"{s['id']}_spec.json")
    os.makedirs(os.path.dirname(sp), exist_ok=True)
    json.dump(s, open(sp, "w"))
    subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "render_short.py"), sp], check=True)
