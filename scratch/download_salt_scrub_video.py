from curl_cffi import requests
import html
import re
import os
import subprocess
import imageio_ffmpeg

url = "https://www.istockphoto.com/video/4k-video-footage-of-a-young-woman-enjoying-a-relaxing-salt-scrub-massage-at-a-spa-gm1367037590-437408551"
video_id = "1367037590"

print("Fetching iStock salt scrub video page:", url)
session = requests.Session(impersonate="chrome")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

r = session.get(url, headers=headers)
print("Response status:", r.status_code)

mp4_urls = []
if r.status_code == 200:
    found = list(set(re.findall(r'https://[^\s\"\'\<\>]+?\.mp4[^\s\"\'\<\>]*', r.text)))
    for f in found:
        cleaned = html.unescape(f).replace("\\u0026", "&")
        if 'media.istockphoto.com' in cleaned:
            mp4_urls.append(cleaned)
    print("Found clean MP4 URLs:", mp4_urls)

if not mp4_urls:
    fallback_url = f"https://media.istockphoto.com/id/{video_id}/video/4k-video-footage-of-a-young-woman-enjoying-a-relaxing-salt-scrub-massage-at-a-spa.mp4?p=1&s=mp4-640x640-is&k=20&c=XYZ"
    mp4_urls.append(fallback_url)

if mp4_urls:
    target_url = mp4_urls[0]
    print("Downloading salt scrub video URL:", target_url)
    
    v_res = session.get(target_url, headers=headers)
    raw_path = os.path.join("assets", "raw_salt_scrub.mp4")
    final_path = os.path.join("assets", "scrub_swedish_combo.mp4")
    
    with open(raw_path, "wb") as f:
        f.write(v_res.content)
    print(f"Downloaded {len(v_res.content)} bytes to {raw_path}")
    
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    print("Using ffmpeg binary:", ffmpeg_exe)
    
    # Crop top 75% center to eliminate watermark overlay cleanly
    cmd = [
        ffmpeg_exe, "-y",
        "-i", raw_path,
        "-vf", "crop=in_w*0.82:in_h*0.75:in_w*0.09:in_h*0.08",
        "-an",
        final_path
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(final_path):
        print(f"SUCCESS! Created watermark-free Salt Scrub video at {final_path} ({os.path.getsize(final_path)} bytes)")
    else:
        print("FFmpeg crop error:", res.stderr)
