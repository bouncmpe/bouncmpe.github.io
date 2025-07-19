import os
import re
import unicodedata

# ── 1) Read inputs from GitHub Actions
title  = os.getenv("ISSUE_TITLE", "").strip()
body   = os.getenv("ISSUE_BODY",  "").strip()
labels = os.getenv("ISSUE_LABELS", "").lower()

# ── 2) Determine news vs. event
content_type = "news" if "news" in labels else "event"

# ── 3) Slugify helper
def slugify(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii","ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-_")

# ── 4) Parse body into { Heading → Value } (multiline safe)
def parse_issue_body(md):
    fields = {}
    blocks = re.split(r"^###\s+", md, flags=re.MULTILINE)[1:]
    for blk in blocks:
        lines = blk.splitlines()
        if not lines: 
            continue
        label = lines[0].strip()
        val   = "\n".join(lines[1:]).strip()
        fields[label] = val
    return fields

parsed = parse_issue_body(body)

# ── 5) DEBUG: print parsed fields (remove/comment out later)
print("🔍 Parsed fields:")
for k,v in parsed.items():
    print(f" • {repr(k)} → {repr(v[:30] + ('…' if len(v)>30 else ''))}")

# ── 6) Case‑insensitive lookup helper
def get_field(fragment):
    for k,v in parsed.items():
        if fragment.lower() in k.lower():
            return v.strip()
    return ""

# ── 7) Build folder & filename
raw_date = get_field("date and time") or get_field("date")
date     = raw_date.split("T")[0] if raw_date else "unknown-date"
slug     = slugify(title)
folder   = f"content/{content_type}s/{date}-{content_type}-{slug}"
os.makedirs(folder, exist_ok=True)
lang     = "tr" if re.search(r"[çğıöşüÇĞİÖŞÜ]", title) else "en"
out_md   = f"{folder}/index.{lang}.md"

# ── 8) Build YAML frontmatter
fm = ["---"]
if content_type == "news":
    fm += [
        "type: news",
        f"title: {title}",
        f"description: {get_field('description')}",
        f"date: {date}"
    ]
    thumb = get_field("image")
    if thumb: fm.append(f"thumbnail: {thumb}")
    fm.append("featured: false")
else:
    speaker = get_field("speaker") or get_field("name")
    fm += [
        "type: phd-thesis-defense",
        f"title: {title}",
        f"name: {speaker}",
        f"datetime: {raw_date}",
        f"duration: {get_field('duration')}",
        f"location: {get_field('location')}"
    ]
fm.append("---\n")

# ── 9) Pull in your real body text
#    First try explicit fields:
body_content = (
    get_field("content")
    or get_field("extra information")
    or get_field("abstract")
)

# ── 10) If still empty, fallback on *all* fields except these keys
if not body_content:
    exclude = {"title","description","date","image","thumbnail",
               "speaker","name","datetime","duration","location","featured"}
    parts = []
    for label,val in parsed.items():
        if all(e not in label.lower() for e in exclude):
            parts.append(val)
    body_content = "\n\n".join(parts)

# ── 11) Write out the markdown file
with open(out_md, "w", encoding="utf-8") as f:
    f.write("\n".join(fm))
    f.write(body_content)

print(f" Created markdown at: {out_md}")

