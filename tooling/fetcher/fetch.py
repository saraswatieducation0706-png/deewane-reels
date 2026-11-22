#!/usr/bin/env python3
"""GitHub Actions web fetcher for the unattended job runs.

A request file fetch/requests/<name>.txt holds one item per line:
  https://...            fetch the page (HTML -> Markdown text with links, PDF -> text)
  raw: https://...       save the raw response (HTML/CSS source)
  search: <query>        Bing web search - UNRELIABLE from GitHub (bot pages); do not rely on it
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
    # make every link absolute first, so the run can follow "official website" / PDF links
    html = re.sub(r'(href|src)\s*=\s*(["\'])(.*?)\2',
                  lambda m: f'{m.group(1)}="{urllib.parse.urljoin(base, m.group(3).strip())}"', html, flags=re.I | re.S)
    html = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", html, flags=re.I | re.S)
    h = html2text.HTML2Text(); h.body_width = 0; h.ignore_images = True; h.ignore_emphasis = True
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

def _clean(s):
    import html as _h
    return _h.unescape(re.sub(r"<[^>]+>", "", s)).strip()

def search(q):
    """Bing web search (first ~20 results: title, link, snippet)."""
    out, st = [], 0
    for first in (1, 11):
        r = requests.get("https://www.bing.com/search", params={"q": q, "first": first, "setlang": "en-IN", "cc": "IN"},
                         headers=H, timeout=30)
        st = r.status_code
        for blk in re.findall(r'<li class="b_algo".*?</li>', r.text, re.S):
            a = re.search(r'<h2[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', blk, re.S)
            p = re.search(r"<p[^>]*>(.*?)</p>", blk, re.S)
            if a:
                href = a.group(1)
                if "bing.com/ck/a" in href:   # decode Bing redirect links
                    u = urllib.parse.parse_qs(urllib.parse.urlparse(_clean(href)).query).get("u", [""])[0]
                    if u.startswith("a1"):
                        import base64
                        try: href = base64.urlsafe_b64decode(u[2:] + "==").decode()
                        except Exception: pass
                out.append(f"- {_clean(a.group(2))}\n  {_clean(href)}\n  {_clean(p.group(1)) if p else ''}")
    return st, "search", f"SEARCH: {q}\n\n" + "\n".join(out)

def main(req):
    name = os.path.splitext(os.path.basename(req))[0]
    outd = os.path.join("fetch", "results", name); os.makedirs(outd, exist_ok=True)
    items = [l.strip() for l in open(req, encoding="utf-8") if l.strip() and not l.strip().startswith("#")]
    idx = []
    for n, it in enumerate(items, 1):
        rec = {"n": n, "url": it, "ok": False}
        for attempt in (1, 2):
            try:
                if it.lower().startswith("search:"):
                    st, ty, txt = search(it[7:].strip())
                elif it.lower().startswith("raw:"):
                    r = requests.get(it[4:].strip(), headers=H, timeout=45); st, ty, txt = r.status_code, "raw", r.text
                else:
                    st, ty, txt = fetch(it)
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
