import streamlit as st  # type: ignore[import-not-found]

from app.auth.authentication import register_user
from app.database.database import SessionLocal


def show_register():

    st.title("📝 Create Your EduAccess AI Account")

    st.write(
        "Create an account to personalize your learning experience."
    )

    with st.form("registration_form"):

        full_name = st.text_input(
            "Full Name",
            placeholder="Enter your full name"
        )

        email = st.text_input(
            "Email",
            placeholder="student@example.com"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a strong password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password"
        )

        submitted = st.form_submit_button(
            "Create Account",
            use_container_width=True
        )

    if submitted:

        if not full_name:
            st.error("Please enter your full name.")
            return

        if not email:
            st.error("Please enter your email.")
            return

        if not password:
            st.error("Please enter a password.")
            return

        if len(password) < 8:
            st.error(
                "Password must contain at least 8 characters."
            )
            return

        if password != confirm_password:
            st.error(
                "Passwords do not match."
            )
            return

        db = SessionLocal()

        try:

            user, message = register_user(
                db=db,
                full_name=full_name,
                email=email,
                password=password
            )

            if user:
                st.success(
                    "🎉 Account created successfully!"
                )

                st.info(
                    "Your accessibility profile has been created. "
                    "You will configure it after login."
                )

            else:
                st.error(message)

        finally:
            db.close()