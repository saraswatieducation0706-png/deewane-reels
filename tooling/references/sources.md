# Finding and verifying notifications

## 0. Reading websites: ONLY through the GitHub fetcher (Naveen, 23 Nov 2026 — replaces the 9 Nov rule)

Scheduled runs start in a fresh cloud container every day, so "Always allow" never carries over and every
`WebFetch` / `WebSearch` call to a new site can stop the run waiting for Naveen. The shell cannot reach job sites
either (proxy 403). So in this skill:

- **NEVER call `WebFetch` or `WebSearch`** (not even once, not even for an official PDF), and NEVER use the
  built-in browser, Claude in Chrome, computer use or any `mcp__remote-devices__*` / `mcp__Claude_Browser__*` /
  `mcp__claude-in-chrome__*` tool. Do not request folder or site access. Do not edit ~/.claude/settings.json.
- Read every web page and PDF with the repo's fetcher, which runs on GitHub Actions (push-triggered, no
  permissions needed, ~60–90 s per batch):

  ```bash
  cd ~/deewane-reels
  python3 tooling/scripts/gh_fetch.py leads https://www.freejobalert.com/latest-notifications/ https://www.indgovtjobs.in/ ...
  # or many URLs from a file (one per line):
  python3 tooling/scripts/gh_fetch.py official --file /tmp/urls.txt
  ```
  It prints the results folder (`fetch/results/<label>_<time>/`) and a table (n, ok, status, type, chars, file).
  Each page is `NNN.md`: HTML → Markdown with absolute links; PDF → `pdftotext -layout` text (a note says when
  the PDF is scanned). Put `raw: <url>` on a line to save the raw source instead.
- **Batch**: send ALL lead-site URLs in one call, then all official pages / PDFs of the day's candidates in one
  or two more calls (up to ~40 URLs per call). Don't fetch one URL at a time.
- Read the result files with `grep -n` / `sed -n` / Python (they are long — freejobalert pages are 600K+ chars);
  never `cat` a whole file. Follow links found in a page by putting them in the next batch.
- A page with `ok: false`, an error, a timeout or almost no text (JS-rendered sites such as ssc.gov.in give
  ~30 chars) = "site refuses access": do not retry more than once; official site → §4 "official site refuses
  access" row (2 lead sites); lead site → use the other lead sites. List skipped sites in SUMMARY.md.
- Scanned PDF (the text file says so): fetch it again as `file: <pdf url>` — you get the PDF itself
  (`NNN.pdf`); rasterise the pages (`pdftoppm -r 110 -png`) and read them with the Read tool.
