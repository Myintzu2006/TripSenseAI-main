"""Build destination ground-spending evidence from attributable public pages.

The primary source is Budget Your Trip. Ground spending is the sum of its published
per-person daily meals, local transportation, and sightseeing/activity averages.
Accommodation and flights are excluded. Destination pages are preferred; a named
traveler base or country page is used only as an explicitly labelled Low-confidence
proxy.
"""

from __future__ import annotations

import csv
import html
import json
from pathlib import Path
import re
import sys
import time
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DESTINATIONS_PATH = ROOT / "data" / "destinations.csv"
BASES_PATH = ROOT / "data" / "destination_bases.csv"
OUTPUT_PATH = ROOT / "data" / "destination_costs.csv"
CACHE_PATH = ROOT / "data" / "cost_collection_cache.json"
SITEMAP_URL = "https://www.budgetyourtrip.com/sitemap_https.php"
USER_AGENT = "AsiaCompassDataResearch/3.0 (educational travel project)"
COLLECTED_AT = "2026-09-02"

FIELDS = [
    "destination",
    "cost_model",
    "currency",
    "reported_daily_total",
    "accommodation_typical",
    "ground_spend_typical",
    "food_typical",
    "local_transport_typical",
    "activities_typical",
    "evidence_scope",
    "evidence_location",
    "source_1_url",
    "source_method",
    "collected_at",
    "confidence",
    "notes",
]

COUNTRY_SLUGS = {
    "Myanmar": ["myanmar"],
    "Thailand": ["thailand"],
    "Vietnam": ["vietnam"],
    "Cambodia": ["cambodia"],
    "Malaysia": ["malaysia"],
    "Singapore": ["singapore"],
    "Indonesia": ["indonesia"],
    "Philippines": ["philippines"],
    "Japan": ["japan"],
    "South Korea": ["south-korea"],
    "Laos": ["laos"],
    "Bangladesh": ["bangladesh"],
    "Bhutan": ["bhutan"],
    "Nepal": ["nepal"],
    "Sri Lanka": ["sri-lanka"],
    "India": ["india"],
    "Maldives": ["maldives"],
    "China": ["china"],
    "Mongolia": ["mongolia"],
    "Taiwan": ["taiwan"],
    "Brunei": ["brunei"],
    "Timor-Leste": ["timor-leste", "east-timor"],
    "Hong Kong": ["hong-kong"],
    "Macau": ["macao", "macau"],
    "Kazakhstan": ["kazakhstan"],
    "Kyrgyzstan": ["kyrgyzstan"],
    "Uzbekistan": ["uzbekistan"],
    "Tajikistan": ["tajikistan"],
    "Turkmenistan": ["turkmenistan"],
    "Georgia": ["georgia"],
}

DESTINATION_ALIASES = {
    "Almaty (Kazakhstan)": ["almaty"],
    "Astana (Kazakhstan)": ["astana"],
    "Cameron Highlands": ["cameron-highlands"],
    "Cebu": ["cebu", "cebu-island"],
    "Coron": ["coron", "coron-island"],
    "Delhi": ["new-delhi", "delhi"],
    "Ha Long Bay": ["ha-long-bay", "halong-bay", "ha-long"],
    "Hpa-An": ["hpa-an", "hpa-an"],
    "Hue": ["hue"],
    "Jeju": ["jeju-island", "jeju"],
    "Karakorum": ["kharkhorin", "karakorum"],
    "Kenting": ["kenting", "hengchun"],
    "Koh Samui": ["koh-samui"],
    "Malacca": ["malacca", "melaka"],
    "Malé": ["male"],
    "Ninh Binh": ["ninh-binh"],
    "Okinawa": ["okinawa", "naha"],
    "Sapa": ["sapa", "sa-pa"],
    "Seminyak": ["seminyak"],
    "Taroko Gorge": ["taroko-gorge"],
}

PROXY_ALIASES = {
    "Cameron Highlands": [("Tanah Rata", "tanah-rata")],
    "Paro Taktsang": [("Paro", "paro")],
    "Seminyak": [("Kuta", "kuta")],
    "Taroko Gorge": [("Hualien", "hualien")],
}

