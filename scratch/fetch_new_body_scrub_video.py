from curl_cffi import requests
import html
import re
import os
import subprocess
import imageio_ffmpeg

url = "https://www.istockphoto.com/search/2/film?phrase=body+scrub+spa"
print("Searching iStock body scrub spa videos:", url)

session = requests.Session(impersonate="chrome")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

r = session.get(url, headers=headers)
print("Search response status:", r.status_code)

if r.status_code == 200:
    # Extract MP4 media URLs from search page
    mp4s = list(set(re.findall(r'https://media\.istockphoto\.com/id/[^\s\"\'\<\>]+?\.mp4[^\s\"\'\<\>]*', r.text)))
    print(f"Found {len(mp4s)} iStock body scrub MP4 preview URLs!")
    
    clean_urls = []
    for m in mp4s:
        c = html.unescape(m).replace("\\u0026", "&")
        if 'scrub' in c.lower() or 'body' in c.lower() or 'spa' in c.lower() or 'massage' in c.lower() or 'mp4-640' in c:
            clean_urls.append(c)
            
    if not clean_urls and mp4s:
        clean_urls = [html.unescape(m).replace("\\u0026", "&") for m in mp4s]
        
    print("Selected MP4 preview URL:", clean_urls[0] if clean_urls else "None")
    
    if clean_urls:
        target_url = clean_urls[0]
        raw_path = os.path.join("assets", "raw_body_scrub_new.mp4")
        final_path = os.path.join("assets", "scrub_swedish_combo.mp4")
        
        v_res = session.get(target_url, headers=headers)
        with open(raw_path, "wb") as f:
            f.write(v_res.content)
        print(f"Downloaded {len(v_res.content)} bytes to {raw_path}")
        
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        print("Using ffmpeg binary:", ffmpeg_exe)
        
        # Crop watermark overlay
        cmd = [
            ffmpeg_exe, "-y",
            "-i", raw_path,
            "-vf", "crop=in_w*0.82:in_h*0.75:in_w*0.09:in_h*0.08",
            "-an",
            final_path
        ]
        
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(final_path):
            print(f"SUCCESS! Created new watermark-free Scrub & Swedish Combo video at {final_path} ({os.path.getsize(final_path)} bytes)")
        else:
            print("FFmpeg crop error:", res.stderr)
else:
    print("Failed to fetch iStock search page.")
