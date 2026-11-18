from ai.client import chat_complete, has_api_key
from recommender.constants import BUDGET_GUIDE
from recommender.evidence import accommodations_for_destination, costs_for_destination
from recommender.explain import explain_match

LIVE_WORDS = [
    "hotel price",
    "flight",
    "train price",
    "ticket price",
    "opening hour",
    "open today",
    "visa",
    "safety alert",
    "live weather",
    "weather now",
    "weather today",
    "current price",
    "how much is a hotel",
    "tonight",
]


def destination_facts(row):
    accommodations = accommodations_for_destination(row["name"])
    costs = costs_for_destination(row["name"])
    ground_spend = None if costs.empty else float(costs.iloc[0]["ground_spend_typical"])
    return {
        "name": row["name"],
        "country": row["country"],
        "region": row["region"],
        "budget": row["budget"],
        "place_type": row["place_type"],
        "weather": row["weather"],
        "trip_days_min": int(row["trip_days_min"]),
        "trip_days_max": int(row["trip_days_max"]),
        "culture": int(row["culture"]),
        "food": int(row["food"]),
        "nature": int(row["nature"]),
        "nightlife": int(row["nightlife"]),
        "shopping": int(row["shopping"]),
        "quiet": int(row["quiet"]),
        "adventure": int(row["adventure"]),
        "transport": int(row["transport"]),
        "description": row["description"],
        "best_months": row["best_months"],
        "attractions": row["attractions"],
        "local_food": row["local_food"],
        "transportation_info": row["transportation_info"],
        "activities": row["activities"],
        "travel_tips": row["travel_tips"],
        "representative_accommodations": accommodations["property_name"].tolist(),
        "ground_spend_typical": ground_spend,
    }


def answer_question(question, row, prefs=None, history=None):
    question = (question or "").strip()
    if not question:
        return "Ask a question about this destination."
    facts = destination_facts(row)
    why = explain_match(row, prefs or {})
    if has_api_key():
        try:
            return _llm_answer(question, facts, why, history)
        except Exception:
            return fallback_answer(question, facts, why)
    return fallback_answer(question, facts, why)


def fallback_answer(question, facts, why):
    q = question.lower()
    if any(word in q for word in LIVE_WORDS) or ("price" in q and "hotel" in q):
        hotel_note = ""
        representative_stays = facts.get("representative_accommodations", [])
        if representative_stays:
            hotel_note = (
                " Representative properties in the evidence catalog: "
                + ", ".join(representative_stays)
                + ". Use their source links on this page to check current operation and rooms."
            )
        return (
            "Live hotel prices, flights, visas, and current weather are not stored in this project. "
            f"It is a {facts['place_type']} place. A typical stay is "
            f"{facts['trip_days_min']} to {facts['trip_days_max']} days. "
            f"Best months in our data: {facts['best_months']}."
            f"{hotel_note}"
        )
    if any(word in q for word in ["budget", "cost", "expensive", "cheap", "dollar", "usd", "how much"]):
        if facts.get("ground_spend_typical") is None:
            return (
                f"There is not yet enough sourced ground-spending evidence for "
                f"{facts['name']}. Flights and accommodation are handled separately, "
                "and the system will not guess a daily cost."
            )
        return (
            f"The sourced typical ground-spending estimate for {facts['name']} is "
            f"about ${facts['ground_spend_typical']:.0f} per person per day, excluding "
            f"flights and accommodation. {BUDGET_GUIDE}"
        )
    if any(word in q for word in ["why", "recommend", "match", "fit"]):
        return why
    if any(word in q for word in ["food", "eat", "dish", "cuisine"]):
        return f"In {facts['name']}, try: {facts['local_food']}."
    if any(word in q for word in ["attraction", "see", "visit", "temple", "do there"]):
        return f"Popular attractions: {facts['attractions']}."
    if any(word in q for word in ["day", "how long", "stay"]):
        return (
            f"The system suggests {facts['trip_days_min']} to {facts['trip_days_max']} days "
            f"in {facts['name']}."
        )
    if any(word in q for word in ["clothes", "pack", "wear", "weather"]):
        return (
            f"The system describes typical weather as {facts['weather']}. "
            "Pack for that climate and for walking. "
            "This is general travel advice, not live weather."
        )
    if any(word in q for word in ["transport", "get around", "train", "bus"]):
        return facts["transportation_info"]
    if any(word in q for word in ["tip", "advice", "should i"]):
        return facts["travel_tips"]
    if any(word in q for word in ["honeymoon", "romantic", "couple"]):
        return (
            f"{facts['name']} has quiet {facts['quiet']}/5, culture {facts['culture']}/5, "
            f"and nature {facts['nature']}/5. "
            "That can work for a calm cultural trip, even if we do not have a honeymoon field."
        )
    return (
        f"{facts['name']} is in {facts['country']}. {facts['description']} "
        f"Best months: {facts['best_months']}. "
        f"If you ask about food, attractions, days, or transport, I can use the database."
    )


