import pandas as pd
import streamlit as st

from ai.chatbot import answer_question
from ai.client import has_api_key
from app_pages.auth_dialog import show_auth_dialog
from recommender.auth import is_trip_saved, remove_saved_trip, save_trip
from recommender.constants import BUDGET_GUIDE, REGIONS
from recommender.data import load_destinations
from recommender.evidence import (
    accommodations_for_destination,
    affordability_for_destination,
    costs_for_destination,
)
from recommender.explain import explain_match
from recommender.images import (
    destination_images,
    wikipedia_destination_images,
)

results = st.session_state.get("results")
prefs = st.session_state.get("preferences") or {}
selected = st.session_state.get("selected_destination")
user = st.session_state.get("user")

if results is None or (isinstance(results, pd.DataFrame) and results.empty):
    catalog = load_destinations()
    names = catalog["name"].tolist()
else:
    catalog = results
    names = results["name"].tolist()

if not names:
    st.info("Get recommendations first, then pick a destination.")
    st.stop()

default_index = 0
selected_name = None
if selected is not None:
    if isinstance(selected, dict):
        selected_name = selected.get("name")
    elif isinstance(selected, pd.Series):
        selected_name = selected.get("name") if hasattr(selected, "get") else selected["name"]
    elif isinstance(selected, str):
        selected_name = selected

if selected_name and selected_name in names:
    default_index = names.index(selected_name)

current_name = names[default_index]
is_saved = is_trip_saved(user["id"], current_name) if user else False

topbar = st.container(horizontal=True, vertical_alignment="bottom")
with topbar:
    choice = st.selectbox("Choose a destination", names, index=default_index)

    choice_row = catalog.loc[catalog["name"] == choice].iloc[0]
    choice_is_saved = is_trip_saved(user["id"], choice) if user else False
    if choice_is_saved:
        if st.button("Saved 🔖", key=f"guide_save_{choice}", help="Click to remove from saved trips"):
            remove_saved_trip(user["id"], choice)
            st.toast(f"Removed {choice} from saved trips.", icon="🗑️")
            st.rerun()
    else:
        if st.button("Save to My Trips 🔖", key=f"guide_save_{choice}"):
            if not user:
                show_auth_dialog("Sign in to save trips to your profile.")
            else:
                save_trip(user["id"], choice, choice_row["country"])
                st.toast(f"Saved {choice} to your trips!", icon="✨")
                st.rerun()

    if st.button("Back to matches", icon=":material/arrow_back:"):
        st.switch_page("app_pages/results.py")

row = catalog.loc[catalog["name"] == choice].iloc[0]
st.session_state.selected_destination = row.to_dict()
accommodation_records = accommodations_for_destination(row["name"])
cost_records = costs_for_destination(row["name"])
affordability = affordability_for_destination(row["name"], prefs)

if st.session_state.get("_chat_dest") != choice:
    st.session_state.chat_messages = []
    st.session_state._chat_dest = choice

photo = destination_images(
    ((row["name"], row["country"]),)
).get(row["name"], {})

visual, overview = st.columns((1.2, 1), vertical_alignment="center")
with visual:
    if photo:
        article_url = photo.get("article_url")

        if article_url:
            st.image(
                photo["image_url"],
                caption=f"[Source: {photo['source_label']}]({article_url})",
                width="stretch",
                link=article_url,
            )
        else:
            st.image(
                photo["image_url"],
                caption=f"Source: {photo['source_label']}",
                width="stretch",
            )
    else:
        st.info(
            "A verified destination photo is temporarily unavailable.",
            icon=":material/image_not_supported:",
        )
        if st.button("Retry photo", icon=":material/refresh:"):
            wikipedia_destination_images.clear()
            st.rerun()

with overview:
    st.badge(
        f"{int(row['match_pct'])}% preference fit"
        if "match_pct" in row
        else "Destination guide",
        icon=":material/auto_awesome:",
        color="green",
    )
    st.title(row["name"])
    st.caption(
        f":material/location_on: {row['country']} · "
        f"{REGIONS.get(row['region'], row['region'])}"
    )
    st.write(row["description"])
    st.markdown(
        f":green-badge[{str(row['place_type']).title()}] "
        f":blue-badge[{str(row['weather']).title()} weather]"
    )
    st.write(
        f"**Suggested stay:** {int(row['trip_days_min'])}–"
        f"{int(row['trip_days_max'])} days"
    )
    st.caption(explain_match(row, prefs))

st.subheader("Know before you go")
facts = st.columns(3)
with facts[0].container(border=True, height="stretch"):
    st.caption(":material/calendar_month: BEST TIME")
    st.write(row["best_months"])
with facts[1].container(border=True, height="stretch"):
    st.caption(":material/restaurant: LOCAL FOOD")
    st.write(row["local_food"])
with facts[2].container(border=True, height="stretch"):
    st.caption(":material/directions_bus: GETTING AROUND")
    st.write(row["transportation_info"])

details = st.columns(2, vertical_alignment="top")
with details[0].container(border=True):
    st.subheader("What to see", anchor=False)
    st.caption(":material/place: HIGHLIGHTS")
    st.write(row["attractions"])
    st.caption(":material/directions_walk: ACTIVITIES")
    st.write(row["activities"])
with details[1].container(border=True):
    st.subheader("Travel note", anchor=False)
    st.caption(":material/lightbulb: LOCAL TIP")
    st.write(row["travel_tips"])

