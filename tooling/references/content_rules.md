# Content rules

## A. Which notifications qualify

All four must hold:

1. **Government** — central/state government departments, PSUs, public sector banks, RBI/SEBI/NABARD and
   other regulators/statutory bodies, government universities/institutes, courts, defence officer entries,
   state PSCs/SSBs. (Contract posts in government bodies count — mark them "Contract" on screen.)
2. **Education OR pay** — at least one post requires a bachelor's degree (any discipline, or a specific
   one such as B.E./B.Tech/B.Com) as its qualification, **or** the post's starting monthly pay is more than
   ₹30,000 (basic pay of 7th CPC Pay Level 6 or above = ₹35,400+, or a stated consolidated/gross pay over
   ₹30,000). Use the figure written in the notification; never estimate.
3. **Fresher-friendly** — at least one qualifying post needs no prior work experience. Posts that require
   experience are dropped from the reel entirely (don't mention them, don't count their vacancies). If every
   post needs experience → skip the notification (tracker status `skipped`, reason "experience only").
4. **Time left** — the last date to apply is at least 2 days after the run date
   (run on 7 Oct → last date must be 9 Oct or later). Otherwise skip (`skipped`, "deadline too close").

"New" = published or first listed within the lookback window (since the latest tracker run date, minus one
day of overlap; on the very first run, the last 3 days) and not already in the tracker.

## B. What to extract (from the official notification only)

Mandatory — find each one, or explicitly record "not mentioned in notification":
- Organisation name (full + short) and post name(s); advertisement number
- Education qualification for each fresher post (degree, discipline, minimum % if any)
- **Final-year students** — can they apply? (look for "appearing", "final year", "result awaited", cut-off
  date for possessing the qualification). If silent, say so; never assume.
- Post/branch-wise vacancies (total per post/branch; category-wise split NOT needed)
- Age limit (min–max, cut-off date) — mention "relaxation as per government rules" only if the notification
  says so
- Other eligibility (GATE score year, nationality, physical standards, domicile/language, bond, etc.)
- Selection process in order (CBT / written / skill test / GD / interview / document verification) and the
  weightage of each stage in the final merit, if stated
- Exam pattern: number of sections, questions per section, marks, total time, marks per correct answer,
  negative marking per wrong answer
- Opening and closing dates for application; tentative exam / interview date
Also include if present and useful: pay scale / CTC, application fee (and exemptions), job location,
probation/bond, where to apply (official website).

Save the extracted facts as `facts.json` and a short `source.md` listing official_url, pdf_url, and where each
fact was found (page/section). Nothing goes into the script that is not in `facts.json`.

## C. Writing the reel script

Order (skip a scene only when the notification truly has nothing for it):
1. `hook` — emotional line + the news (see below)
2. `card` — who is hiring: organisation, post, job type (Regular/Contract), location if notable
3. `count` total vacancies (+ salary as `note` if short) and/or `table` post/branch-wise vacancies
4. `card` — eligibility: degree, final-year yes/no, age limit, key extra condition (e.g. "GATE 2026 score")
5. `card` or `table` — salary/pay (if not already shown) and application fee
6. `steps` — selection process (+ weightage note)
7. `pattern` — exam pattern (one scene per stage if there are two exam stages)
8. `dates` — apply from, last date, exam date
9. `card` — "Apply only on: <official website>" (+ 1 line like "Read full notification before applying").
   Never add "we could not verify / details not yet verified" lines to any scene, even for unverified reels.

Length: as long as the content needs, 45 seconds to 3 minutes. Do not pad thin notifications; do not cut
mandatory fields to save time.

**Emotional line** (spoken right after the fixed welcome, as the start of the hook voice): one sentence that
speaks to a 21–35-year-old job seeker and fits THIS notification — e.g. secure PSU career with a big salary,
a chance for freshers without experience, a bank job in your own state, a last-date reminder. Vary it every
reel. No false promises ("guaranteed selection"), no fear-mongering.

Accuracy: numbers, dates, ages and percentages on screen and in voice must match the notification exactly.
When the notification is ambiguous, say "as per notification" rather than guessing.

## D. Metadata (`metadata.md` per reel)

```
# <reel number>. <Org short> — <post>

## YouTube title  (≤ 95 chars, include org, post, vacancies/key hook; add #Shorts at the end if room)
## Instagram / YouTube description
<2–3 line summary: org, post, vacancies, eligibility, last date>
<key facts as short lines with emoji bullets: 🎓 Eligibility, 👨‍🎓 Final year, 🎂 Age, 💰 Salary, 📝 Selection, 📅 Dates>
🔗 Official website: <official_url>
⚠️ Always read the official notification before applying.
(No "unverified" / "could not verify" wording anywhere in the title or description, even for unverified reels — Naveen, 9 Oct 2026.)

📚 Prepare with DIG Career Thrust — Test Series & Study Material
📱 App: https://play.google.com/store/apps/details?id=co.jack.iurlk
💬 Telegram: https://t.me/digcareerthrust
🌐 Website: https://web.digcareerthrust.com/login

## Tags  (comma-separated, ≤ 450 characters; org name variants, post, "<org> recruitment 2026", "govt jobs for freshers", "engineering jobs", etc.)
## Hashtags  (10–15; e.g. #GovtJobs #SarkariNaukri #<Org>Recruitment #FreshersJobs #Shorts)
## Posting slot  (e.g. 18:00 IST)
```
