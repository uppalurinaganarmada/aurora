import os
import subprocess
import imageio_ffmpeg

url = "https://www.pexels.com/video/close-up-video-of-a-person-getting-body-massage-9335857/"
raw_path = os.path.join("assets", "raw_swedish_massage.mp4")
final_path = os.path.join("assets", "swedish_massage.mp4")

print("Downloading Pexels video 9335857 using yt_dlp...")

cmd_dl = [
    "python", "-m", "yt_dlp",
    "--impersonate", "chrome",
    "-o", raw_path,
    url
]

subprocess.run(cmd_dl)

if os.path.exists(raw_path):
    print(f"Downloaded raw video ({os.path.getsize(raw_path)} bytes)")
    
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    print("Using ffmpeg binary:", ffmpeg_exe)
    
    # Trim video to 20 seconds using -t 20
    cmd_trim = [
        ffmpeg_exe, "-y",
        "-i", raw_path,
        "-t", "20",
        "-an",
        "-c:v", "copy",
        final_path
    ]
    
    res = subprocess.run(cmd_trim, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(final_path):
        print(f"SUCCESS! Created 20-second Swedish Massage video at {final_path} ({os.path.getsize(final_path)} bytes)")
    else:
        print("FFmpeg trim error:", res.stderr)
else:
    print("Failed to download Pexels video 9335857.")
