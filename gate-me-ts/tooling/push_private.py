#!/usr/bin/env python3
"""Upload files to the PRIVATE repo saraswatieducation0706-png/gate-me-ts-files through the GitHub API
(no git clone or repo attachment needed). Token comes from env GMTS_TOKEN (fine-grained, Contents read+write
on gate-me-ts-files only). Never print the token.

Usage: GMTS_TOKEN=... python3 push_private.py <local file> <repo path> [<local file> <repo path> ...]
       GMTS_TOKEN=... python3 push_private.py --get <repo path> <local file>     (download)
       GMTS_TOKEN=... python3 push_private.py --ls <repo dir>                    (list)
Prints one line per file: OK <repo path> or FAIL <repo path> <reason>. Exit code 1 if any failed."""
import os, sys, json, base64, urllib.parse, urllib.request, urllib.error

REPO = "saraswatieducation0706-png/gate-me-ts-files"
API = f"https://api.github.com/repos/{REPO}/contents/"
TOK = os.environ.get("GMTS_TOKEN", "").strip()


def req(method, path, body=None):
    url = API + urllib.parse.quote(path)
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {TOK}", "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "gate-me-ts",
        "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return resp.status, json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, {"message": e.read().decode(errors="replace")[:300]}


def put(local, path):
    st, cur = req("GET", path)
    sha = cur.get("sha") if st == 200 and isinstance(cur, dict) else None
    body = {"message": f"add {path}", "content": base64.b64encode(open(local, "rb").read()).decode(),
            "branch": "main"}
    if sha:
        body["sha"] = sha
    st, res = req("PUT", path, body)
    return st in (200, 201), f"HTTP {st} {res.get('message', '')}"[:200]


if __name__ == "__main__":
    if not TOK:
        print("FAIL no GMTS_TOKEN"); sys.exit(1)
    a = sys.argv[1:]
    if a and a[0] == "--get":
        st, res = req("GET", a[1])
        if st != 200:
            print("FAIL", a[1], st); sys.exit(1)
        if res.get("content"):
            data = base64.b64decode(res["content"])
        else:  # files over 1 MB come without inline content
            r = urllib.request.Request(res["download_url"], headers={"Authorization": f"Bearer {TOK}"})
            data = urllib.request.urlopen(r, timeout=120).read()
        open(a[2], "wb").write(data); print("OK", a[1]); sys.exit(0)
    if a and a[0] == "--ls":
        st, res = req("GET", a[1] if len(a) > 1 else "")
        if st != 200:
            print("FAIL", st); sys.exit(1)
        for it in res:
            print(it["type"], it["path"])
        sys.exit(0)
    bad = 0
    for local, path in zip(a[0::2], a[1::2]):
        ok, msg = put(local, path)
        print("OK" if ok else "FAIL", path, "" if ok else msg)
        bad += not ok
    sys.exit(1 if bad else 0)
