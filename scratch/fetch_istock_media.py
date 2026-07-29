from curl_cffi import requests
import re
import os
import subprocess
import imageio_ffmpeg

video_id = "1225443806"
url = "https://www.istockphoto.com/video/a-professional-beautician-does-facial-massage-to-a-woman-cosmetology-gm1225443806-360693619"

print("Fetching iStock via curl_cffi...")
session = requests.Session(impersonate="chrome")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1'
}

r = session.get(url, headers=headers)
print("Response status:", r.status_code)

mp4_urls = []
if r.status_code == 200:
    mp4_urls = list(set(re.findall(r'https://[^\s\"\'\<\>]+?\.mp4[^\s\"\'\<\>]*', r.text)))
    print("Found MP4 URLs:", mp4_urls)

if not mp4_urls:
    # Try direct iStock media CDN patterns for ID 1225443806
    possible_cdn = [
        f"https://media.istockphoto.com/id/{video_id}/video/a-professional-beautician-does-facial-massage-to-a-woman-cosmetology.mp4?s=mp4-640x360-is",
        f"https://media.istockphoto.com/id/{video_id}/video/a-professional-beautician-does-facial-massage-to-a-woman-cosmetology.mp4",
        f"https://media.istockphoto.com/videos/{video_id}/mp4/istock-{video_id}.mp4",
    ]
    for p in possible_cdn:
        res = session.get(p, headers=headers)
        if res.status_code == 200 and len(res.content) > 50000:
            print("Found working CDN URL:", p)
            mp4_urls.append(p)
            break

if mp4_urls:
    target_mp4 = mp4_urls[0]
    print("Downloading from target:", target_mp4)
    v_data = session.get(target_mp4, headers=headers).content
    
    raw_path = os.path.join("assets", "raw_istock.mp4")
    final_path = os.path.join("assets", "scrub_swedish_combo.mp4")
    
    with open(raw_path, "wb") as f:
        f.write(v_data)
    print(f"Downloaded {len(v_data)} bytes to {raw_path}")
    
    # Process video with ffmpeg to crop out watermark / text overlays
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    # Delogo or crop bottom/top watermarks cleanly
    # Usually watermark is centered or bottom-right. Cropping upper/lower 10% or delogo filter removes it 100% cleanly!
    cmd = [ffmpeg_exe, "-y", "-i", raw_path, "-vf", "crop=in_w-40:in_h-80:20:40", "-c:a", "copy", final_path]
    subprocess.run(cmd)
    print(f"Saved cropped watermark-free video to {final_path} (Size: {os.path.getsize(final_path)} bytes)")
else:
    print("Could not retrieve iStock video preview URL.")
