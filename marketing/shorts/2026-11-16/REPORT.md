# GATE 2027 Tips: 3 shorts for review (rendered 12 Nov 2026)

For Ritu's review. **Nothing has been booked, scheduled or posted** (no Metricool, no YouTube). `gate90/status.json` was not touched.

All three are 1080x1920, 30 fps, H.264 + AAC, rendered with `tooling/scripts/render_challenge.py` using the
real ElevenLabs voice (the channel voice from `tooling/config.json`). No "Hello Everyone" welcome scene; the header line reads
"GATE 2027 Tips"; nothing on screen says GATE90.

| Short | File | Duration | Size | Cover |
|---|---|---|---|---|
| S1: GATE ME or GATE XE? | `S1_xe_vs_me.mp4` | **62.0 s** (2 s over the 40–60 s target) | 5.9 MB | `S1_cover.jpg` |
| S2: 20-minute mock analysis | `S2_mock_analysis.mp4` | 60.0 s | 5.5 MB | `S2_cover.jpg` |
| S3: Negative marking | `S3_negative_marking.mp4` | **61.1 s** (re-rendered 12 Nov, see end; 1.1 s over the 40–60 s target) | 5.6 MB | `S3_cover.jpg` |

## Wording changes
None. All on-screen text and voice lines are exactly as in the brief (`S1_spec.json`, `S2_spec.json`, `S3_spec.json`).
The minus signs in S3 use the real minus character (U+2212), which the font draws correctly.

## Checks done
- **Frames**: one frame near the end of every scene (all items shown) plus a mid-end-scene and end frame, in `frames/`
  (540 px wide). Looked at every one: no text overflow, overlap or clipping; minus signs and "•" bullets render
  (no empty boxes); header "GATE 2027 Tips"; end pill and URL fit inside their shapes. Some lines were shrunk
  automatically to fit (S2 hook sub "Do this for 20 minutes after every mock", S2 end pill, S1 end URL), all still readable.
- **Audio**: every scene's voice clip is non-silent (mean level −22 to −28 dB). Audio length = video length for all
  three (S1 61.93/61.93 s, S2 59.99/59.97 s, S3 53.97/53.93 s). A listen-check was not possible here, so
  pronunciation (e.g. "X. E.", "P. S. U.", "D. I. G. career thrust") still needs one listen by a person.
- **Covers**: made with `thumbnail.py`, header "GATE 2027 TIPS" (the options from the brief, unchanged). All text fits;
  S3's "NEGATIVE MARKING" is the widest line but has clear margins. (`thumbnail.py` also wrote 16:9 `_thumb.jpg`
  files; not committed since only the covers were asked for.)
- **Renderer change**: `render_challenge.py` got the optional spec fields `welcome`, `series`, `end_voice`, `end_cta`,
  `end_url`. Defaults are unchanged: the Day 22 GATE90 reel spec rendered with `--no-tts` before and after the change
  gives **bit-identical decoded frames** (every frame compared with ffmpeg framemd5), and the frames show "GATE ME 90 Days
  Challenge" and "Comment GATE90 for links" as before.

## YOUTUBE_RULES.md pre-publish check (all three)
1. Original script and point: yes, three different topics, not near-copies of earlier videos. (Layout is the same
   red template as the GATE90 reels; the topics and scenes are different.)
2. Real value: yes (paper comparison, a mock-analysis method, marking rules).
3. No third-party clips, music or images: yes (repo assets only, no music).
4. AI label: YouTube `isAiGeneratedContent` false (stylised graphics + AI narration voice that is not a real person's
   clone); Instagram `isAiGenerated` true when booked.
5. No real person's likeness or cloned voice: yes.
6. Nothing against any religion, caste, community or group: yes.
7. No result/job promises or money/private-contact requests: yes. S2 says "you stop losing marks you already know",
   which is advice, not a guaranteed result.
8. Facts against the official source: **partly; see below.**
9. Title and cover honest, no shocking imagery: yes (cover text matches each video).
10. `madeForKids`: false.

