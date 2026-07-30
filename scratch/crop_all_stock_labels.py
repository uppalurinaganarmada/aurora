import os
import subprocess
import imageio_ffmpeg

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
print("Using ffmpeg binary:", ffmpeg_exe)

# Dictionary of video targets and their raw source paths
videos = {
    "assets/thai_massage.mp4": "assets/raw_thai_massage.mp4",
    "assets/deep_tissue_massage.mp4": "assets/raw_deeptissue.mp4",
    "assets/scrub_swedish_combo.mp4": "assets/raw_salt_scrub.mp4",
    "assets/scrub_deep_tissue.mp4": "assets/raw_scrub_deeptissue.mp4"
}

# Strong crop: crop center 60% of video (eliminates top/bottom/side stock logos completely!)
for final_path, raw_path in videos.items():
    if os.path.exists(raw_path):
        print(f"Processing tight crop for {final_path} from {raw_path}...")
        cmd = [
            ffmpeg_exe, "-y",
            "-i", raw_path,
            "-vf", "crop=in_w*0.62:in_h*0.58:in_w*0.19:in_h*0.12",
            "-an",
            final_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"SUCCESS! Re-cropped {final_path} ({os.path.getsize(final_path)} bytes)")
        else:
            print(f"Error cropping {final_path}:", res.stderr)
    else:
        print(f"Raw file {raw_path} not found.")
