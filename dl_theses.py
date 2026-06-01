#!/usr/bin/env python3
"""Download theses PDFs into thesis/.

Google Drive: uses gdown if available, falls back to urllib with confirm=t.
Direct URLs: plain urllib download.
"""
import os
import sys
import time
import urllib.request

DEST = os.path.join(os.path.dirname(__file__), "thesis")
os.makedirs(DEST, exist_ok=True)

# Try to import gdown (pip install gdown) for reliable GDrive downloads
try:
    import gdown
    HAS_GDOWN = True
except ImportError:
    HAS_GDOWN = False
    print("gdown not found – falling back to urllib (may fail for large files).\n"
          "Install with:  pip install gdown", file=sys.stderr)


def dl_gdrive(filename, file_id):
    path = os.path.join(DEST, filename)
    if os.path.exists(path):
        print(f"SKIP {filename} (already exists)")
        return
    if HAS_GDOWN:
        try:
            gdown.download(id=file_id, output=path, quiet=False)
            print(f"OK  {filename}")
        except Exception as e:
            print(f"FAIL {filename}: {e}")
    else:
        url = f"https://drive.google.com/uc?export=download&id={file_id}&confirm=t"
        _dl_url(filename, url)


def dl_url(filename, url):
    path = os.path.join(DEST, filename)
    if os.path.exists(path):
        print(f"SKIP {filename} (already exists)")
        return
    _dl_url(filename, url)


def _dl_url(filename, url):
    path = os.path.join(DEST, filename)
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            ),
        })
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        with open(path, "wb") as f:
            f.write(data)
        print(f"OK  {filename}  ({len(data) // 1024} KB)")
    except Exception as e:
        print(f"FAIL {filename}: {e}")
    time.sleep(1)


# ── Theses ────────────────────────────────────────────────────────────────────
dl_gdrive("granero_msc.pdf",    "156gX_S1wC6laya6wc6B6mhUDK_x5jI-d")
dl_gdrive("parodi_msc.pdf",     "1y18n8s7G7aNF915tvr4bannGVHs9bF8x")
dl_gdrive("foggetti_phd.pdf",   "1t_DMEh3UT390dZSNOVJ4w1hli-E2HJ1g")
dl_gdrive("artyukhin_phd.pdf",  "127BQ69C7hAYD6L31q03n1kIkPPTLP5LB")
dl_url(   "ponet_phd.pdf",
          "https://ricerca.sns.it/retrieve/e3aacdfe-6160-4c98-e053-3705fe0acb7e/"
          "Ponet_Thesis_revised.pdf")
