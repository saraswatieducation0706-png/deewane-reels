"""Vertical Instagram Reel teaser (1080x1920) cut from a 16:9 long video.
python3 make_teaser.py <long.mp4> <start_seconds> <duration_seconds> "<Title>" "<top line>" <out.mp4>
Layout: blurred, darkened copy of the video fills the frame; the 16:9 video sits in the middle;
title on top; "Watch the full video on YouTube" footer.
"""
import os, subprocess, sys, tempfile
from PIL import Image
import cb_common as cb

src, start, dur, title, top, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6]
W, H = 1080, 1920
work = tempfile.mkdtemp(prefix="cbt_")
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
t1 = cb.text_block(W, top, "body_italic", 44, (255, 236, 200), W - 160)
t2 = cb.text_block(W, title, "serif_bold", 96, (255, 255, 255), W - 140, max_lines=3)
ov.alpha_composite(t1, (0, 160))
ov.alpha_composite(t2, (0, 160 + t1.height - 40))
f1 = cb.text_block(W, "Watch the full video on YouTube", "serif", 64, (255, 255, 255), W - 140)
f2 = cb.text_block(W, "Christ's Blessings", "body_italic", 46, (255, 236, 200), W - 160)
ov.alpha_composite(f1, (0, 1380))
ov.alpha_composite(f2, (0, 1380 + f1.height - 30))
ovp = os.path.join(work, "ov.png"); ov.save(ovp)
fade_out = max(0, dur - 2.5)
fc = (f"[0:v]split[a][b];"
      f"[a]scale=-2:{H},crop={W}:{H},boxblur=30:3,eq=brightness=-0.18[bg];"
      f"[b]crop=iw*0.78:ih,scale={W}:-2[fg];"
      f"[bg][fg]overlay=(W-w)/2:(H-h)/2-40[v1];"
      f"[v1][1:v]overlay=0:0,fade=t=in:d=0.6,fade=t=out:st={fade_out}:d=2.5,format=yuv420p[v];"
      f"[0:a]afade=t=in:d=1,afade=t=out:st={fade_out}:d=2.5,loudnorm=I=-15:TP=-1.5[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-t", str(dur), "-i", src, "-i", ovp,
                "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-r", "30", "-c:v", "libx264", "-preset", "medium",
                "-crf", "21", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-movflags", "+faststart", out], check=True)
print(out)
