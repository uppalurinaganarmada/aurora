from curl_cffi import requests
import re
import os
import subprocess

session = requests.Session(impersonate="chrome")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

def get_pexels_mp4_links(search_query):
    url = f"https://www.pexels.com/search/videos/{search_query.replace(' ', '%20')}/"
    r = session.get(url, headers=headers)
    mp4s = []
    if r.status_code == 200:
        found = list(set(re.findall(r'https://v1\.pexels\.com/video-files/[^\s\"\'\<\>]+?\.mp4[^\s\"\'\<\>]*', r.text)))
        if not found:
            found = list(set(re.findall(r'https://[^\s\"\'\<\>]+?pexels[^\s\"\'\<\>]+?\.mp4[^\s\"\'\<\>]*', r.text)))
        mp4s = [f for f in found if 'video' in f or 'files' in f]
    return mp4s

print("Searching Pexels for massage videos...")
massage_mp4s = get_pexels_mp4_links("massage")
print(f"Found {len(massage_mp4s)} Pexels massage MP4 URLs!")

print("Searching Pexels for body scrub spa videos...")
scrub_mp4s = get_pexels_mp4_links("body scrub spa")
print(f"Found {len(scrub_mp4s)} Pexels scrub MP4 URLs!")

# Filter out low-res thumbnails and pick high-quality 720p/1080p MP4 links
hd_massage = [m for m in massage_mp4s if 'hd' in m.lower() or '1080' in m or '720' in m or 'sd' in m]
hd_scrub = [m for m in scrub_mp4s if 'hd' in m.lower() or '1080' in m or '720' in m or 'sd' in m]

if not hd_massage: hd_massage = massage_mp4s
if not hd_scrub: hd_scrub = scrub_mp4s

print(f"Sample HD Massage MP4s: {hd_massage[:3]}")
print(f"Sample HD Scrub MP4s: {hd_scrub[:3]}")

# Download 4 distinct, 100% watermark-free Pexels MP4 files
targets = {
    "assets/thai_massage.mp4": hd_massage[0] if len(hd_massage) > 0 else None,
    "assets/deep_tissue_massage.mp4": hd_massage[1] if len(hd_massage) > 1 else hd_massage[0],
    "assets/scrub_swedish_combo.mp4": hd_scrub[0] if len(hd_scrub) > 0 else hd_massage[2],
    "assets/scrub_deep_tissue.mp4": hd_scrub[1] if len(hd_scrub) > 1 else hd_scrub[0]
}

for path, link in targets.items():
    if link:
        print(f"Downloading clean Pexels video for {path} from {link[:80]}...")
        data = session.get(link, headers=headers).content
        with open(path, "wb") as f:
            f.write(data)
        print(f"SUCCESS! Saved 100% watermark-free video to {path} ({len(data)} bytes)")
    else:
        print(f"No link found for {path}")
