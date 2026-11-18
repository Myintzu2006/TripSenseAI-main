from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import re
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

import streamlit as st


WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_TITLE_OVERRIDES = {
    "Kenting": "Kenting National Park",
    "Koh Samui": "Ko Samui",
    "Lantau / Big Buddha": "Tian Tan Buddha",
    "Everest Region": "Mount Everest",
    "North Malé Atoll": "North Malé Atoll",
}

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOCAL_IMAGE_DIR = PROJECT_ROOT / "assets" / "destinations"
IMAGE_MANIFEST = LOCAL_IMAGE_DIR / "manifest.json"
IMAGE_EXTENSIONS = (".webp", ".jpg", ".jpeg", ".png")


def _image_filename(name):
    """Convert a destination name into a filename such as 'bagan'."""
    return re.sub(r"[^a-z0-9]+", "-", name.casefold()).strip("-")


def destination_images(destinations):
    """Use local photos first and Wikipedia for missing photos."""
    requested = tuple(
        dict.fromkeys(
            (str(name).strip(), str(country).strip())
            for name, country in destinations
            if name and country
        )
    )

    images = {}
    missing = []
    try:
        manifest = json.loads(IMAGE_MANIFEST.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        manifest = {}
    local_files = {
        path.name.casefold(): path
        for path in LOCAL_IMAGE_DIR.iterdir()
        if path.is_file() and path.suffix.casefold() in IMAGE_EXTENSIONS
    } if LOCAL_IMAGE_DIR.is_dir() else {}

    for name, country in requested:
        attribution = manifest.get(name, {})
        relative_path = attribution.get("local_path")
        if relative_path:
            manifest_path = PROJECT_ROOT / relative_path
            if manifest_path.is_file():
                license_name = attribution.get("license") or "free license"
                creator = attribution.get("creator", "").strip()
                creator_label = creator if 0 < len(creator) <= 80 else ""
                label_parts = [
                    attribution.get("source_label") or "Wikimedia Commons"
                ]
                if creator_label:
                    label_parts.append(creator_label)
                label_parts.append(license_name)
                images[name] = {
                    "image_url": str(manifest_path),
                    "article_url": attribution.get("file_page_url"),
                    "source_label": " · ".join(label_parts),
                    "matched_title": attribution.get("article_title") or name,
                    "creator": attribution.get("creator", ""),
                }
                continue

        filename = _image_filename(name)
        local_path = None

        for extension in IMAGE_EXTENSIONS:
            candidate = local_files.get(f"{filename}{extension}".casefold())
            if candidate:
                local_path = candidate
                break

        if local_path:
            images[name] = {
                "image_url": str(local_path),
                "article_url": None,
                "source_label": "Local photo",
                "matched_title": name,
            }
        else:
            missing.append((name, country))

    if missing:
        images.update(wikipedia_destination_images(tuple(missing)))

    return images


def _fetch_json(params):
    request = Request(
        f"{WIKIPEDIA_API}?{urlencode(params)}",
        headers={"User-Agent": "AsiaCompassTravelRecommender/1.1"},
    )
    with urlopen(request, timeout=8) as response:
        return json.load(response)


def _photo_from_page(page):
    title = str(page.get("title", ""))
    source = page.get("thumbnail", {}).get("source")
    if not title or not source:
        return None
    return {
        "image_url": source,
        "article_url": "https://en.wikipedia.org/wiki/"
        + quote(title.replace(" ", "_")),
        "source_label": "Wikipedia",
        "matched_title": title,
    }


def _search_destination_photo(name, country):
    params = {
        "action": "query",
        "format": "json",
        "formatversion": 2,
        "generator": "search",
        "gsrsearch": f'intitle:"{name}" {country}',
        "gsrnamespace": 0,
        "gsrlimit": 5,
        "prop": "pageimages",
        "piprop": "thumbnail",
        "pithumbsize": 1200,
        "pilicense": "free",
    }
    try:
        payload = _fetch_json(params)
    except (OSError, ValueError, TimeoutError):
        return None
    pages = payload.get("query", {}).get("pages", [])
    pages = sorted(pages, key=lambda page: page.get("index", 999))
    for page in pages:
        photo = _photo_from_page(page)
        if photo:
            return photo
    return None


@st.cache_data(ttl="5m", max_entries=50, show_spinner=False)
def wikipedia_destination_images(destinations):
    """Return live, sourced destination photos with title-search fallback."""
    requested = tuple(
        dict.fromkeys(
            (str(name).strip(), str(country).strip())
            for name, country in destinations
            if name and country
        )
    )
    if not requested:
        return {}

    title_to_destination = {}
    titles = []
    for name, _country in requested:
        title = WIKIPEDIA_TITLE_OVERRIDES.get(name, name)
        titles.append(title)
        title_to_destination[title.casefold()] = name

    params = {
        "action": "query",
        "format": "json",
        "formatversion": 2,
        "redirects": 1,
        "prop": "pageimages",
        "piprop": "thumbnail",
        "pithumbsize": 1200,
        "pilicense": "free",
        "titles": "|".join(titles),
    }

    try:
        payload = _fetch_json(params)
    except (OSError, ValueError, TimeoutError):
        return {}

    query = payload.get("query", {})
    aliases = dict(title_to_destination)
    for item in query.get("normalized", []):
        original = aliases.get(str(item.get("from", "")).casefold())
        if original:
            aliases[str(item.get("to", "")).casefold()] = original
    for item in query.get("redirects", []):
        original = aliases.get(str(item.get("from", "")).casefold())
        if original:
            aliases[str(item.get("to", "")).casefold()] = original

    images = {}
    for page in query.get("pages", []):
        title = str(page.get("title", ""))
        original = aliases.get(title.casefold())
        photo = _photo_from_page(page)
        if original and photo:
            images[original] = photo

    missing = [(name, country) for name, country in requested if name not in images]
    if missing:
        with ThreadPoolExecutor(max_workers=min(4, len(missing))) as executor:
            futures = {
                executor.submit(_search_destination_photo, name, country): name
                for name, country in missing
            }
            for future in as_completed(futures):
                photo = future.result()
                if photo:
                    images[futures[future]] = photo

    return images
