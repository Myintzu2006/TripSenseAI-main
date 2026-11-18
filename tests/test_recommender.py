import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from recommender.catalog import catalog_rows
from recommender.constants import COUNTRIES, PLACE_TYPES, budget_label
from recommender.data import load_destinations
from recommender.encode import active_feature_blocks, destination_matrix, user_vector
from recommender.export_csv import CSV_PATH
from recommender.explain import explain_match
from recommender.filter import hard_filter
from recommender.prefs import normalize_preferences
from recommender.rank import recommend


def test_catalog_size_and_countries():
    rows = catalog_rows()
    assert len(rows) == 160
    assert len(COUNTRIES) == 30
    assert set(r["country"] for r in rows) == set(COUNTRIES)
    assert len({r["name"].strip().casefold() for r in rows}) == len(rows)
    assert all(r["place_type"] in PLACE_TYPES for r in rows)
    assert "south_asia" in set(r["region"] for r in rows)
    assert "central_asia" in set(r["region"] for r in rows)


def test_csv_matches_catalog():
    rows = catalog_rows()
    df = load_destinations(CSV_PATH)
    assert len(df) == len(rows)
    assert set(df["name"]) == {row["name"] for row in rows}
    assert set(df["country"]) == set(COUNTRIES)
    assert not df["name"].str.strip().str.casefold().duplicated().any()
    assert "Kyoto" in set(df["name"])
    assert "Luang Prabang" in set(df["name"])
    assert "Taipei" in set(df["name"])


def test_region_filter_removes_japan():
    df = load_destinations()
    prefs = normalize_preferences({"region": "southeast_asia"})
    filtered = hard_filter(df, prefs)
    assert "Japan" not in set(filtered["country"])
    assert "Thailand" in set(filtered["country"])


def test_legacy_budget_label_is_not_a_hard_filter():
    df = load_destinations()
    prefs = normalize_preferences({"budget": "low"})
    filtered = hard_filter(df, prefs)
    assert set(filtered["budget"]) == {"low", "medium", "high"}


def test_east_asia_historical_ranks_strong_historical_matches():
    df = load_destinations()
    prefs = normalize_preferences(
        {
            "budget": "medium",
            "region": "east_asia",
            "place_type": "historical",
            "weather": "cool",
            "culture": 5,
            "food": 5,
            "quiet": 4,
            "nightlife": 1,
            "nature": 3,
            "shopping": 2,
            "adventure": 2,
            "top_k": 6,
        }
    )
    ranked, message = recommend(df, prefs)
    assert message is None
    names = list(ranked["name"])
    assert names[0] in {"Gyeongju", "Kyoto", "Nara", "Kanazawa"}
    assert {"Kyoto", "Nara", "Kanazawa"}.issubset(set(names))


def test_unselected_experiences_do_not_affect_ranking():
    prefs = normalize_preferences({"country": "Myanmar"})
    assert prefs["culture"] == 0
    assert prefs["food"] == 0
    assert prefs["nature"] == 0
    bagan = load_destinations().loc[lambda frame: frame["name"] == "Bagan"].iloc[0]
    explanation = explain_match(bagan, prefs)
    assert "nightlife" not in explanation
    assert "shopping" not in explanation


def test_requested_experience_intensity_changes_fit():
    df = load_destinations()
    seeks_nightlife = normalize_preferences({"nightlife": 5, "top_k": 10})
    avoids_nightlife = normalize_preferences({"nightlife": 1, "top_k": 10})
    seek_results, _ = recommend(df, seeks_nightlife)
    avoid_results, _ = recommend(df, avoids_nightlife)
    assert seek_results.iloc[0]["nightlife"] >= avoid_results.iloc[0]["nightlife"]


def test_match_score_is_cosine_similarity():
    df = load_destinations().loc[lambda frame: frame["country"] == "Myanmar"]
    prefs = normalize_preferences(
        {"culture": 5, "food": 4, "quiet": 3, "top_k": len(df)}
    )
    blocks = active_feature_blocks(prefs)
    expected = cosine_similarity(
        user_vector(prefs, blocks), destination_matrix(df, blocks, prefs)
    )[0]

    ranked, message = recommend(df, prefs)
    expected_by_name = dict(zip(df["name"], expected))

    assert message is None
    assert np.allclose(
        ranked["match_score"], ranked["name"].map(expected_by_name)
    )


def test_single_score_cosine_similarity_does_not_collapse_to_one():
    df = load_destinations()
    prefs = normalize_preferences({"nightlife": 5})
    ranked, _ = recommend(df, prefs, k=len(df))

    assert ranked["match_score"].nunique() > 1
    assert ranked.iloc[0]["nightlife"] == 5
    assert ranked.loc[ranked["nightlife"] == 1, "match_score"].max() < 1.0


def test_strict_ground_budget_uses_only_sufficient_evidence():
    df = load_destinations()
    prefs = normalize_preferences(
        {
            "country": "Myanmar",
            "trip_days": 5,
            "ground_budget_total": 200,
            "strict_budget": True,
            "top_k": 10,
        }
    )
    ranked, message = recommend(df, prefs)
    assert message is None
    assert set(ranked["name"]) == {"Bagan", "Mandalay", "Yangon"}
    assert set(ranked["cost_confidence"]) == {"Medium"}
    assert set(ranked["affordability_status"]) <= {
        "Comfortably within budget",
        "Within estimated budget",
    }


def test_changing_preferences_changes_ranking():
    df = load_destinations()
    quiet = normalize_preferences(
        {
            "place_type": "historical",
            "quiet": 5,
            "nightlife": 1,
            "culture": 5,
            "top_k": 5,
        }
    )
    party = normalize_preferences(
        {
            "place_type": "city",
            "quiet": 1,
            "nightlife": 5,
            "shopping": 5,
            "top_k": 5,
        }
    )
    quiet_names = list(recommend(df, quiet)[0]["name"])
    party_names = list(recommend(df, party)[0]["name"])
    assert quiet_names != party_names


def test_budget_label_keeps_level_and_shows_usd():
    text = budget_label("medium")
    assert text.startswith("Medium")
    assert "$60" in text
    assert "$150" in text


def test_south_asia_filter():
    df = load_destinations()
    prefs = normalize_preferences({"region": "south_asia"})
    filtered = hard_filter(df, prefs)
    assert set(filtered["region"]) == {"south_asia"}
    assert "Nepal" in set(filtered["country"])
    assert "Japan" not in set(filtered["country"])
