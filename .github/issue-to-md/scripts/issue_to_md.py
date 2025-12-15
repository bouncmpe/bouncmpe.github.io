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
    "seminar",
    "special-event",
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
    issue_obj: Any  # Keep reference to GitHub issue object for commenting

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
        issue_obj=issue,
    )

def post_issue_comment(issue_obj: Any, message: str) -> None:
    """Post a comment to the GitHub issue."""
    try:
        issue_obj.create_comment(message)
        dprint(f"Posted comment to issue #{issue_obj.number}")
    except Exception as e:
        dprint(f"Failed to post comment: {e}")

# ────────────────────────────────────────────────────────────────────────────────
# Media handling
# ────────────────────────────────────────────────────────────────────────────────

IMG_MD_RE = re.compile(r"!\[[^\]]*\]\((https?://[^\)]+)\)")
IMG_SRC_RE = re.compile(r'src="(https?://[^"]+)"')

# Allowed image formats
ALLOWED_IMAGE_FORMATS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}

# Content-Type to extension mapping for common image types
CONTENT_TYPE_TO_EXT = {
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/svg+xml": ".svg",
}

def validate_image_format(url: str) -> tuple[bool, str]:
    """
    Validate if the image URL has an allowed format.
    Returns (is_valid, error_message).
    """
    # Extract file extension from URL
    path = Path(url.split("?")[0])  # Remove query params
    ext = path.suffix.lower()
    
    # If no extension in URL, we'll validate during download via Content-Type
    # So return True here and let download_image_if_present handle it
    if not ext:
        return True, ""
    
    if ext not in ALLOWED_IMAGE_FORMATS:
        return False, f"Invalid image format '{ext}'. Allowed formats: {', '.join(sorted(ALLOWED_IMAGE_FORMATS))}"
    return True, ""

def find_all_images(text: str) -> list[str]:
    """
    Find all image URLs in markdown or HTML text.
    Returns list of URLs.
    """
    if not text:
        return []
    urls = []
    # Find markdown images
    for match in IMG_MD_RE.finditer(text):
        urls.append(match.group(1))
    # Find HTML images
    for match in IMG_SRC_RE.finditer(text):
        urls.append(match.group(1))
    return urls

def find_uploaded_files(text: str) -> list[str]:
    """
    Find all GitHub file upload URLs in text (images or other files).
    Returns list of URLs.
    """
    if not text:
        return []
    # GitHub upload URLs pattern
    file_url_pattern = re.compile(r'https?://(?:github\.com/[^/]+/[^/]+/files/\d+/[^)\s]+|github\.com/user-attachments/[^)\s]+)')
    return file_url_pattern.findall(text)

def _validate_file_uploads(markdown_text: str) -> list[str]:
    """Validate file uploads in text and return errors."""
    errors = []
    file_matches = find_uploaded_files(markdown_text)
    
    for file_url in file_matches:
        dprint(f"Found file upload URL: {file_url}")
        path = Path(file_url.split("?")[0])
        ext = path.suffix.lower()
        if ext and ext not in ALLOWED_IMAGE_FORMATS:
            errors.append(
                f"Invalid file type '{ext}' uploaded to image field. "
                f"Only image files are allowed: {', '.join(sorted(ALLOWED_IMAGE_FORMATS))}"
            )
            dprint(f"Rejected non-image file: {ext}")
    return errors

def _extract_image_url(markdown_or_html: str) -> Optional[str]:
    """Extract image URL from markdown or HTML."""
    m = IMG_MD_RE.search(markdown_or_html) or IMG_SRC_RE.search(markdown_or_html)
    return m.group(1) if m else None

