from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

import streamlit as st

from app_pages.auth_dialog import show_auth_dialog
from recommender.auth import (
    delete_user_session,
    get_saved_trips_count,
    get_user_by_session,
)

st.set_page_config(
    page_title="TripSense AI | Thoughtful Asian Travel",
    page_icon="🧭",
    layout="wide",
)

st.html(
    """
    <style>
      /* Global fonts and user-friendly clean styling */
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

      html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      }

      /* Card styling */
      div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px;
        border-color: rgba(22, 101, 52, 0.12);
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04);
        transition: box-shadow 0.2s ease;
      }

      div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 8px 30px -4px rgba(0, 0, 0, 0.08);
      }

      /* Destination photo styling */
      div[data-testid="stImage"] img {
        aspect-ratio: 16 / 9;
        object-fit: cover;
        border-radius: 14px;
      }

      /* Header styling */
      .tripsense-nav-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 800;
        font-size: 1.35rem;
        color: #1b4332;
        letter-spacing: -0.02em;
        text-decoration: none;
      }

      .tripsense-nav-brand span.dot {
        color: #e76f51;
      }

      .tripsense-user-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.92rem;
        color: #2d3748;
        font-weight: 500;
      }
    </style>
    """
)

st.session_state.setdefault("user", None)
st.session_state.setdefault("pending_prefs", None)
st.session_state.setdefault("preferences", None)
st.session_state.setdefault("results", None)
st.session_state.setdefault("filter_message", None)
st.session_state.setdefault("selected_destination", None)
st.session_state.setdefault("chat_messages", [])
st.session_state.setdefault("parsed_preview", None)

# Restore session across browser page refresh (F5)
if not st.session_state.get("user"):
    session_token = st.query_params.get("session")
    if session_token:
        restored_user = get_user_by_session(session_token)
        if restored_user:
            st.session_state.user = restored_user
        else:
            if "session" in st.query_params:
                del st.query_params["session"]

user = st.session_state.get("user")
saved_count = get_saved_trips_count(user["id"]) if user else 0

# Top navigation bar
nav_col1, nav_col2 = st.columns([1.5, 2.5], vertical_alignment="center")

with nav_col1:
    st.markdown(
        """
        <div class="tripsense-nav-brand">
          🧭 TripSense AI<span class="dot">.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav_col2:
    if user:
        u_col1, u_col2, u_col3 = st.columns([1.8, 1.2, 0.8], vertical_alignment="center")
        with u_col1:
            st.markdown(
                f"<div class='tripsense-user-pill'>👋 Hi, <b>{user['full_name']}</b></div>",
                unsafe_allow_html=True,
            )
        with u_col2:
            if st.button(f"🔖 Saved trips ({saved_count})", key="nav_saved_trips_btn", width="stretch"):
                st.switch_page("app_pages/saved_trips.py")
        with u_col3:
            if st.button("Logout", key="nav_logout_btn", width="stretch"):
                active_token = st.query_params.get("session")
                if active_token:
                    delete_user_session(active_token)
                if "session" in st.query_params:
                    del st.query_params["session"]
                st.session_state.user = None
                st.toast("You have logged out.", icon="👋")
                st.rerun()
    else:
        st_col1, st_col2 = st.columns([2, 1], vertical_alignment="center")
        with st_col1:
            st.caption("Browse freely · Sign in to save & view matches")
        with st_col2:
            if st.button("Sign In / Register", type="secondary", icon=":material/login:", key="nav_login_btn", width="stretch"):
                show_auth_dialog()

st.divider()

page = st.navigation(
    [
        st.Page("app_pages/home.py", title="Discover", icon=":material/travel_explore:"),
        st.Page("app_pages/results.py", title="Your matches", icon=":material/auto_awesome:"),
        st.Page("app_pages/destination.py", title="Destination guide", icon=":material/map:"),
        st.Page("app_pages/saved_trips.py", title="Saved trips", icon=":material/bookmark:"),
    ],
    position="top",
)
page.run()
