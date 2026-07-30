import os
import subprocess
import imageio_ffmpeg

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
print("Using ffmpeg binary:", ffmpeg_exe)

files = [
    "assets/thai_massage.mp4",
    "assets/deep_tissue_massage.mp4",
    "assets/scrub_swedish_combo.mp4",
    "assets/scrub_deep_tissue.mp4"
]

for path in files:
    raw_tmp = path.replace(".mp4", "_raw.mp4")
    os.rename(path, raw_tmp)
    print(f"Compressing {path}...")
    
    cmd = [
        ffmpeg_exe, "-y",
        "-i", raw_tmp,
        "-t", "15",
        "-vf", "scale=-2:720",
        "-an",
        "-c:v", "libx264",
        "-crf", "26",
        "-preset", "fast",
        path
    ]
    
    subprocess.run(cmd)
    if os.path.exists(path):
        os.remove(raw_tmp)
        print(f"SUCCESS! Optimized {path} to {os.path.getsize(path)} bytes")