def _download_and_save_image(url: str, issue_number: int) -> tuple[str, list[str]]:
    """Download image and save to uploads directory."""
    errors = []
    try:
        dprint("Downloading image:", url)
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        ctype = (resp.headers.get("Content-Type") or "").split(";")[0].strip()
        dprint(f"Content-Type: {ctype}")
        
        ext = CONTENT_TYPE_TO_EXT.get(ctype) or mimetypes.guess_extension(ctype) or Path(url).suffix or ".png"
        dprint(f"Determined extension: {ext}")
        
        if ext.lower() not in ALLOWED_IMAGE_FORMATS:
            error_msg = (
                f"Invalid image type. Server returned content type '{ctype}' "
                f"(extension: '{ext}'). Allowed formats: {', '.join(sorted(ALLOWED_IMAGE_FORMATS))}"
            )
            errors.append(error_msg)
            dprint(error_msg)
            return "", errors
        
        fname = f"{issue_number}_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
        ensure_dirs(UPLOADS_DIR)
        path = UPLOADS_DIR / fname
        path.write_bytes(resp.content)
        rel = f"uploads/{fname}"
        dprint("Saved image to", path, "→", rel)
        return rel, []
    except Exception as e:
        error_msg = f"Failed to download image from {url}: {str(e)}"
        errors.append(error_msg)
        dprint(error_msg)
        return "", errors

def download_image_if_present(markdown_or_html: str, validate_only: bool = False) -> tuple[str, list[str]]:
    """
    Looks for an image URL in markdown or HTML; downloads to assets/uploads/.
    
    Args:
        markdown_or_html: Text containing image references
        validate_only: If True, only validate without downloading
    
    Returns:
        Tuple of (relative_path, list_of_errors)
    """
    if not markdown_or_html:
        return "", []
    
    # Validate any file uploads first
    errors = _validate_file_uploads(markdown_or_html)
    if errors:
        return "", errors
    
    # Extract image URL
    url = _extract_image_url(markdown_or_html)
    if not url:
        file_matches = find_uploaded_files(markdown_or_html)
        if file_matches:
            errors.append(
                "File uploaded but not in proper image markdown format. "
                "Please use image files (JPG, PNG, GIF, WebP, SVG) and ensure they display as images in the preview."
            )
        return "", errors
    
    # Validate format
    is_valid, error_msg = validate_image_format(url)
    if not is_valid:
        errors.append(error_msg)
        dprint(f"Image validation failed: {error_msg}")
        return "", errors
    
    if validate_only:
        return "", []
    
    # Download the image
    return _download_and_save_image(url, ISSUE_NUMBER)

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

def _extract_basic_fields(fields: Dict[str, str], issue_title: str, issue_created_at: datetime) -> Dict[str, Any]:
    """Extract and normalize basic fields from issue."""
    content_kind = get_field(fields, ["content_kind", "event_type"], "news").strip().lower()
    is_event = content_kind in EVENT_KINDS
    
    title_en = get_field(fields, ["event_title_en", "news_title_en", "title_en"], issue_title)
    title_tr = get_field(fields, ["event_title_tr", "news_title_tr", "title_tr"], "")
    
    raw_date = get_field(fields, ["date", "date_yyyy_mm_dd"], None if is_event else "")
    raw_time = get_field(fields, "time", None if is_event else "")
    
    return {
        "content_kind": content_kind,
        "is_event": is_event,
        "title_en": title_en,
        "title_tr": title_tr,
        "date_val": normalize_date(raw_date, issue_created_at),
        "time_val": normalize_time(raw_time),
        "presenter": get_field(fields, "speaker_presenter_name", ""),
        "duration": get_field(fields, "duration", ""),
        "location_en": get_field(fields, "location_en", ""),
        "location_tr": get_field(fields, "location_tr", get_field(fields, "location_en", "")),
    }

def _validate_dedicated_image_field(fields: Dict[str, str]) -> tuple[str, list[str]]:
    """Validate dedicated image field and download if present."""
    image_field = get_field(fields, ["image_markdown", "image_drag_drop_here"], "")
    if image_field:
        dprint("Validating dedicated image field...")
        return download_image_if_present(image_field, validate_only=False)
    return "", []