- The fetcher deletes request files older than 3 days by itself. Commit nothing else into `fetch/`.
- If `gh_fetch.py` itself fails (push rejected 6 times, no result after 15 min): stop finding new jobs, book
  nothing new, and say so at the top of SUMMARY.md and in the final message (don't fall back to WebFetch).

## 1. Daily lead sites (checked every run — leads only)

Fetch each listing page and collect notifications posted since the last tracker run date (minus 1 day overlap).
All checked working on 7 Oct 2026.

| # | URL | Notes |
|---|---|---|
| 1 | https://www.freejobalert.com/latest-notifications/ | Best single source: post date + last date + qualification |
| 2 | https://www.freejobalert.com/government-jobs/ | Central govt / PSU / defence |
| 3 | https://www.freejobalert.com/engineering-jobs/ | PSU & technical |
| 4 | https://www.freejobalert.com/bank-jobs/ | Banks, insurance |
| 5 | https://www.freejobalert.com/railway-jobs/ | Railways, metro rail |
| 6 | https://www.freejobalert.com/state-government-jobs/ | All states, has per-state pages |
| 7 | https://www.indgovtjobs.in/ | |
| 8 | https://www.rojgarresult.com/ | |
| 9 | https://www.sarkariexam.com/ | List has no last dates — open entries |
| 10 | https://www.mysarkarinaukri.com/ | |
| 11 | https://www.fresherslive.com/government-jobs | |
| 12 | https://www.sarkarinaukriblog.com/ | Big national notifications |
| 13 | https://www.govtjobguru.in/ | Big state recruitments |
| 14 | https://majhinaukri.in/ | National listings, partly Marathi |

Don't use (tested 7 Oct 2026): sarkariresult.com (403), jagranjosh.com (blocked), employmentnews.gov.in,
careerpower.in, recruitment.guru (stale), adda247.com/jobs, testbook.com (no lists).
Pages are long — grep the fetched Markdown for entries posted in the lookback window (org, post, qualification,
vacancies, last date and the link). If a site fails, note it in SUMMARY.md and continue.

## 1a. YouTube leads — dropped (23 Nov 2026)

They needed `WebSearch`, which can stop an unattended run, and search engines return junk to the fetcher. Use
the lead sites in §1 and the official sites in §2–3 only.

## 2. Official sites — central (direct check for fresh notices + verification)

UPSC upsc.gov.in · SSC ssc.gov.in · IBPS ibps.in · SBI sbi.bank.in/web/careers (SBI moved to .bank.in;
other banks are moving too — follow redirects) · RBI opportunities.rbi.org.in · RRBs rrbcdg.gov.in ·
ONGC ongcindia.com · IOCL iocl.com · NTPC ntpc.co.in · BHEL careers.bhel.in · POWERGRID powergrid.in ·
Coal India coalindia.in · ISRO isro.gov.in · DRDO drdo.gov.in

## 3. Official sites — states (verification; check Gujarat daily, others when a lead points there)

Gujarat: gpsc.gujarat.gov.in · gsssb.gujarat.gov.in · ojas.gujarat.gov.in
Maharashtra: mpsc.gov.in · Rajasthan: rpsc.rajasthan.gov.in, rsmssb.rajasthan.gov.in
Madhya Pradesh: mppsc.mp.gov.in, esb.mp.gov.in · Uttar Pradesh: uppsc.up.nic.in, upsssc.gov.in
Bihar: bpsc.bihar.gov.in, bssc.bihar.gov.in · Haryana: hpsc.gov.in, hssc.gov.in
Punjab: ppsc.gov.in, sssb.punjab.gov.in · Delhi: dsssb.delhi.gov.in
Karnataka: kpsc.kar.nic.in · Tamil Nadu: tnpsc.gov.in · Kerala: keralapsc.gov.in
Telangana: tgpsc.gov.in · Andhra Pradesh: psc.ap.gov.in · West Bengal: wbpsc.gov.in
Odisha: opsc.gov.in, ossc.gov.in · Assam: apsc.nic.in · Jharkhand: jpsc.gov.in, jssc.jharkhand.gov.in
Chhattisgarh: psc.cg.gov.in, vyapam.cgstate.gov.in · Uttarakhand: psc.uk.gov.in, sssc.uk.gov.in
Himachal Pradesh: hppsc.hp.gov.in · J&K: jkpsc.nic.in, jkssb.nic.in · Goa: gpsc.goa.gov.in
Domains change; if one fails, the lead site's "official website" link is the authority — follow it.

## 4. Verification rule (Naveen's rule, 7 Oct 2026)

For every candidate, try the official website (page text, or the full PDF advertisement if there is one).

| Outcome | Action |
|---|---|
| Official site opens and the notification is there | **Verified.** Use ONLY the official facts (they override any aggregator figure). `"verified": true` in spec → footer "Verified from official source". |
| Official site opens, notification found, but aggregator details were wrong | Still verified — use the official facts. Note the corrections in source.md. |
| Official site opens but the notification can't be found there, or the official text contradicts the lead on something basic (doesn't exist, different org/post, already closed) | **Skip** — doubtful. Tracker status `skipped`, reason "not found / contradicts official site". |
| Official site refuses access (403, blocked, timeout after one retry, robots, login/captcha wall) | **Proceed unverified** (allowed by Naveen). Take facts from the lead pages and confirm the key facts (posts, vacancies, qualification, age, last date) on at least 2 independent lead sites; where they disagree, say "as per notification" instead of a number. Set `"verified": false` → footer "Official site: <domain> — check notification before applying". Mark "UNVERIFIED (official site not accessible)" in SUMMARY.md and source.md only (internal). **Never use the word "unverified" (or "could not verify / not yet verified / could not be opened") in the title, description, tags or hashtags** (Naveen, 9 Oct 2026) — the description keeps only the usual "⚠️ Always read the official notification before applying." line. **Do not put any "could not verify / not yet verified" line in the video itself** (voice or on-screen) — the footer is enough (Naveen, 7 Oct 2026). |

## 5. Reading the official notification

- Text on the page → read the page text. PDF available → read the PDF (prefer the full detailed
  advertisement over a short one).
- Fetch the PDF URL with `gh_fetch.py` (it returns the text with layout); grep it for each group of facts
  (eligibility & vacancies; age & pay; selection & exam pattern; dates & fee).
- Scanned PDF without text → fetch it as `file: <url>`, rasterise and read the pages (§0).
Record `official_url`, `pdf_url`, advertisement number, and where each fact was found.
