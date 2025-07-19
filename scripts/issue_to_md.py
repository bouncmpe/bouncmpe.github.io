import os, re, unicodedata

# 1) Inputs
labels = os.getenv("ISSUE_LABELS", "").lower()
body = os.getenv("ISSUE_BODY", "").strip()

# 2) Determine content type
type_is_news = "news" in labels

# 3) Slugify helper
def slugify(text):
    t = unicodedata.normalize("NFKD", text)
    t = t.encode("ascii", "ignore").decode("ascii")
    t = re.sub(r"[^\w\s-]", "", t.lower())
    return re.sub(r"[-\s]+", "-", t).strip("-_")

# 4) Parse issue body into {Heading: Value}
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

# 5) Helper to fetch by label
def get_label_field(*labels_to_try):
    for lab in labels_to_try:
        for k, v in parsed.items():
            if k.lower() == lab.lower():
                return v
    return ""

# 6) Common date and slug
if type_is_news:
    date = get_label_field("Date (YYYY-MM-DD)")
    slug = slugify(get_label_field("News Title (EN)"))
    folder = f"content/news/{date}-news-{slug}"
else:
    raw_dt = get_label_field("Date and Time (ISO format)")
    date = raw_dt.split("T")[0]
    slug = slugify(get_label_field("Event Title (EN)"))
    folder = f"content/events/{date}-event-{slug}"

os.makedirs(folder, exist_ok=True)

# 7) Build and write files
def write_md(lang):
    if type_is_news:
        fm = [
            "---",
            "type: news",
            f"title: {get_label_field('News Title (' + lang.upper() + ')')}",
            f"description: {get_label_field('Short Description (' + lang.upper() + ')')}",
            f"date: {date}",
        ]
        thumb = get_label_field("Image path (optional)")
        if thumb:
            fm.append(f"thumbnail: {thumb}")
        fm.append("featured: false")
        fm.append("---\n")
        content = get_label_field('Full Content (' + lang.upper() + ')')
    else:
        fm = [
            "---",
            "type: phd-thesis-defense",
            f"title: {get_label_field('Event Title (' + lang.upper() + ')')}",
            f"name: {get_label_field('Speaker/Presenter Name')}",
            f"datetime: {raw_dt}",
            f"duration: {get_label_field('Duration')}",
            f"location: {get_label_field('Location (' + lang.upper() + ')')}",
            "---\n"
        ]
        content = get_label_field('Description (' + lang.upper() + ')')

    path = f"{folder}/index.{lang.lower()}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(fm))
        f.write(content)
    print(f"✅ Created: {path}")

for l in ['en', 'tr']:
    write_md(l)
