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
        if not lines: continue
        label = lines[0].strip()
        val   = "\n".join(lines[1:]).strip()
        fields[label] = val
    return fields

parsed = parse_issue_body(body)

# ── 5) Debug (remove/comment out once you confirm fields)
print("🔍 Parsed fields:")
for k,v in parsed.items():
    print(f" • {repr(k)} → {repr(v[:30] + ('…' if len(v)>30 else ''))}")

# ── 6) Case‑insensitive lookup
def get_field(fragment):
    for k,v in parsed.items():
        if fragment.lower() in k.lower():
            return v.strip()
    return ""

# ── 7) Build folder & filenames
raw_date = get_field("date and time") or get_field("date")
date     = raw_date.split("T")[0] if raw_date else "unknown-date"
slug     = slugify(title)
folder   = f"content/{content_type}s/{date}-{content_type}-{slug}"
os.makedirs(folder, exist_ok=True)
lang     = "tr" if re.search(r"[çğıöşüÇĞİÖŞÜ]", title) else "en"
out_md   = f"{folder}/index.{lang}.md"

# ── 8) Frontmatter assembly
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
    fm += [
        "type: phd-thesis-defense",
        f"title: {title}",
        f"name: {get_field('speaker') or get_field('name')}",
        f"datetime: {raw_date}",
        f"duration: {get_field('duration')}",
        f"location: {get_field('location')}"
    ]
fm.append("---\n")

# ── 9) Body content: first try known fields, else fallback
body_content = (
    get_field("content")
    or get_field("extra information")
    or get_field("abstract")
)
if not body_content:
    # fallback: take every parsed value not used in frontmatter
    used_keys = {
        # for news
        "description","date","image","thumbnail",
        # for event
        "speaker","name","datetime","duration","location"
    }
    parts = []
    for label,val in parsed.items():
        if not any(u in label.lower() for u in used_keys):
            parts.append(val)
    body_content = "\n\n".join(parts)

# ── 10) Write the file
with open(out_md, "w", encoding="utf-8") as f:
    f.write("\n".join(fm))
    f.write(body_content)

print(f"✅ Created markdown at: {out_md}")

