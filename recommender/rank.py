import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from recommender.encode import active_feature_blocks, destination_matrix, user_vector
from recommender.evidence import affordability_for_destination, daily_ground_budget
from recommender.filter import hard_filter


def recommend(df, prefs, k=None):
    top_k = k or prefs.get("top_k") or 5
    filtered = hard_filter(df, prefs)
    if filtered.empty:
        return filtered, "No destinations match those region and country filters."

    ranked = filtered.copy()
    blocks = active_feature_blocks(prefs)
    if blocks:
        destinations = destination_matrix(ranked, blocks, prefs)
        preference = user_vector(prefs, blocks)
        ranked["match_score"] = cosine_similarity(preference, destinations)[0]
    else:
        ranked["match_score"] = np.zeros(len(ranked), dtype=float)
    ranked["match_pct"] = (ranked["match_score"] * 100).round().astype(int)
    affordability = ranked["name"].map(
        lambda name: affordability_for_destination(name, prefs)
    )
    ranked["affordability_status"] = affordability.map(lambda item: item["status"])
    ranked["affordability_rank"] = affordability.map(lambda item: item["rank"])
    ranked["ground_spend_typical"] = affordability.map(
        lambda item: item["ground_spend_typical"]
    )
    ranked["cost_confidence"] = affordability.map(lambda item: item["confidence"])
    ranked["strict_budget_eligible"] = affordability.map(
        lambda item: item["strict_eligible"]
    )

    if prefs.get("strict_budget") and daily_ground_budget(prefs) is not None:
        ranked = ranked[ranked["strict_budget_eligible"]]
        if ranked.empty:
            return ranked.reset_index(drop=True), (
                "No destination with sourced cost evidence is currently within that "
                "ground-spending budget. Turn off strict budget mode to see preference "
                "matches with clear affordability warnings."
            )

    sort_columns = ["match_score", "name"]
    ascending = [False, True]
    if daily_ground_budget(prefs) is not None:
        sort_columns = ["affordability_rank", "match_score", "name"]
        ascending = [True, False, True]
    ranked = ranked.sort_values(sort_columns, ascending=ascending).head(top_k)
    return ranked.reset_index(drop=True), None
