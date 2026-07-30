import os
import subprocess

# List of target Pexels video URLs for 100% watermark-free spa massage videos
pexels_sources = {
    "assets/thai_massage.mp4": "https://www.pexels.com/video/a-therapist-massaging-a-person-3997931/",
    "assets/deep_tissue_massage.mp4": "https://www.pexels.com/video/a-masseuse-massaging-a-woman-s-back-3997937/",
    "assets/scrub_swedish_combo.mp4": "https://www.pexels.com/video/a-woman-getting-a-body-scrub-in-a-spa-3997933/",
    "assets/scrub_deep_tissue.mp4": "https://www.pexels.com/video/woman-getting-a-back-massage-3997986/"
}

for final_path, pexels_url in pexels_sources.items():
    print(f"Downloading 100% watermark-free HD video for {final_path} from Pexels: {pexels_url}")
    cmd = [
        "python", "-m", "yt_dlp",
        "--impersonate", "chrome",
        "-o", final_path,
        pexels_url
    ]
    res = subprocess.run(cmd)
    if os.path.exists(final_path):
        print(f"SUCCESS! Saved pristine video at {final_path} ({os.path.getsize(final_path)} bytes)")
    else:
        print(f"Failed downloading {pexels_url}")
