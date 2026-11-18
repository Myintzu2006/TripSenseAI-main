"""Download one freely licensed Wikimedia photo for every destination.

The script resolves a relevant English Wikipedia article, obtains its free page
image and attribution from Wikimedia Commons, downloads a 1600px thumbnail, and
writes ``assets/destinations/manifest.json``. Re-running it audits existing
downloads and fills gaps; pass ``--refresh`` to replace valid existing files.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import mimetypes
from pathlib import Path
import re
import sys
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "destinations.csv"
IMAGE_DIR = ROOT / "assets" / "destinations"
MANIFEST_PATH = IMAGE_DIR / "manifest.json"
WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "AsiaCompassTravelRecommender/1.2 (educational project)"
MIN_REQUEST_INTERVAL = 0.8
_last_request_at = 0.0
SUPPORTED_MIME_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}
NON_PHOTO_WORDS = (
    "diagram",
    "flag",
    "figures",
    "landsat",
    "locator",
    "logo",
    "map",
    "relief",
    "route",
    "satellite",
    "seal",
    "sentinel",
    "topographic",
)
TITLE_OVERRIDES = {
    "Everest Region": "Mount Everest",
    "Hong Kong - Central": "Central, Hong Kong",
    "Kenting": "Kenting National Park",
    "Koh Samui": "Ko Samui",
    "Kowloon / Tsim Sha Tsui": "Tsim Sha Tsui",
    "Lantau / Big Buddha": "Tian Tan Buddha",
    "Macau Historic Centre": "Historic Centre of Macau",
    "Sai Kung / Geopark": "Hong Kong UNESCO Global Geopark",
    "Singapore City": "Singapore",
    "Stanley / Cheung Chau": "Cheung Chau",
}
COMMONS_SEARCH_OVERRIDES = {
    "Ari Atoll": "Ari Atoll Maldives lagoon island",
    "Hue": "Hue Vietnam Perfume River landscape",
    "Maafushi": "Maafushi Maldives beach island",
    "Okinawa": "Okinawa Japan beach landscape",
    "Sai Kung / Geopark": "Hong Kong UNESCO Global Geopark coast",
    "Svaneti": "Svaneti Georgia mountains landscape",
    "Sun Moon Lake": "Sun Moon Lake landscape",
    "Tashkent": "Tashkent Uzbekistan park landscape",
    "Ulu Temburong National Park": "Ulu Temburong Brunei rainforest",
}
COMMONS_FILE_OVERRIDES = {
    "Ari Atoll": "Sun island - Maldives - panoramio.jpg",
    "Hue": "Hue Vietnam Perfume-River-01.jpg",
    "Maafushi": (
        "Beach Scene - Maafushi Island - South Male Atoll - Maldives - 01 "
        "(14272892886).jpg"
    ),
    "Sai Kung / Geopark": "Wang Chau Kok Arch - Sai Kung (Hong Kong).jpg",
    "Svaneti": "Caucasus Mountains, Svaneti, Georgia.jpg",
    "Sun Moon Lake": "Sun-Moon-Lake Taiwan Lake-seen-from-Wen-Wu-Temple-01.jpg",
    "Tashkent": "Sunlight Passing Through Trees in Tashkent Botanical Garden.jpg",
    "Ulu Temburong National Park": "Over borneo.jpg",
}


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.casefold()).strip("-")


def open_with_retries(request: Request, timeout: int, attempts: int = 5):
    global _last_request_at
    for attempt in range(attempts):
        delay = MIN_REQUEST_INTERVAL - (time.monotonic() - _last_request_at)
        if delay > 0:
            time.sleep(delay)
        try:
            _last_request_at = time.monotonic()
            return urlopen(request, timeout=timeout)
        except OSError as exc:
            if attempt == attempts - 1:
                raise RuntimeError(f"Wikimedia request failed: {exc}") from exc
            time.sleep(2 * (attempt + 1))
    raise AssertionError("unreachable")


def api_json(endpoint: str, params: dict) -> dict:
    request = Request(
        f"{endpoint}?{urlencode(params)}",
        headers={"User-Agent": USER_AGENT},
    )
    try:
        with open_with_retries(request, timeout=30) as response:
            return json.load(response)
    except ValueError as exc:
        raise RuntimeError(f"Invalid Wikimedia API response: {exc}") from exc


def article_candidate(name: str) -> str:
    if name in TITLE_OVERRIDES:
        return TITLE_OVERRIDES[name]
    return re.sub(r"\s*\([^)]*\)\s*$", "", name).strip()


def page_with_image(title: str) -> dict | None:
    payload = api_json(
        WIKIPEDIA_API,
        {
            "action": "query",
            "format": "json",
            "formatversion": 2,
            "redirects": 1,
            "prop": "pageimages|info",
            "piprop": "name",
            "pilicense": "free",
            "inprop": "url",
            "titles": title,
        },
    )
    for page in payload.get("query", {}).get("pages", []):
        if not page.get("missing") and page.get("pageimage"):
            return page
    return None


def search_page(name: str, country: str) -> dict | None:
    payload = api_json(
        WIKIPEDIA_API,
        {
            "action": "query",
            "format": "json",
            "formatversion": 2,
            "generator": "search",
            "gsrsearch": f'intitle:"{name}" {country}',
            "gsrnamespace": 0,
            "gsrlimit": 8,
            "prop": "pageimages|info",
            "piprop": "name",
            "pilicense": "free",
            "inprop": "url",
        },
    )
    pages = sorted(
        payload.get("query", {}).get("pages", []),
        key=lambda page: page.get("index", 999),
    )
    return next((page for page in pages if page.get("pageimage")), None)


def commons_image(file_name: str) -> dict | None:
    title = file_name if file_name.startswith("File:") else f"File:{file_name}"
    payload = api_json(
        COMMONS_API,
        {
            "action": "query",
            "format": "json",
            "formatversion": 2,
            "prop": "imageinfo",
            "iiprop": "url|mime|extmetadata",
            "iiurlwidth": 1280,
            "titles": title,
        },
    )
    for page in payload.get("query", {}).get("pages", []):
        info = (page.get("imageinfo") or [None])[0]
        if info and info.get("mime") in SUPPORTED_MIME_TYPES:
            info["description_url"] = info.get("descriptionurl")
            return info
    return None


def image_is_suitable(title: str, info: dict) -> bool:
    metadata = info.get("extmetadata", {})
    searchable = " ".join(
        [title]
        + [str((metadata.get(key) or {}).get("value", "")) for key in (
            "ImageDescription",
            "ObjectName",
            "Artist",
        )]
    ).casefold()
    return not any(word in searchable for word in NON_PHOTO_WORDS)


def search_commons_image(name: str, country: str) -> tuple[str, dict] | None:
    search_term = COMMONS_SEARCH_OVERRIDES.get(name, name)
    search_expression = search_term if name in COMMONS_SEARCH_OVERRIDES else f'"{name}"'
    payload = api_json(
        COMMONS_API,
        {
            "action": "query",
            "format": "json",
            "formatversion": 2,
            "generator": "search",
            "gsrsearch": (
                f'{search_expression} {country} -map -satellite -locator filetype:bitmap'
            ),
            "gsrnamespace": 6,
            "gsrlimit": 20,
            "prop": "imageinfo",
            "iiprop": "url|mime|extmetadata",
            "iiurlwidth": 1280,
        },
    )
    pages = sorted(
        payload.get("query", {}).get("pages", []),
        key=lambda page: page.get("index", 999),
    )
    for page in pages:
        title = str(page.get("title", ""))
        info = (page.get("imageinfo") or [None])[0]
        if (
            info
            and info.get("mime") in SUPPORTED_MIME_TYPES
            and image_is_suitable(title, info)
        ):
            info["description_url"] = info.get("descriptionurl")
            return title.removeprefix("File:"), info
    return None


def clean_metadata(value: dict | None) -> str:
    text = str((value or {}).get("value", ""))
    return html.unescape(re.sub(r"<[^>]+>", "", text)).strip()


def download(url: str, path: Path) -> None:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with open_with_retries(request, timeout=60) as response:
        body = response.read()
    if len(body) < 5_000:
        raise RuntimeError(f"Downloaded file is unexpectedly small ({len(body)} bytes)")
    path.write_bytes(body)


def load_catalog() -> list[dict[str, str]]:
    with CATALOG_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        return {}
    try:
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_manifest(manifest: dict) -> None:
    ordered = {key: manifest[key] for key in sorted(manifest, key=str.casefold)}
    MANIFEST_PATH.write_text(
        json.dumps(ordered, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def existing_is_valid(entry: dict) -> bool:
    relative_path = entry.get("local_path")
    if not relative_path:
        return False
    path = ROOT / relative_path
    return path.is_file() and path.stat().st_size >= 5_000


def process_destination(row: dict[str, str], manifest: dict, refresh: bool) -> str:
    name, country = row["name"], row["country"]
    previous = manifest.get(name, {})
    if previous.get("manual") and existing_is_valid(previous):
        return "manual"
    if not refresh and existing_is_valid(previous):
        return "alive"

    page = page_with_image(article_candidate(name)) or search_page(name, country)
    if name in COMMONS_FILE_OVERRIDES:
        file_name = COMMONS_FILE_OVERRIDES[name]
    elif name in COMMONS_SEARCH_OVERRIDES:
        file_name = ""
    else:
        file_name = page["pageimage"] if page else ""
    info = commons_image(file_name) if file_name else None
    if info and not image_is_suitable(file_name, info):
        info = None
    if not info:
        direct_match = search_commons_image(name, country)
        if not direct_match:
            return "missing_commons_photo"
        file_name, info = direct_match

    metadata = info.get("extmetadata", {})
    image_url = info.get("thumburl") or info.get("url")
    extension = SUPPORTED_MIME_TYPES[info["mime"]]
    local_path = IMAGE_DIR / f"{slug(name)}{extension}"
    download(image_url, local_path)

    manifest[name] = {
        "country": country,
        "local_path": local_path.relative_to(ROOT).as_posix(),
        "article_title": page.get("title", "") if page else "",
        "article_url": page.get("fullurl", "") if page else "",
        "file_name": file_name,
        "file_page_url": info.get("description_url", ""),
        "image_url": image_url,
        "creator": clean_metadata(metadata.get("Artist")),
        "credit": clean_metadata(metadata.get("Credit")),
        "license": clean_metadata(metadata.get("LicenseShortName")),
        "license_url": clean_metadata(metadata.get("LicenseUrl")),
        "downloaded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    save_manifest(manifest)
    return "downloaded"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true", help="replace valid downloads")
    parser.add_argument("--limit", type=int, help="process only the first N destinations")
    parser.add_argument(
        "--destination",
        action="append",
        help="process only this exact destination name (repeatable)",
    )
    args = parser.parse_args()

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    rows = load_catalog()
    if args.destination:
        selected = set(args.destination)
        rows = [row for row in rows if row["name"] in selected]
        unknown = selected - {row["name"] for row in rows}
        if unknown:
            parser.error("unknown destination(s): " + ", ".join(sorted(unknown)))
    if args.limit is not None:
        rows = rows[: args.limit]

    counts: dict[str, int] = {}
    failures: list[tuple[str, str]] = []
    for index, row in enumerate(rows, 1):
        try:
            status = process_destination(row, manifest, args.refresh)
        except (OSError, RuntimeError) as exc:
            status = "error"
            failures.append((row["name"], str(exc)))
        counts[status] = counts.get(status, 0) + 1
        print(f"[{index:03}/{len(rows):03}] {row['name']}: {status}", flush=True)

    alive = sum(1 for row in rows if existing_is_valid(manifest.get(row["name"], {})))
    print(f"\nAlive local photos: {alive}/{len(rows)}")
    print("Statuses: " + ", ".join(f"{key}={value}" for key, value in sorted(counts.items())))
    if failures:
        print("Failures:")
        for name, error in failures:
            print(f"- {name}: {error}")
    return 0 if alive == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
