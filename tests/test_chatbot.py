from ai.chatbot import fallback_answer


FACTS = {
    "name": "Kyoto",
    "country": "Japan",
    "region": "east_asia",
    "budget": "medium",
    "place_type": "historical",
    "weather": "cool",
    "trip_days_min": 4,
    "trip_days_max": 6,
    "culture": 5,
    "food": 5,
    "nature": 4,
    "nightlife": 2,
    "shopping": 3,
    "quiet": 4,
    "adventure": 2,
    "transport": 5,
    "description": "A historical city.",
    "best_months": "March to May",
    "attractions": "Fushimi Inari; Kiyomizu-dera",
    "local_food": "Kaiseki; yudofu; matcha desserts",
    "transportation_info": "Buses and trains cover the city.",
    "activities": "Temple visits",
    "travel_tips": "Popular gates are crowded early.",
}


def test_food_uses_database():
    answer = fallback_answer("What food should I try?", FACTS, "why")
    assert "Kaiseki" in answer


def test_live_price_does_not_guess():
    answer = fallback_answer("How much is a hotel tonight?", FACTS, "why")
    assert "not stored" in answer.lower()
    assert "tonight" not in answer.lower()
    assert "$" not in answer


def test_why_uses_explanation():
    answer = fallback_answer("Why did you recommend this?", FACTS, "Kyoto fits because it is historical.")
    assert "historical" in answer
