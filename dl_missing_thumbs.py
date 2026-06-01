#!/usr/bin/env python3
"""Download thumbnails for publications that don't have them yet."""
import urllib.request, time, os, re
from PIL import Image
from io import BytesIO

THUMBS = "/home/sergey/iqmt.eu/thumbnails"
os.makedirs(THUMBS, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

def fetch_html(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode('utf-8', errors='ignore'), r.url

def find_og_image(html):
    m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html)
    if m: return m.group(1)
    m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', html)
    if m: return m.group(1)
    return None

def download_image(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()

def save_thumbnail(name, data, target_w=320, target_h=162):
    img = Image.open(BytesIO(data)).convert('RGB')
    # Crop to target aspect ratio from center, then resize
    src_w, src_h = img.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h
    if src_ratio > target_ratio:
        # wider than needed — crop sides
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, src_h))
    else:
        # taller than needed — crop top portion (keep top for figures)
        new_h = int(src_w / target_ratio)
        img = img.crop((0, 0, src_w, new_h))
    img = img.resize((target_w, target_h), Image.LANCZOS)
    path = f"{THUMBS}/{name}.png"
    img.save(path, 'PNG', optimize=True)
    print(f"  saved {name}.png ({target_w}x{target_h})")
    return path

def process(name, url, fallback_img_url=None):
    print(f"\n--- {name} ---")
    path = f"{THUMBS}/{name}.png"
    if os.path.exists(path):
        print(f"  already exists, skipping")
        return

    img_url = fallback_img_url
    if not img_url:
        try:
            html, final_url = fetch_html(url)
            img_url = find_og_image(html)
            print(f"  og:image = {img_url}")
        except Exception as e:
            print(f"  fetch failed: {e}")

    if img_url:
        try:
            data = download_image(img_url)
            save_thumbnail(name, data)
        except Exception as e:
            print(f"  image download failed: {e}")
    else:
        print(f"  no image found")
    time.sleep(1)

papers = [
    # (output name, paper URL, optional direct image URL)
    ("larkin_length_afm_writing",
     "https://www.researchsquare.com/article/rs-9405081/v1"),

    ("nonlocal_magnetoelectric_switching",
     "https://www.sciencedirect.com/science/article/pii/S2950636025003676"),

    ("competition_dyfeO3_soliton",
     "https://journals.aps.org/prresearch/abstract/10.1103/kwrl-x4hw"),

    ("carbides_honeycomb",
     "https://pubs.aip.org/jap/article/138/8/084303/3360235/Group-IV-binary-carbides-with-double-layer"),

    ("trimerization_domain_walls",
     "https://journals.aps.org/prb/abstract/10.1103/PhysRevB.111.184101"),

    ("multiferroic_kinks_nispintronic",
     "https://www.nature.com/articles/s44306-024-00020-9"),

    ("ferroelectricity_mof",
     "https://arxiv.org/abs/2204.09546"),
]

for name, url, *rest in papers:
    fallback = rest[0] if rest else None
    process(name, url, fallback)

print("\nDone.")