with st.container(border=True):
    st.subheader("Budget evidence", anchor=False)
    if cost_records.empty:
        st.info(
            "Insufficient sourced cost evidence for this destination.",
            icon=":material/info:",
        )
    else:
        cost = cost_records.iloc[0]
        budget_summary, budget_source = st.columns(
            (1, 2),
            vertical_alignment="center",
        )
        with budget_summary:
            st.metric(
                "Typical ground spending",
                f"${float(cost['ground_spend_typical']):.0f} per person/day",
                help="Excludes flights and accommodation.",
            )
            st.write(f"**Budget status:** {affordability['status']}")
        with budget_source:
            st.caption(
                f"{cost['confidence']} confidence · {cost['evidence_scope']}: "
                f"{cost['evidence_location']} · collected {cost['collected_at']}"
            )
            st.caption(cost["source_method"])
            if cost["notes"]:
                st.caption(cost["notes"])
            st.link_button(
                "View cost source",
                cost["source_1_url"],
                icon=":material/open_in_new:",
            )

property_types = set(accommodation_records["property_type"]) if not accommodation_records.empty else set()
if property_types and property_types <= {"Hotel"}:
    accommodation_heading = "Hotels in or near this destination"
elif property_types and property_types <= {"Hotel", "Resort"}:
    accommodation_heading = "Hotels and resorts in or near this destination"
else:
    accommodation_heading = "Representative places to stay"
st.subheader(accommodation_heading)
st.caption(
    "These are representative properties, not a claim of room availability. "
    "Use the official property link to check current operation, prices, and rooms."
)
if accommodation_records.empty:
    st.info(
        "No verified representative hotel has been added for this destination yet.",
        icon=":material/fact_check:",
    )
else:
    accommodation_columns = st.columns(len(accommodation_records))
    for column, (_, accommodation) in zip(
        accommodation_columns, accommodation_records.iterrows()
    ):
        with column.container(border=True, height="stretch"):
            st.subheader(accommodation["property_name"], anchor=False)
            st.caption(
                f"{accommodation['property_type']} · base: "
                f"{accommodation['recommended_base']}"
            )
            st.write(accommodation["location"])
            if accommodation.get("distance_km", "") != "":
                st.caption(
                    f"Approx. {float(accommodation['distance_km']):.1f} km from "
                    "the selected base"
                )
            st.write(
                f"**Evidence:** {accommodation['confidence']} confidence · "
                f"reviewed {accommodation['verified_at']}"
            )
            st.caption(accommodation["source_type"])
            link = accommodation["official_url"] or accommodation["source_url"]
            st.link_button(
                "View property source",
                link,
                icon=":material/open_in_new:",
                width="stretch",
            )

    if accommodation_records["data_license"].str.contains(
        "OpenStreetMap", case=False, na=False
    ).any():
        st.caption(
            "[OpenStreetMap data © contributors (ODbL)]"
            "(https://www.openstreetmap.org/copyright)"
        )

st.caption(BUDGET_GUIDE)

st.subheader("Ask TripSense AI Concierge")
st.caption(
    "Get realistic travel advice, custom itineraries, local tips, and practical logistics tailored to your journey."
)

if not user:
    with st.container(border=True):
        st.info(
            "The TripSense AI Concierge is available exclusively for registered members. "
            "Sign in or create a free account to ask questions, design custom itineraries, and get personalized local tips.",
            icon=":material/lock:",
        )
        col_auth1, col_auth2 = st.columns([1, 2])
        with col_auth1:
            if st.button("Sign In / Register to Chat", type="primary", icon=":material/login:", width="stretch", key="chat_auth_btn"):
                show_auth_dialog("Sign in or create an account to use the AI Concierge.")
else:
    if not has_api_key():
        st.info(
            "No OpenRouter key found. Answers will use the destination catalog only.",
            icon=":material/database:",
        )

    suggestions = {
        "🗺️ 3-Day Itinerary": "Can you design a realistic 3-day itinerary for this destination with morning, afternoon, and evening highlights and crowd tips?",
        "🍜 Best Foods & Markets": "What are the must-try local dishes and signature food streets or night markets to visit here?",
        "🏨 Neighborhoods & Hotels": "Which areas or neighborhoods are best to stay in across different budgets, and what is the typical accommodation cost?",
        "💡 Local Etiquette & Hacks": "What are essential cultural etiquette rules, scams to avoid, and local insider tips for travelers here?",
        "🚇 Getting Around & Apps": "What are the most convenient transportation options and local mobile apps (e.g. ride-hailing, transit cards) to use?",
    }

    if not st.session_state.chat_messages:
        picked = st.pills("Try asking", list(suggestions.keys()), key="chat_suggestions")
        if picked:
            st.session_state.chat_messages.append(
                {"role": "user", "content": suggestions[picked]}
            )
            st.rerun()

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("Ask about this destination", submit_mode="disable")
    if prompt:
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        st.rerun()

    if st.session_state.chat_messages and st.session_state.chat_messages[-1]["role"] == "user":
        question = st.session_state.chat_messages[-1]["content"]
        history = st.session_state.chat_messages[:-1]
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = answer_question(question, row, prefs, history)
            st.write(reply)
        st.session_state.chat_messages.append({"role": "assistant", "content": reply})
