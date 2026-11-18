import streamlit as st

from app_pages.auth_dialog import show_auth_dialog
from recommender.auth import get_saved_trips, remove_saved_trip
from recommender.constants import budget_label
from recommender.data import load_destinations
from recommender.images import destination_images

user = st.session_state.get("user")

with st.container(horizontal_alignment="center"):
    st.badge(
        "TripSense AI · Personal Travel Bookmarks",
        icon=":material/bookmark:",
        color="green",
    )
    st.title("Saved Trips", text_alignment="center")
    st.write("Keep track of your dream destinations and revisit their guides anytime.")

if not user:
    st.info(
        "You are currently browsing as a guest. Sign in or create an account to view and manage your saved destinations.",
        icon=":material/account_circle:",
    )
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Sign In / Register", type="primary", icon=":material/login:", width="stretch"):
            show_auth_dialog("Sign in to access your saved trips.")
    with col2:
        if st.button("Discover Destinations", icon=":material/travel_explore:", width="stretch"):
            st.switch_page("app_pages/home.py")
    st.stop()

saved_records = get_saved_trips(user["id"]) if user else []

if not saved_records:
    st.space("medium")
    st.info(
        "You haven't saved any trips yet! Explore destinations and click the bookmark button to collect places you love.",
        icon=":material/bookmark_border:",
    )
    if st.button("Discover Destinations", type="primary", icon=":material/travel_explore:"):
        st.switch_page("app_pages/home.py")
    st.stop()

st.write(f"You have **{len(saved_records)}** saved destination(s).")
st.space("small")

df_all = load_destinations()
dest_dict = {row["name"]: row for _, row in df_all.iterrows()}

requests = tuple((item["destination_name"], item["country"]) for item in saved_records)
photos = destination_images(requests)

for item in saved_records:
    name = item["destination_name"]
    country = item["country"]
    saved_at = item.get("saved_at", "")
    dest_row = dest_dict.get(name)

    with st.container(border=True):
        col_img, col_info, col_actions = st.columns([1.2, 2.3, 1], vertical_alignment="center")

        with col_img:
            photo = photos.get(name)
            if photo and photo.get("url"):
                st.image(photo["url"], use_container_width=True)
            else:
                st.info("No preview available", icon=":material/image:")

        with col_info:
            st.subheader(name)
            st.caption(f":material/public: {country}")
            if dest_row is not None:
                style_tag = str(dest_row["place_type"]).title()
                budget_tag = budget_label(dest_row["budget"])
                weather_tag = str(dest_row["weather"]).title()
                st.write(f"Style: **{style_tag}** · Budget: **{budget_tag}** · Weather: **{weather_tag}**")
                st.write(dest_row["description"][:160] + "..." if len(dest_row["description"]) > 160 else dest_row["description"])
            if saved_at:
                st.caption(f"Saved on {saved_at[:10]}")

        with col_actions:
            if st.button("View Guide", key=f"guide_{name}", icon=":material/arrow_forward:", width="stretch", type="primary"):
                if dest_row is not None:
                    st.session_state.selected_destination = dest_row.to_dict()
                else:
                    st.session_state.selected_destination = df_all.loc[df_all["name"] == name].iloc[0].to_dict()
                st.switch_page("app_pages/destination.py")

            if st.button("Remove", key=f"remove_{name}", icon=":material/delete:", width="stretch"):
                remove_saved_trip(user["id"], name)
                st.toast(f"Removed {name} from your saved trips.", icon="🗑️")
                st.rerun()
