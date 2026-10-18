# Christ's Blessings — weekly automation runbook

Channel: "Christ's Blessings" (YouTube `UCfIz3Cf_fpfaNhHe0LiQOqw`), mostly US/UK/Canada/Australia viewers.
Owner: Naveen. Lane: comfort and prayer for everyday struggles (anxiety, sleep, grief, tiredness, decisions,
fresh starts), plus Bible stories explained simply. Non-denominational. Scripture: **KJV only**.

Every week = 7 Shorts (one per day) + 2 long videos (a guided prayer and a Bible story).
Two scheduled tasks run this runbook:

| Task | When (IST) | Job |
| --- | --- | --- |
| Weekly scripts | Wednesday ~19:50 | Write next week's scripts, put them in a Claude Doc for Naveen, notify him |
| Weekly production | Saturday ~09:50 | Apply Naveen's edits, render, upload, schedule in Metricool, check last week's posts |

## 0. Setup (every run)
1. `add_repo` saraswatieducation0706-png/deewane-reels (access push), then
   `git clone --depth 1 https://github.com/saraswatieducation0706-png/deewane-reels ~/deewane-reels` (10-min timeout).
   `CB=~/deewane-reels/christs-blessings`, tools in `$CB/tooling`.
2. ElevenLabs key: given in the task prompt. `export XI=<key>`. Never print it or commit it.
3. `pip install fonttools --break-system-packages -q` is not needed (fonts are committed). Check `ffmpeg` exists.
4. `config.json` holds the voice (`grmNvOIiKqGVQEIGb9XO`, Naveen's "Crist's Blessings" ElevenLabs voice),
   Metricool brand id `7503136`, timezone.

"Next week" = the Monday after the run date. `python3 $CB/tooling/slots.py <monday>` prints the IST posting
times (Shorts 07:00 US Eastern daily; long videos 20:00 US Eastern on Wednesday and Saturday). The script
handles US daylight-saving changes.

## 1. Weekly scripts task
1. Read `$CB/topics_log.json` (everything already covered) and `$CB/weeks/` (last two weeks' files).
2. Performance check: Metricool `getAnalyticsAvailableMetrics` / `getAnalyticsDataByMetrics` for brand 7503136
   (YouTube) over the last 14 days. Note the 2 best and 2 worst Shorts by views and the long video watch time.
   Lean next week's topics toward what worked. If analytics are unavailable, carry on.
3. Plan next week:
   - 7 Short themes, no theme or verse used in the last 14 days; rotate templates A–E so no template appears
     on two days in a row (A dawn/sunrise lake, B illustrated hills or forest path, C gold text on dark,
     D candle, E parchment "pray with me"). Scenes: `dawn_lake`, `sunrise_lake`, `hills_sunset`, `forest_fork`,
     `dark_gold`, `candle`, `parchment`.
   - long1 (Wednesday ET) = a guided prayer (sleep, anxiety, morning, healing of the heart, gratitude…), about
     25–30 min including a 15–18 min music-only tail when it is a sleep prayer.
   - long2 (Saturday ET) = a Bible story explained, 10–14 min: the story, its background, 3–4 lessons, a prayer.
   - Advent override (see §5).
4. Write each Short exactly in the Week 1 structure (see `weeks/2026-10-19/shorts.json`): hook (honest, one
   sentence), ref ("Book N, verse M."), verse (KJV, word for word), reflection (original, 50–70 words, concrete),
   prayer (one or two sentences, ends "Amen."), close (gentle; invite prayer requests or a share). 110–150 words.
   Title ≤ 70 chars, description with the reference "(KJV)", 4 hashtags, 6 tags, a cover of 2–3 words.
5. **Verify every verse** against a KJV source with WebFetch (e.g. kingjamesbibleonline.org or biblegateway
   KJV). Fix any wording difference. Never paraphrase inside the "verse" segment.
6. Long scripts: write `weeks/<monday>/long1_script.txt` and `long2_script.txt` in the format read by
   `tooling/script_to_spec.py` (see Week 1 files): `## Chapter | scene`, `[pause]` (6 s), `[long pause]`
   (10 s), a paragraph ending `| scene` switches scenery. Scenes for long videos: `night_lake` (sleep),
   `galilee_dusk`, `storm` (rain added), `calm_dawn`, `sunrise_lake`, `dawn_lake`, `hills_sunset`, `candle`,
   `parchment`, `dark_gold`. Sleep prayers end with
   `## Quiet music for sleep | night_lake | music_only=1080 | dim=0.45 | card=Rest in His peace`.
   Add `long.json` with title, thumbnail big text (≤ 3 words) + small line, description (with the wellbeing
   line for sleep/anxiety videos), tags, hashtags.
7. Commit the week folder (`git -c user.name="Christ's Blessings Bot" -c user.email=bot@digcareerthrust.com`),
   rebase on origin/main, push.
8. Make a Claude Doc "Christ's Blessings — Week of <Mon d Mon>" (docs tools) with: the posting schedule, then
   every Short (title, script, description) and both long scripts. At the top: "Edit anything directly. To
   stop a video, write HOLD in its heading. Production runs Saturday morning; no reply needed."
9. Send Naveen a push notification: "Next week's Christ's Blessings scripts are ready for review: <doc link>.
   Production runs Saturday morning." (PushNotification via ToolSearch.)

## 2. Weekly production task
1. Find next week's folder `weeks/<monday>/`. If it is missing (scripts task failed), run §1 steps 1–7 now.
2. Read the week's Claude Doc (docs tools `read`). Apply Naveen's edits to `shorts.json` / the long scripts.
   Any video whose heading contains HOLD is skipped (list it in the report). Re-verify edited verses.
3. Render:
   - Shorts: `cd $CB/tooling && python3 render_week_shorts.py ../weeks/<monday>` (≈1 min each).
   - Long: `python3 script_to_spec.py ../weeks/<monday>/long1_script.txt <abs out mp4> '<json>'` with
     `{"intro": "<title>", "subtitles": "dim", "seed": <n>, "music_key": "D", "music_db": -16, "lufs": -20}` for
     sleep prayers, `{"subtitles": "normal", "music_db": -23, "lufs": -16}` for stories; then
     `python3 render_long.py <spec>` (≈1.3× real time — run in the background, long timeouts).
   - Thumbnails: `python3 make_thumb.py <out.jpg> <scene> "<big>" "<small>" <seed>`.
   - Check 3–4 frames of every video (`ffmpeg -ss <t> -i x.mp4 -frames:v 1 f.png`, then look at them):
     no text overflow, captions readable. Re-render if not.
4. Upload: copy final MP4s + thumbnails to `$CB/media/<monday>/`, commit, push. Files must be < 95 MB
   (GitHub limit); if a long video is bigger, re-encode with `-crf 30 -maxrate 1200k`. Check each raw URL
   `https://raw.githubusercontent.com/saraswatieducation0706-png/deewane-reels/main/christs-blessings/media/<monday>/<file>`
   returns 200 with the right content-length before scheduling.
   Delete `media/` folders older than 14 days in the same commit (Metricool keeps its own copy).
5. Schedule with Metricool `createScheduledPost` (blogId `7503136`), one call per video, using the IST times from
   `slots.py` (`date` = `<time>+05:30`, `publicationDate.timezone` = `Asia/Calcutta`). Format used in Week 1:
   ```json
   {"autoPublish": true, "draft": false, "descendants": [], "firstCommentText": "", "hasNotReadNotes": false,
    "shortener": false, "smartLinkData": {"ids": []}, "media": ["<raw mp4 url>"], "mediaAltText": [],
    "providers": [{"network": "youtube"}],
    "publicationDate": {"dateTime": "<YYYY-MM-DDTHH:MM:SS>", "timezone": "Asia/Calcutta"},
    "text": "<description incl. hashtags>",
    "youtubeData": {"title": "<title>", "type": "short" | "video", "privacy": "public", "tags": [...],
                    "category": "PEOPLE_BLOGS", "madeForKids": false, "isAiGeneratedContent": false}}
   ```
   Long videos: `type: "video"`, add `videoThumbnailUrl` = raw thumbnail URL. If Metricool rejects the
   thumbnail (VIDEO_THUMBNAIL_NOT_APPLICABLE — channel not verified for custom thumbnails), retry without it
   and tell Naveen to verify the channel at youtube.com/verify. Long video descriptions include the chapter
   list from `<out>_chapters.txt`.
   `isAiGeneratedContent` stays false while visuals are stylised illustrations (not realistic people or
   events); set it true for any video showing realistic AI-made people or scenes.
6. Confirm with `getScheduledPosts` (brand 7503136, next 8 days) that every video is booked once **and at the
   requested IST time**. Metricool's servers run on Madrid time and shift posts by ±1 hour near the European
   clock changes (last Sunday of March and October): on 25 Oct 2026 a 05:30 IST booking was stored as 06:30,
   and 05:29 as 04:29. If a stored time is off, update the post and re-check; any time between 18:00 and 22:00
   US Eastern is acceptable for long videos, 06:00–08:00 US Eastern for Shorts.
7. Posting check for the past 7 days: `getScheduledPosts` (now − 7 days → now). Any post with provider status
   ERROR, or still PENDING/PUBLISHING > 30 min after its time, and not live elsewhere: re-book it once at the
   next free 2-hour gap before Tuesday. Never post a video twice.
8. Append next week's entries to `topics_log.json`, commit, push.
9. Push notification to Naveen: "Christ's Blessings: next week booked — 7 Shorts + 2 long videos (list any HOLD or
   failures)." If everything failed, say what failed in one line.

## 3. Content rules (YouTube policies)
- Every script carries an original reflection; never a bare reading over a background (inauthentic-content
  policy). Vary templates, scenes, music keys and seeds week to week.
- No fear or guilt bait ("God's warning", "don't skip", "if you ignore this"), no prophecies, no miracle or
  money promises, no claims to cure anything. Titles and thumbnails must match the content.
- Sleep/anxiety videos: spiritual comfort only, and the description includes: "This prayer is not a substitute
  for professional care. If you are struggling, please reach out to someone you trust or a local helpline."
- Not made for kids. No artist music (the music is generated by `cb_common.music_loop`). No film clips.
- Long video descriptions end with: "We will never ask you for money or to message us privately."

## 4. Things only Naveen can do in YouTube Studio (remind once if not done)
Banner and About text (in the Week 1 doc), playlists, comment filter (hold potentially inappropriate comments;
blocked words: whatsapp, telegram, crypto, bitcoin, investment, forex, contact me, text me, +1), 2-step
verification, channel verification for custom thumbnails, monetization status under Earn.

## 5. Advent "24 Days to Christmas" (2026)
- Week of Mon 23 Nov: normal Shorts Mon–Sat. That week's long2 (Sat 28 Nov 20:00 ET = Sunday 29 Nov morning
  IST) is the Hope Sunday kickoff: "Advent Begins: Waiting with Hope" (Isaiah 40:31). Sunday 29 Nov Short:
  "Advent starts today" teaser.
