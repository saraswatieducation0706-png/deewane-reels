# Scene kinds for `render_reel.py`

Spec file (one per reel):

```json
{
  "out": "/abs/path/01_ONGC_GT/reel.mp4",
  "source": "ongcindia.com",
  "verified": true,
  "scenes": [ {"kind": "hook", ...}, ... ]
}
```

- `source` = the official domain the facts were verified on. It is printed at the bottom of every frame
  ("Verified from official source: …"), so it must be the real official domain, never an aggregator.
- `verified`: false only when the official site refused access (footer then says "check notification before applying").
- Do **not** add the welcome or end scenes; the renderer adds them (signature line + website/QR outro).
- Every scene needs `voice` (spoken text) and the fields below. Scene length = voice clip + 0.4 s,
  so the voice decides timing. On-screen text auto-shrinks to fit, but keep it short anyway.

| kind | fields | limits / tips |
|---|---|---|
| `hook` | `title` [line1, line2], `sub` | MUST be first. Voice = emotional line + the news. line1/2 ≤ 16 chars each (e.g. "ONGC GT", "2,500 POSTS"). `sub` ≤ 40 chars. |
| `card` | `title`, `lines` [1–4] | Each line ≤ 34 chars. Use for organisation/post, eligibility, salary, fee, how to apply. |
| `count` | `title`, `num` (int), `label`, optional `note` | Big animated number. `note` ≤ 34 chars (e.g. "Salary: ₹40,000 – 1,40,000"). |
| `table` | `title`, `rows` [[label, value], …] 1–7, optional `note` | Post/branch-wise vacancies, age limits by post, salary by post. label ≤ 26 chars, value ≤ 7 chars. More than 7 rows → split across two table scenes ("Vacancies (1/2)", "(2/2)"). |
| `steps` | `title`, `steps` [2–5], optional `note` | Selection process in order. `note` for weightage, e.g. "Merit: CBT 85% + Interview 15%". |
| `pattern` | `title`, `header` [3], `rows` [[a,b,c], …] 1–6, `chips` [0–3] | Exam pattern. Default header ["Section","Qs","Marks"]. chips for duration and marking, e.g. "Duration: 2 hours", "+1 correct  |  −0.25 wrong". |
| `dates` | `title`, `lines` [[label, value], …] 2–4 | Last item is highlighted red — put the LAST DATE last unless exam date is listed; then order: apply from, last date, exam. Values ≤ 14 chars ("30 Oct 2026"). |

Voice-text rules (ElevenLabs reads exactly what is written):
- Acronyms read letter-by-letter → write with dots and spaces: "O. N. G. C.", "B. H. E. L.", "C. B. T.".
  Acronyms said as words stay as words: ISRO, SAIL, GAIL, NABARD, SEBI, GATE.
- Money in Indian words: "forty thousand rupees", "one lakh forty thousand rupees per month".
- Dates spoken naturally: "thirtieth October", not "30/10/2026".
- Keep each scene's voice ≤ ~30 words; one idea per scene.


## 16:9 job videos — `render_job_landscape.py` (from 27 Oct 2026)

Same spec file and the same scene kinds (`hook`, `card`, `count`, `table`, `pattern`, `steps`, `dates`), rendered
at 1920x1080 with the landscape welcome and a website/QR + "Subscribe" end scene. Differences and additions:
- Any scene may carry `"chapter": "<label>"` → YouTube chapters in `<out>.chapters.txt` ("0:00 Intro" is added;
  chapters under 10 s are merged; fewer than 3 → none). Also returned in the script's JSON output.
- `hook`: `title` 1–2 lines (≤ 22 chars each; line 2 is gold), `sub` ≤ 60 chars.
- `card`: 1–5 lines, ≤ 40 chars each.
- `count`: optional `notes` list (≤ 3 pills on the right; first is white, others dark red) instead of `note`.
- `table`: label ≤ 34 chars, value ≤ 14 chars, ≤ 7 rows.
- `steps`: 2–5 steps shown left→right; each label wraps to ≤ 3 lines (≤ ~30 chars is best).
- `dates`: 2–4 columns; values may wrap to 2 lines.
- `pattern`: table on the left, `chips` (≤ 3) stacked on the right.
- `job` (Sunday roundup, one per job): `title` ("Job 3 of 12"), `org`, `post`, `type`, `posts`, `rows` ≤ 5
  [label, value ≤ 60 chars], `last_date`.
- `index` (Sunday roundup overview): `title`, `rows` ≤ 10 [name ≤ 32 chars, last date ≤ 8 chars, e.g. "30 Oct"].
Render time ≈ 1x real time (a 4-minute video takes ~4 minutes).

## 9:16 teaser — `render_reel.py` with `"teaser": true`

Spec as for a reel plus `"teaser": true`: no welcome scene; the renderer appends a 6 s end card "Full details
video on our YouTube channel — Deewane: IES & GATE Point". Use `hook` + 1–2 `card` scenes; keep the total at
30–45 s (check the `duration_s` the script prints).
