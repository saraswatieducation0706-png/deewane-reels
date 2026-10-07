# Finding and verifying notifications

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
Pages are long — ask WebFetch only for entries posted in the lookback window with org, post, qualification,
vacancies, last date and the link. If a site fails, note it in SUMMARY.md and continue.

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
| Official site refuses access (403, blocked, timeout after one retry, robots, login/captcha wall) | **Proceed unverified** (allowed by Naveen). Take facts from the lead pages and confirm the key facts (posts, vacancies, qualification, age, last date) on at least 2 independent lead sites; where they disagree, say "as per notification" instead of a number. Set `"verified": false` → footer "Official site: <domain> — check notification before applying". Mark "UNVERIFIED (official site not accessible)" in SUMMARY.md and source.md, and add "⚠️ Please confirm details on the official website before applying." to the description. |

## 5. Reading the official notification

- Text on the page → read the page text. PDF available → read the PDF (prefer the full detailed
  advertisement over a short one).
- `WebFetch` the PDF URL; for long PDFs ask for one group of facts at a time (eligibility & vacancies; age &
  pay; selection & exam pattern; dates & fee).
- Scanned PDF without text → rasterise and read the pages.
Record `official_url`, `pdf_url`, advertisement number, and where each fact was found.
