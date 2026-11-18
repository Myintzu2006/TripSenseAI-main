from recommender.constants import (
    BUDGETS,
    COUNTRIES,
    COUNTRY_ALIASES,
    PLACE_TYPES,
    REGION_ALIASES,
    REGIONS,
    SCORE_COLS,
    TRANSPORT_TO_SCORE,
    WEATHERS,
)


def default_preferences():
    return {
        "budget": None,
        "region": None,
        "country": None,
        "place_type": None,
        "weather": None,
        "transportation": None,
        "culture": 0,
        "food": 0,
        "nature": 0,
        "nightlife": 0,
        "shopping": 0,
        "quiet": 0,
        "adventure": 0,
        "trip_days": None,
        "ground_budget_total": None,
        "strict_budget": False,
        "top_k": 5,
    }


def _clean_str(value):
    if value is None:
        return None
    text = str(value).strip().lower()
    if text in {"", "any", "none", "null", "n/a"}:
        return None
    return text


def _as_int(value, minimum=0, maximum=5):
    if value is None or value == "":
        return None
    try:
        number = int(round(float(value)))
    except (TypeError, ValueError):
        return None
    return max(minimum, min(maximum, number))


def normalize_preferences(raw):
    prefs = default_preferences()
    if not raw:
        return prefs

    budget = _clean_str(raw.get("budget"))
    if budget in BUDGETS:
        prefs["budget"] = budget

    region = _clean_str(raw.get("region"))
    if region in REGIONS:
        prefs["region"] = region
    elif region in REGION_ALIASES:
        prefs["region"] = REGION_ALIASES[region]

    country_raw = raw.get("country")
    country = _clean_str(country_raw)
    if country in COUNTRY_ALIASES:
        prefs["country"] = COUNTRY_ALIASES[country]
    elif country_raw and str(country_raw).strip() in COUNTRIES:
        prefs["country"] = str(country_raw).strip()

    place_type = _clean_str(raw.get("place_type"))
    if place_type in PLACE_TYPES:
        prefs["place_type"] = place_type

    weather = _clean_str(raw.get("weather"))
    if weather in WEATHERS:
        prefs["weather"] = weather

    transportation = _clean_str(raw.get("transportation"))
    if transportation in TRANSPORT_TO_SCORE:
        prefs["transportation"] = transportation
        prefs["transport"] = TRANSPORT_TO_SCORE[transportation]

    for col in SCORE_COLS:
        if col == "transport" and "transport" in prefs:
            continue
        value = _as_int(raw.get(col))
        if value is not None:
            prefs[col] = value

    days = raw.get("trip_days")
    if days not in (None, ""):
        try:
            prefs["trip_days"] = max(1, min(30, int(round(float(days)))))
        except (TypeError, ValueError):
            pass

    ground_budget = raw.get("ground_budget_total")
    if ground_budget not in (None, ""):
        try:
            value = float(ground_budget)
            if value > 0:
                prefs["ground_budget_total"] = round(value, 2)
        except (TypeError, ValueError):
            pass

    prefs["strict_budget"] = bool(raw.get("strict_budget", False))

    top_k = raw.get("top_k")
    if top_k not in (None, ""):
        try:
            prefs["top_k"] = max(1, min(10, int(top_k)))
        except (TypeError, ValueError):
            pass

    return prefs
