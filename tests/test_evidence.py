from recommender.evidence import (
    accommodations_for_destination,
    affordability_for_destination,
    costs_for_destination,
    load_accommodations,
    load_destination_costs,
)
from recommender.data import load_destinations


def test_accommodations_cover_the_full_destination_catalog():
    expected = set(load_destinations()["name"])
    stays = load_accommodations()
    assert set(stays["destination"]) == expected
    assert stays.groupby("destination").size().between(1, 2).all()
    assert stays["source_url"].str.startswith("https://").all()
    assert stays["verified_at"].str.match(r"\d{4}-\d{2}-\d{2}").all()
    assert stays["property_name"].str.strip().ne("").all()
    assert not stays.assign(
        normalized_name=stays["property_name"].str.strip().str.casefold()
    ).duplicated(["destination", "normalized_name"]).any()


def test_openstreetmap_records_include_license_and_cautious_source_language():
    stays = load_accommodations()
    osm = stays[stays["source_url"].str.contains("openstreetmap.org", na=False)]
    assert not osm.empty
    assert osm["data_license"].str.contains("ODbL", na=False).all()
    assert osm["source_type"].str.contains(
        "operation not independently verified", case=False, na=False
    ).all()


def test_evidence_lookup_handles_catalog_and_unknown_destinations():
    assert accommodations_for_destination("Not a real catalog destination").empty
    assert costs_for_destination("Not a real catalog destination").empty
    assert not costs_for_destination("Tokyo").empty


def test_cost_evidence_covers_catalog_with_traceable_scope_and_formula():
    expected = set(load_destinations()["name"])
    costs = load_destination_costs()
    assert set(costs["destination"]) == expected
    assert costs.groupby("destination").size().eq(1).all()
    assert costs["source_1_url"].str.startswith("https://").all()
    assert costs["collected_at"].str.match(r"\d{4}-\d{2}-\d{2}").all()
    assert set(costs["evidence_scope"]) <= {
        "Destination",
        "Nearby base proxy",
        "Country proxy",
    }
    assert costs["evidence_location"].str.strip().ne("").all()
    derived = costs["reported_daily_total"].astype(float) - costs[
        "accommodation_typical"
    ].astype(float)
    assert (derived.round(2) == costs["ground_spend_typical"].astype(float)).all()


def test_affordability_uses_total_budget_divided_by_days():
    result = affordability_for_destination(
        "Yangon", {"ground_budget_total": 200, "trip_days": 5}
    )
    assert result["daily_budget"] == 40
    assert result["status"] == "Within estimated budget"


def test_affordability_uses_new_destination_evidence():
    result = affordability_for_destination(
        "Tokyo", {"ground_budget_total": 500, "trip_days": 5}
    )
    assert result["ground_spend_typical"] == 103
    assert result["status"] == "Stretch budget"
