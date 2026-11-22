#!/usr/bin/env python3
"""GitHub Actions web fetcher for the unattended job runs.

A request file fetch/requests/<name>.txt holds one item per line:
  https://...            fetch the page (HTML -> Markdown text with links, PDF -> text)
  search: <query>        DuckDuckGo web search (titles, links, snippets)
  # comment              ignored
Results go to fetch/results/<name>/: 001.md, 002.md ... and index.json
[{n, url, ok, status, type, chars, file, error}].
"""
import sys, os, json, re, subprocess, urllib.parse, time
import requests, html2text

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")
H = {"User-Agent": UA, "Accept-Language": "en-IN,en;q=0.9,hi;q=0.8"}
MAXC = 400_000

def to_md(html, base):
    h = html2text.HTML2Text(baseurl=base); h.body_width = 0; h.ignore_images = True
    h.ignore_emphasis = True; h.protect_links = True
    return h.handle(html)

def fetch(url):
    r = requests.get(url, headers=H, timeout=45, allow_redirects=True, verify=True)
    ct = r.headers.get("content-type", "").lower()
    if "pdf" in ct or r.content[:5] == b"%PDF-":
        open("/tmp/x.pdf", "wb").write(r.content)
        txt = subprocess.run(["pdftotext", "-layout", "/tmp/x.pdf", "-"], capture_output=True, text=True).stdout
        if len(txt.strip()) < 200:
            txt += "\n[PDF has little or no text layer - probably scanned. pages: " + \
                subprocess.run(["pdfinfo", "/tmp/x.pdf"], capture_output=True, text=True).stdout + "]"
        return r.status_code, "pdf", f"URL: {r.url}\n\n" + txt
    r.encoding = r.encoding or r.apparent_encoding
    return r.status_code, "html", f"URL: {r.url}\n\n" + to_md(r.text, r.url)

def search(q):
    r = requests.post("https://html.duckduckgo.com/html/", data={"q": q, "kl": "in-en"}, headers=H, timeout=30)
    out = []
    for m in re.finditer(r'class="result__a" href="([^"]+)"[^>]*>(.*?)</a>.*?class="result__snippet"[^>]*>(.*?)</a>', r.text, re.S):
        href = m.group(1)
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
        href = qs.get("uddg", [href])[0]
        clean = lambda s: re.sub(r"<[^>]+>", "", s).replace("&amp;", "&").replace("&#x27;", "'").strip()
        out.append(f"- {clean(m.group(2))}\n  {href}\n  {clean(m.group(3))}")
    return r.status_code, "search", f"SEARCH: {q}\n\n" + "\n".join(out)

def main(req):
    name = os.path.splitext(os.path.basename(req))[0]
    outd = os.path.join("fetch", "results", name); os.makedirs(outd, exist_ok=True)
    items = [l.strip() for l in open(req, encoding="utf-8") if l.strip() and not l.strip().startswith("#")]
    idx = []
    for n, it in enumerate(items, 1):
        rec = {"n": n, "url": it, "ok": False}
        for attempt in (1, 2):
            try:
                st, ty, txt = search(it[7:].strip()) if it.lower().startswith("search:") else fetch(it)
                f = f"{n:03d}.md"
                open(os.path.join(outd, f), "w", encoding="utf-8").write(txt[:MAXC])
                rec.update(ok=200 <= st < 400, status=st, type=ty, chars=len(txt), file=f); break
            except Exception as e:
                rec.update(error=f"{type(e).__name__}: {str(e)[:200]}")
                time.sleep(3)
        idx.append(rec)
    json.dump(idx, open(os.path.join(outd, "index.json"), "w"), indent=1, ensure_ascii=False)
    open(os.path.join(outd, "DONE"), "w").write(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

if __name__ == "__main__":
    for r in sys.argv[1:]:
        main(r)
