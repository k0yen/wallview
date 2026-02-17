import os
import json
import requests
from datetime import datetime

# Configuration
SAVE_DIR = "wallpapers"
JSON_FILE = "wallpapers.json"
# You can get a free key at api.nasa.gov. 'DEMO_KEY' works but has limits.
NASA_API_URL = "https://api.nasa.gov/planetary/apod?api_key=1OPB8bDryQxm4Q3l5tqQzKzEn3WBdm0HYWhY3fiB"

def fetch_wallpaper():
    os.makedirs(SAVE_DIR, exist_ok=True)
    
    # 1. Get the image URL from NASA
    response = requests.get(NASA_API_URL).json()
    img_url = response.get("hdurl") or response.get("url")
    date_str = response.get("date", datetime.now().strftime("%Y-%m-%d"))
    
    if not img_url or response.get("media_type") != "image":
        print("Today is a video or no image found. Skipping.")
        return

    # 2. Download the image
    img_data = requests.get(img_url).content
    filename = f"{date_str}-nasa.jpg"
    filepath = os.path.join(SAVE_DIR, filename)

    with open(filepath, 'wb') as handler:
        handler.write(img_data)
    print(f"Saved: {filename}")

def update_manifest():
    # 3. Traverse folder and save to JSON dynamically
    valid_exts = ('.jpg', '.jpeg', '.png', '.webp')
    files = [os.path.join(SAVE_DIR, f) for f in os.listdir(SAVE_DIR) 
             if f.lower().endswith(valid_exts)]
    
    # Sort by name (which is date) so newest appears last or first
    files.sort(reverse=True) 

    with open(JSON_FILE, 'w') as f:
        json.dump(files, f, indent=2)
    print(f"Updated {JSON_FILE} with {len(files)} wallpapers.")

if __name__ == "__main__":
    fetch_wallpaper()
    update_manifest()

