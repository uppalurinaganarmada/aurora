import urllib.request
import re
import os
import subprocess

pin_url = "https://in.pinterest.com/pin/21603273207964484/"
print("Fetching pin:", pin_url)

req = urllib.request.Request(pin_url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})

html = urllib.request.urlopen(req).read().decode('utf-8')
mp4_urls = list(set(re.findall(r'https://v1\.pinimg\.com/videos/[^\s\"\'\<\>]+?\.mp4', html)))

print("Found MP4s:", mp4_urls)

if not mp4_urls:
    # Look for m3u8 or other video streams
    m3u8_urls = list(set(re.findall(r'https://[^\s\"\'\<\>]+?\.m3u8', html)))
    print("Found M3U8s:", m3u8_urls)

target_mp4 = None
if mp4_urls:
    # Pick the largest/highest quality MP4
    for u in mp4_urls:
        if 'expMp4' in u or '720p' in u or '1080p' in u or 'hls' not in u:
            target_mp4 = u
            break
    if not target_mp4:
        target_mp4 = mp4_urls[0]

print("Target MP4:", target_mp4)

if target_mp4:
    out_video_path = os.path.join("assets", "audio_pin_source.mp4")
    out_audio_path = os.path.join("assets", "bg_soundscape.mp3")
    
    print("Downloading video stream...")
    req_mp4 = urllib.request.Request(target_mp4, headers={'User-Agent': 'Mozilla/5.0'})
    video_data = urllib.request.urlopen(req_mp4).read()
    
    with open(out_video_path, 'wb') as f:
        f.write(video_data)
    print(f"Downloaded {len(video_data)} bytes to {out_video_path}")
    
    # Try ffmpeg to extract and trim 30 seconds audio
    try:
        cmd = ["ffmpeg", "-y", "-i", out_video_path, "-t", "30", "-vn", "-acodec", "libmp3lame", "-ab", "192k", out_audio_path]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(out_audio_path):
            print(f"Successfully extracted 30s MP3 audio using ffmpeg: {out_audio_path}")
        else:
            print("ffmpeg failed or not available, using raw MP4 stream for audio element:", res.stderr)
            # Copy or save as mp4 audio source
            out_audio_mp4 = os.path.join("assets", "bg_soundscape.mp4")
            with open(out_audio_mp4, 'wb') as f:
                f.write(video_data)
            print("Saved as bg_soundscape.mp4")
    except Exception as ex:
        print("FFmpeg exception:", ex)
