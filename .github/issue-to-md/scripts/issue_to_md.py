import os
import re
import sys
import mimetypes
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

import requests
from github import Github
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from datetime import datetime
import zoneinfo

# ────────────────────────────────────────────────────────────────────────────────
# Configuration & Globals
# ────────────────────────────────────────────────────────────────────────────────

IST_TZ = zoneinfo.ZoneInfo("Europe/Istanbul")

DEBUG = os.getenv("DEBUG", "1") != "0"

def dprint(*args, **kwargs):
    if DEBUG:
        print("[DEBUG]", *args, **kwargs)

def project_root() -> Path:
    """
    Determine repository root:
    - If PROJECT_ROOT is set (workflow passes it), use it.
    - Else use parent-of-parent of this script (since working dir is .github/issue-to-md/).
    """
    env_root = os.getenv("PROJECT_ROOT")
    return Path(env_root).resolve() if env_root else Path(__file__).resolve().parents[2]

# Required env vars from workflow
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
GITHUB_TOKEN      = os.getenv("GITHUB_TOKEN")
ISSUE_NUMBER_STR  = os.getenv("ISSUE_NUMBER", "0")

if not GITHUB_REPOSITORY or not GITHUB_TOKEN or ISSUE_NUMBER_STR == "0":
    missing = [n for n in ["GITHUB_REPOSITORY", "GITHUB_TOKEN", "ISSUE_NUMBER"] if not os.getenv(n)]
    raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")

ISSUE_NUMBER = int(ISSUE_NUMBER_STR)

ROOT        = project_root()
ASSETS_DIR  = ROOT / "assets"
UPLOADS_DIR = ASSETS_DIR / "uploads"
CONTENT_DIR = ROOT / "content"
TEMPLATES_DIR = Path(".") / "templates"  # relative to working dir (.github/issue-to-md/)

# Content kinds that are considered "events"
EVENT_KINDS = {
    "phd-thesis-defense",
    "ms-thesis-defense",
    "seminar", "special-event",
}

# ────────────────────────────────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text).strip("-")
    return text

def read_template(env: Environment, path: str) -> Optional[Any]:
    try:
        return env.get_template(path)
    except TemplateNotFound:
        return None

def ensure_dirs(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
    dprint("Wrote file:", path)

# ────────────────────────────────────────────────────────────────────────────────
# Parsing
# ────────────────────────────────────────────────────────────────────────────────

def normalize_key_from_label(label: str) -> str:
    """
    Normalize GitHub issue-form labels to stable keys.
    We match on label text, not placeholder values.
    """
    key = re.sub(r"[^a-z0-9]+", "_", (label or "").lower()).strip("_")
    return key

def parse_fields(body: str) -> Dict[str, str]:
    """
    Parse issue body like:
        ### Label
        value...
    into {normalized_key: value}.
    """
    parts = re.split(r"^###\s+", body or "", flags=re.MULTILINE)[1:]
    parsed: Dict[str, str] = {}
    for part in parts:
        lines = part.splitlines()
        if not lines:
            continue
        label = lines[0].strip()
        value = "\n".join(lines[1:]).strip()
        key = normalize_key_from_label(label)
        parsed[key] = value
        dprint(f"Parsed field '{label}' → '{key}': {value!r}")
    return parsed

def get_field(fields: Dict[str, str], keys: Iterable[str] | str, default: Optional[str] = "") -> str:
    if isinstance(keys, str):
        keys = [keys]
    for k in keys:
        v = fields.get(k)
        if v:
            dprint(f"get_field '{k}': {v!r}")
            return v
    dprint(f"get_field default for {list(keys)}: {default!r}")
    return default or ""

# ────────────────────────────────────────────────────────────────────────────────
# Date/Time normalization
# ────────────────────────────────────────────────────────────────────────────────

def normalize_date(date_str: Optional[str], issue_created_at_utc: datetime) -> str:
    """
    Accepts YYYY-MM-DD from the issue form; otherwise fallback to issue.created_at in Istanbul.
    """
    if date_str and re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str.strip()):
        return date_str.strip()
    # fallback — convert created_at (UTC) to Istanbul date
    ist_dt = issue_created_at_utc.astimezone(IST_TZ)
    return ist_dt.date().isoformat()