# These source pages are excluded because their current published values are extreme
# internal outliers against the same source's country benchmark. The original URL and
# reason remain in the methodology and collection code rather than being silently used.
EXCLUDED_DESTINATION_URLS = {
    "Goa": {"https://www.budgetyourtrip.com/india/goa"},
    "Kerala": {"https://www.budgetyourtrip.com/india/kerala"},
}

# Used only when Budget Your Trip has no complete country page. Each alternative
# publishes a per-person daily category breakdown. These remain Low confidence
# because they are country-wide modeled or single-traveler estimates.
SUPPLEMENTAL_COUNTRY_EVIDENCE = {
    "Brunei": {
        "url": "https://www.neverendingfootsteps.com/cost-of-travel-brunei-budget/",
        "reported_daily_total": 57.0,
        "accommodation_typical": 30.0,
        "ground_spend_typical": 27.0,
        "food_typical": 20.0,
        "local_transport_typical": 2.0,
        "activities_typical": 5.0,
        "source_method": (
            "Published 2026 mid-range per-person daily food, transport, and activity "
            "breakdown; flights and accommodation excluded"
        ),
        "source_note": "Current firsthand travel-writer budget breakdown.",
    },
    "Timor-Leste": {
        "url": "https://exploreeverycountry.com/countries/timor-leste/budget-travel-guide/",
        "reported_daily_total": 100.0,
        "accommodation_typical": 50.0,
        "ground_spend_typical": 50.0,
        "food_typical": 25.0,
        "local_transport_typical": 13.0,
        "activities_typical": 12.0,
        "source_method": (
            "Published 2026 mid-range per-person daily food, transport, and activity "
            "breakdown; flights and accommodation excluded"
        ),
        "source_note": "Modeled country planning estimate; guidance only.",
    },
    "Tajikistan": {
        "url": "https://travelcostcalculator.org/cost/tajikistan",
        "reported_daily_total": 132.0,
        "accommodation_typical": 57.0,
        "ground_spend_typical": 75.0,
        "food_typical": 34.0,
        "local_transport_typical": 15.0,
        "activities_typical": 26.0,
        "source_method": (
            "Published August 2026 standard-traveler country model; food, local "
            "transport, and sightseeing summed; flights and accommodation excluded"
        ),
        "source_note": "Regional/CPI model rather than destination observations.",
    },
    "Turkmenistan": {
        "url": "https://travelcostcalculator.org/cost/turkmenistan",
        "reported_daily_total": 132.0,
        "accommodation_typical": 55.0,
        "ground_spend_typical": 77.0,
        "food_typical": 34.0,
        "local_transport_typical": 17.0,
        "activities_typical": 26.0,
        "source_method": (
            "Published August 2026 standard-traveler country model; food, local "
            "transport, and sightseeing summed; flights and accommodation excluded"
        ),
        "source_note": "Regional/CPI model rather than destination observations.",
    },
}


def fetch_text(url, attempts=5):
    for attempt in range(attempts):
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(request, timeout=60) as response:
                return response.read().decode("utf-8", "ignore")
        except HTTPError as error:
            if error.code not in {429, 500, 502, 503, 504} or attempt + 1 == attempts:
                raise
            retry_after = int(error.headers.get("Retry-After", "4") or 4)
            time.sleep(max(4, retry_after) * (attempt + 1))
        except (URLError, TimeoutError):
            if attempt + 1 == attempts:
                raise
            time.sleep(3 * (attempt + 1))


def slugify(value):
    value = unicodedata.normalize("NFKD", str(value))
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = re.sub(r"\([^)]*\)", "", value.casefold())
    value = value.replace("&", " and ").replace("/", " ")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def clean_text(raw):
    text = re.sub(r"<script\b.*?</script>", " ", raw, flags=re.I | re.S)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def money(pattern, text):
    match = re.search(pattern, text, flags=re.I | re.S)
    if not match:
        return None
    return float(match.group(1).replace(",", ""))


