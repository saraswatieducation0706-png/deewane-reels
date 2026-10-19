# GATE ME 2027 Test Series — production procedure

Paid test series sold by Naveen Yadav (Dig Career Thrust). Blueprint, coverage plan and quality bar were agreed on
19 Oct 2026. **Test questions, answer keys, test JSON and Word/PDF outputs are paid content: never commit them to
this public repo.** They go to the PRIVATE repo `saraswatieducation0706-png/gate-me-ts-files` and to Google Drive.

## Fixed facts
- Series: 40 topic tests (TT01–TT40), 13 full-subject tests (ST01–ST13), 15 full-length mocks (FLT01–FLT15),
  12 formula-note PDFs. Topic lists and question counts per topic: `tooling/plan.json`
  (`topics[*].tt_q` = questions in its topic test, `st_q` = in its subject test, `mocks` = 0-based mock indices it
  must appear in; `tts[*].no` = TT number). Subject test order ST01–ST13: GA, EM, MEC, SOM, TOM, MD, MAT, FM, HT, TD, APP, MFG, IE.
  Mock section split per subject: `MOCK_SLOTS` in `tooling/register.py` (1-mark, 2-mark questions).
- Queue of batches (one batch per run): `queue.json`; progress: `status.json` (`done`, `drive_saved`).
- Drive root "GATE ME 2027 Test Series Course" `1_Y3Cj-AT31PcyF0a4Q8fpNXcPikDWaPG`:
  01 Topic Tests `1NXc7zhvfoN57iOuU8pmd9zOOOoEOfbiq` · 02 Subject Tests `16dXs-DXJzrYts5A8pbGcJpwUdFQHeMf4` ·
  03 Full-Length Mocks `1BLtHgJsaJcOh1M2x7gpyUz4hINC10DEr` · 04 Formula Notes PDFs `1GfSHTKL4CYvXhrW6VCTH5-Iy1OZ2k2Zy` ·
  00 Planning `11q1hDm-AX6UOVZXhPcUy2xL2fkob8kce` · 99 Question source files `1wZLZqV0h6BJtpdnrSc-s9w7maZdGymYh`.
- Drive copy: Make scenario **8054068** ("GATE ME TS – copy file from private repo to Drive"), run with
  `scenarios_run` (responsive true) and data `{path, folder_id, file_name}` where `path` is the file's path inside
  gate-me-ts-files, URL-encoded with Python `urllib.parse.quote(path)` (spaces, & etc.). Tested OK with TT12 on 19 Oct. One run per file. Never upload files through the Drive connector as
  base64 (far too costly).

## Question rules (every test)
- Topic and subject tests: 33 Q = Q1–16 one-mark + Q17–33 two-mark = 50 marks, 90 min.
  Mix: 21 MCQ + 4 integer + 8 fill_ups, numericals spread over both halves (about 5 in the 1-mark half).
  Exception: GA Verbal (TT01) is all MCQ, as in GATE.
- Mocks: 65 Q, 100 marks, 30 one-mark + 35 two-mark. Section A = General Aptitude 10 Q (5×1 + 5×2, ~2 numerical);
  Section B = Technical 55 Q (Maths 5×1 + 4×2, core per MOCK_SLOTS), about 20 numerical in B. Topics for mock k
  = every topic whose `mocks` list contains k-1 (repeat appearances need a new set-up, never the same question).
- MCQ: 4 options, 1 correct, negative 0.33 (1-mark) / 0.67 (2-mark). integer: whole-number answer, 0 negative.
  fill_ups: `range [lo, hi]` about ±0.5–1 % of the exact value, question says "round off to N decimal places", 0 negative.
- Difficulty a notch above GATE: ~25 % GATE-level (one concept, non-textbook set-up), ~50 % GATE+ (two linked
  concepts or a hidden condition), ~25 % advanced (three steps across topics). No pure formula substitution.
  1-mark ≤ 2 min, 2-mark ≤ 4 min to solve. Distractors come from real mistakes (units, end conditions, sign
  convention, gauge vs absolute, factor of 2). Stay inside the GATE ME syllabus; give any table data needed.
