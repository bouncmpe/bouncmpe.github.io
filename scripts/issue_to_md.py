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

# 3) Slugify
def slugify(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-_")

# 4) Parse issue body
def parse_issue_body(md):
    fields = {}
    blocks = re.split(r"^#{1,6}\s+", md, flags=re.MULTILINE)[1:]
    for blk in blocks:
        lines = blk.splitlines()
        if not lines:
            continue
        label = lines[0].strip()
        value = "\n".join(lines[1:]).strip()
        fields[label] = value
    return fields

parsed = parse_issue_body(body)

# 5) Helper to fetch field
def get_field(label):
    return parsed.get(label, "").strip()

# 6) Download image if present (returns local path or empty)
def download_image(md_link):
    print("🔍 Image field:", md_link)
    # Match Markdown ![](url) or HTML <img src="url">
    md_match = re.search(r"\((https?://[^)]+)\)", md_link)
    html_match = re.search(r'src="([^"]+)"', md_link)
    url = md_match.group(1) if md_match else html_match.group(1) if html_match else None

    if not url:
        print("❌ No valid image URL found.")
        return ""

    try:
        r = requests.get(url)
        r.raise_for_status()

        content_type = r.headers.get("Content-Type", "")
        ext = {
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "image/jpg": ".jpg",
            "image/gif": ".gif"
        }.get(content_type, "")

        filename = os.path.basename(urlparse(url).path)
        if not os.path.splitext(filename)[1] and ext:
            filename += ext  # Add extension if missing

        save_dir = "uploads"
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)

        with open(save_path, "wb") as f:
            f.write(r.content)

        print(f"✅ Saved image to: {save_path}")
        return save_path
    except Exception as e:
        print(f"❌ Failed to download image: {e}")
        return ""

# 7) Determine folder & date
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

# 8) Process image
img_md = get_field("Image (drag & drop here)") if is_news else get_field("Image (optional, drag & drop)")
th_thumb = download_image(img_md) if img_md else ""

# 9) Write files for en & tr
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

    path = f"{base}/index.{lang}.md"
    with open(path, 'w', encoding='utf-8') as f:
        f.write("\n".join(fm))
        f.write(content)
    print(f"✅ Created: {path}")