- 1–24 Dec: the daily Short is the Advent Short for that day (opener "Day N of 24 Days to Christmas"; scene
  rotation as usual). Topics/scriptures:
  1 Isaiah 9:2 · 2 Isaiah 11:1-2 · 3 Isaiah 7:14 · 4 Micah 5:2 · 5 Isaiah 40:1-2 · 6 Isaiah 9:6 (Peace Sunday) ·
  7 Luke 1:13 · 8 Luke 1:24-25 · 9 Luke 1:37 · 10 Luke 1:38 · 11 Luke 1:46-49 · 12 Matthew 1:20-24 ·
  13 Luke 2:10 (Joy Sunday) · 14 Luke 2:4-5 · 15 Luke 2:7 · 16 Luke 2:8-9 · 17 Luke 2:13-14 · 18 Luke 2:19 ·
  19 Luke 2:29-32 · 20 John 3:16 (Love Sunday) · 21 Luke 2:36-38 · 22 John 1:14 · 23 John 1:5 · 24 Luke 2:11.
- Long videos in December: Peace Sunday (Isaiah 9:6), Joy Sunday (Luke 2:10), Love Sunday (John 3:16) — each
  booked Saturday 20:00 ET; the midweek long video stays a guided prayer (Christmas-themed). Christmas Day long
  video: "The Christmas Story, Read Slowly" (Luke 2:1-20) with a family prayer, booked 24 Dec 20:00 ET.
- Scripts for Advent weeks are still written the Wednesday before, as usual.
