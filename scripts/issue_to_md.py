import os, re, unicodedata

# 1) Inputs
type_labels = os.getenv("ISSUE_LABELS", "").lower()
body = os.getenv("ISSUE_BODY", "").strip()

# 2) Determine type
content_type = "news" if "news" in type_labels else "event"

# 3) Slugify helper
def slugify(text):
    t = unicodedata.normalize("NFKD", text)
    t = t.encode("ascii","ignore").decode("ascii")
    t = re.sub(r"[^\w\s-]","", t.lower())
    return re.sub(r"[-\s]+","-", t).strip("-_")

# 4) Parse issue body
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

# 5) Mapping IDs to labels
mapping = {
    # Event
    'title_en': 'Event Title (EN)', 'title_tr': 'Event Title (TR)',
    'name': 'Speaker/Presenter Name', 'datetime': 'Date and Time (ISO format)',
    'duration': 'Duration', 'location_en': 'Location (EN)', 'location_tr': 'Location (TR)',
    'description_en': 'Description (EN)', 'description_tr': 'Description (TR)',
    # News
    'news_title_en': 'News Title (EN)', 'news_title_tr': 'News Title (TR)',
    'date': 'Date (YYYY-MM-DD)', 'thumbnail': 'Image path (optional)',
    'short_en': 'Short Description (EN)', 'short_tr': 'Short Description (TR)',
    'content_en': 'Full Content (EN)', 'content_tr': 'Full Content (TR)',
}

def get_field(fid):
    label = mapping.get(fid)
    return parsed.get(label, "").strip()

# 6) Common extraction
raw_date = get_field('date') if content_type=='news' else get_field('datetime')
_date = raw_date.split('T')[0] if 'T' in raw_date else raw_date
slug = slugify(get_field('news_title_en') if content_type=='news' else get_field('title_en'))
base_folder = f"content/{content_type}s/{_date}-{content_type}-{slug}"
os.makedirs(base_folder, exist_ok=True)

# 7) Frontmatter templates
def make_frontmatter(lang):
    if content_type=='news':
        return [
            '---',
            f"type: news",
            f"title: {get_field('news_title_' + lang)}",
            f"description: {get_field('short_' + lang)}",
            f"date: {_date}",
            f"thumbnail: {get_field('thumbnail')}",
            'featured: false',
            '---\n'
        ]
    else:
        return [
            '---',
            'type: phd-thesis-defense',
            f"title: {get_field('title_' + lang)}",
            f"name: {get_field('name')}",
            f"datetime: {raw_date}",
            f"duration: {get_field('duration')}",
            f"location: {get_field('location_' + lang)}",
            '---\n'
        ]

# 8) Write files for each language
for lang in ['en','tr']:
    fm = make_frontmatter(lang)
    body_text = get_field('content_' + lang)
    out_file = f"{base_folder}/index.{lang}.md"
    with open(out_file,'w',encoding='utf-8') as f:
        f.write("\n".join(fm))
        f.write(body_text)
    print(f" Created: {out_file}")
