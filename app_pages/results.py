import streamlit as st

from app_pages.auth_dialog import show_auth_dialog
from recommender.auth import is_trip_saved, remove_saved_trip, save_trip
from recommender.constants import BUDGET_GUIDE, REGIONS
from recommender.evidence import daily_ground_budget
from recommender.explain import explain_match
from recommender.images import (
    destination_images,
    wikipedia_destination_images,
)

with st.container(horizontal_alignment="center"):
    st.badge(
        "Curated for your travel style",
        icon=":material/auto_awesome:",
        color="green",
    )
    st.title("Your best matches", text_alignment="center")
    st.write(
        "A personalized list of places that balance your budget, interests, and preferred pace."
    )

results = st.session_state.get("results")
prefs = st.session_state.get("preferences")
message = st.session_state.get("filter_message")
user = st.session_state.get("user")

if results is None or prefs is None or results.empty:
    if results is None or prefs is None:
        st.info("Start on Discover to create your recommendations.", icon=":material/info:")
        if st.button("Plan a trip", icon=":material/arrow_back:"):
            st.switch_page("app_pages/home.py")
    elif message:
        st.warning(message, icon=":material/search_off:")
        if st.button("Adjust preferences", icon=":material/tune:"):
            st.switch_page("app_pages/home.py")
    elif results.empty:
        st.warning("No destinations matched. Try broader filters.", icon=":material/search_off:")
    st.stop()
else:
    parsed = st.session_state.get("parsed_preview")
    if parsed:
        with st.expander(
            "What we understood from your description", icon=":material/psychology:"
        ):
            st.json(parsed)

    photo_requests = tuple(
        (row["name"], row["country"]) for _, row in results.iterrows()
    )
    photos = destination_images(photo_requests)
    missing_photos = [name for name, _country in photo_requests if name not in photos]
    if missing_photos:
        photo_notice = st.container(horizontal=True, vertical_alignment="center")
        with photo_notice:
            st.caption(
                f"Live photos are temporarily unavailable for {len(missing_photos)} "
                "destination(s). No artificial images are shown."
            )
            if st.button("Retry photos", icon=":material/refresh:"):
                wikipedia_destination_images.clear()
                st.rerun()

    st.caption(
        f"{len(results)} recommendations · Preference fit uses multi-criteria weighted scoring after "
        "region, country, and optional strict affordability filters."
    )
    user_daily_budget = daily_ground_budget(prefs)
    if user_daily_budget is not None:
        st.caption(
            f"Your ground-spending budget: ${user_daily_budget:.2f} per person/day · "
            "flights and accommodation excluded."
        )
    requested_count = int(prefs.get("top_k") or 5)
    if len(results) < requested_count:
        st.info(
            f"Only {len(results)} destinations satisfy the hard filters; "
            f"you requested {requested_count}. They are still ordered by preference fit.",
            icon=":material/info:",
        )

    for start in range(0, len(results), 2):
        columns = st.columns(2)
        for offset, column in enumerate(columns):
            position = start + offset
            if position >= len(results):
                continue
            row = results.iloc[position]
            photo = photos.get(row["name"], {})
            is_saved = is_trip_saved(user["id"], row["name"]) if user else False

            with column.container(border=True, height="stretch"):
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
                heading = st.container(horizontal=True, vertical_alignment="center")
                with heading:
                    st.subheader(f"{position + 1}. {row['name']}")
                    st.badge(f"{int(row['match_pct'])}% preference fit", color="green")
                st.caption(
                    f":material/location_on: {row['country']} · "
                    f"{REGIONS.get(row['region'], row['region'])}"
                )
                st.write(row["description"])
                st.markdown(
                    f":green-badge[{str(row['place_type']).title()}] "
                    f":blue-badge[{str(row['weather']).title()}]"
                )
                status = row.get("affordability_status", "Budget not provided")
                typical = row.get("ground_spend_typical")
                if typical is not None and typical == typical:
                    st.write(
                        f"**Ground spending:** about ${float(typical):.0f}/day · {status} "
                        f"· {row.get('cost_confidence') or 'Unknown'} confidence"
                    )
                elif user_daily_budget is not None:
                    st.write(f"**Ground spending:** {status}")
                metrics = st.container(horizontal=True)
                with metrics:
                    st.metric("Culture", f"{int(row['culture'])}/5", border=True)
                    st.metric("Food", f"{int(row['food'])}/5", border=True)
                    st.metric(
                        "Stay",
                        f"{int(row['trip_days_min'])}–{int(row['trip_days_max'])} days",
                        border=True,
                    )
                st.caption(explain_match(row, prefs))

                # Action buttons: Save trip & Explore guide
                action_col1, action_col2 = st.columns([1, 1.2])
                with action_col1:
                    if is_saved:
                        if st.button("Saved 🔖", key=f"save_{row['name']}", width="stretch", help="Click to remove from saved trips"):
                            remove_saved_trip(user["id"], row["name"])
                            st.toast(f"Removed {row['name']} from saved trips.", icon="🗑️")
                            st.rerun()
                    else:
                        if st.button("Save trip 🔖", key=f"save_{row['name']}", width="stretch"):
                            if not user:
                                show_auth_dialog("Sign in to save trips to your profile.")
                            else:
                                save_trip(user["id"], row["name"], row["country"])
                                st.toast(f"Saved {row['name']} to your trips!", icon="✨")
                                st.rerun()
                with action_col2:
                    if st.button(
                        f"Explore {row['name']}",
                        key=f"ask_{row['name']}",
                        icon=":material/arrow_forward:",
                        type="primary",
                        width="stretch",
                    ):
                        st.session_state.selected_destination = row.to_dict()
                        st.session_state.chat_messages = []
                        st.switch_page("app_pages/destination.py")

    table = results[
        [
            "name",
            "country",
            "place_type",
            "weather",
            "match_pct",
            "ground_spend_typical",
            "affordability_status",
            "culture",
            "food",
            "quiet",
            "nightlife",
        ]
    ].rename(
        columns={
            "match_pct": "preference fit %",
            "ground_spend_typical": "ground spend USD/day",
            "affordability_status": "budget status",
        }
    )
    st.subheader("Compare at a glance")
    st.dataframe(table, hide_index=True, width="stretch")
    st.caption(BUDGET_GUIDE)
