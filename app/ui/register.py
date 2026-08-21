import importlib

from app.auth.authentication import register_user

st = importlib.import_module("streamlit")


def show_register():

    st.title("📝 Create EduAccess AI Account")

    st.write(
        "Create your account and personalize your learning experience."
    )

    st.divider()

    # ========================================================
    # BASIC INFORMATION
    # ========================================================

    st.subheader("👤 Basic Information")

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
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    st.divider()

    # ========================================================
    # DISABILITY PROFILE
    # ========================================================

    st.subheader("♿ Accessibility Profile")

    disability_options = [
        "No disability",
        "Visual impairment",
        "Hearing impairment",
        "Speech impairment",
        "Physical / Motor disability",
        "Learning disability",
        "Dyslexia",
        "Intellectual disability",
        "Autism / Neurodevelopmental support",
        "Multiple disabilities",
        "Other"
    ]

    disability_type = st.selectbox(
        "Select your disability / accessibility need",
        disability_options
    )

    disability_details = st.text_area(
        "Additional accessibility information",
        placeholder=(
            "Tell us anything that can help EduAccess AI "
            "support your learning."
        )
    )

    st.divider()

    # ========================================================
    # LEARNING PREFERENCES
    # ========================================================

    st.subheader("🎓 Learning Preferences")

    preferred_language = st.selectbox(
        "🌐 Preferred Language",
        [
            "English",
            "Hindi",
            "Punjabi"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:

        simple_explanation = st.checkbox(
            "🧩 Simple explanations"
        )

        step_by_step = st.checkbox(
            "🪜 Step-by-step learning"
        )

        repetition_support = st.checkbox(
            "🔁 Repeat important concepts"
        )

        visual_explanation = st.checkbox(
            "📊 Visual / structured explanations"
        )

    with col2:

        text_to_speech = st.checkbox(
            "🔊 Text-to-speech support"
        )

        speech_to_text = st.checkbox(
            "🎤 Speech-to-text support"
        )

        large_text = st.checkbox(
            "🔎 Large text / readability support"
        )

    st.divider()

    # ========================================================
    # CREATE ACCOUNT
    # ========================================================

    if st.button(
        "📝 Create Account",
        use_container_width=True
    ):

        # ----------------------------------------------------
        # Validation
        # ----------------------------------------------------

        if not full_name.strip():

            st.warning(
                "Please enter your full name."
            )

            return

        if not email.strip():

            st.warning(
                "Please enter your email."
            )

            return

        if not password:

            st.warning(
                "Please enter a password."
            )

            return

        if len(password) < 8:

            st.warning(
                "Password must contain at least 8 characters."
            )

            return

        if password != confirm_password:

            st.error(
                "Passwords do not match."
            )

            return

        # ----------------------------------------------------
        # Create account
        # ----------------------------------------------------

        try:

            register_user(

                full_name=full_name,

                email=email,

                password=password,

                disability_type=disability_type,

                disability_details=disability_details,

                preferred_language=preferred_language,

                simple_explanation=simple_explanation,

                step_by_step=step_by_step,

                repetition_support=repetition_support,

                visual_explanation=visual_explanation,

                text_to_speech=text_to_speech,

                speech_to_text=speech_to_text,

                large_text=large_text,
            )

            st.success(
                "🎉 Account created successfully!"
            )

            st.info(
                "You can now go to the Login tab and sign in."
            )

        except ValueError as e:

            st.error(
                str(e)
            )

        except Exception as e:

            st.error(
                "Registration failed."
            )

            st.exception(e)