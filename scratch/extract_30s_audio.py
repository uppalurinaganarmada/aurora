import os
import subprocess
import shutil

video_src = os.path.join("assets", "audio_pin_source.mp4")
audio_dest_mp3 = os.path.join("assets", "bg_soundscape.mp3")
audio_dest_mp4 = os.path.join("assets", "bg_soundscape.mp4")

print(f"Source file size: {os.path.getsize(video_src)} bytes")

# Check if imageio_ffmpeg or moviepy or cv2 is installed, or install/use uv
try:
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    print("Found imageio ffmpeg:", ffmpeg_exe)
    cmd = [ffmpeg_exe, "-y", "-i", video_src, "-t", "30", "-vn", "-acodec", "libmp3lame", "-ab", "192k", audio_dest_mp3]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print("Successfully extracted 30s MP3 audio using imageio_ffmpeg!")
    else:
        # Fallback to copy mp4 with 30s trim
        cmd2 = [ffmpeg_exe, "-y", "-i", video_src, "-t", "30", "-c", "copy", audio_dest_mp4]
        subprocess.run(cmd2)
        print("Extracted 30s MP4 audio/video stream using imageio_ffmpeg!")
except Exception as e:
    print("imageio_ffmpeg error:", e)
    # If imageio_ffmpeg is not installed, install it or copy target MP4
    shutil.copyfile(video_src, audio_dest_mp4)
    print("Copied raw audio/video MP4 to assets/bg_soundscape.mp4")
