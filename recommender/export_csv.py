from pathlib import Path

import pandas as pd

from recommender.catalog import catalog_rows

CSV_PATH = Path(__file__).resolve().parents[1] / "data" / "destinations.csv"
COLUMNS = [
    "name",
    "country",
    "region",
    "budget",
    "place_type",
    "weather",
    "trip_days_min",
    "trip_days_max",
    "culture",
    "food",
    "nature",
    "nightlife",
    "shopping",
    "quiet",
    "adventure",
    "transport",
    "description",
    "best_months",
    "attractions",
    "local_food",
    "transportation_info",
    "activities",
    "travel_tips",
]


def export_csv(path=None):
    target = Path(path) if path else CSV_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(catalog_rows(), columns=COLUMNS)
    df.to_csv(target, index=False)
    return target, len(df)


if __name__ == "__main__":
    path, count = export_csv()
    print(f"Wrote {count} rows to {path}")
