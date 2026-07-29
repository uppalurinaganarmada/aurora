import os
import subprocess
import imageio_ffmpeg

video_src = os.path.join("assets", "audio_pin_source.mp4")
audio_dest_mp3 = os.path.join("assets", "bg_soundscape.mp3")

print(f"Source file size: {os.path.getsize(video_src)} bytes")

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
print("Using ffmpeg binary:", ffmpeg_exe)

# Extract 3 minutes (180 seconds) of audio into high-quality MP3
cmd = [ffmpeg_exe, "-y", "-i", video_src, "-t", "180", "-vn", "-acodec", "libmp3lame", "-ab", "192k", audio_dest_mp3]
res = subprocess.run(cmd, capture_output=True, text=True)

if res.returncode == 0 and os.path.exists(audio_dest_mp3):
    size = os.path.getsize(audio_dest_mp3)
    print(f"Successfully extracted 3-minute (180s) MP3 audio track! File size: {size} bytes ({size / 1024 / 1024:.2f} MB)")
else:
    print("Error extracting audio:", res.stderr)
