import urllib.request
import re
import os

url = "https://www.pexels.com/video/a-close-up-video-of-a-back-massage-6750892/"
print("Fetching Pexels video page:", url)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request(url, headers=headers)
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    print("Page HTML fetched, length:", len(html))
    
    # Extract video MP4 URLs from Pexels page source
    mp4_urls = list(set(re.findall(r'https://video-files\.pexels\.com/video-files/[^\s\"\'\<\>]+?\.mp4', html)))
    if not mp4_urls:
        mp4_urls = list(set(re.findall(r'https://[^\s\"\'\<\>]+?\.mp4', html)))
    
    print("Found MP4 URLs:", mp4_urls)
    
    target_url = None
    for u in mp4_urls:
        if 'hd' in u.lower() or '720' in u or '1080' in u or 'sd' in u:
            target_url = u
            break
    if not target_url and mp4_urls:
        target_url = mp4_urls[0]
        
    print("Selected target video URL:", target_url)
    
    if target_url:
        out_path = os.path.join("assets", "coconut_oil_massage.mp4")
        print("Downloading video stream to:", out_path)
        req_video = urllib.request.Request(target_url, headers=headers)
        video_bytes = urllib.request.urlopen(req_video).read()
        
        with open(out_path, 'wb') as f:
            f.write(video_bytes)
        print(f"Downloaded successfully! File size: {len(video_bytes)} bytes ({len(video_bytes) / 1024 / 1024:.2f} MB)")
    else:
        print("No MP4 URL found on Pexels page source.")
except Exception as e:
    print("Error downloading Pexels video:", e)
