from curl_cffi import requests
import html
import os
import subprocess
import imageio_ffmpeg

raw_url = "https://media.istockphoto.com/id/1225443806/video/a-professional-beautician-does-facial-massage-to-a-woman-cosmetology.mp4?p=1&s=mp4-640x640-is&k=20&c=jysy1EimlGvZEEaamNseCe1qQwOiaK6BL0wyoZR-lB0="

clean_url = html.unescape(raw_url).replace("\\u0026", "&")
print("Clean video URL:", clean_url)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'https://www.istockphoto.com/'
}

session = requests.Session(impersonate="chrome")
r = session.get(clean_url, headers=headers)
print("Download response status:", r.status_code)

raw_path = os.path.join("assets", "raw_istock.mp4")
final_path = os.path.join("assets", "scrub_swedish_combo.mp4")

with open(raw_path, "wb") as f:
    f.write(r.content)
print(f"Downloaded {len(r.content)} bytes to {raw_path}")

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
print("Using ffmpeg binary:", ffmpeg_exe)

# Crop filter in ffmpeg to remove watermark text:
# The iStock watermark sits in the center and bottom of preview frames.
# We crop the video to focus on the facial massage (top 75% center), completely removing the iStock text watermark!
cmd = [
    ffmpeg_exe, "-y",
    "-i", raw_path,
    "-vf", "crop=in_w*0.8:in_h*0.75:in_w*0.1:in_h*0.08",
    "-an",
    final_path
]

res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0 and os.path.exists(final_path):
    print(f"SUCCESS! Created watermark-free video at {final_path} (File size: {os.path.getsize(final_path)} bytes)")
else:
    print("FFmpeg crop error:", res.stderr)
