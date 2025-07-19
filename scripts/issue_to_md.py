import os
import re
import unicodedata

# GitHub Actions environment variables
title = os.getenv("ISSUE_TITLE", "").strip()
body = os.getenv("ISSUE_BODY", "").strip()
labels = os.getenv("ISSUE_LABELS", "").lower()

# Determine content type
content_type = "news" if "news" in labels else "event"

# Slugify title for folder name
def slugify(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-_")

# Parse issue body safely (supports multiline content)
def parse_issue_body(body):
    fields = {}
    blocks = re.split(r"###\s+", body)[1:]
    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) > 1:
            label = lines[0].strip()
            value = "\n".join(lines[1:]).strip()
            fields[label] = value
    return fields

parsed = parse_issue_body(body)

# Helper to get fields case-insensitively
def get_field(key_contains):
    for k, v in parsed.items():
        if key_contains.lower() in k.lower():
            return v.strip()
    return ""

# Get datetime + slugify title
raw_date = get_field("date and time") or get_field("date")
date = raw_date.split("T")[0]
slug = slugify(title)
folder_path = f"content/{content_type}s/{date}-{content_type}-{slug}"
os.makedirs(folder_path, exist_ok=True)

# Detect language (tr or en)
lang_suffix = "tr" if re.search(r"[çğıöşü]", title.lower()) else "en"
filepath = f"{folder_path}/index.{lang_suffix}.md"

# Build frontmatter
frontmatter = "---\n"
if content_type == "news":
    frontmatter += f"type: news\n"
    frontmatter += f"title: {title}\n"
    frontmatter += f"description: {get_field('description')}\n"
    frontmatter += f"date: {date}\n"
    thumbnail = get_field("image path")
    if thumbnail:
        frontmatter += f"thumbnail: {thumbnail}\n"
    frontmatter += f"featured: false\n"
else:  # Event
    frontmatter += f"type: phd-thesis-defense\n"
    frontmatter += f"title: {title}\n"
    frontmatter += f"name: {get_field('speaker')}\n"
    frontmatter += f"datetime: {raw_date}\n"
    frontmatter += f"duration: {get_field('duration')}\n"
    frontmatter += f"location: {get_field('location')}\n"
frontmatter += "---\n\n"

# Append full content
markdown_content = frontmatter + (get_field("content") or get_field("extra") or get_field("abstract"))

# Write to file
with open(filepath, "w", encoding="utf-8") as f:
    f.write(markdown_content)

print(f" Created: {filepath}")

