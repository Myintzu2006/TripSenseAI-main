from pathlib import Path

import pandas as pd
import streamlit as st


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
ACCOMMODATIONS_PATH = DATA_DIR / "accommodations.csv"
COSTS_PATH = DATA_DIR / "destination_costs.csv"


@st.cache_data(max_entries=3, show_spinner=False)
def load_accommodations(path=None):
    csv_path = Path(path) if path else ACCOMMODATIONS_PATH
    return pd.read_csv(csv_path).fillna("")


@st.cache_data(max_entries=3, show_spinner=False)
def load_destination_costs(path=None):
    csv_path = Path(path) if path else COSTS_PATH
    return pd.read_csv(csv_path).fillna("")


def accommodations_for_destination(name, limit=2):
    accommodations = load_accommodations()
    matches = accommodations[
        accommodations["destination"].str.casefold() == str(name).casefold()
    ]
    return matches.head(limit).reset_index(drop=True)


def costs_for_destination(name):
    costs = load_destination_costs()
    return costs[costs["destination"].str.casefold() == str(name).casefold()].reset_index(
        drop=True
    )


def daily_ground_budget(prefs):
    total = prefs.get("ground_budget_total")
    days = prefs.get("trip_days")
    if not total or not days:
        return None
    return round(float(total) / float(days), 2)


def affordability_for_destination(name, prefs):
    """Compare a user's daily ground budget with dated evidence, without guessing."""
    daily_budget = daily_ground_budget(prefs)
    if daily_budget is None:
        return {
            "status": "Budget not provided",
            "rank": 5,
            "daily_budget": None,
            "ground_spend_typical": None,
            "evidence": None,
            "confidence": None,
            "strict_eligible": False,
        }

    records = costs_for_destination(name)
    if records.empty:
        return {
            "status": "Insufficient cost evidence",
            "rank": 4,
            "daily_budget": daily_budget,
            "ground_spend_typical": None,
            "evidence": None,
            "confidence": None,
            "strict_eligible": False,
        }

    evidence = records.iloc[0].to_dict()
    typical = float(evidence["ground_spend_typical"])
    if daily_budget >= typical * 1.25:
        status, rank = "Comfortably within budget", 0
    elif daily_budget >= typical:
        status, rank = "Within estimated budget", 1
    elif daily_budget >= typical * 0.8:
        status, rank = "Stretch budget", 2
    else:
        status, rank = "Above budget", 3

    confidence = str(evidence.get("confidence", "")).title()
    strict_eligible = confidence in {"High", "Medium"} and rank in {0, 1}

    return {
        "status": status,
        "rank": rank,
        "daily_budget": daily_budget,
        "ground_spend_typical": typical,
        "evidence": evidence,
        "confidence": confidence,
        "strict_eligible": strict_eligible,
    }
