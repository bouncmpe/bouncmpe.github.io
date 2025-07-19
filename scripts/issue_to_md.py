import os, re, unicodedata

# 1) Inputs
title  = os.getenv("ISSUE_TITLE","").strip()
body   = os.getenv("ISSUE_BODY","").strip()
labels = os.getenv("ISSUE_LABELS","").lower()

# 2) news vs event
content_type = "news" if "news" in labels else "event"

# 3) Slugify helper
def slugify(t):
    t = unicodedata.normalize("NFKD", t)
    t = t.encode("ascii","ignore").decode("ascii")
    t = re.sub(r"[^\w\s-]","", t.lower())
    return re.sub(r"[-\s]+","-", t).strip("-_")

# 4) Parse headings and values
def parse_issue_body(md):
    fields = {}
    # split on any heading ####
    blocks = re.split(r"^#{1,6}\s+", md, flags=re.MULTILINE)[1:]
    for blk in blocks:
        lines = blk.splitlines()
        label = lines[0].strip()
        val   = "\n".join(lines[1:]).strip()
        fields[label] = val
    return fields

parsed = parse_issue_body(body)

# DEBUG: show parsed keys
print(" Parsed fields:")
for k,v in parsed.items():
    print(f"  • {repr(k)} -> {repr(v[:40]+'…' if len(v)>40 else v)}")

# 5) Case‑insensitive find
def get_field(frag):
    for k,v in parsed.items():
        if frag.lower() in k.lower():
            return v.strip()
    return ""

# 6) Build folder & filename
raw_date = get_field("start date and time") or get_field("date and time") or get_field("date")
date     = raw_date.split("T")[0] if raw_date else "unknown-date"
slug     = slugify(title)
folder   = f"content/{content_type}s/{date}-{content_type}-{slug}"
os.makedirs(folder, exist_ok=True)
lang     = "tr" if re.search(r"[çğıöşüÇĞİÖŞÜ]", title) else "en"
out_md   = f"{folder}/index.{lang}.md"

# 7) Build frontmatter
fm = ["---"]
if content_type == "news":
    fm += [
        "type: news",
        f"title: {title}",
        f"date: {date}",
        f"thumbnail: {get_field('poster or cover image') or ''}",
        "featured: false"
    ]
else:
    fm += [
        "type: phd-thesis-defense",
        f"title: {title}",
        f"name: {get_field('event name')}",
        f"datetime: {raw_date}",
        f"duration: {get_field('duration')}",
        f"location: {get_field('location')}"
    ]
fm.append("---\n")

# 8) Extract body text for events from Description fields
body_text = ""
if content_type == "news":
    # news currently has no body beyond frontmatter
    body_text = ""
else:
    if lang == "en":
        body_text = parsed.get("Description (EN)", "")
    else:
        body_text = parsed.get("Description (TR)", "")

# 9) Write file
with open(out_md, "w", encoding="utf-8") as f:
    f.write("\n".join(fm))
    f.write(body_text)

print(f" Created markdown at: {out_md}")

