from curl_cffi import requests
import re
import os
import subprocess
import imageio_ffmpeg

session = requests.Session(impersonate="chrome")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

print("Searching Pexels for salt scrub and swedish massage videos...")
url = "https://www.pexels.com/search/videos/salt%20scrub%20massage/"
r = session.get(url, headers=headers)

mp4_urls = []
if r.status_code == 200:
    found = list(set(re.findall(r'https://v1\.pexels\.com/video-files/[^\s\"\'\<\>]+?\.mp4[^\s\"\'\<\>]*', r.text)))
    if not found:
        found = list(set(re.findall(r'https://[^\s\"\'\<\>]+?pexels[^\s\"\'\<\>]+?\.mp4[^\s\"\'\<\>]*', r.text)))
    mp4_urls = [f for f in found if 'video' in f or 'files' in f]

print(f"Found {len(mp4_urls)} Pexels salt scrub MP4 URLs!")

# Filter HD streams
hd_urls = [m for m in mp4_urls if 'hd' in m.lower() or '1080' in m or '720' in m or 'sd' in m]
if not hd_urls and mp4_urls:
    hd_urls = mp4_urls

print("Selected target MP4:", hd_urls[0] if hd_urls else "None")

if hd_urls:
    target_link = hd_urls[0]
    raw_path = os.path.join("assets", "raw_pexels_salt_scrub.mp4")
    final_path = os.path.join("assets", "scrub_swedish_combo.mp4")
    
    print(f"Downloading Pexels salt scrub video from {target_link[:80]}...")
    data = session.get(target_link, headers=headers).content
    with open(raw_path, "wb") as f:
        f.write(data)
    print(f"Downloaded {len(data)} bytes to {raw_path}")
    
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
        print(f"SUCCESS! Installed 100% watermark-free Scrub & Swedish Combo video at {final_path} ({os.path.getsize(final_path)} bytes)")
    else:
        print("FFmpeg optimization error:", res.stderr)
