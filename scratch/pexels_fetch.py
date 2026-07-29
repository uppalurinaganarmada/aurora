import requests
import re
import os

url = "https://www.pexels.com/video/a-close-up-video-of-a-back-massage-6750892/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

r = requests.get(url, headers=headers)
print("Status code:", r.status_code)

if r.status_code == 200:
    mp4s = list(set(re.findall(r'https://[^\s\"\'\<\>]+?\.mp4', r.text)))
    print("Found MP4 links:", mp4s)
    
    # Download the best quality MP4
    if mp4s:
        target = mp4s[0]
        for m in mp4s:
            if '1080' in m or '720' in m or 'hd' in m:
                target = m
                break
        print("Downloading from:", target)
        v_res = requests.get(target, headers=headers)
        out_path = os.path.join("assets", "coconut_oil_massage.mp4")
        with open(out_path, "wb") as f:
            f.write(v_res.content)
        print(f"Downloaded {len(v_res.content)} bytes to {out_path}!")
else:
    print("Failed to fetch Pexels page, status:", r.status_code)
