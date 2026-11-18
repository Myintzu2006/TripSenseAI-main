PLACE_TYPES = [
    "historical",
    "beach",
    "nature",
    "city",
    "mountain",
    "romantic",
    "adventure",
]

WEATHERS = ["hot", "warm", "cool", "cold"]

BUDGETS = ["low", "medium", "high"]
BUDGET_RANK = {"low": 1, "medium": 2, "high": 3}
BUDGET_USD = {
    "low": "$25–$60 per person per day",
    "medium": "$60–$150 per person per day",
    "high": "$150+ per person per day",
}
BUDGET_GUIDE = (
    "Ground-spending estimates are in USD per person and exclude flights and "
    "accommodation. They cover ordinary meals, local transport, attractions, and "
    "other recorded on-trip spending. Every published estimate shows its source, "
    "review date, confidence, and whether it is destination-level or a disclosed proxy."
)


def budget_label(level):
    key = str(level or "").strip().lower()
    if key not in BUDGET_USD:
        return str(level)
    return f"{key.title()} ({BUDGET_USD[key]})"


REGIONS = {
    "southeast_asia": "Southeast Asia",
    "east_asia": "East Asia",
    "south_asia": "South Asia",
    "central_asia": "Central Asia",
}

REGION_COUNTRIES = {
    "southeast_asia": [
        "Brunei",
        "Cambodia",
        "Indonesia",
        "Laos",
        "Malaysia",
        "Myanmar",
        "Philippines",
        "Singapore",
        "Thailand",
        "Timor-Leste",
        "Vietnam",
    ],
    "east_asia": [
        "China",
        "Hong Kong",
        "Japan",
        "Macau",
        "Mongolia",
        "South Korea",
        "Taiwan",
    ],
    "south_asia": [
        "Bangladesh",
        "Bhutan",
        "India",
        "Maldives",
        "Nepal",
        "Sri Lanka",
    ],
    "central_asia": [
        "Georgia",
        "Kazakhstan",
        "Kyrgyzstan",
        "Tajikistan",
        "Turkmenistan",
        "Uzbekistan",
    ],
}

COUNTRIES = [
    "Myanmar",
    "Thailand",
    "Vietnam",
    "Cambodia",
    "Malaysia",
    "Singapore",
    "Indonesia",
    "Philippines",
    "Japan",
    "South Korea",
    "Laos",
    "Bangladesh",
    "Bhutan",
    "Nepal",
    "Sri Lanka",
    "India",
    "Maldives",
    "China",
    "Mongolia",
    "Taiwan",
    "Brunei",
    "Timor-Leste",
    "Hong Kong",
    "Macau",
    "Kazakhstan",
    "Kyrgyzstan",
    "Uzbekistan",
    "Tajikistan",
    "Turkmenistan",
    "Georgia",
]

SCORE_COLS = [
    "culture",
    "food",
    "nature",
    "nightlife",
    "shopping",
    "quiet",
    "adventure",
    "transport",
]

TRANSPORT_TO_SCORE = {
    "public": 5,
    "walking": 4,
    "taxi": 3,
    "rental": 3,
}

COUNTRY_ALIASES = {
    "korea": "South Korea",
    "south korea": "South Korea",
    "republic of korea": "South Korea",
    "burma": "Myanmar",
    "myanmar": "Myanmar",
    "thailand": "Thailand",
    "vietnam": "Vietnam",
    "viet nam": "Vietnam",
    "cambodia": "Cambodia",
    "malaysia": "Malaysia",
    "singapore": "Singapore",
    "indonesia": "Indonesia",
    "philippines": "Philippines",
    "japan": "Japan",
    "laos": "Laos",
    "bangladesh": "Bangladesh",
    "bhutan": "Bhutan",
    "nepal": "Nepal",
    "sri lanka": "Sri Lanka",
    "india": "India",
    "maldives": "Maldives",
    "china": "China",
    "mongolia": "Mongolia",
    "taiwan": "Taiwan",
    "roc": "Taiwan",
    "brunei": "Brunei",
    "timor-leste": "Timor-Leste",
    "east timor": "Timor-Leste",
    "hong kong": "Hong Kong",
    "hk": "Hong Kong",
    "macau": "Macau",
    "macao": "Macau",
    "kazakhstan": "Kazakhstan",
    "kyrgyzstan": "Kyrgyzstan",
    "uzbekistan": "Uzbekistan",
    "tajikistan": "Tajikistan",
    "turkmenistan": "Turkmenistan",
    "georgia": "Georgia",
}

REGION_ALIASES = {
    "southeast asia": "southeast_asia",
    "south east asia": "southeast_asia",
    "sea": "southeast_asia",
    "east asia": "east_asia",
    "northeast asia": "east_asia",
    "south asia": "south_asia",
    "indian subcontinent": "south_asia",
    "central asia": "central_asia",
}