- Solution text (one paragraph): "Concept: … Steps: … (equations with units) … Answer: … Trap: …" — no topic IDs,
  no tags, no "[T0xx]".
- Figures wherever geometry/loading/flow carries information (~20 % of core questions; more in Mechanics, SOM,
  TOM, FM): matplotlib with `gate90/tooling/figlib.py`, clean black line drawings, labelled, no answer leaks.
  Render all figures into one contact sheet and LOOK at it before building.
- Freshness: no question may repeat one already in the series or in GATE90. Before writing, read the private
  repo's `src/*.json` for the same subject and skim `gate90/content/*_practice.json` for the same topic.
- Verify EVERY numerical answer and every MCQ key in Python with asserts (see `tooling/example_verify_TT12.py`).
  Quality bar: TT12 (`src/TT12.json` in the private repo; figures `tooling/example_figs_TT12.py`).
- Math: `\(...\)`, no space just inside the delimiters, powers with braces (`\cos^{2}30°`, not `\cos^230°`).

## Formula notes (PDF per subject)
- Subjects: EM (Engineering Mathematics, plus a 2-page GA quantitative-formula appendix), MEC, SOM, TOM, MD, MAT,
  FM, HT, TD, APP, MFG, IE. File name `GATE ME Formula Notes - <Subject name>.pdf`.
- Every formula card: formula (typeset), symbol table (symbol | meaning | SI unit), units to substitute and
  conversions that catch students, assumptions of the derivation, valid when / not valid when, a figure where it
  aids understanding, common traps. A4 portrait, 2–3 cards per page, contents page, QR codes page last
  (website web.digcareerthrust.com/login and app play.google.com/store/apps/details?id=co.jack.iurlk).
- The first notes batch builds `tooling/build_notes.py` (commit it here; content JSON goes to the private repo),
  renders pages to PNG and looks at them. Send that first PDF for Naveen's approval in the final message.

## A run (one batch)
1. Clone this repo (and run `add_repo` for gate-me-ts-files with access "push", then clone it to ~/gate-me-ts-files).
   If gate-me-ts-files cannot be attached, keep outputs locally, send them with SendUserFile, and push-notify
   Naveen: "GATE ME TS: Drive save failed for <items> — private repo not reachable."
2. Read `queue.json` + `status.json`; the batch to make = the first batch with any item not in `done`
   (catch-up is automatic if a run was missed). Make every item of that batch not yet done.
3. For each test: write `src/<ID>.json` + `src/<ID>_figs.py` (private repo), verify, build with
   `python3 tooling/build_ts.py src/<ID>.json "out/<file name>" <figdir> GATEMETS:<ID>` (mocks: add `--mock`),
   check with pandoc (counts of correct/incorrect, integer, fill_ups; marks), render one page to PNG and look.
   File names: `GATE ME TS - TTnn - <title>.docx`, `GATE ME TS - STnn - <subject>.docx`,
   `GATE ME TS - FLTnn - Section A - General Aptitude.docx` and `GATE ME TS - FLTnn - Section B - Technical.docx`.
4. Commit outputs + sources to gate-me-ts-files (`out/`, `src/`) and push (fetch + rebase first).
5. Copy every new output file to its Drive folder with Make scenario 8054068 and also the `src/<ID>.json` to
   folder 99. Check each run's status; on any failure retry once, then push-notify Naveen naming the files that
   did not reach Drive. Add each saved file to `status.json` `drive_saved`.
6. Add finished IDs to `status.json` `done`; commit and push this repo (fetch + rebase first).
7. Send each finished Word/PDF file with SendUserFile (status proactive) as a backup.
8. Finish with one short message: items made, Drive status, anything that failed. Do not touch GATE90 files.
