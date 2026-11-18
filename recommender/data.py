from pathlib import Path

import pandas as pd
import streamlit as st

CSV_PATH = Path(__file__).resolve().parents[1] / "data" / "destinations.csv"


@st.cache_data(max_entries=5, show_spinner=False)
def load_destinations(path=None):
    csv_path = Path(path) if path else CSV_PATH
    df = pd.read_csv(csv_path)
    score_cols = [
        "culture",
        "food",
        "nature",
        "nightlife",
        "shopping",
        "quiet",
        "adventure",
        "transport",
        "trip_days_min",
        "trip_days_max",
    ]
    for col in score_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df
