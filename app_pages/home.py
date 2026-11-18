import streamlit as st

from ai.client import has_api_key
from ai.parser import parse_preference_text
from app_pages.auth_dialog import show_auth_dialog
try:
    from recommender.constants import (
        BUDGET_GUIDE,
        COUNTRIES,
        PLACE_TYPES,
        REGION_COUNTRIES,
        REGIONS,
        WEATHERS,
    )
except ImportError:
    from recommender.constants import (
        BUDGET_GUIDE,
        COUNTRIES,
        PLACE_TYPES,
        REGIONS,
        WEATHERS,
    )
    REGION_COUNTRIES = {
        "southeast_asia": [
            "Brunei", "Cambodia", "Indonesia", "Laos", "Malaysia", "Myanmar",
            "Philippines", "Singapore", "Thailand", "Timor-Leste", "Vietnam",
        ],
        "east_asia": [
            "China", "Hong Kong", "Japan", "Macau", "Mongolia", "South Korea", "Taiwan",
        ],
        "south_asia": [
            "Bangladesh", "Bhutan", "India", "Maldives", "Nepal", "Sri Lanka",
        ],
        "central_asia": [
            "Georgia", "Kazakhstan", "Kyrgyzstan", "Tajikistan", "Turkmenistan", "Uzbekistan",
        ],
    }
from recommender.data import load_destinations
from recommender.prefs import normalize_preferences
from recommender.rank import recommend

def run_search(prefs):
    df = load_destinations()
    results, message = recommend(df, prefs)
    st.session_state.preferences = prefs
    st.session_state.results = results
    st.session_state.filter_message = message
    st.session_state.selected_destination = None
    st.session_state.chat_messages = []
    st.session_state.parsed_preview = prefs.get("_parsed")
    st.switch_page("app_pages/results.py")

# Auto-resume search if user just authenticated with pending preferences
if st.session_state.get("user") and st.session_state.get("pending_prefs"):
    pending = st.session_state.pop("pending_prefs")
    run_search(pending)

