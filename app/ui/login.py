from importlib import import_module


from app.auth.authentication import (
    login_user as authenticate_user,
    register_user,
)

from app.auth.session import (
    create_login_session,
)

# Load Streamlit dynamically so editors do not report an unresolved import
# when the dependency is not installed in the active Python environment.
st = import_module("streamlit")


# ============================================================
# LOGIN + REGISTRATION PAGE
# ============================================================

def show_login():

    # ========================================================
    # HEADER
    # ========================================================

    st.markdown(
        """
        <div style="
            text-align: center;
            padding: 20px 0 10px 0;
        ">
            <h1>♿ EduAccess AI</h1>
            <p style="font-size: 18px;">
                Inclusive AI-Powered Education
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # ========================================================
    # LOGIN / REGISTER TABS
    # ========================================================

    login_tab, register_tab = st.tabs(
        [
            "🔐 Login",
            "📝 Create Account",
        ]
    )

    # ========================================================
    # LOGIN TAB
    # ========================================================

    with login_tab:

        st.subheader("🔐 Student Login")

        st.write(
            "Login to access your personalized "
            "EduAccess AI learning environment."
        )

        with st.form(
            "login_form",
            clear_on_submit=False,
        ):

            email = st.text_input(
                "📧 Email",
                placeholder="Enter your email",
                key="login_email",
            )

            password = st.text_input(
                "🔑 Password",
                type="password",
                placeholder="Enter your password",
                key="login_password",
            )

            login_button = st.form_submit_button(
                "🚀 Login",
                use_container_width=True,
            )

        # ====================================================
        # LOGIN PROCESS
        # ====================================================

        if login_button:

            email = email.strip()
            password = password.strip()

            # ------------------------------------------------
            # VALIDATION
            # ------------------------------------------------

            if not email:

                st.error(
                    "❌ Please enter your email."
                )

            elif not password:

                st.error(
                    "❌ Please enter your password."
                )

            elif "@" not in email:

                st.error(
                    "❌ Please enter a valid email address."
                )

            else:

                try:

                    # ----------------------------------------
                    # AUTHENTICATE USER
                    # ----------------------------------------

                    user = authenticate_user(
                        email=email,
                        password=password,
                    )

                    # ----------------------------------------
                    # INVALID LOGIN
                    # ----------------------------------------

                    if user is None:

                        st.error(
                            "❌ Invalid email or password."
                        )

                    # ----------------------------------------
                    # SUCCESSFUL LOGIN
                    # ----------------------------------------

                    else:

                        create_login_session(
                            user
                        )

                        st.success(
                            "✅ Login successful!"
                        )

                        st.info(
                            "Opening your dashboard..."
                        )

                        st.rerun()

                except Exception as error:

                    st.error(
                        "❌ Login failed."
                    )

                    st.exception(error)

    # ========================================================
    # REGISTRATION TAB
    # ========================================================

    with register_tab:

        st.subheader(
            "📝 Create Your EduAccess AI Account"
        )

        st.write(
            "Create an account and personalize "
            "your learning and accessibility preferences."
        )

        # ====================================================
        # REGISTRATION FORM
        # ====================================================

        with st.form(
            "registration_form",
            clear_on_submit=False,
        ):

            # =================================================
            # BASIC INFORMATION
            # =================================================

            st.markdown(
                "### 👤 Basic Information"
            )

            full_name = st.text_input(
                "Full Name",
                placeholder="Enter your full name",
                key="register_full_name",
            )

            email = st.text_input(
                "Email",
                placeholder="Enter your email address",
                key="register_email",
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a password",
                key="register_password",
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Enter your password again",
                key="register_confirm_password",
            )

            # =================================================
            # ACCESSIBILITY INFORMATION
            # =================================================

            st.markdown(
                "### ♿ Accessibility Information"
            )

            disability_options = [
                "No disability",
                "Visual impairment",
                "Hearing impairment",
                "Mobility impairment",
                "Learning disability",
                "Cognitive disability",
                "Speech impairment",
                "Multiple disabilities",
                "Other",
            ]

            disability_type = st.selectbox(
                "Disability Type",
                disability_options,
                key="register_disability_type",
            )

            disability_details = st.text_area(
                "Additional Accessibility Details",
                placeholder=(
                    "Optional: describe any accessibility "
                    "requirements that may help personalize "
                    "your learning experience."
                ),
                key="register_disability_details",
            )

            # =================================================
            # LANGUAGE
            # =================================================

            st.markdown(
                "### 🌐 Language"
            )

            preferred_language = st.selectbox(
                "Preferred Language",
                [
                    "English",
                    "Hindi",
                    "Hinglish",
                ],
                key="register_language",
            )

            # =================================================
            # LEARNING PREFERENCES
            # =================================================

            st.markdown(
                "### 🎯 Learning Preferences"
            )

            learning_col1, learning_col2 = st.columns(2)

            with learning_col1:

                simple_explanation = st.checkbox(
                    "👨‍🏫 Simple Explanation",
                    value=True,
                    key="register_simple",
                    help=(
                        "Use easy-to-understand explanations."
                    ),
                )

                step_by_step = st.checkbox(
                    "📚 Step-by-Step",
                    value=True,
                    key="register_step",
                    help=(
                        "Explain concepts step by step."
                    ),
                )

                repetition_support = st.checkbox(
                    "🔁 Repeat Important Points",
                    value=False,
                    key="register_repetition",
                    help=(
                        "Repeat important information."
                    ),
                )

            with learning_col2:

                visual_explanation = st.checkbox(
                    "📊 Use Examples",
                    value=True,
                    key="register_visual",
                    help=(
                        "Use examples to explain concepts."
                    ),
                )

            # =================================================
            # COMMUNICATION ACCESSIBILITY
            # =================================================

            st.markdown(
                "### 🗣️ Communication Accessibility"
            )

            communication_col1, communication_col2 = (
                st.columns(2)
            )

            with communication_col1:

                text_to_speech = st.checkbox(
                    "🔊 Text-to-Speech",
                    value=False,
                    key="register_tts",
                    help=(
                        "Enable spoken AI responses."
                    ),
                )

            with communication_col2:

                speech_to_text = st.checkbox(
                    "🎤 Speech-to-Text",
                    value=False,
                    key="register_stt",
                    help=(
                        "Use voice input for questions."
                    ),
                )

            # =================================================
            # VISUAL ACCESSIBILITY
            # =================================================

            st.markdown(
                "### 👁️ Visual Accessibility"
            )

            visual_col1, visual_col2 = st.columns(2)

            with visual_col1:

                large_text = st.checkbox(
                    "🔎 Large Text",
                    value=False,
                    key="register_large_text",
                    help=(
                        "Increase the size of important text."
                    ),
                )

            with visual_col2:

                high_contrast = st.checkbox(
                    "⚫ High Contrast",
                    value=False,
                    key="register_high_contrast",
                    help=(
                        "Improve visual contrast."
                    ),
                )

            dyslexia_friendly = st.checkbox(
                "📖 Dyslexia-Friendly Text",
                value=False,
                key="register_dyslexia",
                help=(
                    "Increase spacing and readability "
                    "for easier reading."
                ),
            )

            # =================================================
            # TERMS / INFORMATION
            # =================================================

            st.info(
                "💡 Your accessibility preferences are "
                "saved with your account and can be changed "
                "later from Settings."
            )

            # =================================================
            # REGISTER BUTTON
            # =================================================

            register_button = st.form_submit_button(
                "📝 Create Account",
                use_container_width=True,
            )

        # ====================================================
        # REGISTRATION PROCESS
        # ====================================================

        if register_button:

            # ------------------------------------------------
            # CLEAN INPUT
            # ------------------------------------------------

            full_name = full_name.strip()
            email = email.strip().lower()
            password = password.strip()
            confirm_password = confirm_password.strip()

            disability_details = (
                disability_details.strip()
            )

            # ------------------------------------------------
            # VALIDATION
            # ------------------------------------------------

            if not full_name:

                st.error(
                    "❌ Please enter your full name."
                )

            elif not email:

                st.error(
                    "❌ Please enter your email."
                )

            elif "@" not in email:

                st.error(
                    "❌ Please enter a valid email address."
                )

            elif not password:

                st.error(
                    "❌ Please create a password."
                )

            elif len(password) < 6:

                st.error(
                    "❌ Password must contain at least "
                    "6 characters."
                )

            elif password != confirm_password:

                st.error(
                    "❌ Passwords do not match."
                )

            else:

                try:

                    # ========================================
                    # CREATE USER
                    # ========================================

                    user = register_user(

                        # ------------------------------------
                        # BASIC INFORMATION
                        # ------------------------------------

                        full_name=full_name,

                        email=email,

                        password=password,

                        # ------------------------------------
                        # ACCESSIBILITY INFORMATION
                        # ------------------------------------

                        disability_type=(
                            disability_type
                        ),

                        disability_details=(
                            disability_details
                        ),

                        # ------------------------------------
                        # LANGUAGE
                        # ------------------------------------

                        preferred_language=(
                            preferred_language
                        ),

                        # ------------------------------------
                        # LEARNING PREFERENCES
                        # ------------------------------------

                        simple_explanation=(
                            simple_explanation
                        ),

                        step_by_step=(
                            step_by_step
                        ),

                        repetition_support=(
                            repetition_support
                        ),

                        visual_explanation=(
                            visual_explanation
                        ),

                        # ------------------------------------
                        # COMMUNICATION ACCESSIBILITY
                        # ------------------------------------

                        text_to_speech=(
                            text_to_speech
                        ),

                        speech_to_text=(
                            speech_to_text
                        ),

                        # ------------------------------------
                        # VISUAL ACCESSIBILITY
                        # ------------------------------------

                        large_text=(
                            large_text
                        ),

                        high_contrast=(
                            high_contrast
                        ),

                        dyslexia_friendly=(
                            dyslexia_friendly
                        ),
                    )

                    # ========================================
                    # SUCCESS
                    # ========================================

                    if user is not None:

                        st.success(
                            "🎉 Account created successfully!"
                        )

                        st.info(
                            "Please open the 🔐 Login tab "
                            "and login with your new account."
                        )

                    else:

                        st.error(
                            "❌ Account could not be created."
                        )

                # ============================================
                # DUPLICATE EMAIL / VALIDATION ERROR
                # ============================================

                except ValueError as error:

                    st.error(
                        f"❌ {error}"
                    )

                # ============================================
                # OTHER DATABASE ERROR
                # ============================================

                except Exception as error:

                    st.error(
                        "❌ Registration failed."
                    )

                    st.exception(error)


# ============================================================
# END OF LOGIN MODULE
# ============================================================
