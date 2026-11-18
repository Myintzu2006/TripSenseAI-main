"""Build representative accommodation coverage from attributable open data.

Coordinates come from Wikipedia's API. Accommodation identities come from
OpenStreetMap through Overpass. Existing official/government records are preserved.
The generated records do not claim operation, price, or room availability.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
import sys
import time
from urllib.parse import urlencode
from urllib.error import HTTPError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DESTINATIONS_PATH = ROOT / "data" / "destinations.csv"
ACCOMMODATIONS_PATH = ROOT / "data" / "accommodations.csv"
BASES_PATH = ROOT / "data" / "destination_bases.csv"
CACHE_PATH = ROOT / "data" / "accommodation_collection_cache.json"
WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
OVERPASS_API = "https://overpass-api.de/api/interpreter"
USER_AGENT = "AsiaCompassDataResearch/2.0 (educational travel project)"
VERIFIED_AT = "2026-09-02"

FIELDS = [
    "destination",
    "recommended_base",
    "property_name",
    "property_type",
    "location",
    "distance_km",
    "official_url",
    "source_url",
    "source_type",
    "verified_at",
    "confidence",
    "data_license",
]

# A destination can be a region, park, island, route, or paired area rather than a
# hotel-searchable town. These bases make that choice explicit and reviewable.
BASE_OVERRIDES = {
    "Addu Atoll": ["Hithadhoo, Addu City"],
    "Altai Tavan Bogd": ["Ölgii (city)"],
    "Ari Atoll": ["Mahibadhoo"],
    "Atauro Island": ["Vila Maumeta"],
    "Cameron Highlands": ["Tanah Rata"],
    "Charyn Canyon": ["Saty, Kazakhstan"],
    "Coloane": ["Coloane"],
    "Coron": ["Coron, Palawan"],
    "Everest Region": ["Namche Bazaar", "Lukla"],
    "Gobi Desert": ["Dalanzadgad"],
    "Ha Long Bay": ["Hạ Long"],
    "Hong Kong - Central": ["Central, Hong Kong"],
    "Iskanderkul Lake": ["Panjakent"],
    "Issyk-Kul": ["Cholpon-Ata"],
    "Jaco Island": ["Tutuala"],
    "Karakorum": ["Kharkhorin"],
    "Kenting": ["Hengchun"],
    "Kerala": ["Kochi"],
    "Koh Rong": ["Koh Rong"],
    "Kowloon / Tsim Sha Tsui": ["Tsim Sha Tsui"],
    "Kuang Si Falls": ["Luang Prabang"],
    "Lake Khuvsgul": ["Khatgal"],
    "Lantau / Big Buddha": ["Tung Chung"],
    "Lombok": ["Mataram"],
    "Mandai": ["Mandai, Singapore"],
    "Mount Ramelau": ["Hato-Udo"],
    "Muara Beach": ["Muara, Brunei"],
    "North Malé Atoll": ["Hulhumalé"],
    "Okinawa": ["Naha"],
    "Pamir Highway": ["Khorugh"],
    "Paro Taktsang": ["Paro, Bhutan"],
    "Phobjikha Valley": ["Gangteng Monastery"],
    "Pulau Ubin": ["Changi Village"],
    "Sai Kung / Geopark": ["Sai Kung Town"],
    "Song-Kul": ["Kochkor"],
    "Stanley / Cheung Chau": ["Stanley, Hong Kong", "Cheung Chau"],
    "Sundarbans": ["Mongla"],
    "Taman Negara": ["Kuala Tahan"],
    "Taroko Gorge": ["Hualien City"],
    "Ulu Temburong National Park": ["Bangar, Brunei"],
    "Yangykala Canyon": ["Balkanabat"],
}

TITLE_OVERRIDES = {
    "Bagerhat": "Bagerhat",
    "Bandarban": "Bandarban",
    "Ella": "Ella, Sri Lanka",
    "Georgia": "Georgia (country)",
    "Goa": "Goa",
    "Hpa-An": "Hpa-an",
    "Kep": "Kep, Cambodia",
    "Malé": "Malé",
    "Mandai, Singapore": "Singapore Zoo",
    "Pai": "Pai, Thailand",
    "Sapa": "Sa Pa",
    "Seminyak": "Kuta, Bali",
    "Stanley, Hong Kong": "Stanley, Hong Kong",
    "Hue": "Huế",
}

# Coordinates used only when the English Wikipedia API has no coordinate-bearing
# page for the named base. Sources are documented beside each value.
COORD_OVERRIDES = {
    # US NGA geographic-name record for Hithadhoo in Seenu (Addu), Maldives:
    # https://geographic.org/geographic_names/name.php?c=maldives&fid=4007&uni=264793
    "Hithadhoo, Addu City": (-0.6, 73.083333),
    # Autoridade Administrativa de Ataúro: https://atauro.gov.tl/pt/posto/suku/vila-maumeta/
    "Vila Maumeta": (-8.267807068, 125.6032484),
    # Historic Centre of Macau UNESCO/Wikipedia coordinates.
    "Macau Historic Centre": (22.1912917, 113.5364611),
    # English Wikipedia article "Taipa".
    "Taipa Village": (22.15972, 113.55944),
    # Kazakhstan national tourism portal: https://kazakhstan.travel/en/attractions/77
    "Saty, Kazakhstan": (43.06911, 78.40908),
}

OSM_TYPES = {
    "hotel": "Hotel",
    "guest_house": "Guesthouse",
    "hostel": "Hostel",
    "motel": "Motel",
    "resort": "Resort",
    "apartment": "Serviced apartment",
    "chalet": "Lodge / chalet",
    "alpine_hut": "Mountain hut",
    "wilderness_hut": "Wilderness hut",
    "camp_site": "Camp",
}


def fetch_json(url, data=None, attempts=6):
    body = data.encode("utf-8") if isinstance(data, str) else data
    for attempt in range(attempts):
        try:
            request = Request(url, data=body, headers={"User-Agent": USER_AGENT})
            with urlopen(request, timeout=120) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code not in {429, 502, 503, 504} or attempt + 1 == attempts:
                raise
            retry_after = int(error.headers.get("Retry-After", "5") or 5)
            time.sleep(max(5, retry_after) * (attempt + 1))
        except Exception:
            if attempt + 1 == attempts:
                raise
            time.sleep(3 * (attempt + 1))


def wikipedia_coordinates(titles):
    params = {
        "action": "query",
        "format": "json",
        "formatversion": 2,
        "redirects": 1,
        "prop": "coordinates",
        "colimit": "max",
        "titles": "|".join(titles),
    }
    payload = fetch_json(f"{WIKIPEDIA_API}?{urlencode(params)}")
    aliases = {title.casefold(): title for title in titles}
    query = payload.get("query", {})
    for item in query.get("normalized", []):
        original = aliases.get(str(item.get("from", "")).casefold())
        if original:
            aliases[str(item.get("to", "")).casefold()] = original
    for item in query.get("redirects", []):
        original = aliases.get(str(item.get("from", "")).casefold())
        if original:
            aliases[str(item.get("to", "")).casefold()] = original
    result = {}
    for page in query.get("pages", []):
        coords = page.get("coordinates") or []
        original = aliases.get(str(page.get("title", "")).casefold())
        if original and coords:
            result[original] = (float(coords[0]["lat"]), float(coords[0]["lon"]))
    return result


def search_coordinate(title, country):
    time.sleep(1.0)
    params = {
        "action": "query",
        "format": "json",
        "formatversion": 2,
        "generator": "search",
        "gsrsearch": f'intitle:"{title}" {country}',
        "gsrlimit": 5,
        "prop": "coordinates",
        "colimit": "max",
    }
    payload = fetch_json(f"{WIKIPEDIA_API}?{urlencode(params)}")
    for page in sorted(
        payload.get("query", {}).get("pages", []),
        key=lambda item: item.get("index", 999),
    ):
        coords = page.get("coordinates") or []
        if coords:
            return float(coords[0]["lat"]), float(coords[0]["lon"])
    return None


def distance_km(lat1, lon1, lat2, lon2):
    radius = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    value = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return radius * 2 * math.atan2(math.sqrt(value), math.sqrt(1 - value))


def search_radius(destination):
    remote = {
        "Altai Tavan Bogd", "Charyn Canyon", "Darvaza Gas Crater", "Everest Region",
        "Gobi Desert", "Iskanderkul Lake", "Jaco Island", "Lake Khuvsgul",
        "Mount Ramelau", "Pamir Highway", "Phobjikha Valley", "Song-Kul",
        "Sundarbans", "Taman Negara", "Ulu Temburong National Park", "Yangykala Canyon",
    }
    return 30000 if destination in remote else 8000


def overpass_elements(bases):
    clauses = []
    for base in bases:
        clauses.append(
            f'nwr(around:{base["radius"]},{base["lat"]:.6f},{base["lon"]:.6f})'
            '["tourism"~"^(hotel|guest_house|hostel|motel|resort|apartment|chalet|alpine_hut|wilderness_hut|camp_site)$"]'
            '["name"];'
        )
    query = "[out:json][timeout:120];(" + "".join(clauses) + ");out center tags;"
    return fetch_json(OVERPASS_API, data=urlencode({"data": query})).get("elements", [])


def element_coordinates(element):
    if "lat" in element and "lon" in element:
        return float(element["lat"]), float(element["lon"])
    center = element.get("center") or {}
    if "lat" in center and "lon" in center:
        return float(center["lat"]), float(center["lon"])
    return None


def clean_website(value):
    value = str(value or "").strip()
    if not value:
        return ""
    if value.startswith("http://") or value.startswith("https://"):
        return value
    return "https://" + value


def candidate_from_element(element, base, country):
    tags = element.get("tags") or {}
    coords = element_coordinates(element)
    if not coords:
        return None
    distance = distance_km(base["lat"], base["lon"], coords[0], coords[1])
    if distance * 1000 > base["radius"]:
        return None
    name = str(tags.get("name:en") or tags.get("name") or "").strip()
    tourism = str(tags.get("tourism") or "")
    if not name or tourism not in OSM_TYPES:
        return None
    website = clean_website(tags.get("contact:website") or tags.get("website"))
    address_parts = [
        tags.get("addr:housenumber"), tags.get("addr:street"), tags.get("addr:city")
    ]
    location = ", ".join(str(part).strip() for part in address_parts if part)
    if not location:
        location = f'{base["display_base"]}, {country}'
    osm_type = element["type"]
    osm_id = element["id"]
    return {
        "destination": base["destination"],
        "recommended_base": base["display_base"],
        "property_name": name,
        "property_type": OSM_TYPES[tourism],
        "location": location,
        "distance_km": f"{distance:.1f}",
        "official_url": website,
        "source_url": f"https://www.openstreetmap.org/{osm_type}/{osm_id}",
        "source_type": "OpenStreetMap accommodation record; operation not independently verified",
        "verified_at": VERIFIED_AT,
        "confidence": "Medium" if website else "Low",
        "data_license": "OpenStreetMap data © contributors, ODbL",
        "_score": (0 if website else 1, distance, name.casefold()),
    }


def read_destinations():
    with DESTINATIONS_PATH.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_existing():
    if not ACCOMMODATIONS_PATH.exists():
        return []
    with ACCOMMODATIONS_PATH.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    # Only preserve manually researched official/government evidence. Generated
    # OpenStreetMap rows are rebuilt from the cache so ranking changes and the
    # two-record cap are applied deterministically on every refresh.
    rows = [
        row
        for row in rows
        if "openstreetmap.org" not in str(row.get("source_url", "")).casefold()
    ]
    for row in rows:
        row.setdefault("distance_km", "")
        row.setdefault("data_license", "Property or registry source; see source URL")
    return rows


def resolve_bases(destinations):
    base_records = []
    title_context = {}
    for row in destinations:
        destination = row["name"]
        bases = BASE_OVERRIDES.get(destination, [destination])
        for display_base in bases:
            title = TITLE_OVERRIDES.get(display_base, display_base)
            key = (destination, display_base)
            title_context.setdefault(title, []).append((key, row["country"]))

    coordinates = {}
    titles = list(title_context)
    for start in range(0, len(titles), 40):
        coordinates.update(wikipedia_coordinates(titles[start : start + 40]))

    for title, contexts in title_context.items():
        for key, country in contexts:
            coords = COORD_OVERRIDES.get(key[1]) or coordinates.get(title)
            if not coords:
                coords = search_coordinate(title, country)
            if not coords:
                print(f"MISSING_COORDINATE\t{key[0]}\t{key[1]}", flush=True)
                continue
            base_records.append(
                {
                    "destination": key[0],
                    "display_base": key[1],
                    "wikipedia_title": title,
                    "country": country,
                    "lat": coords[0],
                    "lon": coords[1],
                    "radius": search_radius(key[0]),
                }
            )
    return base_records


def collect_candidates(bases):
    candidates = {base["destination"]: [] for base in bases}
    cache = {}
    if CACHE_PATH.exists():
        cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))

    def cache_key(base):
        return f'{base["destination"]}|{base["display_base"]}'

    pending = [base for base in bases if cache_key(base) not in cache]
    for start in range(0, len(pending), 4):
        batch = pending[start : start + 4]
        print(f"OVERPASS_BATCH\t{start // 4 + 1}\t{len(batch)} bases", flush=True)
        elements = overpass_elements(batch)
        for base in batch:
            seen_sources = set()
            rows = []
            for element in elements:
                candidate = candidate_from_element(element, base, base["country"])
                if not candidate or candidate["source_url"] in seen_sources:
                    continue
                seen_sources.add(candidate["source_url"])
                candidate["_score"] = list(candidate["_score"])
                rows.append(candidate)
            cache[cache_key(base)] = rows
        CACHE_PATH.write_text(
            json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    for base in bases:
        candidates[base["destination"]].extend(cache.get(cache_key(base), []))
    return candidates


def select_rows(destinations, existing, candidates):
    existing_by_destination = {}
    for row in existing:
        existing_by_destination.setdefault(row["destination"], []).append(row)

    output = []
    gaps = []
    remote_destinations = {
        "Altai Tavan Bogd", "Charyn Canyon", "Darvaza Gas Crater", "Everest Region",
        "Gobi Desert", "Iskanderkul Lake", "Jaco Island", "Lake Khuvsgul",
        "Mount Ramelau", "Pamir Highway", "Phobjikha Valley", "Song-Kul",
        "Sundarbans", "Taman Negara", "Ulu Temburong National Park", "Yangykala Canyon",
    }

    def suitability_score(row, destination):
        property_type = row["property_type"]
        if destination in remote_destinations:
            type_order = {
                "Lodge / chalet": 0,
                "Mountain hut": 0,
                "Wilderness hut": 0,
                "Camp": 0,
                "Resort": 1,
                "Hotel": 1,
                "Guesthouse": 1,
                "Motel": 2,
                "Hostel": 2,
                "Serviced apartment": 2,
            }
        else:
            type_order = {
                "Hotel": 0,
                "Resort": 0,
                "Guesthouse": 1,
                "Motel": 1,
                "Lodge / chalet": 2,
                "Serviced apartment": 2,
                "Hostel": 2,
                "Mountain hut": 3,
                "Wilderness hut": 3,
                "Camp": 3,
            }
        distance = float(row.get("distance_km") or 9999)
        has_website = 0 if row.get("official_url") else 1
        return (
            type_order.get(property_type, 9),
            has_website,
            distance,
            row["property_name"].casefold(),
        )

    for destination in destinations:
        name = destination["name"]
        chosen = list(existing_by_destination.get(name, []))[:2]
        used_names = {row["property_name"].strip().casefold() for row in chosen}
        available = sorted(
            candidates.get(name, []),
            key=lambda row: suitability_score(row, name),
        )
        for row in available:
            if len(chosen) >= 2:
                break
            normalized = row["property_name"].strip().casefold()
            if normalized in used_names:
                continue
            used_names.add(normalized)
            row = {key: value for key, value in row.items() if not key.startswith("_")}
            chosen.append(row)
            if len(chosen) >= 2:
                break
        if not chosen:
            gaps.append(name)
        output.extend(chosen)
    return output, gaps


def write_outputs(rows, bases):
    with ACCOMMODATIONS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in FIELDS} for row in rows)

    with BASES_PATH.open("w", encoding="utf-8", newline="") as handle:
        fields = ["destination", "recommended_base", "wikipedia_title", "country", "latitude", "longitude", "search_radius_km"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for base in bases:
            writer.writerow(
                {
                    "destination": base["destination"],
                    "recommended_base": base["display_base"],
                    "wikipedia_title": base["wikipedia_title"],
                    "country": base["country"],
                    "latitude": f'{base["lat"]:.6f}',
                    "longitude": f'{base["lon"]:.6f}',
                    "search_radius_km": base["radius"] // 1000,
                }
            )


def main():
    destinations = read_destinations()
    existing = read_existing()
    print(f"DESTINATIONS\t{len(destinations)}", flush=True)
    bases = resolve_bases(destinations)
    print(f"RESOLVED_BASES\t{len(bases)}", flush=True)
    candidates = collect_candidates(bases)
    rows, gaps = select_rows(destinations, existing, candidates)
    write_outputs(rows, bases)
    coverage = len({row["destination"] for row in rows})
    print(f"ROWS\t{len(rows)}", flush=True)
    print(f"COVERAGE\t{coverage}/{len(destinations)}", flush=True)
    if gaps:
        print("GAPS\t" + "|".join(gaps), flush=True)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