with st.container(horizontal_alignment="center"):
    st.badge(
        "THOUGHTFUL TRIPS, MATCHED TO YOU",
        icon=":material/auto_awesome:",
        color="green",
    )
    st.markdown(
        """
        <div style="text-align: center; margin-top: 6px; margin-bottom: 8px;">
          <h1 style="font-size: 2.75rem; font-weight: 800; color: #1b4332; line-height: 1.15; margin-bottom: 12px;">
            Asia is calling.<br>
            <span style="position: relative; display: inline-block;">
              Where will you go?
              <svg style="position: absolute; bottom: -8px; left: 0; width: 100%; height: 10px;" viewBox="0 0 200 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M2 9.5C55 3 145 2 198 8" stroke="#E76F51" stroke-width="4" stroke-linecap="round"/>
              </svg>
            </span>
          </h1>
          <p style="font-size: 1.12rem; color: #4a5568; max-width: 650px; margin: 0 auto; line-height: 1.6;">
            Tell us what makes a trip unforgettable. TripSense AI turns your travel style
            into destination ideas that feel unmistakably yours.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.space("small")
st.caption("START YOUR JOURNEY")
st.subheader("What does your ideal escape look like?")

mode = st.segmented_control(
    "How do you want to start?",
    options=["Choose preferences", "Describe your dream trip"],
    default="Choose preferences",
    required=True,
    key="input_mode",
    width="stretch",
)

if mode == "Choose preferences":
    with st.container(border=True):
        st.caption("THE ESSENTIALS")
        basics = st.container(horizontal=True)
        with basics:
            region = st.selectbox(
                "Region",
                ["Any"] + list(REGIONS.values()),
                key="pref_region",
            )
            region_map = {label: key for key, label in REGIONS.items()}
            selected_region_key = region_map.get(region)
            if selected_region_key and selected_region_key in REGION_COUNTRIES:
                available_countries = ["Any"] + REGION_COUNTRIES[selected_region_key]
            else:
                available_countries = ["Any"] + COUNTRIES

            current_country = st.session_state.get("pref_country", "Any")
            country_index = (
                available_countries.index(current_country)
                if current_country in available_countries
                else 0
            )
            country = st.selectbox(
                "Country",
                available_countries,
                index=country_index,
                key="pref_country",
            )
            top_k = st.selectbox("How many results", [5, 8, 10], index=0, key="pref_top_k")
        details = st.container(horizontal=True)
        with details:
            place_type = st.selectbox(
                "Place style",
                ["Any"] + [item.title() for item in PLACE_TYPES],
                key="pref_place_type",
            )
            weather = st.selectbox(
                "Weather",
                ["Any"] + [item.title() for item in WEATHERS],
                key="pref_weather",
            )
            transportation = st.selectbox(
                "Transportation",
                ["Any", "Public transport", "Taxi", "Rental", "Walking"],
                key="pref_transportation",
            )
        st.caption("SPENDING PLAN")
        st.write("Accommodation and flights are intentionally handled separately.")
        extras = st.container(horizontal=True)
        with extras:
            trip_days = st.number_input(
                "Trip length (days)", min_value=0, max_value=30, value=0, key="pref_trip_days"
            )
            ground_budget_total = st.number_input(
                "On-trip spending budget (USD)",
                min_value=0,
                max_value=100000,
                value=0,
                step=50,
                key="pref_ground_budget_total",
                help="Total per-person budget for meals, local transport, attractions, and ordinary spending. Flights and accommodation are excluded.",
            )
            strict_budget = st.checkbox(
                "Only show verified within-budget places",
                key="pref_strict_budget",
                help="Destinations without sourced cost evidence will be excluded. Leave this off while evidence coverage is still growing.",
            )

        st.caption("FINE-TUNE YOUR MATCH")
        st.subheader("How much of each experience do you want?")
        st.caption("0 means no preference, 1 means avoid it, and 5 means seek it strongly.")
        scores = st.container(horizontal=True)
        with scores:
            culture = st.slider("Culture", 0, 5, 0, key="pref_culture")
            food = st.slider("Local food", 0, 5, 0, key="pref_food")
            nature = st.slider("Nature", 0, 5, 0, key="pref_nature")
            nightlife = st.slider("Nightlife", 0, 5, 0, key="pref_nightlife")
        scores2 = st.container(horizontal=True)
        with scores2:
            shopping = st.slider("Shopping", 0, 5, 0, key="pref_shopping")
            quiet = st.slider("Peace and quiet", 0, 5, 0, key="pref_quiet")
            adventure = st.slider("Adventure", 0, 5, 0, key="pref_adventure")

        submitted = st.button(
            "Find my destinations",
            type="primary",
            icon=":material/arrow_forward:",
            width="stretch",
            key="find_dest_btn",
        )

    st.caption(BUDGET_GUIDE)

    if submitted:
        transport_map = {
            "Public transport": "public",
            "Taxi": "taxi",
            "Rental": "rental",
            "Walking": "walking",
        }
        region_map = {label: key for key, label in REGIONS.items()}
        raw = {
            "region": region_map.get(region),
            "country": None if country == "Any" else country,
            "place_type": None if place_type == "Any" else place_type.lower(),
            "weather": None if weather == "Any" else weather.lower(),
            "transportation": transport_map.get(transportation),
            "culture": culture,
            "food": food,
            "nature": nature,
            "nightlife": nightlife,
            "shopping": shopping,
            "quiet": quiet,
            "adventure": adventure,
            "trip_days": trip_days or None,
            "ground_budget_total": ground_budget_total or None,
            "strict_budget": strict_budget,
            "top_k": top_k,
        }
        if ground_budget_total and not trip_days:
            st.error("Add your trip length so the system can calculate a daily budget.")
        else:
            prefs = normalize_preferences(raw)
            if not st.session_state.get("user"):
                st.session_state.pending_prefs = prefs
                show_auth_dialog("Sign in or create an account to view your personalized destination matches.")
            else:
                run_search(prefs)

else:
    st.caption("DESCRIBE IT YOUR WAY")
    st.write(
        "Mention your budget, mood, favorite activities, ideal weather, or anything "
        "you would rather avoid."
    )
    if not has_api_key():
        st.warning(
            "Add an OpenRouter key in `.env` or Streamlit secrets to use this mode. "
            "The preference planner still works.",
            icon=":material/key:",
        )
    text = st.text_area(
        "Describe your trip",
        placeholder="I have $400 for five days, excluding flights and hotels. I want a quiet historical place with local food.",
        height=180,
    )
    if st.button(
        "Find my destinations",
        type="primary",
        icon=":material/auto_awesome:",
        width="stretch",
    ):
        try:
            with st.spinner("Reading your preferences..."):
                prefs = parse_preference_text(text)
            prefs["top_k"] = 5
            if not st.session_state.get("user"):
                st.session_state.pending_prefs = prefs
                show_auth_dialog("Sign in or create an account to view your personalized destination matches.")
            else:
                run_search(prefs)
        except Exception as error:
            st.error(str(error), icon=":material/error:")

st.space("small")
with st.container(horizontal=True, horizontal_alignment="distribute"):
    st.caption(":material/public: 30 countries")
    st.caption(":material/location_on: 160 destinations")
    st.caption(":material/verified: 12 sourced stays · 3 cost estimates")
