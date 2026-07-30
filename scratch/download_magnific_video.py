from curl_cffi import requests
import html
import os
import re
import subprocess
import imageio_ffmpeg

url = "https://www.magnific.com/free-video/man-receiving-back-massage_1742697"
video_id = "1742697"

print("Fetching Magnific video page:", url)
session = requests.Session(impersonate="chrome")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

r = session.get(url, headers=headers)
print("Page response status:", r.status_code)

mp4_urls = []
if r.status_code == 200:
    found = list(set(re.findall(r'https://[^\s\"\'\<\>]+?\.mp4[^\s\"\'\<\>]*', r.text)))
    for f in found:
        cleaned = html.unescape(f).replace("\\u0026", "&")
        mp4_urls.append(cleaned)
    print("Found MP4 URLs:", mp4_urls)

if not mp4_urls:
    # Look for video src tags or data-src tags
    sources = re.findall(r'src=["\'](https://[^\s"\'\<\>]+\.mp4[^"\'\<\>]*)["\']', r.text)
    mp4_urls.extend(sources)

if mp4_urls:
    target_url = mp4_urls[0]
    print("Downloading target video URL:", target_url)
    
    v_res = session.get(target_url, headers=headers)
    raw_path = os.path.join("assets", "raw_magnific_1742697.mp4")
    final_path = os.path.join("assets", "scrub_swedish_combo.mp4")
    
    with open(raw_path, "wb") as f:
        f.write(v_res.content)
    print(f"Downloaded {len(v_res.content)} bytes to {raw_path}")
    
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    print("Using ffmpeg binary:", ffmpeg_exe)
    
    # Compress & format for fast web playback (720p 30fps H.264)
    cmd_opt = [
        ffmpeg_exe, "-y",
        "-i", raw_path,
        "-t", "15",
        "-vf", "scale=-2:720",
        "-an",
        "-c:v", "libx264",
        "-crf", "24",
        "-preset", "fast",
        final_path
    ]
    
    res = subprocess.run(cmd_opt, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(final_path):
        print(f"SUCCESS! Installed Scrub & Swedish Combo video at {final_path} ({os.path.getsize(final_path)} bytes)")
    else:
        print("FFmpeg optimization error:", res.stderr)
else:
    print("Could not retrieve Magnific video preview URL.")
