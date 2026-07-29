import urllib.request
import re
import sys

url = 'https://in.pinterest.com/pin/315674255154938077/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

print("Fetching Pinterest page source...")
req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        
        # Look for video URLs in pinimg
        matches = re.findall(r'(https://v1\.pinimg\.com/videos/mc/[^\s"\'\<\>]+\.mp4)', html)
        if not matches:
            matches = re.findall(r'(https://[^\s"\'\<\>]+\.mp4[^\s"\'\<\>]*)', html)
            
        print("Found matches:", set(matches))

        if matches:
            video_url = list(set(matches))[0]
            # Clean URL parameters if any
            clean_url = video_url.split('?')[0]
            print("Downloading exact video from:", clean_url)
            
            video_req = urllib.request.Request(clean_url, headers=headers)
            with urllib.request.urlopen(video_req) as vresp, open('assets/hero_bg_video.mp4', 'wb') as f:
                f.write(vresp.read())
            print("EXACT PINTEREST VIDEO DOWNLOADED SUCCESSFULLY!")
        else:
            print("No direct mp4 match found in initial HTML, searching JSON payload...")
            json_matches = re.findall(r'https%3A%2F%2Fv1\.pinimg\.com%2Fvideos%2F[^\s"\'\<\>]+', html)
            if json_matches:
                unquoted = urllib.parse.unquote(json_matches[0])
                print("Found unquoted video URL:", unquoted)
                video_req = urllib.request.Request(unquoted, headers=headers)
                with urllib.request.urlopen(video_req) as vresp, open('assets/hero_bg_video.mp4', 'wb') as f:
                    f.write(vresp.read())
                print("EXACT PINTEREST VIDEO DOWNLOADED SUCCESSFULLY FROM JSON!")
except Exception as e:
    print("Error:", e)
