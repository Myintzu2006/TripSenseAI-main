from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from recommender.catalog import catalog_rows


def atom(value):
    text = str(value).strip().lower().replace(" ", "_").replace("-", "_")
    if re.fullmatch(r"[a-z][a-z0-9_]*", text):
        return text
    return "'" + text.replace("'", "''") + "'"


def generate():
    rows = catalog_rows()
    lines = [
        "% Asia travel recommender facts and rules",
        "% Separate from the Python system. Query with SWI-Prolog.",
        ":- discontiguous destination/1.",
        ":- discontiguous country/2.",
        ":- discontiguous region/2.",
        ":- discontiguous place_type/2.",
        ":- discontiguous budget/2.",
        ":- discontiguous weather/2.",
        ":- discontiguous trip_days/3.",
        ":- discontiguous culture/2.",
        ":- discontiguous food/2.",
        ":- discontiguous nature/2.",
        ":- discontiguous nightlife/2.",
        ":- discontiguous shopping/2.",
        ":- discontiguous quiet/2.",
        ":- discontiguous adventure/2.",
        ":- discontiguous transport/2.",
        "",
    ]
    for row in rows:
        name = atom(row["name"])
        lines.append(f"destination({name}).")
        lines.append(f"country({name}, {atom(row['country'])}).")
        lines.append(f"region({name}, {atom(row['region'])}).")
        lines.append(f"place_type({name}, {atom(row['place_type'])}).")
        lines.append(f"budget({name}, {atom(row['budget'])}).")
        lines.append(f"weather({name}, {atom(row['weather'])}).")
        lines.append(f"trip_days({name}, {row['trip_days_min']}, {row['trip_days_max']}).")
        lines.append(f"culture({name}, {row['culture']}).")
        lines.append(f"food({name}, {row['food']}).")
        lines.append(f"nature({name}, {row['nature']}).")
        lines.append(f"nightlife({name}, {row['nightlife']}).")
        lines.append(f"shopping({name}, {row['shopping']}).")
        lines.append(f"quiet({name}, {row['quiet']}).")
        lines.append(f"adventure({name}, {row['adventure']}).")
        lines.append(f"transport({name}, {row['transport']}).")
        lines.append("")

    lines.extend(
        [
            "% Basic classification rules",
            "historical_destination(X) :-",
            "    place_type(X, historical).",
            "",
            "southeast_asia_destination(X) :-",
            "    region(X, southeast_asia).",
            "",
            "east_asia_destination(X) :-",
            "    region(X, east_asia).",
            "",
            "south_asia_destination(X) :-",
            "    region(X, south_asia).",
            "",
            "central_asia_destination(X) :-",
            "    region(X, central_asia).",
            "",
            "low_budget_destination(X) :-",
            "    budget(X, low).",
            "",
            "cool_east_asia(X) :-",
            "    region(X, east_asia),",
            "    weather(X, cool).",
            "",
            "% Multi-criteria and high-rating inference rules",
            "historical_southeast_asia(X) :-",
            "    region(X, southeast_asia),",
            "    place_type(X, historical).",
            "",
            "quiet_historical(X) :-",
            "    place_type(X, historical),",
            "    quiet(X, Q),",
            "    Q >= 4.",
            "",
            "nature_escape(X) :-",
            "    nature(X, N),",
            "    N >= 4,",
            "    quiet(X, Q),",
            "    Q >= 3.",
            "",
            "foodie_paradise(X) :-",
            "    food(X, F),",
            "    F >= 4.",
            "",
            "nightlife_hub(X) :-",
            "    nightlife(X, NL),",
            "    NL >= 4.",
            "",
            "adventure_seeker(X) :-",
            "    adventure(X, A),",
            "    A >= 4.",
            "",
            "cultural_explorer(X) :-",
            "    culture(X, C),",
            "    C >= 4.",
            "",
            "budget_foodie_southeast_asia(X) :-",
            "    region(X, southeast_asia),",
            "    budget(X, low),",
            "    food(X, F),",
            "    F >= 4.",
            "",
            "short_trip_destination(X) :-",
            "    trip_days(X, _, Max),",
            "    Max =< 3.",
            "",
            "budget_short_trip(X) :-",
            "    budget(X, low),",
            "    trip_days(X, _, Max),",
            "    Max =< 3.",
            "",
            "easy_transit_city(X) :-",
            "    place_type(X, city),",
            "    transport(X, T),",
            "    T >= 3.",
            "",
            "% Flexible query predicate",
            "recommend_trip(X, Region, Budget, MinNature, MinCulture) :-",
            "    region(X, Region),",
            "    budget(X, Budget),",
            "    nature(X, N),",
            "    N >= MinNature,",
            "    culture(X, C),",
            "    C >= MinCulture.",
            "",
        ]
    )
    path = Path(__file__).with_name("destinations.pl")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


if __name__ == "__main__":
    print(generate())
