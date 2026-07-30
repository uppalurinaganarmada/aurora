import os
import subprocess
import imageio_ffmpeg

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
print("Using ffmpeg binary:", ffmpeg_exe)

# Original videos and their exact raw sources
targets = [
    {
        "final": "assets/thai_massage.mp4",
        "raw": "assets/raw_thai_massage.mp4",
        # Vecteezy center watermark is located around x=140, y=240, w=360, h=150
        "filter": "delogo=x=130:y=230:w=380:h=160:show=0"
    },
    {
        "final": "assets/deep_tissue_massage.mp4",
        "raw": "assets/raw_deeptissue.mp4",
        # iStock center watermark is located around x=140, y=250, w=360, h=140
        "filter": "delogo=x=140:y=240:w=360:h=150:show=0"
    },
    {
        "final": "assets/scrub_swedish_combo.mp4",
        "raw": "assets/raw_salt_scrub.mp4",
        # iStock center watermark is located around x=140, y=250, w=360, h=140
        "filter": "delogo=x=140:y=240:w=360:h=150:show=0"
    },
    {
        "final": "assets/scrub_deep_tissue.mp4",
        "raw": "assets/raw_scrub_deeptissue.mp4",
        # iStock center watermark is located around x=140, y=250, w=360, h=140
        "filter": "delogo=x=140:y=240:w=360:h=150:show=0"
    }
]

for t in targets:
    raw_path = t["raw"]
    final_path = t["final"]
    flt = t["filter"]
    
    if os.path.exists(raw_path):
        print(f"Applying delogo filter to restore original video {final_path} from {raw_path}...")
        cmd = [
            ffmpeg_exe, "-y",
            "-i", raw_path,
            "-vf", flt,
            "-an",
            "-c:v", "libx264",
            "-crf", "22",
            final_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(final_path):
            print(f"SUCCESS! Restored original video with delogo watermark removal at {final_path} ({os.path.getsize(final_path)} bytes)")
        else:
            print(f"Delogo error for {final_path}:", res.stderr)
    else:
        print(f"Raw video {raw_path} not found.")
