import urllib.request, time, os

os.makedirs("/home/sergey/iqmt.eu/thumbnails", exist_ok=True)

def dl(name, url):
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
            'Referer': 'https://sites.google.com/',
        })
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        ext = 'png' if b'PNG' in data[:8] else 'jpg'
        path = f"/home/sergey/iqmt.eu/thumbnails/{name}.{ext}"
        with open(path, 'wb') as f:
            f.write(data)
        print(f"OK  {name}.{ext}  ({len(data)//1024} KB)")
    except Exception as e:
        print(f"FAIL {name}: {e}")
    time.sleep(0.5)

images = [
    ("highlight-1", "https://lh3.googleusercontent.com/sitesv/AA5AbUAmiCbJ7OkUN_Ra2VkCuvTk_a4vJMQZrOEcsGTBjwWW194ZWzdOuXHyyfqT2I8WV4MSue0rcwnxYuq4oK1EhXvEsfGSyVBiLS4AR6IrAxSzJVwFpdrAwm-WqhdFzirOnCjoj69xgvDWNj2deo7c322c2z_5_G7Zzb4csc77KlFiLnbU2vBw_aEBURB4yaecKMlDrcVz=s320"),
    ("highlight-2", "https://lh3.googleusercontent.com/sitesv/AA5AbUDDmSiMhBJph-V544h_USPViWSQvcVIHMMThs190upa-R94tMWvtdF8mzX2lRDrbUU9Q2N8H2nAXdkvGF_y-AHPQtxYa4hsUOmSBs83eAZi4qdz-5M4J4nWeFQv2bYczhb-0-cfrHDbQzcOLZtubEr5z6uO618S7-nXANFN5DGQKFhBEGKNyVuZB-B775fB555rmz7G=s320"),
    ("highlight-3", "https://lh3.googleusercontent.com/sitesv/AA5AbUCnpW39P1UjqElVZ6ECiQIJQRSra6zFHRPIasWyeBw4KS1A35x-hvpdBj6p0sFeEB46d0BuaAPq_y7TiTblFbtB_L5n5tvn_pP9DdpIINA-j2VT7a-SCi9Rm9lDdKbAumFd4uxkzRkdzLFQjUJRuoXeaCwVZnWxQMZgZlnMkEhzl4H9mW0XwhkpWlRJXKtKpVNxyQ=s320"),
    ("highlight-4", "https://lh3.googleusercontent.com/sitesv/AA5AbUCkhVVDzNEgxn-cJGaexw-CDaGPik3pVIxSkUnCZBzV_eIDBs4Vxr6KQEjBCAo38BUIccA_7Iw6Ijd33Hj_NF-jj3ZdASYpRqleDNDU6gngMjtZsi8CPhElFaxRllAXMfB0HjFIEMtR2kMTo3-SFTDzTiKu6vNIqDKBW8-AYSFCycqQkv0WjS1zf0KpHtaVqWMplu=s320"),
    ("highlight-5", "https://lh3.googleusercontent.com/sitesv/AA5AbUCJWjpoMUOwIbKbaieCycKaDk1VJJke1uyiqq8eVNIUIr7lpVlfja8hmQjT5V3cYCK1RxzRjNrA32OYOw5ecBEKHP74k4uRGSgFAPc3JndK-OiJkecpi2sA5e3GURjDFBmyEF50B9gS9pSR45bkI0-A4jp_qrDfGl2KCSO-iQcXM_PGLkXNhy9Z-7WGBV-XU86rPFbWp8t9ohRvzaPznZgiWLnamr0RSF=s320"),
    ("highlight-6", "https://lh3.googleusercontent.com/sitesv/AA5AbUBrZuekR5MMMuS79oQ3z8_KajiVeZMQs1Ym9PD48tTIsERsmye8UJ2UiotoOuNgVqoq0uBWINyGjF8k20JfeVh1h96LuTvOtUMvqz0Q1_qvQi4f-IuQDgA90-jXXuw2pXYww2wc_j4OGNidPprwLfduYdJVYyWe2jFmjrOHSIdnQ4reDP8H11WqhJFPuGdQ1a3X8NVzyPHz4Qc=s320"),
    ("nature-2022",  "https://lh3.googleusercontent.com/sitesv/AA5AbUDJ7AkO87Lu8LXTO0ufLMunKZOuqH3gaD7JXaXhKIi_NTBRSwRya0C3cLQ3nLwMfwVDEQAvKGUSJJUSNUqMoyJriPza9u70Rp-CRYYVrazS8-WHpuJau8LrCxz1AblUl5a8BbTUaapZFLZvYjHRqldu8djTTnkFcrz69lS-7KM8MCg_C9JDMyPEdG620yDzGH2MCDASCn53-R9ANvAydGeLfBy4FN855KQ39gA=s320"),
    ("prb-2023",     "https://lh3.googleusercontent.com/sitesv/AA5AbUDQiWScZXgAoT_eNZ1YZDXIztd10vxDd_eeKXNmDB1xOSwgcQ00e-9zCZxT80hDQUX0mbWcB_MhrBomLHefiXleQAbn2vv1H5ryfbmpMTJAjbj8UKsj3e0MSMPiqUnWIr1Ps7IRvylyZ37NNgmTdQoqlmNdB2796LWodW_RkEW_Og7vrHwaWu9JN_fwYcl7fNzIPDPnCbK3IMX=s320"),
    ("natmat-2021",  "https://lh3.googleusercontent.com/sitesv/AA5AbUAxxl8FUOOWkeNY0_rpkXH1rZqnoC5GRSiM4nBOUa7YGk6GMM6HnUsygLYmtk4x6rCuazsCyww1L-QLeWXkOQ9PnYBFIcBZa7DJjmoeOXl6-1ziYXbtp_OYwYyd090MKDdnU3HUJkuLijR7rJA_ehGVXT0RxUfYbEw_mifK8L6yZy0Prz9ugVtS8-famLRlouLWAlVqfJJWBQosZQ4--A5cyGcfVVNAd6598dE=s320"),
]

for name, url in images:
    dl(name, url)
