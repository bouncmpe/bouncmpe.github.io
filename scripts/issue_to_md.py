import os, re, unicodedata

# 1) Inputs
title  = os.getenv("ISSUE_TITLE","").strip()
body   = os.getenv("ISSUE_BODY","").strip()
labels = os.getenv("ISSUE_LABELS","").lower()

# 2) Type
content_type = "news" if "news" in labels else "event"

# 3) Slugify helper
def slugify(t):
    t = unicodedata.normalize("NFKD", t)
    t = t.encode("ascii","ignore").decode("ascii")
    t = re.sub(r"[^\w\s-]","", t.lower())
    return re.sub(r"[-\s]+","-", t).strip("-_")

# 4) Parse body into fields
def parse_issue_body(md):
    fields = {}
    blocks = re.split(r"^#{1,6}\s+", md, flags=re.MULTILINE)[1:]
    for blk in blocks:
        lines = blk.splitlines()
        if not lines: continue
        label = lines[0].strip()
        val   = "\n".join(lines[1:]).strip()
        fields[label] = val
    return fields

parsed = parse_issue_body(body)

# DEBUG: dump parsed fields
print("🔍 Parsed fields dump:")
for k, v in parsed.items():
    print(f"  • {repr(k)} -> {repr(v[:50] + ('…' if len(v)>50 else ''))}")

# 5) Lookup helper
def get_field(fragment):
    for k,v in parsed.items():
        if fragment.lower() in k.lower():
            return v.strip()
    return ""

# 6) Build paths
raw_date = get_field("date and time") or get_field("date")
date     = raw_date.split("T")[0] if raw_date else "unknown-date"
slug     = slugify(title)
folder   = f"content/{content_type}s/{date}-{content_type}-{slug}"
os.makedirs(folder, exist_ok=True)
lang     = "tr" if re.search(r"[çğıöşüÇĞİÖŞÜ]", title) else "en"
outfile  = f"{folder}/index.{lang}.md"

# 7) Frontmatter
fm = ["---"]
if content_type=="news":
    fm += [
      "type: news",
      f"title: {title}",
      f"description: {get_field('description')}",
      f"date: {date}",
    ]
    img = get_field("image")
    if img: fm.append(f"thumbnail: {img}")
    fm.append("featured: false")
else:
    speaker = get_field("speaker") or get_field("name")
    fm += [
      "type: phd-thesis-defense",
      f"title: {title}",
      f"name: {speaker}",
      f"datetime: {raw_date}",
      f"duration: {get_field('duration')}",
      f"location: {get_field('location')}",
    ]
fm.append("---\n")

# 8) === NEW DEBUG: Show what we're about to try as body ===
print("🔍 Attempting to extract body text from these keys:")
for key in parsed.keys():
    print(f"   - {repr(key)}")

# 9) Extract body text
body_text = (
    get_field("content")
    or get_field("extra information")
    or get_field("abstract")
)
print(f"🔍 After primary get_field: body_text={repr(body_text[:100] + ('…' if len(body_text)>100 else ''))}")

# 10) Fallback if still empty
if not body_text:
    print("🔍 body_text empty, running fallback on leftover fields")
    exclude = {
        "title","description","date","image","thumbnail",
        "speaker","name","datetime","duration","location","featured"
    }
    parts = []
    for label, val in parsed.items():
        if not any(e in label.lower() for e in exclude):
            print(f"   • Fallback includes from {repr(label)}: {repr(val[:50]+'…' if len(val)>50 else val)}")
            parts.append(val)
    body_text = "\n\n".join(parts)
    print(f"🔍 After fallback: body_text={repr(body_text[:100] + ('…' if len(body_text)>100 else ''))}")

# 11) Write file
with open(outfile,"w",encoding="utf-8") as f:
    f.write("\n".join(fm))
    f.write(body_text)

print(f"✅ Created markdown at: {outfile}")

