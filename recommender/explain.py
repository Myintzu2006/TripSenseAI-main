from recommender.constants import REGIONS, SCORE_COLS, budget_label

LABELS = {
    "culture": "culture",
    "food": "food",
    "nature": "nature",
    "nightlife": "nightlife",
    "shopping": "shopping",
    "quiet": "quiet places",
    "adventure": "adventure",
    "transport": "easy transport",
}


def explain_match(row, prefs):
    bits = []
    if prefs.get("place_type") and prefs["place_type"] == row["place_type"]:
        bits.append(f"it is a {row['place_type']} destination")
    if prefs.get("weather") and prefs["weather"] == row["weather"]:
        bits.append(f"typical weather is {row['weather']}")
    if prefs.get("budget"):
        bits.append(f"the budget level is {budget_label(row['budget'])}")
    if prefs.get("region"):
        bits.append(f"it is in {REGIONS.get(row['region'], row['region'])}")
    if prefs.get("country") and prefs["country"] == row["country"]:
        bits.append(f"it is in {row['country']}")

    for col in SCORE_COLS:
        user_val = prefs.get(col)
        dest_val = int(row[col])
        label = LABELS[col]
        if not user_val:
            continue
        if user_val >= 4 and dest_val >= 4:
            bits.append(f"it scores high for {label} ({dest_val}/5)")
        elif user_val <= 2 and dest_val <= 2:
            bits.append(f"it is not a strong {label} place, which matches what you asked for")

    days = prefs.get("trip_days")
    if days:
        bits.append(
            f"a typical stay is {int(row['trip_days_min'])} to {int(row['trip_days_max'])} days"
        )

    if not bits:
        return (
            f"{row['name']} is a {row['place_type']} destination in {row['country']} "
            "in the destination catalog."
        )
    return f"{row['name']} fits because " + "; ".join(bits) + "."
