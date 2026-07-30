import os
import subprocess
import imageio_ffmpeg

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
print("Using ffmpeg binary:", ffmpeg_exe)

# Process all 4 raw original videos with clean natural HD framing and NO BLUR filter whatsoever
targets = [
    {
        "final": "assets/thai_massage.mp4",
        "raw": "assets/raw_thai_massage.mp4",
        "crop": "crop=in_w*0.72:in_h*0.68:in_w*0.14:in_h*0.14"
    },
    {
        "final": "assets/deep_tissue_massage.mp4",
        "raw": "assets/raw_deeptissue.mp4",
        "crop": "crop=in_w*0.72:in_h*0.68:in_w*0.14:in_h*0.14"
    },
    {
        "final": "assets/scrub_swedish_combo.mp4",
        "raw": "assets/raw_salt_scrub.mp4",
        "crop": "crop=in_w*0.72:in_h*0.68:in_w*0.14:in_h*0.14"
    },
    {
        "final": "assets/scrub_deep_tissue.mp4",
        "raw": "assets/raw_scrub_deeptissue.mp4",
        "crop": "crop=in_w*0.72:in_h*0.68:in_w*0.14:in_h*0.14"
    }
]

for t in targets:
    raw_path = t["raw"]
    final_path = t["final"]
    crp = t["crop"]
    
    if os.path.exists(raw_path):
        print(f"Rendering natural unblurred video for {final_path} from {raw_path}...")
        cmd = [
            ffmpeg_exe, "-y",
            "-i", raw_path,
            "-vf", crp,
            "-an",
            "-c:v", "libx264",
            "-crf", "20",
            "-preset", "slow",
            final_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(final_path):
            print(f"SUCCESS! Rendered natural unblurred video at {final_path} ({os.path.getsize(final_path)} bytes)")
        else:
            print(f"Error for {final_path}:", res.stderr)
    else:
        print(f"Raw video {raw_path} not found.")
