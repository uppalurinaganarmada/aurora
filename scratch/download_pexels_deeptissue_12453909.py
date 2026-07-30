import os
import subprocess
import imageio_ffmpeg

url = "https://www.pexels.com/video/massage-on-back-12453909/"
raw_path = os.path.join("assets", "raw_pexels_deeptissue_12453909.mp4")
final_path = os.path.join("assets", "deep_tissue_massage.mp4")

print("Downloading Pexels video 12453909 using yt_dlp...")

cmd_dl = [
    "python", "-m", "yt_dlp",
    "--impersonate", "chrome",
    "-o", raw_path,
    url
]

subprocess.run(cmd_dl)

if os.path.exists(raw_path):
    print(f"Downloaded raw Pexels video ({os.path.getsize(raw_path)} bytes)")
    
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
        print(f"SUCCESS! Installed 100% watermark-free Deep Tissue video at {final_path} ({os.path.getsize(final_path)} bytes)")
    else:
        print("FFmpeg optimization error:", res.stderr)
else:
    print("Failed to download Pexels video 12453909.")
