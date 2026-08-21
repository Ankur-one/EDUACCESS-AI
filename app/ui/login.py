import streamlit as st  # pyright: ignore[reportMissingImports]

from app.auth.authentication import login_user
from app.auth.session import create_login_session


def show_login():

    st.title("🔐 Login to EduAccess AI")

    st.write(
        "Login to access your personalized learning environment."
    )

    st.divider()

    email = st.text_input(
        "📧 Email"
    )

    password = st.text_input(
        "🔑 Password",
        type="password"
    )

    st.write("")

    if st.button(
        "Login",
        use_container_width=True
    ):

        if not email or not password:

            st.warning(
                "Please enter your email and password."
            )

            return

        try:

            user = login_user(
                email=email,
                password=password
            )

            if user:

                create_login_session(user)

                st.success(
                    f"Welcome, {user.full_name}! 🎉"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid email or password."
                )

        except Exception as e:

            st.error(
                "Login failed."
            )

            st.exception(e)