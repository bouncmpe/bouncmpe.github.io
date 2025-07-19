import os
import re
import unicodedata

# ── 1) Read environment variables set by GitHub Actions
title  = os.getenv("ISSUE_TITLE", "").strip()
body   = os.getenv("ISSUE_BODY",  "").strip()
labels = os.getenv("ISSUE_LABELS", "").lower()

# ── 2) Determine whether this is a news or an event
content_type = "news" if "news" in labels else "event"

# ── 3) Slugify the title for use in folder names
def slugify(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-_")

# ── 4) Parse the issue body into a dict of “Heading → Value”
def parse_issue_body(md):
    fields = {}
    # Split on “### ” markers
    blocks = re.split(r"^###\s+", md, flags=re.MULTILINE)[1:]
    for block in blocks:
        lines = block.splitlines()
        if not lines: 
            continue
        label = lines[0].strip()
        value = "\n".join(lines[1:]).strip()
        fields[label] = value
    return fields

parsed = parse_issue_body(body)

# ── 5) DEBUG: print out exactly what headings GitHub gave us
print(" Parsed fields and sample values:")
for k, v in parsed.items():
    sample = v[:30] + ("…" if len(v) > 30 else "")
    print(f"  • {repr(k)} → {repr(sample)}")

# ── 6) Helper to find a field by partial, case-insensitive match
def get_field(key_fragment):
    for label, val in parsed.items():
        if key_fragment.lower() in label.lower():
            return val.strip()
    return ""

# ── 7) Extract core values
raw_date = get_field("date and time") or get_field("date")
date     = raw_date.split("T")[0] if raw_date else ""
slug     = slugify(title)
folder   = f"content/{content_type}s/{date}-{content_type}-{slug}"
os.makedirs(folder, exist_ok=True)

# Pick language suffix by detecting Turkish chars in title
lang = "tr" if re.search(r"[çğıöşüÇĞİÖŞÜ]", title) else "en"
out_file = f"{folder}/index.{lang}.md"

# ── 8) Build YAML frontmatter
fm = ["---"]
if content_type == "news":
    fm.append(f"type: news")
    fm.append(f"title: {title}")
    fm.append(f"description: {get_field('description')}")
    fm.append(f"date: {date}")
    thumb = get_field("image")
    if thumb:
        fm.append(f"thumbnail: {thumb}")
    fm.append("featured: false")
else:
    fm.append(f"type: phd-thesis-defense")
    fm.append(f"title: {title}")
    # match any speaker/presenter/name field
    speaker = get_field("speaker") or get_field("name")
    fm.append(f"name: {speaker}")
    fm.append(f"datetime: {raw_date}")
    fm.append(f"duration: {get_field('duration')}")
    fm.append(f"location: {get_field('location')}")
fm.append("---\n")

# ── 9) Determine body content (supports multiline)
body_content = (
    get_field("full content")
    or get_field("extra information")
    or get_field("abstract")
    or ""
)

# ── 10) Write the file as UTF‑8
with open(out_file, "w", encoding="utf-8") as f:
    f.write("\n".join(fm))
    f.write(body_content)

print(f" Created markdown at: {out_file}")

