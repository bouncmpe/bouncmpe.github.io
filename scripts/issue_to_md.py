import os
import re
import unicodedata
import requests
from github import Github
from urllib.parse import urlparse

# 1) Read inputs
issue_number = int(os.getenv("ISSUE_NUMBER"))
token = os.getenv("GITHUB_TOKEN")
repo_name = os.getenv("REPO_NAME")

g = Github(token)
repo = g.get_repo(repo_name)
issue = repo.get_issue(number=issue_number)

labels = ",".join([label.name.lower() for label in issue.labels])
body = issue.body.strip()

is_news = "news" in labels

# 2) Slugify helper
def slugify(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-_ ")

# 3) Parse issue body into a dict of fields
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

# 4) Simple getter
def get_field(label):
    return parsed.get(label, "").strip()

# 5) Download image if present: save under assets/uploads to match site structure
#    Returns frontmatter path 'uploads/<filename>'.
def download_image(md_input):
    print(f" Raw image input: {md_input}")
    url = None
    # Try Markdown syntax
    m = re.search(r"!\[[^\]]*\]\((https?://[^)]+)\)", md_input)
    if m:
        url = m.group(1)
    else:
        # Try HTML <img src="..."
        m2 = re.search(r'src=\"(https?://[^\"]+)\"', md_input)
        if m2:
            url = m2.group(1)
    if not url:
        print(" No valid image URL found.")
        return ""

    print(f" Downloading image from: {url}")
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f" Failed to fetch image: {e}")
        return ""

    # Infer extension from Content-Type
    ct = resp.headers.get("Content-Type", "")
    ext = ''
    if 'png' in ct:
        ext = '.png'
    elif 'jpeg' in ct or 'jpg' in ct:
        ext = '.jpg'
    elif 'gif' in ct:
        ext = '.gif'

    # Build filename
    path_part = urlparse(url).path
    name = os.path.basename(path_part) or 'image'
    if not os.path.splitext(name)[1] and ext:
        name += ext

    # Save under assets/uploads
    save_dir = os.path.join('assets', 'uploads')
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, name)

    try:
        with open(save_path, 'wb') as f:
            f.write(resp.content)
        print(f" Saved image to: {save_path}")
        # Return frontmatter path
        return f"uploads/{name}"
    except Exception as e:
        print(f" Error saving image: {e}")
        return ""

# 6) Determine base folder and date
if is_news:
    date = get_field('Date (YYYY-MM-DD)')
    slug = slugify(get_field('News Title (EN)'))
    base = f"content/news/{date}-news-{slug}"
else:
    raw_dt = get_field('Date and Time (ISO format)')
    date = raw_dt.split('T')[0]
    slug = slugify(get_field('Event Title (EN)'))
    base = f"content/events/{date}-event-{slug}"

os.makedirs(base, exist_ok=True)

# 7) Process image field
img_label = 'Image (drag & drop here)' if is_news else 'Image (optional, drag & drop)'
img_md = get_field(img_label)
thumbnail_path = download_image(img_md) if img_md else ''

# 8) Write bilingual markdown files
for lang in ['en', 'tr']:
    fm = ['---']
    if is_news:
        fm += [
            'type: news',
            f"title: {get_field(f'News Title ({lang.upper()})')}",
            f"description: {get_field(f'Short Description ({lang.upper()})')}",
            f"date: {date}"
        ]
        if thumbnail_path:
            fm.append(f"thumbnail: {thumbnail_path}")
        fm.append('featured: false')
    else:
        fm += [
            'type: phd-thesis-defense',
            f"title: {get_field(f'Event Title ({lang.upper()})')}",
            f"name: {get_field('Speaker/Presenter Name')}",
            f"datetime: {raw_dt}",
            f"duration: {get_field('Duration')}",
            f"location: {get_field(f'Location ({lang.upper()})')}"
        ]
    fm.append('---\n')
    content_label = 'Full Content' if is_news else 'Description'
    content = get_field(f'{content_label} ({lang.upper()})')
    out_file = f"{base}/index.{lang}.md"
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(fm))
        f.write(content)
    print(f" Created: {out_file}")