def _llm_answer(question, facts, why, history):
    dest_name = facts.get("name", "this destination")
    country = facts.get("country", "")
    region = facts.get("region", "")
    ground_spend = facts.get("ground_spend_typical")
    spend_str = (
        f"approx ${ground_spend:.0f} per person/day (for meals, local transport, entrance fees, excluding flights & accommodation)"
        if ground_spend
        else "moderate local spending"
    )
    accommodations = ", ".join(facts.get("representative_accommodations", []))

    system = f"""You are TripSense AI's Expert Travel Concierge and Local Insider for {dest_name}, {country} ({region}).
Your role is to give travelers real-world, practical, up-to-date, and inspiring advice as an experienced local guide.

DESTINATION CONTEXT:
- Destination: {dest_name}, {country}
- Experience Style: {facts.get('place_type', '').title()} | Climate: {facts.get('weather', '').title()}
- Recommended Length of Stay: {facts.get('trip_days_min', 3)} to {facts.get('trip_days_max', 7)} days
- Best Travel Window: {facts.get('best_months', '')}
- Typical Daily On-Trip Spend: {spend_str}
- Signature Local Dishes: {facts.get('local_food', '')}
- Key Landmarks: {facts.get('attractions', '')}
- Primary Local Transport: {facts.get('transportation_info', '')}
- Recommended Stays: {accommodations or 'Local guesthouses, boutique hotels, and resorts'}
- Travel Fit: {why}

STRICT CONVERSATIONAL GUIDELINES:
1. NEVER speak like a computer system. DO NOT say "based on stored facts", "in the project database", "our database indicates", or "not available in the catalog". Speak 100% naturally, warmly, and authoritatively as a seasoned travel advisor.
2. Address Modern Apps & Real-World Reality Accurately:
   - If modern services like ride-hailing apps (Grab/Gojek/Uber) or smart transit cards do NOT operate in this destination (e.g. in Bagan, Inle Lake, or rural spots), explain that as a real-world travel fact (e.g., "In Bagan, app-based ride-hailing like Grab does not operate. Instead, the absolute best and most flexible way to explore is by renting an electric bike (e-bike)...").
   - If modern apps DO operate in the destination (e.g. Bangkok, Singapore, Tokyo, Kuala Lumpur, Seoul), name the exact apps to download (Grab, Gojek, Kakao T, Suica/Pasmo, Navitime, etc.).
3. Practical, Realistic Advice:
   - Itineraries: Give clear morning, afternoon, and evening breakdowns with crowd-beating tips.
   - Neighborhoods: Describe distinct vibes and realistic price ranges ($15-35 budget, $40-80 mid-range, $100+ luxury).
   - Food: Recommend specific markets, dish names, and food streets.
   - Cash & Payments: Clearly explain cash-reliance vs card acceptance and local currency tips.
4. Presentation: Use clean markdown with clear headers, bullet points, and bold text for effortless reading.
"""
    messages = [{"role": "system", "content": system}]
    for item in history or []:
        messages.append({"role": item["role"], "content": item["content"]})
    messages.append({"role": "user", "content": question})
    return chat_complete(messages, temperature=0.35)
