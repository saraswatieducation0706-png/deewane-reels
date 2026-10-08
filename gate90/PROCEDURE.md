# GATE ME 90 Days Challenge: run procedure

Owner: Naveen Yadav (Deewane: IES & GATE Point / Dig Career Thrust). Approved samples: Day 1 (8 Oct 2026).
This file is read by the scheduled runs. Never put API keys or tokens in this public repo.

## Fixed facts
- Day 1 = Mon 19 Oct 2026, Day 90 = Sat 30 Jan 2027. Mon–Sat only; Sundays free. GATE 2027 starts 6 Feb 2027.
- Master Schedule (Google Sheet, source of truth for each day's topic): id `1pzAT-8WSAPDq7h9zYl1S03Z4oJWRGLach9_dA2f5-J8`
  (columns: Day, Date, Phase, Subject, Topic, Topics covered, Test type, Test Qs, Test duration (min), Days to GATE, Reel title, Test link, …).
  Read it with Drive `read_file_content`.
- Drive folder "GATE ME 90 Days Challenge" `1gWCUtcZa6GSIdXFOdpf2ZTmeWRM478JF`; toppers folder "04 Toppers" `1TI1IY4uL_sTo-GfPDYQegkETSnG8Fqnm`.
- Public links: practice PDF `https://raw.githubusercontent.com/saraswatieducation0706-png/deewane-reels/main/gate90/pdfs/Day{N}_Practice.pdf`
  (Make.com posts it to Telegram at 8 AM — it MUST exist before 8 AM on Day N). Reels and covers go in `gate90/reels/`.
- Metricool brand (blogId) `7269466`, timezone `Asia/Calcutta`. Networks: YouTube Short + Instagram Reel.
- Status file: `gate90/status.json` (`produced`, `test_delivered`, `reel_scheduled` = lists of day numbers).
- Course (₹1, enrol once, all 90 tests): https://iurlk.courses.store/909124 . Test windows: topic/weekly/revision tests open 7–9 PM (60 min to attempt), full mocks 7–11 PM (180 min).
- Accuracy is checked by Naveen's team, but still verify every numerical answer with Python before building.

## Setup (every run)
1. `add_repo` saraswatieducation0706-png/deewane-reels (push); `git clone --depth 1 https://github.com/saraswatieducation0706-png/deewane-reels ~/deewane-reels` (10-min timeout).
2. For reel runs: export the ElevenLabs key exactly as the `deewane-job-reels` skill's set-up step says (never print it, never commit it).
3. `pip install --break-system-packages -q weasyprint` if `import weasyprint` fails. ffmpeg and pandoc are needed.
4. Commit as "Deewane Reels Bot <bot@digcareerthrust.com>"; before pushing: `git fetch origin main && git rebase origin/main`.

## A. Production run (content for days not yet produced)
Goal: stay well ahead of the calendar until all 90 days are produced. Per run, produce the next unproduced days in
order: up to **3 days**, or **1 day** if it is a full-length mock (65 questions). Stop when all 90 are in `produced`.

For each day N (row N of the Master Schedule):
1. **Test** (private, Word): `Test Qs` questions, single-correct MCQs with exactly 4 options.
   - 20-question days: Q1–10 are 1 mark (negative 0.33), Q11–20 are 2 marks (negative 0.67); total 30 marks.
   - Weekly test (Saturday): 4 questions on each of the week's 5 topics. Revision days: spread over the subjects named.
   - Full-length mock (65 Q, 100 marks): GA 10 (5×1 + 5×2), Engineering Mathematics ≈ 13 marks, the rest core ME
     across all subjects in GATE weightage; 30 one-mark + 35 two-mark questions in total, 1-mark questions first.
   - GATE-level, moderate to hard; plausible distractors; 1–3 sentence solution stating the principle.
   - Math as `\( ... \)`; diagrams with `gate90/tooling/figlib.py` (pin = triangle + hatched ground, roller = triangle on
     circles, fixed = hatched wall, double-headed dimension arrows, labels never overlapping lines). Look at every figure.
   - JSON as in `build_test.py`'s docstring; build: `python3 gate90/tooling/build_test.py test.json "Day N - Test - <Topic>.docx" <figdir> GATE90:D{N}`.
   - Check: pandoc round-trip shows one `correct` per table and the right counts; render to PDF and look at a page.
   - **Never commit test questions or test JSON to this public repo.**
2. **Practice set** (public PDF): 15 questions (mix of MCQ and NAT; mocks: 15 mixed-subject), all different from the
   test, with step-by-step solutions (Concept, steps, answer, exam tip) and solution FBDs where useful.
   - JSON format: `gate90/content/day01_practice.json` (copy its structure, fill day/subject/topic/days_to_gate/summary/
     minutes/test_qs/test_minutes/test_marking/next_day from the sheet; next_day "" on Day 90; for mocks test_minutes 180).
   - Build: `python3 gate90/tooling/build_practice_pdf.py dayNN_practice.json <figdir> gate90/pdfs/Day{N}_Practice.pdf`
     and look at the rendered pages (pdftoppm) for overflow or broken figures.
   - Commit the PDF, `gate90/content/dayNN_practice.json` and the figure script.
3. Freshness: before writing, skim the previous days' `gate90/content/*_practice.json` for that subject and avoid
   repeating the same set-ups or numbers.
4. Deliver: send each test .docx to Naveen with SendUserFile (status proactive), one line saying which day and that
   it is ready for his team's check and website upload. Add N to `produced` and `test_delivered`; push.
5. If anything fails, push what is complete and send a push notification naming the day and the problem.

## B. Reel run (each study-day evening, after the test)
1. Today (IST) = test day P; N = the next study day (P+1; Saturday → Monday's day). If N > 90 or N is already in
   `reel_scheduled`, stop. Read row N (and row P) from the Master Schedule.
2. Toppers of Day P: the website cannot export results, so Naveen uploads a **screenshot of the rank list** to the
   Drive folder 04 Toppers, titled `Day{P}_Toppers` (png/jpg; several screenshots allowed: `Day{P}_Toppers_2` …).
   Read it with Drive `read_file_content`; if names or marks are unclear, download it (`download_file_content`),
   decode to a file and look at the image. Take everyone with rank 1–3 (ties share a rank; include all tied).
   Marks as shown ("x/30", or "x/100" for mocks). Photos are optional: toppers send them to Naveen, who uploads them
   as `Day{P}_<Student Name>.jpg/png`; match by name. No photo → leave the photo out (the renderer draws a blank
   circle). Spell names exactly as on the screenshot. No screenshot by run time → make the reel without the toppers
   scene (no apology, no mention).
3. Write `spec.json` for `tooling/scripts/render_challenge.py` (scene kinds: `tooling/references/scene_kinds.md`, plus
   `toppers`): see `gate90/content/day01_reel_spec.json` for the pattern.
   - `footer`: "Day N/90  •  <Days to GATE> days to GATE 2027". Never show calendar dates in the reel.
   - Scenes: hook ["DAY N/90", short subject or "GATE ME"] + a motivating sub; card "Today's Topic" (subject, topic);
     steps "Cover Today" (3–4 items from Topics covered, ≤ 30 chars each); card "Quick Tip" (one high-yield fact, 3 lines);
     dates "Today's Plan" (Practice PDF → "Telegram, now"; "Test (₹1 course)" → "7 to 9 PM"; Toppers → "Next reel"; on mock
     days the test line is "Mock (₹1 course)" → "7 to 11 PM" and the voice mentions 65 questions, 3 hours). The practice
     PDF is free; tests are in the "GATE ME 90 Days Challenge" course (₹1, enrol once). Never call the test "free";
     never use the word "free" for anything but the practice PDF;
     LAST: `toppers` scene, title "Day P Toppers", voice congratulating them by name (ranks, shared ranks).
   - Voice: English, "GATE M. E.", numbers in words where natural; ≤ 30 words per scene.
   - Render, check 3 frames, then `tooling/scripts/thumbnail.py <dir>/DayN --org "GATE ME" --big "DAY N/90" --line "<Topic>" --badge "Test Tonight 7 PM" --badge2 "<X> Days to GATE"`.
4. Copy `DayN_reel.mp4` + `DayN_cover.jpg` to `gate90/reels/`, delete reels of days older than N−3 from that folder,
   push, wait for raw URL HTTP 200.
5. `createScheduledPost` for Day N's date at 08:00 (+05:30), YouTube Short + Instagram Reel, exactly like the Day 1
   post (title "Day N/90 | <Topic> | GATE ME 90 Days Challenge #Shorts" ≤ 95 chars; description = day line, topic,
   today's plan (free practice PDF on Telegram; test window 7–9 PM, mocks 7–11 PM, in the ₹1 "GATE ME 90 Days Challenge"
   course), "Comment GATE90 to get all the links", the course link if `course_link` is set in gate90/status.json, the 3
   links, hashtags; YouTube category EDUCATION, madeForKids
   false, isAiGeneratedContent false; Instagram REEL, isAiGenerated true). Confirm with `getScheduledPosts`.
6. Add N to `reel_scheduled`, push. Push-notify Naveen only if something failed (reel not booked by 2 AM = he posts by hand).