def category_value(raw, token):
    match = re.search(
        rf"cost-tile-category-{re.escape(token)}.*?"
        r'<span class="symbol">\s*\$\s*</span>\s*'
        r'<span class="curvalue">([0-9][0-9,.]*)</span>',
        raw,
        flags=re.I | re.S,
    )
    if not match:
        return None
    return float(match.group(1).replace(",", ""))


def parse_cost_page(raw):
    text = clean_text(raw)
    total = money(
        r"(?:typical traveler spends|plan to spend around)\s*\$([0-9][0-9,.]*)",
        text,
    )
    hotel = category_value(raw, "accommodation")
    food = category_value(raw, "food") or money(
        r"\$([0-9][0-9,.]*)\s*(?:\([^)]*\)\s*)?on meals", text
    )
    transport = category_value(raw, "transportation") or money(
        r"\$([0-9][0-9,.]*)\s*(?:\([^)]*\)\s*)?on local transportation", text
    )
    activities = category_value(raw, "entertainment") or money(
        r"Sightseeing activities, entertainment, and entrance tickets.*?"
        r"average of \$([0-9][0-9,.]*)(?:\s*\([^)]*\))?\s*per person, per day",
        text,
    )
    title_match = re.search(r"<title>(.*?)</title>", raw, flags=re.I | re.S)
    title = clean_text(title_match.group(1)) if title_match else ""
    return {
        "title": title,
        "reported_daily_total": total,
        "accommodation_typical": hotel,
        "food_typical": food,
        "local_transport_typical": transport,
        "activities_typical": activities,
    }


def complete(record):
    total = record.get("reported_daily_total")
    accommodation = record.get("accommodation_typical")
    return total is not None and accommodation is not None and total > accommodation


def load_catalog():
    with DESTINATIONS_PATH.open(encoding="utf-8-sig", newline="") as handle:
        destinations = list(csv.DictReader(handle))
    with BASES_PATH.open(encoding="utf-8-sig", newline="") as handle:
        bases = list(csv.DictReader(handle))
    by_destination = {}
    for row in bases:
        by_destination.setdefault(row["destination"], []).append(row["recommended_base"])
    return destinations, by_destination


def sitemap_urls():
    raw = fetch_text(SITEMAP_URL)
    return set(html.unescape(url) for url in re.findall(r"<loc>(.*?)</loc>", raw))


def city_candidates(destination, country, country_slug, bases, published_urls):
    aliases = DESTINATION_ALIASES.get(destination, []) + [slugify(destination)]
    seen = set()
    for alias in aliases:
        url = f"https://www.budgetyourtrip.com/{country_slug}/{alias}"
        if (
            url in published_urls
            and url not in seen
            and url not in EXCLUDED_DESTINATION_URLS.get(destination, set())
        ):
            seen.add(url)
            yield "Destination", destination, url
    for location, alias in PROXY_ALIASES.get(destination, []):
        url = f"https://www.budgetyourtrip.com/{country_slug}/{alias}"
        if url in published_urls and url not in seen:
            seen.add(url)
            yield "Nearby base proxy", location, url
    for base in bases:
        alias = slugify(base.split(",")[0])
        url = f"https://www.budgetyourtrip.com/{country_slug}/{alias}"
        if (
            url in published_urls
            and url not in seen
            and url not in EXCLUDED_DESTINATION_URLS.get(destination, set())
        ):
            seen.add(url)
            yield "Nearby base proxy", base, url


def read_cache():
    if not CACHE_PATH.exists():
        return {}
    return json.loads(CACHE_PATH.read_text(encoding="utf-8"))


