# Job videos — format and routing (Naveen, 27 Oct 2026)

Replaces the old "one 9:16 reel per notification on YouTube Shorts + Instagram + Facebook" format for
government job notifications. GATE90 reels are NOT affected (they stay Shorts/Reels).

Why: YouTube analytics (7–22 Oct 2026) showed contract/apprentice reels got ~40% fewer views than permanent
ones (same watch %), and the channel's long 16:9 videos earned 10x the watch time and 2.5x the subscribers of
all Shorts, with YouTube search as the biggest traffic source.

## 1. What gets made

| Job type | Daily run | Sunday |
|---|---|---|
| **Permanent** | one 16:9 YouTube video + one 9:16 teaser (Instagram + Facebook) per notification, as many as there are free slots | same |
| **Apprentice / contract** | NOT made — recorded in the tracker as `weekly_queue` with its facts. **Exception (urgent):** if its last date is on or before *coming Sunday + 2 days*, make it the same day like a permanent job | ONE combined 16:9 "this week's apprentice & contract jobs" video + teaser, containing every queued job with last date ≥ Sunday + 2 days and any new ones found on Sunday |

Job type — decide from the official notification:
- **Permanent**: regular / permanent posts incl. probation, PSC / SSB / SSC / RRB / bank / insurance exams,
  PSU regular posts (GET, MT, Executive Trainee, Assistant Manager…), defence officer entries, regular faculty.
- **Apprentice**: apprenticeship / trainee under the Apprentices Act (NATS / NAPS), stipend-based.
- **Contract**: contractual, fixed-term / tenure, "short term basis", project posts (Project Associate /
  Scientist / Engineer), Young Professional, JRF / SRF / RA, consultant, guest / ad-hoc / panel teachers,
  Senior / Junior Resident (tenure), walk-ins for temporary posts.
- If a notification mixes types, use the type of the majority of fresher vacancies; if it is unclear and the
  notification does not say "regular", treat it as contract.

"Last date" for a walk-in = the (last) walk-in date.

## 2. The 16:9 YouTube video (`render_job_landscape.py`)

Same spec format and scene kinds as the reel (`scene_kinds.md`), rendered at 1920x1080. Add `"chapter"` to the
scene that starts each section (YouTube chapters are written to `<out>.chapters.txt`; put them in the
description). Script order for one notification (skip a scene only when the notification has nothing for it):

1. `hook` (no chapter) — emotional line + the news. 2 title lines ≤ 22 chars each, `sub` ≤ 60 chars.
2. `card` "Overview" — organisation, post(s), job type, location, advt no.
3. `count` / `table` "Vacancies" — total + post/branch-wise (`count` can take `notes` [≤3] for pay/job type).
4. `table` / `card` "Eligibility" — degree & discipline, minimum %, final-year yes/no, age (with cut-off date),
   key extra conditions (GATE score, domicile, physical). Use two scenes if needed.
5. `card` / `table` "Salary & fee" — pay level / CTC / stipend, allowances if stated, application fee + exemptions.
6. `steps` "Selection process" (+ weightage note).
7. `pattern` "Exam pattern" (one scene per exam stage).
8. `card` "Syllabus" — only if the notification gives the syllabus (main subjects, ≤ 5 lines).
9. `dates` "Important dates".
10. `steps` "How to apply" — the online steps the notification gives (register, fill form, upload, pay, print).
11. `card` — "Apply only on: <official website>" + "Read full notification before applying".

Length: 2–5 minutes, whatever the notification genuinely supports — no padding (YOUTUBE_RULES §1).
Each scene's voice ≤ ~40 words, one idea per scene. Cards up to 5 lines (≤ 40 chars each), tables up to 7 rows.

### Sunday roundup video
- Scenes: `hook` ("<N> Apprentice & Contract Govt Jobs This Week") → `index` "This Week's Jobs" (rows
  [name ≤ 32 chars, last date], ≤ 10 per scene; split into "(1/2)", "(2/2)") → one `job` scene per job, sorted by
  last date, each with `"chapter": "<Org short> <post>"` → `card` "How to apply" (apply only on each official
  site, read the notification) .
- `job` fields: `title` ("Job 3 of 12"), `org`, `post`, `type` ("Apprentice" / "Contract" / "Walk-in"),
  `posts` ("54 Seats"), `rows` ≤ 5 [label, value] (Qualification, Stipend/Pay, Age, Selection, Apply at),
  `last_date`. Voice ≤ 45 words per job.
- `source` in the spec: "official notifications (links in description)"; `verified`: true only if every job
  in it is verified.
- If there are no queued jobs, there is no roundup that Sunday.

## 3. The 9:16 teaser (`render_reel.py` with `"teaser": true`)

