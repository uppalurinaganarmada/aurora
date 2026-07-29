import urllib.request
import re

url = 'https://in.pinterest.com/pin/726557352487893082/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

print("Checking all video stream variants from Pinterest pin 726557352487893082...")
req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        
        matches = set(re.findall(r'(https://v1\.pinimg\.com/videos/[^\s"\'\<\>]+\.mp4)', html))
        print("Found video streams:")
        
        max_size = 0
        best_url = None
        
        for vurl in matches:
            clean_url = vurl.split('?')[0]
            try:
                head_req = urllib.request.Request(clean_url, headers=headers, method='HEAD')
                with urllib.request.urlopen(head_req) as hresp:
                    size = int(hresp.headers.get('Content-Length', 0))
                    print(f"URL: {clean_url} | Size: {size} bytes")
                    if size > max_size:
                        max_size = size
                        best_url = clean_url
            except Exception as e:
                print(f"Could not fetch size for {clean_url}: {e}")
                
        if best_url:
            print(f"\nDownloading LARGEST / HIGHEST QUALITY VIDEO ({max_size} bytes): {best_url}")
            vreq = urllib.request.Request(best_url, headers=headers)
            with urllib.request.urlopen(vreq) as vresp, open('assets/hero_bg_video.mp4', 'wb') as f:
                f.write(vresp.read())
            print("CRISP HIGH-RES VIDEO DOWNLOADED SUCCESSFULLY TO ASSETS/HERO_BG_VIDEO.MP4!")
except Exception as e:
    print("Error:", e)
