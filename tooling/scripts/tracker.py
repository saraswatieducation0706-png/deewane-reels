#!/usr/bin/env python3
"""Dedup helper for job notifications.

A record (covered or candidate) is a JSON object:
  {"org": "Oil and Natural Gas Corporation", "org_short": "ONGC", "advt_no": "ONGC/GT/2026/01",
   "post": "Graduate Trainee", "last_date": "2026-10-30", "official_url": "https://...",
   "status": "covered" | "skipped", "reason": "...", "run_date": "2026-10-07", "reel": "file.mp4"}

Commands
  tracker.py merge a.json b.json ...            -> prints one merged JSON list (all past run files)
  tracker.py check covered.json candidates.json -> prints JSON: {"new": [...], "dup": [[cand, matched_id], ...]}
                                                  (also collapses duplicates *within* the candidate list,
                                                   e.g. the same job found on 3 different websites)
"""
import json, re, sys

STOP = {"the", "of", "and", "for", "in", "limited", "ltd", "india", "indian", "corporation", "corp", "co",
        "company", "recruitment", "notification", "post", "posts", "vacancy", "vacancies", "advt", "no", "2025",
        "2026", "2027", "online", "apply", "form", "various", "&", "-"}

def toks(s):
    return {t for t in re.split(r"[^a-z0-9]+", (s or "").lower()) if t and t not in STOP}

def norm_advt(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())

def org_key(r):
    return (r.get("org_short") or "").lower().strip() or " ".join(sorted(toks(r.get("org"))))

def same(a, b):
    ua, ub = (a.get("official_url") or "").rstrip("/"), (b.get("official_url") or "").rstrip("/")
    if ua and ua == ub and ua.lower().endswith(".pdf"):
        return True
    oa, ob = org_key(a), org_key(b)
    org_match = oa and ob and (oa == ob or len(toks(a.get("org")) & toks(b.get("org"))) >= 2)
    if not org_match:
        return False
    na, nb = norm_advt(a.get("advt_no")), norm_advt(b.get("advt_no"))
    if na and nb:
        return na == nb
    pa, pb = toks(a.get("post")), toks(b.get("post"))
    jac = len(pa & pb) / max(1, len(pa | pb))
    return jac >= 0.5 and (a.get("last_date") == b.get("last_date") or not a.get("last_date") or not b.get("last_date"))

def rid(r):
    return f"{org_key(r)}|{r.get('advt_no') or r.get('post')}|{r.get('last_date')}"

def main():
    cmd = sys.argv[1]
    if cmd == "merge":
        out = []
        for p in sys.argv[2:]:
            data = json.load(open(p))
            out.extend(data if isinstance(data, list) else data.get("records", []))
        print(json.dumps(out, ensure_ascii=False, indent=1))
    elif cmd == "check":
        covered = json.load(open(sys.argv[2])); cands = json.load(open(sys.argv[3]))
        new, dup = [], []
        for c in cands:
            m = next((x for x in covered if same(c, x)), None) or next((x for x in new if same(c, x)), None)
            (dup.append([c, rid(m)]) if m else new.append(c))
        print(json.dumps({"new": new, "dup": dup}, ensure_ascii=False, indent=1))
    else:
        sys.exit(__doc__)

if __name__ == "__main__":
    main()
