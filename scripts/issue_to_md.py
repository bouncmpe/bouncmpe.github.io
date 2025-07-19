import os, re, unicodedata

# 1. Inputs from GitHub Actions
body = os.getenv("ISSUE_BODY", "").strip()
labels = os.getenv("ISSUE_LABELS", "").lower()

# 2. Content type
content_type = "event"

# 3. Slugify helper
def slugify(text):
    t = unicodedata.normalize("NFKD", text)
    t = t.encode("ascii", "ignore").decode("ascii")
    t = re.sub(r"[^\w\s-]", "", t.lower())
    return re.sub(r"[-\s]+", "-", t).strip("-_ ")

# 4. Parse issue body into {Heading: Value}
def parse_issue_body(md):
    fields = {}
    blocks = re.split(r"^#{1,6}\s+", md, flags=re.MULTILINE)[1:]
    for blk in blocks:
        lines = blk.splitlines()
        label = lines[0].strip()
        val = "\n".join(lines[1:]).strip()
        fields[label] = val
    return fields

parsed = parse_issue_body(body)

# 5. Map form IDs to labels
def get_field(id_label):
    mapping = {
        'title_en': 'Event Title (EN)',
        'title_tr': 'Event Title (TR)',
        'name': 'Speaker/Presenter Name',
        'datetime': 'Date and Time (ISO format)',
        'duration': 'Duration',
        'location_en': 'Location (EN)',
        'location_tr': 'Location (TR)',
        'description_en': 'Description (EN)',
        'description_tr': 'Description (TR)',
    }
    return parsed.get(mapping[id_label], "").strip()

# 6. Extract core values
raw_dt = get_field('datetime')
date = raw_dt.split('T')[0]
title_en = get_field('title_en')
title_tr = get_field('title_tr')
slug = slugify(title_en)
folder = f"content/events/{date}-event-{slug}"
os.makedirs(folder, exist_ok=True)

# 7. Common frontmatter lines
def make_frontmatter(title):
    return [
        "---",
        "type: phd-thesis-defense",
        f"title: {title}",
        f"name: {get_field('name')}",
        f"datetime: {raw_dt}",
        f"duration: {get_field('duration')}",
        f"location: {get_field(f'location_{'en' if title==title_en else 'tr'}')}",
        "---\n"
    ]

# 8. Write both language files
for lang, title_val, loc_id, desc_id in [
    ('en', title_en, 'location_en', 'description_en'),
    ('tr', title_tr, 'location_tr', 'description_tr')
]:
    fm = make_frontmatter(title_val)
    body_text = get_field(desc_id)
    out = f"{folder}/index.{lang}.md"
    with open(out, 'w', encoding='utf-8') as f:
        f.write("\n".join(fm))
        f.write(body_text)
    print(f" Created: {out}")

