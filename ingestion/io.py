import requests
import xml.etree.ElementTree as ET
import json
import os


def parse_sitemap(sitemap_url):
    print(f"[SITEMAP] Fetching: {sitemap_url}")

    res = requests.get(sitemap_url)
    res.raise_for_status()

    root = ET.fromstring(res.content)

    ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    urls = []

    for url in root.findall("ns:url", ns):
        loc = url.find("ns:loc", ns).text
        lastmod = url.find("ns:lastmod", ns).text

        urls.append({
            "url": loc,
            "lastmod": lastmod
        })

    print(f"[SITEMAP] Found {len(urls)} URLs")
    return urls


def write_jsonl(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "a", encoding="utf-8") as f:
        if data:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")