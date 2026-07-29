import urllib.request
import re

url = 'https://in.pinterest.com/pin/811351689165819940/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

print("Fetching new Pinterest pin 811351689165819940...")
req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        
        matches = re.findall(r'(https://v1\.pinimg\.com/videos/iht/[^\s"\'\<\>]+\.mp4)', html)
        if not matches:
            matches = re.findall(r'(https://v1\.pinimg\.com/videos/[^\s"\'\<\>]+\.mp4)', html)
        if not matches:
            matches = re.findall(r'(https://[^\s"\'\<\>]+\.mp4[^\s"\'\<\>]*)', html)
            
        print("Found video URLs:", set(matches))

        urls = list(set(matches))
        best_url = None
        for u in urls:
            if '720w' in u or 'expMp4' in u:
                best_url = u
                break
        if not best_url and urls:
            best_url = urls[0]
            
        if best_url:
            clean_url = best_url.split('?')[0]
            print("Downloading target video:", clean_url)
            vreq = urllib.request.Request(clean_url, headers=headers)
            with urllib.request.urlopen(vreq) as vresp, open('assets/hero_bg_video.mp4', 'wb') as f:
                f.write(vresp.read())
            print("SUCCESSFULLY DOWNLOADED NEW PINTEREST VIDEO!")
except Exception as e:
    print("Error:", e)
