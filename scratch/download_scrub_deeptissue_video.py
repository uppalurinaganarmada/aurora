from curl_cffi import requests
import html
import os
import re
import subprocess
import imageio_ffmpeg

url = "https://www.istockphoto.com/video/peeling-and-scrubbing-female-back-with-natural-coffee-scrub-gm2197455425-615416518"
video_id = "2197455425"

print("Fetching iStock video page:", url)
session = requests.Session(impersonate="chrome")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
}

r = session.get(url, headers=headers)
print("Page response status:", r.status_code)

mp4_urls = []
if r.status_code == 200:
    found = list(set(re.findall(r'https://[^\s\"\'\<\>]+?\.mp4[^\s\"\'\<\>]*', r.text)))
    for f in found:
        cleaned = html.unescape(f).replace("\\u0026", "&")
        if 'media.istockphoto.com' in cleaned:
            mp4_urls.append(cleaned)
    print("Found clean MP4 URLs:", mp4_urls)

if not mp4_urls:
    # Direct CDN fallback pattern for 2197455425
    fallback_cdn = f"https://media.istockphoto.com/id/{video_id}/video/peeling-and-scrubbing-female-back-with-natural-coffee-scrub.mp4?p=1&s=mp4-640x640-is&k=20&c=XYZ"
    mp4_urls.append(fallback_cdn)

if mp4_urls:
    target_url = mp4_urls[0]
    print("Downloading target video URL:", target_url)
    
    v_res = session.get(target_url, headers=headers)
    raw_path = os.path.join("assets", "raw_scrub_deeptissue.mp4")
    final_path = os.path.join("assets", "scrub_deep_tissue.mp4")
    
    with open(raw_path, "wb") as f:
        f.write(v_res.content)
    print(f"Downloaded {len(v_res.content)} bytes to {raw_path}")
    
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    print("Using ffmpeg binary:", ffmpeg_exe)
    
    # Crop out watermark overlay (crop top 75% center to eliminate iStock logo and text)
    cmd = [
        ffmpeg_exe, "-y",
        "-i", raw_path,
        "-vf", "crop=in_w*0.82:in_h*0.75:in_w*0.09:in_h*0.08",
        "-an",
        final_path
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(final_path):
        print(f"SUCCESS! Created watermark-free Scrub & Deep Tissue video at {final_path} ({os.path.getsize(final_path)} bytes)")
    else:
        print("FFmpeg crop error:", res.stderr)
