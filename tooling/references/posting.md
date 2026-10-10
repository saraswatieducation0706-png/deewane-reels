# Posting: GitHub hosting → Metricool → YouTube Shorts + Instagram Reels + Facebook Page

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

## 3. Create the post (one call per reel, all three networks together)

`createScheduledPost` with `blogId` = config `metricool_blog_id`, `date` = slot as `YYYY-MM-DDTHH:MM:00+05:30`,
and `info` JSON:

```json
{
  "autoPublish": true, "draft": false, "descendants": [], "firstCommentText": "",
  "hasNotReadNotes": false, "shortener": false, "smartLinkData": {"ids": []},
  "media": ["<raw reel url>"],
  "videoThumbnailUrl": "<raw cover url>",
  "mediaAltText": [],
  "providers": [{"network": "youtube"}, {"network": "instagram"}, {"network": "facebook"}],
  "publicationDate": {"dateTime": "YYYY-MM-DDTHH:MM:00", "timezone": "Asia/Calcutta"},
  "text": "<description from metadata.md — summary, key facts, official link, 3 DIG links, then hashtags>",
  "youtubeData": {"title": "<YouTube title, ≤ 95 chars, ends with #Shorts if room>", "type": "short",
                   "privacy": "public", "tags": ["<tag>", "..."], "category": "EDUCATION",
                   "madeForKids": false, "isAiGeneratedContent": false},
  "instagramData": {"type": "REEL", "showReelOnFeed": true, "collaborators": [], "isAiGenerated": true},
  "facebookData": {"type": "POST", "title": "<YouTube title without #Shorts>"}
}
```

- Facebook Page (added 10 Oct 2026, Naveen's DIG Career Thrust page, Metricool facebookData id 881767725512382):
  use `type: "POST"` (a video post), NOT `"REEL"` — Facebook's Reels API only accepts videos up to 90 s and
  our reels run 95 s–3 min, so REEL would fail at publish time. Vertical video posts still play full-screen.
  `title` = the YouTube title without "#Shorts". Same text and cover as the other networks.
- If a network is disconnected in Metricool (getBrandSettings → networksData has no instagramData /
  facebookData / youtubeData), schedule on the networks that are connected, and say at the top of SUMMARY.md
  which network is disconnected so Naveen can reconnect it.
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
same `info` format as §3 (YouTube + Instagram + Facebook). Then confirm with `getScheduledPosts`. If it fails twice, give Naveen the MP4, cover
and metadata to post by hand.

## 4. Verify

Call `getScheduledPosts` for the posting window and confirm every reel appears at its slot with
`youtube`, `instagram` and `facebook` providers. Put the result table in SUMMARY.md.

## 5. Nightly posting check (Naveen, 10 Oct 2026)

Runs every night at ~22:20 IST, after the day's last post (22:00). Goal: every reel is live on **YouTube, Instagram
and the Facebook Page**; anything that failed is re-posted the next day at an in-between time.

1. `getBrandSettings` — note which networks are connected (`networksData`: youtubeData, instagramData, facebookData).
2. `getScheduledPosts` (brandId 7269466, timezone Asia/Calcutta) from **now − 48 h to now** (results are large —
   save to a file and parse with Python; the list includes already-published posts with per-network status).
   Also fetch **now → now + 48 h** to know the times already booked.
3. A post "failed" on a network when its provider status is `ERROR`, or it is still `PENDING`/`PUBLISHING`
   more than 30 minutes after its publication time. Ignore drafts (`draft: true`) and test posts.
4. Group by reel (same `media[0]` URL). A reel is **missing on a network** if NO post with that media URL has
   `PUBLISHED` on that network (a later re-post may already have fixed it — then do nothing).
   Skip a reel/network if a future post with the same media + network is already booked (re-post pending).
   Skip a reel/network that already failed twice for the same network (≥ 2 ERRORs) — list it for Naveen to post
   by hand instead of looping.
   Skip job reels whose last date is less than 1 day after the new slot ("too close to last date").
5. Re-post slots — **tomorrow**, at in-between times that never coincide with the regular slots
   (10/12/14/16/18/20/22, GATE90 08:00) or anything already booked: try 11:00, 13:00, 15:00, 17:00, 19:00, 21:00,
   then 11:30, 13:30, 15:30, 17:30, 19:30, 21:30, then 10:30, 12:30, 14:30, 16:30. A slot is free only if no
   booked post is within 10 minutes of it. Oldest failures first.
6. For each missing reel: `createScheduledPost` with **only the missing network(s)** in `providers`, same `media`,
   `videoThumbnailUrl`, text and network data as the original post (from the getScheduledPosts record; for
   Facebook use type "POST" if the reel is > 90 s, "REEL" otherwise — job reels are always "POST"). Remove any
   "UNVERIFIED"/"could not verify" line from old captions. Keep `youtubeData` as is, but drop `notifySubscribers`.
7. If a network is disconnected in step 1, still book the re-posts (Naveen usually reconnects quickly) but put
   "RECONNECT <network> in Metricool" first in the report.
8. Report: if anything failed, send Naveen a push notification (PushNotification tool via ToolSearch):
   "Posting check: N reels re-booked for tomorrow (…list: reel → network → time). Reconnect: <network> (if any)."
   If everything was published, finish with one line "All reels posted on YouTube, Instagram and Facebook" and do not
   send a push.