def normalize_time(time_str: Optional[str]) -> str:
    """
    Accepts HH:MM or HH:MM:SS; defaults to 00:00:00 if empty/invalid.
    """
    if not time_str:
        return "00:00:00"
    s = time_str.strip()
    if re.fullmatch(r"\d{2}:\d{2}", s):
        return f"{s}:00"
    if re.fullmatch(r"\d{2}:\d{2}:\d{2}", s):
        return s
    return "00:00:00"

# ────────────────────────────────────────────────────────────────────────────────
# GitHub I/O
# ────────────────────────────────────────────────────────────────────────────────

@dataclass
class IssueData:
    number: int
    title: str
    body: str
    created_at: datetime  

def load_issue() -> IssueData:
    gh = Github(GITHUB_TOKEN)
    repo = gh.get_repo(GITHUB_REPOSITORY)
    issue = repo.get_issue(number=ISSUE_NUMBER)
    dprint(f"Loaded Issue #{ISSUE_NUMBER}: {issue.title!r}")
    return IssueData(
        number=issue.number,
        title=issue.title,
        body=issue.body or "",
        created_at=issue.created_at, 
    )

# ────────────────────────────────────────────────────────────────────────────────
# Media handling
# ────────────────────────────────────────────────────────────────────────────────

IMG_MD_RE = re.compile(r"!\[[^\]]*\]\((https?://[^\)]+)\)")
IMG_SRC_RE = re.compile(r'src="(https?://[^"]+)"')

def download_image_if_present(markdown_or_html: str) -> str:
    """
    Looks for an image URL in markdown or HTML; downloads to assets/uploads/.
    Returns relative path like 'uploads/<filename>' or "" if none.
    """
    if not markdown_or_html:
        return ""
    m = IMG_MD_RE.search(markdown_or_html) or IMG_SRC_RE.search(markdown_or_html)
    if not m:
        return ""
    url = m.group(1)
    dprint("Downloading image:", url)
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    ctype = (resp.headers.get("Content-Type") or "").split(";")[0]
    ext = mimetypes.guess_extension(ctype) or Path(url).suffix or ".png"
    fname = f"{ISSUE_NUMBER}_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
    ensure_dirs(UPLOADS_DIR)
    path = UPLOADS_DIR / fname
    path.write_bytes(resp.content)
    rel = f"uploads/{fname}"
    dprint("Saved image to", path, "→", rel)
    return rel

# ────────────────────────────────────────────────────────────────────────────────
# Renderers
# ────────────────────────────────────────────────────────────────────────────────

@dataclass
class RenderContext:
    is_event: bool
    content_kind: str
    fields: Dict[str, str]
    date_val: str
    time_val: str
    title_en: str
    title_tr: str
    presenter: str
    location_en: str
    location_tr: str
    duration: str
    image_md: str
    out_dir: Path

class BaseRenderer:
    def __init__(self, ctx: RenderContext):
        self.ctx = ctx

    def write(self, path: Path, text: str) -> None:
        write_text(path, text)

class NewsRenderer(BaseRenderer):
    def render(self) -> None:
        # Build front-matter per language
        for lang in ("en", "tr"):
            title = self.ctx.title_en if lang == "en" else self.ctx.title_tr
            desc_key = f"short_description_{lang}"
            body_key = f"full_content_{lang}"
            desc = get_field(self.ctx.fields, desc_key, "")
            body = get_field(self.ctx.fields, body_key, "")

            fm: list[str] = [
                "---",
                "type: news",
                f"title: {title}",
                f"date: {self.ctx.date_val}",
                f"thumbnail: {self.ctx.image_md}",
            ]
            if "\n" in desc:
                fm.append("description: |")
                fm.extend([f"  {line}" for line in desc.splitlines()])
            else:
                fm.append(f"description: {desc}")
            fm.extend(["featured: false", "---", ""])

            out_md = "\n".join(fm + [body])
            self.write(self.ctx.out_dir / f"index.{lang}.md", out_md)

