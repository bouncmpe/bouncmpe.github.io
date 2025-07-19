import os
import re
import unicodedata
import os

# Environment input from GitHub Actions
title = os.getenv("ISSUE_TITLE", "").strip()
body = os.getenv("ISSUE_BODY", "").strip()
labels = os.getenv("ISSUE_LABELS", "").lower()

# Determine type
content_type = "news" if "news" in labels else "event"

# Convert title into slug
def slugify(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-_")

# Parse issue body
def parse_issue_body(body):
    parts = re.split(r"###\s+", body)[1:]  # Skip initial text
    data = {}
    for part in parts:
        lines = part.strip().split("\n", 1)
        key = lines[0].strip().lower()
        value = lines[1].strip() if len(lines) > 1 else ""
        data[key] = value
    return data

parsed = parse_issue_body(body)

# Get values
raw_date = ""
for key in parsed:
    if "date and time" in key.lower() or "date" in key.lower():
        raw_date = parsed[key]
        break
date = raw_date.split("t")[0]
slug = slugify(title)
folder_name = f"{date}-{content_type}-{slug}"
folder_path = f"content/{content_type}s/{folder_name}"
os.makedirs(folder_path, exist_ok=True)

# Determine language
lang_suffix = "tr" if re.search(r"[çğıöşü]", title.lower()) else "en"
filepath = f"{folder_path}/index.{lang_suffix}.md"

# Build frontmatter
frontmatter = "---\n"
if content_type == "news":
    frontmatter += f"type: news\n"
    frontmatter += f"title: {title}\n"
    frontmatter += f"description: {parsed.get('short description', '')}\n"
    frontmatter += f"date: {date}\n"
    thumb = parsed.get("image path (optional)", "").strip()
    if thumb:
        frontmatter += f"thumbnail: {thumb}\n"
    frontmatter += f"featured: false\n"
else:
    frontmatter += f"type: phd-thesis-defense\n"
    frontmatter += f"title: {title}\n"
    frontmatter += f"name: {parsed.get('speaker/presenter name', '')}\n"
    frontmatter += f"datetime: {raw_date}\n"
    frontmatter += f"duration: {parsed.get('duration', '')}\n"
    frontmatter += f"location: {parsed.get('location', '')}\n"
frontmatter += "---\n\n"

# Final content
markdown_content = frontmatter + parsed.get("full content (markdown allowed)", parsed.get("extra information or abstract (optional)", ""))

# Write
with open(filepath, "w", encoding="utf-8") as f:
    f.write(markdown_content)

print(f" Created: {filepath}")
