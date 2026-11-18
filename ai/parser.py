import json
import re

from ai.client import chat_complete, has_api_key
from recommender.constants import COUNTRIES, REGIONS
from recommender.prefs import normalize_preferences

PARSER_SYSTEM = f"""You extract travel preferences from user text.
Return JSON only. No markdown.
Use null when the user did not mention a field.
Schema:
{{
  "region": {" | ".join(f'"{key}"' for key in REGIONS)} | null,
  "country": string | null,
  "place_type": "historical" | "beach" | "nature" | "city" | "mountain" | "romantic" | "adventure" | null,
  "weather": "hot" | "warm" | "cool" | "cold" | null,
  "transportation": "public" | "taxi" | "rental" | "walking" | null,
  "culture": 1-5 | null,
  "food": 1-5 | null,
  "nature": 1-5 | null,
  "nightlife": 1-5 | null,
  "shopping": 1-5 | null,
  "quiet": 1-5 | null,
  "adventure": 1-5 | null,
  "trip_days": number | null,
  "ground_budget_total": number | null
}}
Rules:
- Only put a number in ground_budget_total when the user describes a total on-trip
  spending budget that excludes flights and accommodation
- If the user gives a daily spending budget and trip length, multiply them to produce
  ground_budget_total
- quiet, peaceful, not crowded => quiet 5
- I do not like nightlife => nightlife 1
- I like nightlife => nightlife 5
- An unmentioned interest must stay null; do not assume a neutral score
- history / temples / heritage => place_type historical and culture 5
- beach / island / sea => beach
- mountains / hiking / trekking => mountain or adventure
- Countries must be one of: {", ".join(COUNTRIES)}
- Region mapping: {", ".join(f'{label} => {key}' for key, label in REGIONS.items())}
"""


def parse_preference_text(text):
    if not text or not text.strip():
        raise ValueError("Please type what you want.")
    if not has_api_key():
        raise RuntimeError(
            "OpenRouter API key is missing. Add OPENROUTER_API_KEY in .env or Streamlit secrets."
        )
    raw = chat_complete(
        [
            {"role": "system", "content": PARSER_SYSTEM},
            {"role": "user", "content": text.strip()},
        ],
        temperature=0,
    )
    data = _extract_json(raw)
    prefs = normalize_preferences(data)
    prefs["_source_text"] = text.strip()
    prefs["_parsed"] = data
    return prefs


def _extract_json(text):
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        raise ValueError("The AI did not return usable preference data. Try the form instead.")
    data = json.loads(match.group(0))
    if not isinstance(data, dict):
        raise ValueError("The AI did not return usable preference data. Try the form instead.")
    return data
