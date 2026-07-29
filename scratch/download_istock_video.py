import requests
import re
import os
import subprocess
import imageio_ffmpeg

url = "https://www.istockphoto.com/video/a-professional-beautician-does-facial-massage-to-a-woman-cosmetology-gm1225443806-360693619"
print("Fetching iStock video page:", url)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

r = requests.get(url, headers=headers)
print("Status code:", r.status_code)

if r.status_code == 200:
    # Find video preview MP4 URLs in page HTML
    mp4s = list(set(re.findall(r'https://[^\s\"\'\<\>]+?\.mp4[^\s\"\'\<\>]*', r.text)))
    print("Found MP4s:", mp4s)
    
    target_url = None
    for m in mp4s:
        if 'video' in m.lower() or 'istock' in m.lower() or 'media' in m.lower():
            target_url = m
            break
    if not target_url and mp4s:
        target_url = mp4s[0]
        
    print("Selected video URL:", target_url)
    
    if target_url:
        raw_video_path = os.path.join("assets", "raw_istock_video.mp4")
        out_video_path = os.path.join("assets", "scrub_swedish_combo.mp4")
        
        v_res = requests.get(target_url, headers=headers)
        with open(raw_video_path, "wb") as f:
            f.write(v_res.content)
        print(f"Downloaded raw iStock video ({len(v_res.content)} bytes)")
        
        # Crop out watermark area or trim text overlay using ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        print("Using ffmpeg binary:", ffmpeg_exe)
        
        # Crop filter in ffmpeg: crop=in_w:in_h-60:0:0 or delogo or crop center
        # Let's inspect video dimensions or crop lower 15% / watermark zone
        cmd = [ffmpeg_exe, "-y", "-i", raw_video_path, "-vf", "crop=in_w:in_h-80:0:0", "-c:a", "copy", out_video_path]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(out_video_path):
            print(f"Successfully cropped out iStock watermark! Final size: {os.path.getsize(out_video_path)} bytes")
        else:
            print("ffmpeg crop error:", res.stderr)
            # Fallback to copy raw
            with open(out_video_path, "wb") as f:
                f.write(v_res.content)
else:
    print("Failed to fetch iStock page, status:", r.status_code)