def _validate_content_fields(fields: Dict[str, str], is_event: bool) -> list[str]:
    """Validate content fields for invalid file uploads."""
    if is_event:
        return []
    
    validation_errors = []
    content_fields = [
        ("short_description_en", get_field(fields, "short_description_en", "")),
        ("short_description_tr", get_field(fields, "short_description_tr", "")),
        ("full_content_en", get_field(fields, "full_content_en", "")),
        ("full_content_tr", get_field(fields, "full_content_tr", "")),
    ]
    
    for field_name, field_value in content_fields:
        if not field_value:
            dprint(f"Field '{field_name}' is empty")
            continue
            
        dprint(f"Checking field '{field_name}', content length: {len(field_value)}")
        all_files = find_uploaded_files(field_value)
        dprint(f"Found {len(all_files)} file(s) in {field_name}: {all_files}")
        
        for file_url in all_files:
            is_valid, error_msg = validate_image_format(file_url)
            dprint(f"File: {file_url}, Valid: {is_valid}, Error: {error_msg}")
            if not is_valid:
                validation_errors.append(f"**{field_name}**: {error_msg} (URL: {file_url})")
                dprint(f"Added validation error for {field_name}")
    
    return validation_errors

def _post_validation_error(issue_obj: Any, validation_errors: list[str]) -> None:
    """Post validation error comment to issue."""
    error_message = "## ⚠️ File Validation Failed\n\n"
    error_message += "The following issues were found with files in your submission:\n\n"
    for i, error in enumerate(validation_errors, 1):
        error_message += f"{i}. {error}\n"
    error_message += "\n### Required Actions:\n"
    error_message += "- **All fields**: Only image files are allowed (JPG, JPEG, PNG, GIF, WebP, SVG)\n"
    error_message += "- **Text files and documents**: Remove .txt, .pdf, .doc, and other non-image files\n"
    error_message += "- **Images in content**: You CAN include images in description/content fields, just make sure they're valid image formats\n"
    error_message += "\n### Allowed Image Formats:\n"
    error_message += "✅ " + ", ".join(sorted(ALLOWED_IMAGE_FORMATS)) + "\n"
    error_message += "\nPlease update your issue to fix these issues. The automation will run again when you edit the issue."
    
    post_issue_comment(issue_obj, error_message)
    print("❌ Validation failed. Comment posted to issue.", file=sys.stderr)
    print(f"Found {len(validation_errors)} validation error(s):", file=sys.stderr)
    for error in validation_errors:
        print(f"  - {error}", file=sys.stderr)

# Main
def main() -> int:
    issue = load_issue()
    fields = parse_fields(issue.body)
    
    # Extract basic fields
    basic = _extract_basic_fields(fields, issue.title, issue.created_at)
    
    # Validate dedicated image field
    image_md, img_errors = _validate_dedicated_image_field(fields)
    validation_errors = img_errors.copy()
    
    # Validate content fields
    content_errors = _validate_content_fields(fields, basic["is_event"])
    validation_errors.extend(content_errors)
    
    # Handle validation errors
    if validation_errors:
        _post_validation_error(issue.issue_obj, validation_errors)
        return 1

    # Determine output directory
    if basic["is_event"]:
        out_dir = build_event_dir(
            CONTENT_DIR, basic["date_val"], basic["time_val"],
            basic["presenter"], basic["title_en"], issue.number
        )
    else:
        out_dir = build_news_dir(CONTENT_DIR, basic["date_val"], basic["title_en"])
    ensure_dirs(out_dir)
    dprint("out_dir =", out_dir)

    # Create render context
    ctx = RenderContext(
        is_event=basic["is_event"],
        content_kind=basic["content_kind"] if basic["is_event"] else "news",
        fields=fields,
        date_val=basic["date_val"],
        time_val=basic["time_val"],
        title_en=basic["title_en"],
        title_tr=basic["title_tr"],
        presenter=basic["presenter"],
        location_en=basic["location_en"],
        location_tr=basic["location_tr"],
        duration=basic["duration"],
        image_md=image_md,
        out_dir=out_dir,
    )

    # Render output
    renderer = EventRenderer(ctx) if basic["is_event"] else NewsRenderer(ctx)
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
