# Posting: GitHub hosting → Metricool → YouTube (16:9 job videos) + Instagram & Facebook (9:16 teasers)

**Job notifications (from 27 Oct 2026): each video = a 16:9 YouTube video + a 9:16 teaser on Instagram and the
Facebook Page — two Metricool posts at the same slot (§3). See `job_videos.md`. GATE90 reels keep the old
single-post format (YouTube Short + Instagram Reel + Facebook) described in gate90/PROCEDURE.md.**

**Before booking any reel, follow `/YOUTUBE_RULES.md` (repo root) and run its pre-publish check.**

Metricool only takes media from public URLs. Reels are hosted in the public GitHub repo
`saraswatieducation0706-png/deewane-reels` (config `github_repo`) and served from raw.githubusercontent.com.
Metricool copies the video and cover into its own storage when the post is created (tested 7 Oct 2026),
so the GitHub copy is only needed until scheduling succeeds.

## 1. Upload to GitHub

Preferred (Claude cloud session — GitHub traffic goes through the session proxy):
1. Call `add_repo` (owner `saraswatieducation0706-png`, repo `deewane-reels`, access `push`).
2. `git clone --depth 1 https://github.com/saraswatieducation0706-png/deewane-reels <dir>` (long timeout).
3. Housekeeping: `git rm -r` dated folders (YYYY-MM-DD) older than 3 days — never touch `tooling/` or README.
4. Copy into `<dir>/<YYYY-MM-DD>/`: `NN_video.mp4`, `NN_thumb.jpg`, `NN_teaser.mp4`, `NN_cover.jpg` for each job
   video (simple ASCII names, no spaces; roundup uses NN = `roundup`).
5. Commit as "Deewane Reels Bot <bot@digcareerthrust.com>", `git push origin HEAD`.
   (GitHub Releases are blocked in this session type — use plain commits.)