30–45 seconds for Instagram + Facebook. No welcome scene; the renderer adds a 6-second end card
"Full details video on our YouTube channel — Deewane: IES & GATE Point".
- Scenes: `hook` (≤ 25 words of voice) + 1–2 `card`s with the key facts (posts, pay, eligibility, LAST DATE).
- Total voice ~70–100 words. Check the rendered duration is 30–45 s; adjust the text if not.
- Roundup teaser: hook "<N> apprentice & contract jobs this week" + one card listing the 4 biggest
  (org + seats) + "Last dates from <first>".

## 4. vidIQ optimisation (before booking anything)

At the start of the run call `vidiq_balance`. Daily credit budget = totalCredits ÷ days until
`renewableResetsAt` (round down). Typical cost: 15 credits per video, +22 for an AI thumbnail.
If the vidIQ tools are not available in the session, do steps 1–5 by hand and say "vidIQ not connected —
titles/tags optimised manually" at the top of SUMMARY.md and in the final message.

Per video (permanent video, urgent apprentice/contract video, roundup):
1. `vidiq_keyword_research` (mode research, keyword "<Org short> recruitment 2026" — or the exam name, e.g.
   "UPPSC RO ARO 2026" — country "IN", limit 10). Primary keyword = the highest-volume keyword that names this
   organisation / exam / post (fall back to the seed). Keep 5–8 relevant related keywords for tags.
2. `vidiq_generate_titles` (type long, regionCode IN, language en, numTitles 5) with a draft title and a
   3-line description.
3. Final title (≤ 100 chars, no #Shorts): primary keyword near the start + the strongest HONEST hook from
   step 2. Every number must be true; no false urgency ("before it's too late", "last chance" unless the last
   date really is within 3 days), no "guaranteed", nothing YOUTUBE_RULES forbids.
4. `vidiq_score_title` (type long, channelId UCw3eyA3edUq3AJkh8HFLD2Q). If < 70, write one better variant,
   score it, keep the higher. (Skip this step when over the daily budget.)
5. Tags: primary keyword first, then related keywords, org name variants, post, exam, "<org> recruitment 2026",
   "govt jobs for freshers" … (≤ 450 chars). 3–5 hashtags at the end of the YouTube description; 10–15 in
   the teaser caption.
6. Thumbnail (1280x720): `thumbnail.py` (big org name + the key number, ≤ 6 words, badges) — `<NN>_thumb.jpg`.
   vidIQ cannot score our own image before upload (it only accepts YouTube-hosted images).
   For the Sunday roundup and at most 2 big national recruitments a week (UPSC / SSC / RRB / IBPS / SBI / major
   PSU, or ≥ 500 posts): `vidiq_generate_thumbnail` (orientation landscape, title, userQuery giving the exact
   text to show, red-and-white Deewane style, no logos, no State Emblem, no real people) → `vidiq_job_poll`
   until completed → LOOK at the image: every word and number must be exactly right and readable. If anything
   is wrong, use the `thumbnail.py` thumbnail instead. If it is right, use its imageUrl as the YouTube
   `videoThumbnailUrl`.
Record the primary keyword, the vidIQ title scores and credits used in metadata.md and SUMMARY.md.

## 5. Metadata (`metadata.md` per video)

```
# <NN>. <Org short> — <post>   (type: permanent | apprentice | contract | roundup; urgent: yes/no)
## vidIQ   primary keyword, related keywords used, title score(s), credits used
## YouTube title
## YouTube description
<2–3 line summary: org, post, vacancies, eligibility, last date>
⏱️ Chapters
<chapters.txt lines>
<key facts with emoji bullets: 🎓 Eligibility, 👨‍🎓 Final year, 🎂 Age, 💰 Salary/Stipend, 📝 Selection, 📅 Dates>
🔗 Official website: <official_url>      (roundup: one line per job)
⚠️ Always read the official notification before applying.

📚 Prepare with DIG Career Thrust — Test Series & Study Material
📱 App: https://play.google.com/store/apps/details?id=co.jack.iurlk
💬 Telegram: https://t.me/digcareerthrust
🌐 Website: https://web.digcareerthrust.com/login
#<3–5 hashtags>
## Tags
## Teaser caption (Instagram + Facebook)
<1–2 line hook + key facts (emoji bullets) + "▶️ Full details video on YouTube: Deewane: IES & GATE Point
(@deewaneiesgate)" + official website + the 3 DIG links + 10–15 hashtags; < 2,000 chars>
## Posting slot
```
No "unverified" / "could not verify" wording anywhere (title, description, caption, video).

## 6. Files and posting

Per video in the day's folder: `<NN>_video.mp4` (16:9), `<NN>_thumb.jpg` (1280x720), `<NN>_teaser.mp4` (9:16),
`<NN>_cover.jpg` (1080x1920). Upload all four to GitHub, check each raw URL = 200, then book TWO Metricool
posts at the same slot — see `posting.md` §3.