class EventRenderer(BaseRenderer):
    def render(self) -> None:
        # Try template: templates/events/<content_kind>.md.j2
        env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=False)
        tmpl = read_template(env, f"events/{self.ctx.content_kind}.md.j2")

        for lang in ("en", "tr"):
            title = self.ctx.title_en if lang == "en" else self.ctx.title_tr
            location = self.ctx.location_en if lang == "en" else self.ctx.location_tr

            context = {
                "type": self.ctx.content_kind,
                "title": title,
                "datetime": f"{self.ctx.date_val}T{self.ctx.time_val}",
                "name": self.ctx.presenter,
                "duration": self.ctx.duration,
                "location": location,
                # Add more fields as needed…
            }
            dprint(f"Event context [{lang}]:", context)

            if tmpl:
                rendered = tmpl.render(**context)
                # Keep it compact: strip blank lines; avoid duplicate front-matter keys
                out_md = "\n".join(
                    line for line in rendered.splitlines()
                    if line.strip()
                )
            else:
                # Minimal fallback front-matter if no template
                fm = [
                    "---",
                    f"type: {self.ctx.content_kind}",
                    f"title: {title}",
                    f"datetime: {context['datetime']}",
                    f"name: {self.ctx.presenter}",
                    f"location: {location}",
                    f"duration: {self.ctx.duration}",
                    f"thumbnail: {self.ctx.image_md}",
                    "---",
                    "",
                ]
                out_md = "\n".join(fm)

            self.write(self.ctx.out_dir / f"index.{lang}.md", out_md)

# ────────────────────────────────────────────────────────────────────────────────
# Directory naming rules
# ────────────────────────────────────────────────────────────────────────────────

def build_event_dir(base: Path, date_val: str, time_val: str, presenter: str, fallback_title: str, issue_number: int) -> Path:
    hhmmss = time_val.replace(":", "-")
    who = slugify(presenter) or slugify(fallback_title) or f"issue-{issue_number}"
    return base / "events" / f"{date_val}t{hhmmss}-{who}"

def build_news_dir(base: Path, date_val: str, title_en: str) -> Path:
    return base / "news" / f"{date_val}-news-{slugify(title_en)}"

# ────────────────────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────────────────────

def main() -> int:
    issue = load_issue()
    fields = parse_fields(issue.body)

    # Kind → event or news
    content_kind = get_field(fields, ["content_kind", "event_type"], "news").strip().lower()
    is_event = (content_kind in EVENT_KINDS)

    # Titles (fallback to issue title if EN missing)
    title_en = get_field(fields, ["event_title_en", "news_title_en", "title_en"], issue.title)
    title_tr = get_field(fields, ["event_title_tr", "news_title_tr", "title_tr"], "")

    # Prefer issue body for events; legacy key also accepted
    raw_date = get_field(fields, ["date", "date_yyyy_mm_dd"], None if is_event else "")
    raw_time = get_field(fields, "time", None if is_event else "")

    date_val = normalize_date(raw_date, issue.created_at)
    time_val = normalize_time(raw_time)

    # Event-only fields
    presenter = get_field(fields, "name", "")
    duration  = get_field(fields, "duration", "")
    location_en = get_field(fields, "location_en", "")
    location_tr = get_field(fields, "location_tr", location_en)

    # Image extraction 
    image_md = download_image_if_present(get_field(fields, ["image_markdown", "image_drag_drop_here"], ""))

    # Out directory by type
    if is_event:
        out_dir = build_event_dir(CONTENT_DIR, date_val, time_val, presenter, title_en, issue.number)
    else:
        out_dir = build_news_dir(CONTENT_DIR, date_val, title_en)
    ensure_dirs(out_dir)
    dprint("out_dir =", out_dir)

    ctx = RenderContext(
        is_event=is_event,
        content_kind=content_kind if is_event else "news",
        fields=fields,
        date_val=date_val,
        time_val=time_val,
        title_en=title_en,
        title_tr=title_tr,
        presenter=presenter,
        location_en=location_en,
        location_tr=location_tr,
        duration=duration,
        image_md=image_md,
        out_dir=out_dir,
    )

    renderer = EventRenderer(ctx) if is_event else NewsRenderer(ctx)
    renderer.render()

    print("Processing complete.")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        if DEBUG:
            raise
        sys.exit(1)