def cached_parse(url, cache):
    if url not in cache:
        print(f"FETCH\t{url}", flush=True)
        try:
            cache[url] = parse_cost_page(fetch_text(url))
        except HTTPError as error:
            if error.code != 404:
                raise
            cache[url] = {"missing": True}
        CACHE_PATH.write_text(
            json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        time.sleep(0.8)
    return cache[url]


def select_evidence(row, bases, published_urls, cache):
    destination = row["name"]
    country = row["country"]
    country_slugs = COUNTRY_SLUGS[country]
    for country_slug in country_slugs:
        for scope, location, url in city_candidates(
            destination,
            country,
            country_slug,
            bases.get(destination, []),
            published_urls,
        ):
            parsed = cached_parse(url, cache)
            if complete(parsed):
                return scope, location, url, parsed
    for country_slug in country_slugs:
        url = f"https://www.budgetyourtrip.com/{country_slug}"
        parsed = cached_parse(url, cache)
        if complete(parsed):
            return "Country proxy", country, url, parsed
    supplemental = SUPPLEMENTAL_COUNTRY_EVIDENCE.get(country)
    if supplemental:
        return "Country proxy", country, supplemental["url"], supplemental
    return None


def format_number(value):
    if value is None:
        return ""
    return f"{float(value):.2f}".rstrip("0").rstrip(".")


def build_row(destination, selected):
    scope, location, url, evidence = selected
    ground = evidence.get("ground_spend_typical")
    if ground is None:
        ground = evidence["reported_daily_total"] - evidence["accommodation_typical"]
    if scope == "Destination":
        confidence = "Medium"
        proxy_note = "Destination-level traveler-reported category averages."
    elif scope == "Nearby base proxy":
        confidence = "Low"
        proxy_note = (
            f"Uses {location} as a practical nearby-base proxy; costs may differ across "
            "the destination."
        )
    else:
        confidence = "Low"
        proxy_note = (
            f"Uses the {location} country-level proxy because a complete destination page "
            "was unavailable; local and remote-area costs may differ."
        )
    if destination in EXCLUDED_DESTINATION_URLS:
        proxy_note += (
            " The destination page was excluded because its current value was an extreme "
            "outlier against the same source's country benchmark."
        )
    if evidence.get("source_method"):
        method_note = evidence.get("source_note", "")
    else:
        method_note = (
            "Food, transport, and activity figures are retained as context but are not "
            "summed because Budget Your Trip mixes per-day and per-purchase category "
            "averages."
        )
    return {
        "destination": destination,
        "cost_model": "independent",
        "currency": "USD",
        "reported_daily_total": format_number(evidence["reported_daily_total"]),
        "accommodation_typical": format_number(evidence["accommodation_typical"]),
        "ground_spend_typical": format_number(round(ground, 2)),
        "food_typical": format_number(evidence["food_typical"]),
        "local_transport_typical": format_number(evidence["local_transport_typical"]),
        "activities_typical": format_number(evidence["activities_typical"]),
        "evidence_scope": scope,
        "evidence_location": location,
        "source_1_url": url,
        "source_method": evidence.get(
            "source_method",
            "Published per-person daily total minus published one-person accommodation; "
            "flights excluded by the source and accommodation excluded by derivation",
        ),
        "collected_at": COLLECTED_AT,
        "confidence": confidence,
        "notes": (
            f"{proxy_note} {method_note}"
        ),
    }


def write_rows(rows):
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main():
    destinations, bases = load_catalog()
    print(f"DESTINATIONS\t{len(destinations)}", flush=True)
    published_urls = sitemap_urls()
    print(f"SITEMAP_URLS\t{len(published_urls)}", flush=True)
    cache = read_cache()
    rows = []
    gaps = []
    for index, destination in enumerate(destinations, start=1):
        selected = select_evidence(destination, bases, published_urls, cache)
        if selected is None:
            gaps.append(destination["name"])
            print(f"GAP\t{destination['name']}\t{destination['country']}", flush=True)
            continue
        row = build_row(destination["name"], selected)
        rows.append(row)
        print(
            f"SELECTED\t{index}/{len(destinations)}\t{destination['name']}\t"
            f"{row['evidence_scope']}\t${row['ground_spend_typical']}",
            flush=True,
        )
    if gaps:
        print("GAPS\t" + "|".join(gaps), flush=True)
        return 2
    write_rows(rows)
    print(f"ROWS\t{len(rows)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
