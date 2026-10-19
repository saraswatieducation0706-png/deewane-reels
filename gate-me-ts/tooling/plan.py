import json, datetime as dt
from collections import defaultdict
from register import SUBJECTS, MOCK_SLOTS

W = {"A": 3, "B": 2, "C": 1}
MOCK_MIN = {"A": 4, "B": 2, "C": 1}
N_MOCKS = 15

def apportion(total, weights, minimum):
    n = len(weights)
    alloc = [minimum] * n
    rest = total - minimum * n
    assert rest >= 0, (total, weights)
    s = sum(weights)
    raw = [rest * w / s for w in weights]
    fl = [int(r) for r in raw]
    alloc = [a + f for a, f in zip(alloc, fl)]
    left = rest - sum(fl)
    order = sorted(range(n), key=lambda i: (-(raw[i] - fl[i]), -weights[i], i))
    for i in order[:left]:
        alloc[i] += 1
    return alloc

topics = []   # dicts
tts = []      # topic tests
tid = 0
for scode, sname, tlist in SUBJECTS:
    for ttcode, tttitle, tps in tlist:
        tts.append({"code": ttcode, "subject": scode, "title": tttitle, "topics": []})
        for name, imp in tps:
            tid += 1
            t = {"id": f"T{tid:03d}", "subject": scode, "subject_name": sname, "tt": ttcode,
                 "name": name, "imp": imp, "tt_q": 0, "st_q": 0, "mocks": []}
            topics.append(t); tts[-1]["topics"].append(t)

# Topic tests: 33 Q
for tt in tts:
    al = apportion(33, [W[t["imp"]] for t in tt["topics"]], 2)
    for t, a in zip(tt["topics"], al): t["tt_q"] = a

# Subject tests: 33 Q, every topic >= 1
subj_topics = defaultdict(list)
for t in topics: subj_topics[t["subject"]].append(t)
for s, ts in subj_topics.items():
    al = apportion(33, [W[t["imp"]] for t in ts], 1)
    for t, a in zip(ts, al): t["st_q"] = a

# Mocks
mock_content = [defaultdict(list) for _ in range(N_MOCKS)]
for s, ts in subj_topics.items():
    per = sum(MOCK_SLOTS[s]); total = per * N_MOCKS
    counts = [MOCK_MIN[t["imp"]] for t in ts]
    extra = total - sum(counts)
    assert extra >= 0, s
    add = apportion(extra, [W[t["imp"]] for t in ts], 0)
    counts = [c + a for c, a in zip(counts, add)]
    load = [0] * N_MOCKS
    # place most frequent first, at evenly spaced ideal positions
    for t, c in sorted(zip(ts, counts), key=lambda x: -x[1]):
        for k in range(c):
            ideal = (k + 0.5) * N_MOCKS / c - 0.5
            cands = [m for m in range(N_MOCKS) if load[m] < per]
            nodup = [m for m in cands if m not in t["mocks"]] or cands
            m = min(nodup, key=lambda m: (abs(m - ideal), load[m]))
            t["mocks"].append(m); load[m] += 1
            mock_content[m][s].append(t["id"])
    assert all(l == per for l in load), (s, load)
    for t in ts: t["mocks"].sort()

# checks
for t in topics:
    reps = 1 + len(t["mocks"])  # subject test + mocks, after the topic test
    t["revisions"] = reps
    assert len(t["mocks"]) >= MOCK_MIN[t["imp"]], t
for m in range(N_MOCKS):
    assert sum(len(v) for v in mock_content[m].values()) == 65

# Calendar
D = dt.date
waves = [(D(2026,11,9), ["GA","EM","MEC","SOM"]), (D(2026,11,16), ["TOM","MD","MAT"]),
         (D(2026,11,23), ["FM","HT"]), (D(2026,11,30), ["TD","APP"]), (D(2026,12,7), ["MFG"]),
         (D(2026,12,14), ["IE"])]
st_waves = [(D(2026,12,21), ["GA","EM","MEC","SOM"]), (D(2026,12,28), ["TOM","MD","MAT","FM"]),
            (D(2027,1,4), ["HT","TD","APP","MFG","IE"])]
sundays = [D(2026,12,6) + dt.timedelta(weeks=i) for i in range(9)]
weds = [D(2026,12,23) + dt.timedelta(weeks=i) for i in range(6)]
mock_dates = sorted(sundays + weds)
assert len(mock_dates) == 15 and mock_dates[-1] <= D(2027,1,31)
order = [s for s, _, _ in SUBJECTS]
subj_name = {s: n for s, n, _ in SUBJECTS}

releases = []
n = 0
for d, subs in waves:
    for tt in tts:
        if tt["subject"] in subs:
            n += 1; tt["no"] = n; tt["date"] = d
            releases.append((d, f"TT{n:02d}", "Topic test", f"{subj_name[tt['subject']]} - {tt['title']}", 33, 50, 90))
assert n == 40
k = 0
for d, subs in st_waves:
    for s in subs:
        k += 1
        releases.append((d, f"ST{k:02d}", "Subject test", subj_name[s] + " (full subject)", 33, 50, 90))
assert k == 13
for i, d in enumerate(mock_dates):
    releases.append((d, f"FLT{i+1:02d}", "Full-length mock", f"GATE ME Full-Length Mock {i+1}", 65, 100, 180))
releases.sort(key=lambda r: (r[0], r[1]))

json.dump({"topics": topics, "tts": [{k: (str(v) if k == "date" else v) for k, v in tt.items() if k != "topics"} for tt in tts],
           "mock_content": [dict(m) for m in mock_content],
           "releases": [[str(r[0])] + list(r[1:]) for r in releases]},
          open("plan.json", "w"), indent=1, default=str)

from collections import Counter
print("topics", len(topics), Counter(t["imp"] for t in topics))
for imp in "ABC":
    ms = [len(t["mocks"]) for t in topics if t["imp"] == imp]
    print(imp, "mock appearances min/max", min(ms), max(ms))
print("min revisions", min(t["revisions"] for t in topics))
print("mock dates", [d.strftime("%a %d %b") for d in mock_dates])
print("total Q", 40*33 + 13*33 + 15*65)