(The skill's run already cloned this repo for `tooling/`; reuse that clone.)

Public URLs: `https://raw.githubusercontent.com/<repo>/main/<YYYY-MM-DD>/NN_video.mp4` (same pattern for the others).
Check each with `curl -sI` → HTTP 200 before scheduling (allow ~1 min after push for raw cache).

## 2. Posting slots

- Get already-booked slots: `getScheduledPosts` (brandId = `metricool_blog_id`, timezone `Asia/Calcutta`,
  from now to +3 days).
- Slot queue, in time order: today 18:00, 20:00, 22:00; then tomorrow 10:00, 12:00, 14:00, 16:00, 18:00,
  20:00, 22:00; then the day after 10:00 … (2-hour steps, 10:00–22:00). Skip any slot already booked.
- **Sunday:** the apprentice/contract roundup takes Sunday 18:00; permanent videos follow from 20:00.
- Assign videos in posting order (biggest / national first, then soonest last date, then most vacancies) to the
  free slots. One slot = one 16:9 video + its teaser.
- Rule from Naveen: max 3 videos in the evening (18/20/22); extras go to the next morning from 10:00.
  Permanent notifications beyond the free slots are carried over (not written to the tracker).
- Drop (don't schedule) a reel if its slot falls less than `min_days_left_at_posting` (1 day) before the
  last date; list it in SUMMARY.md as "too close to last date to post".

## 3. Create the posts (TWO posts per job video, same slot)

`createScheduledPost` with `blogId` = config `metricool_blog_id`, `date` = slot as `YYYY-MM-DDTHH:MM:00+05:30`.

**Post A — YouTube (16:9 video)**
```json
{
  "autoPublish": true, "draft": false, "descendants": [], "firstCommentText": "",
  "hasNotReadNotes": false, "shortener": false, "smartLinkData": {"ids": []},
  "media": ["<raw NN_video.mp4 url>"],
  "videoThumbnailUrl": "<raw NN_thumb.jpg url, or the vidIQ AI thumbnail imageUrl>",
  "mediaAltText": [],
  "providers": [{"network": "youtube"}],
  "publicationDate": {"dateTime": "YYYY-MM-DDTHH:MM:00", "timezone": "Asia/Calcutta"},
  "text": "<YouTube description from metadata.md — summary, chapters, key facts, official link, 3 DIG links, 3–5 hashtags>",
  "youtubeData": {"title": "<vidIQ-optimised title, ≤ 100 chars, no #Shorts>", "type": "video",
                   "privacy": "public", "tags": ["<tag>", "..."], "category": "EDUCATION",
                   "madeForKids": false, "isAiGeneratedContent": false}
}
```

**Post B — Instagram + Facebook (9:16 teaser, 30–45 s)**
```json
{
  "autoPublish": true, "draft": false, "descendants": [], "firstCommentText": "",
  "hasNotReadNotes": false, "shortener": false, "smartLinkData": {"ids": []},
  "media": ["<raw NN_teaser.mp4 url>"],
  "videoThumbnailUrl": "<raw NN_cover.jpg url>",
  "mediaAltText": [],
  "providers": [{"network": "instagram"}, {"network": "facebook"}],
  "publicationDate": {"dateTime": "YYYY-MM-DDTHH:MM:00", "timezone": "Asia/Calcutta"},
  "text": "<teaser caption from metadata.md>",
  "instagramData": {"type": "REEL", "showReelOnFeed": true, "collaborators": [], "isAiGenerated": true},
  "facebookData": {"type": "REEL", "title": "<YouTube title>"}
}
```

- The teaser is never posted to YouTube, and the 16:9 video is never posted to Instagram/Facebook.
- Facebook Page (Metricool facebookData id 881767725512382): teasers are ≤ 90 s, so `type: "REEL"` works.
  If Facebook rejects REEL, retry once with `type: "POST"`.
- If a network is disconnected in Metricool (getBrandSettings → networksData has no instagramData /
  facebookData / youtubeData), book the connected ones and say at the top of SUMMARY.md which network
  Naveen must reconnect.
- Instagram caption ≤ 2,200 characters and ≤ 30 hashtags; keep the caption under 2,000 characters.
- YouTube tags: list of strings, total ≤ 450 characters. Custom thumbnails work for long videos.
- `isAiGenerated: true` on Instagram (synthetic voice); `isAiGeneratedContent: false` on YouTube
  (not realistic people/scenes) — Naveen's agreed default (YOUTUBE_RULES §2).
- Monetization is not settable per post: YouTube uses the channel's Upload defaults (On).
- If a call errors, fix and retry once; if it still fails, record the error in SUMMARY.md and leave that
  post for manual posting. Record each returned `plannerUrl` and provider status.
- Telegram is automatic: Make.com posts every new YouTube upload to t.me/digcareerthrust.

## 3a. PDF mode — post immediately

When Naveen attached the notification PDF, don't use the slot queue: after upload and the 200 check, call
`createScheduledPost` with `date` = now + 5 minutes (IST, next whole minute) and the same `publicationDate`,
both posts of §3 (16:9 video on YouTube + teaser on Instagram & Facebook), whatever the job type. Then confirm with `getScheduledPosts`. If it fails twice, give Naveen the MP4, cover
and metadata to post by hand.

## 4. Verify

Call `getScheduledPosts` for the posting window and confirm every job video appears at its slot twice: the
16:9 video with provider `youtube`, and the teaser with `instagram` + `facebook`. Put the result table in SUMMARY.md.

## 5. Nightly posting check (Naveen, 10 Oct 2026)

Runs every night at ~22:20 IST, after the day's last post (22:00). Goal: **every post is live on every network it
was booked for** — 16:9 job videos on YouTube, job teasers on Instagram + Facebook, GATE90 reels on YouTube +
Instagram + Facebook. Anything that failed is re-posted the next day at an in-between time, on the same networks
it was booked for (never move a 16:9 video to Instagram/Facebook or a teaser to YouTube).

1. `getBrandSettings` — note which networks are connected (`networksData`: youtubeData, instagramData, facebookData).
2. `getScheduledPosts` (brandId 7269466, timezone Asia/Calcutta) from **now − 48 h to now** (results are large —
   save to a file and parse with Python; the list includes already-published posts with per-network status).
   Also fetch **now → now + 48 h** to know the times already booked.
3. A post "failed" on a network when its provider status is `ERROR`, or it is still `PENDING`/`PUBLISHING`
   more than 30 minutes after its publication time. Ignore drafts (`draft: true`) and test posts.
   **NEVER post a reel twice on the same network (Naveen, 11 Oct 2026).** If the provider has a `publicUrl` / video id,
   or `detailedStatus` says "published with some warnings" (e.g. "Could not upload video thumbnail"), the reel IS live
   on that network — treat it as PUBLISHED and do not re-post. A thumbnail problem is fixed only on the existing video:
   Metricool cannot change a published video's thumbnail, so list it in the push as "Fix thumbnail by hand:
   <reel> → <publicUrl>" (cover = the post's `videoThumbnailUrl`). If an earlier run booked a re-post of a reel that is
   already live on that network, set that booked post to `draft: true` with `updateScheduledPost` (full original
   content, only `draft` changed) so it never publishes.
4. Group by media (same `media[0]` URL). The networks a media needs = the union of the providers it was booked
   for (a 16:9 job video → youtube; a teaser → instagram + facebook; old job reels and GATE90 reels → youtube +
   instagram + facebook). A media is **missing on a network** if it needs that network and NO post with that
   media URL has `PUBLISHED` on it (a later re-post may already have fixed it — then do nothing).
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
   Facebook use type "POST" if the video is > 90 s, "REEL" otherwise — job teasers are "REEL"). Remove any
   "UNVERIFIED"/"could not verify" line from old captions. Keep `youtubeData` as is, but drop `notifySubscribers`.
7. If a network is disconnected in step 1, still book the re-posts (Naveen usually reconnects quickly) but put
   "RECONNECT <network> in Metricool" first in the report.
8. Report: if anything failed, send Naveen a push notification (PushNotification tool via ToolSearch):
   "Posting check: N reels re-booked for tomorrow (…list: reel → network → time). Reconnect: <network> (if any)."
   If everything was published, finish with one line "All reels posted on YouTube, Instagram and Facebook" and do not
   send a push.