## Things I am unsure of / please check before posting
- **S1 length 62.0 s**, just over the 60 s target. Not trimmed because the brief says to keep the wording exactly.
  If it must be ≤ 60 s, shortening the S1 step-scene voice (e.g. dropping "Many P. S. U. notifications ask for your own
  branch paper.") would bring it to about 58 s.
- **S1 website claims not checked**: `web.digcareerthrust.com/gate-xe` and "one course for every pair" could not be
  opened from this run (the site was blocked by the network here). Please confirm the page exists before posting.
- **S2 "98 GATE ME tests"** is not stated anywhere in this repo; please confirm the number.
- **GATE ME "Engineering Maths 13 / Core 72"**: the official ME paper fixes General Aptitude at 15 marks; the 13-mark
  Engineering Maths share is the usual figure from past papers, not a fixed rule. Same for the XE split (Engineering
  Maths section 15 + GA 15 + two sections of 35 each), which matches the recent GATE XE pattern.
- **S3 marking scheme** (MCQ −1/3 and −2/3; NAT and MSQ no negative marking; MSQ no partial marks) matches GATE
  2024–2026 rules. I could not check the GATE 2027 information brochure itself; the video's voice tells viewers to
  confirm with it, and the footer says "As per the GATE 2027 marking scheme". Please confirm once the brochure is out.
- The end card still shows the Telegram + Website QR codes (from the existing end scene); the brief only asked to
  change the pill text, URL line and voice.

## S3 re-render (wording change, 12 Nov)

Ritu's rule: no guessing in the GATE exam. Only the last scene of `S3_spec.json` ("What To Do", kind `steps`) was
replaced; every other field and scene is unchanged. Re-rendered with `tooling/scripts/render_challenge.py` (real
ElevenLabs voice, same settings as before). Nothing was booked, scheduled or posted. The cover was not changed.

**New file:** `S3_negative_marking.mp4`, 1080x1920, **61.1 s** (was 54.0 s), **5.6 MB** (was 5.0 MB).

**Old wording (last scene)**
- On screen: "Never leave a NAT blank" / "MSQ: answer if fairly sure" / "MCQ: guess after removing 2"
- Voice: "So, never leave a numerical question blank. Type your best answer. In multiple select, answer if you are
  fairly sure. In multiple choice, guess only when you can remove two options."

**New wording (last scene)**
- On screen: "No guessing in GATE" / "MCQ: answer only if sure" / "Solved a NAT or MSQ? Enter it"
- Voice: "So, what should you do? Do not guess in GATE. In multiple choice, a wrong guess takes marks away, so answer
  only when you are sure. In numerical and multiple select questions, if you have solved it, always enter your
  answer. Never leave a solved question blank."

**Checks**
- Frames `frames/S3_scene1–4.jpg`, `S3_end_mid.jpg`, `S3_end.jpg` replaced (540 px wide; one near the end of each
  scene with all items shown, plus mid-end-scene and end). Looked at each: no overflow, overlap or clipping. The third
  step "Solved a NAT or MSQ? Enter it" (longest line) fits inside its pill at a readable size (checked on a full-size
  1080x1920 frame too), so the shorter fallback wording was not needed.
- Minus signs (−1/3, −2/3) render; header reads "GATE 2027 Tips"; nothing on screen says GATE90. On screen, "guess"
  appears only in "No guessing in GATE".
- Audio: every scene's voice clip is non-silent (mean −23 to −26 dB). Scene lengths: hook 6.2 s, table 9.4 s,
  card 14.8 s, steps 20.0 s, end 10.8 s. Audio length 61.09 s = video length 61.10 s.

**Unsure / please check**
- **Length 61.1 s**, 1.1 s over the 40–60 s target, because the new last-scene voice is longer (19.6 s of speech).
  Not trimmed since the wording was given exactly. Dropping "Never leave a solved question blank." (it repeats the
  sentence before) would bring it to about 59 s.
- The voice still says "a wrong guess takes marks away" (as given); on screen the word "guess" only appears in step 1.
- Not listened to by a person here; pronunciation still needs one listen.
