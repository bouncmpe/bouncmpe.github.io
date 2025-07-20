import os
import re
import unicodedata
import requests
from urllib.parse import urlparse

# 1) Inputs
labels = os.getenv("ISSUE_LABELS", "").lower()
body = os.getenv("ISSUE_BODY", "").strip()

# 2) Determine type
is_news = "news" in labels

# 3) Slugify helper
def slugify(text):
    t = unicodedata.normalize("NFKD", text)
    t = t.encode("ascii", "ignore").decode("ascii")
    t = re.sub(r"[^\w\s-]", "", t.lower())
    return re.sub(r"[-\s]+", "-", t).strip("-_")

# 4) Parse issue body into {Heading: Value}
def parse_issue_body(md):
    fields = {}
    blocks = re.split(r"^#{1,6}\s+", md, flags=re.MULTILINE)[1:]
    for blk in blocks:
        lines = blk.splitlines()
        if not lines:
            continue
        label = lines[0].strip()
        val = "\n".join(lines[1:]).strip()
        fields[label] = val
    return fields

parsed = parse_issue_body(body)

# 5) Simple getter

def get_field(label):
    return parsed.get(label, "").strip()

# 6) Download image from markdown or HTML tag
def download_image(md_link):
    print(f" Raw image input: {md_link}")
    url = ""
    # Try markdown syntax
    m = re.search(r"!\[[^\]]*\]\((https?://[^)]+)\)", md_link)
    if m:
        url = m.group(1)
    else:
        # Try any src attribute (for GitHub attachments)
        m2 = re.search(r"src=\"(https?://[^\"]+)\"", md_link)
        if m2:
            url = m2.group(1)
    if not url:
        print(" No valid image URL found in input.")
        return ""
    print(f"📥 Downloading image from: {url}")
    # derive filename and extension from response headers
    save_dir = "uploads"
    os.makedirs(save_dir, exist_ok=True)
    try:
        r = requests.get(url)
        r.raise_for_status()
        # determine extension
        content_type = r.headers.get('Content-Type', '')
        ext = ''
        if 'png' in content_type:
            ext = '.png'
        elif 'jpeg' in content_type:
            ext = '.jpg'
        elif 'gif' in content_type:
            ext = '.gif'
        # base name from last path segment
        base = os.path.basename(urlparse(url).path)
        filename = base + ext
        save_path = os.path.join(save_dir, filename)
        with open(save_path, "wb") as f:
            f.write(r.content)
        print(f" Saved image to: {save_path}")
        return save_path
    except Exception as e:
        print(f" Failed to download: {e}")
        return ""

# 7) Determine folder & date) Determine folder & date
if is_news:
    date = get_field("Date (YYYY-MM-DD)")
    slug = slugify(get_field("News Title (EN)"))
    base = f"content/news/{date}-news-{slug}"
else:
    raw_dt = get_field("Date and Time (ISO format)")
    date = raw_dt.split("T")[0]
    slug = slugify(get_field("Event Title (EN)"))
    base = f"content/events/{date}-event-{slug}"

os.makedirs(base, exist_ok=True)

# 8) Process image field
img_label = "Image (drag & drop here)" if is_news else "Image (optional, drag & drop)"
img_md = get_field(img_label)
print(f"📎 Image field content: {img_md}")
th_thumb = download_image(img_md) if img_md else ""

# 9) Generate .en.md and .tr.md

for lang in ["en", "tr"]:
    fm = ["---"]
    if is_news:
        fm += [
            "type: news",
            f"title: {get_field(f'News Title ({lang.upper()})')}",
            f"description: {get_field(f'Short Description ({lang.upper()})')}",
            f"date: {date}"
        ]
        if th_thumb:
            fm.append(f"thumbnail: {th_thumb}")
        fm.append("featured: false")
    else:
        fm += [
            "type: phd-thesis-defense",
            f"title: {get_field(f'Event Title ({lang.upper()})')}",
            f"name: {get_field('Speaker/Presenter Name')}",
            f"datetime: {raw_dt}",
            f"duration: {get_field('Duration')}",
            f"location: {get_field(f'Location ({lang.upper()})')}"
        ]
    fm.append("---\n")

    content_label = "Full Content" if is_news else "Description"
    content = get_field(f'{content_label} ({lang.upper()})')

    out = f"{base}/index.{lang}.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(fm))
        f.write(content)
    print(f" Created: {out}")
```

