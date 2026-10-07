# Posting: GitHub hosting → Metricool → YouTube Shorts + Instagram Reels

Metricool only takes media from public URLs. Reels are hosted in the public GitHub repo
`saraswatieducation0706-png/deewane-reels` (config `github_repo`) and served from raw.githubusercontent.com.
Metricool copies the video and cover into its own storage when the post is created (tested 7 Oct 2026),
so the GitHub copy is only needed until scheduling succeeds.

## 1. Upload to GitHub

Preferred (Claude cloud session — GitHub traffic goes through the session proxy):
1. Call `add_repo` (owner `saraswatieducation0706-png`, repo `deewane-reels`, access `push`).
2. `git clone --depth 1 https://github.com/saraswatieducation0706-png/deewane-reels <dir>` (long timeout).
3. Housekeeping: `git rm -r` dated folders (YYYY-MM-DD) older than 3 days — never touch `tooling/` or README.
4. Copy into `<dir>/<YYYY-MM-DD>/`: `NN_reel.mp4`, `NN_cover.jpg` for each reel (simple ASCII names, no spaces).
5. Commit as "Deewane Reels Bot <bot@digcareerthrust.com>", `git push origin HEAD`.
   (GitHub Releases are blocked in this session type — use plain commits.)

(The skill's run already cloned this repo for `tooling/`; reuse that clone.)

Public URLs: `https://raw.githubusercontent.com/<repo>/main/<YYYY-MM-DD>/NN_reel.mp4` (same for the cover).
Check each with `curl -sI` → HTTP 200 before scheduling (allow ~1 min after push for raw cache).

## 2. Posting slots

- Get already-booked slots: `getScheduledPosts` (brandId = `metricool_blog_id`, timezone `Asia/Calcutta`,
  from now to +3 days).
- Slot queue, in time order: today 18:00, 20:00, 22:00; then tomorrow 10:00, 12:00, 14:00, 16:00, 18:00,
  20:00, 22:00; then the day after 10:00 … (2-hour steps, 10:00–22:00). Skip any slot already booked.
- Assign reels in posting order (soonest last date first, then most vacancies) to the free slots.
- Rule from Naveen: max 3 reels in the evening (18/20/22); extras go to the next morning from 10:00.
- Drop (don't schedule) a reel if its slot falls less than `min_days_left_at_posting` (1 day) before the
  last date; list it in SUMMARY.md as "too close to last date to post".

## 3. Create the post (one call per reel, both networks together)

`createScheduledPost` with `blogId` = config `metricool_blog_id`, `date` = slot as `YYYY-MM-DDTHH:MM:00+05:30`,
and `info` JSON:

```json
{
  "autoPublish": true, "draft": false, "descendants": [], "firstCommentText": "",
  "hasNotReadNotes": false, "shortener": false, "smartLinkData": {"ids": []},
  "media": ["<raw reel url>"],
  "videoThumbnailUrl": "<raw cover url>",
  "mediaAltText": [],
  "providers": [{"network": "youtube"}, {"network": "instagram"}],
  "publicationDate": {"dateTime": "YYYY-MM-DDTHH:MM:00", "timezone": "Asia/Calcutta"},
  "text": "<description from metadata.md — summary, key facts, official link, 3 DIG links, then hashtags>",
  "youtubeData": {"title": "<YouTube title, ≤ 95 chars, ends with #Shorts if room>", "type": "short",
                   "privacy": "public", "tags": ["<tag>", "..."], "category": "EDUCATION",
                   "madeForKids": false, "isAiGeneratedContent": false},
  "instagramData": {"type": "REEL", "showReelOnFeed": true, "collaborators": [], "isAiGenerated": true}
}
```

- Instagram caption limit 2,200 characters and max 30 hashtags; keep the text under 2,000 characters.
- YouTube tags: list of strings, total ≤ 450 characters.
- `isAiGenerated: true` on Instagram (synthetic voice); `isAiGeneratedContent: false` on YouTube
  (not realistic people/scenes) — Naveen's agreed default.
- Monetization is not settable per post: YouTube uses the channel's Upload defaults (set to On by Naveen in
  YouTube Studio); Instagram has no per-reel switch.
- If the call errors, fix and retry once; if it still fails, record the error and the plannerUrl (if any)
  in SUMMARY.md and leave that reel for manual posting.
- After success, record the returned `plannerUrl` and the provider statuses for each reel.

## 3a. PDF mode — post immediately

When Naveen attached the notification PDF, don't use the slot queue: after upload and the 200 check, call
`createScheduledPost` with `date` = now + 5 minutes (IST, next whole minute) and the same `publicationDate`,
same `info` format as §3. Then confirm with `getScheduledPosts`. If it fails twice, give Naveen the MP4, cover
and metadata to post by hand.

## 4. Verify

Call `getScheduledPosts` for the posting window and confirm every reel appears at its slot with both
`youtube` and `instagram` providers. Put the result table in SUMMARY.md.
