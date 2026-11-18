import streamlit as st

from recommender.auth import authenticate_user, create_user_session, register_user


@st.dialog("Sign in to TripSense AI")
def show_auth_dialog(message="Please sign in or create an account to view and save your destination matches."):
    if message:
        st.info(message, icon=":material/lock:")

    tab_signin, tab_register = st.tabs(["Sign In", "Create Account"])

    with tab_signin:
        with st.form("signin_form", border=False):
            username_or_email = st.text_input(
                "Username or Email",
                placeholder="e.g. traveler or traveler@example.com",
                key="signin_login_field",
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="signin_password_field",
            )
            signin_submitted = st.form_submit_button(
                "Sign In",
                type="primary",
                width="stretch",
                icon=":material/login:",
            )

        if signin_submitted:
            user, error = authenticate_user(username_or_email, password)
            if error:
                st.error(error, icon=":material/error:")
            else:
                token = create_user_session(user["id"])
                st.query_params["session"] = token
                st.session_state.user = user
                st.toast(f"Welcome back, {user['full_name']}!", icon="👋")
                st.rerun()

    with tab_register:
        with st.form("register_form", border=False):
            full_name = st.text_input(
                "Full Name",
                placeholder="e.g. Phyo Khant Kywal",
                key="register_fullname_field",
            )
            reg_username = st.text_input(
                "Choose a Username",
                placeholder="e.g. traveler42",
                key="register_username_field",
            )
            reg_email = st.text_input(
                "Email Address",
                placeholder="e.g. name@example.com",
                key="register_email_field",
            )
            reg_password = st.text_input(
                "Password",
                type="password",
                placeholder="At least 6 characters",
                key="register_password_field",
            )
            reg_confirm = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-type password",
                key="register_confirm_field",
            )
            reg_submitted = st.form_submit_button(
                "Create Account & Continue",
                type="primary",
                width="stretch",
                icon=":material/person_add:",
            )

        if reg_submitted:
            if reg_password != reg_confirm:
                st.error("Passwords do not match.", icon=":material/warning:")
            else:
                user, error = register_user(
                    reg_username,
                    reg_email,
                    reg_password,
                    full_name=full_name,
                )
                if error:
                    st.error(error, icon=":material/error:")
                else:
                    token = create_user_session(user["id"])
                    st.query_params["session"] = token
                    st.session_state.user = user
                    st.toast("Account created successfully! Welcome to TripSense AI.", icon="✨")
                    st.rerun()
