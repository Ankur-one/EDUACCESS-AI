import streamlit as st  # type: ignore[import-not-found]

from app.database.database import SessionLocal
from app.database.models import User
from app.auth.session import get_current_user_id


def show_accessibility():

    st.title("♿ Accessibility Control Center")

    st.write(
        "Customize EduAccess AI according to your learning needs."
    )

    st.divider()

    # ========================================================
    # GET CURRENT USER
    # ========================================================

    user_id = get_current_user_id()

    if not user_id:

        st.error("User session not found.")

        return

    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:

            st.error("Student profile not found.")

            return

        # ====================================================
        # PROFILE
        # ====================================================

        st.subheader(
            "👤 Your Accessibility Profile"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.info(
                f"""
**Student**

{user.full_name}
"""
            )

        with col2:

            st.info(
                f"""
**Accessibility Need**

{user.disability_type}
"""
            )

        if user.disability_details:

            st.write(
                "**Additional Information:**"
            )

            st.write(
                user.disability_details
            )

        st.divider()

        # ====================================================
        # LEARNING PREFERENCES
        # ====================================================

        st.subheader(
            "🎓 Learning Preferences"
        )

        col1, col2 = st.columns(2)

        with col1:

            simple_explanation = st.checkbox(
                "🧩 Simple explanations",
                value=bool(
                    user.simple_explanation
                ),
            )

            step_by_step = st.checkbox(
                "🪜 Step-by-step learning",
                value=bool(
                    user.step_by_step
                ),
            )

            repetition_support = st.checkbox(
                "🔁 Repeat important concepts",
                value=bool(
                    user.repetition_support
                ),
            )

            visual_explanation = st.checkbox(
                "📊 Visual / structured explanations",
                value=bool(
                    user.visual_explanation
                ),
            )

        with col2:

            text_to_speech = st.checkbox(
                "🔊 Text-to-Speech",
                value=bool(
                    user.text_to_speech
                ),
            )

            speech_to_text = st.checkbox(
                "🎤 Speech-to-Text",
                value=bool(
                    user.speech_to_text
                ),
            )

            large_text = st.checkbox(
                "🔎 Large text",
                value=bool(
                    user.large_text
                ),
            )

            high_contrast = st.checkbox(
                "🔳 High contrast",
                value=bool(
                    user.high_contrast
                ),
            )

            dyslexia_friendly = st.checkbox(
                "📖 Dyslexia-friendly mode",
                value=bool(
                    user.dyslexia_friendly
                ),
            )

        st.divider()

        # ====================================================
        # LANGUAGE
        # ====================================================

        st.subheader(
            "🌐 Language"
        )

        languages = [
            "English",
            "Hindi",
            "Punjabi",
        ]

        current_language = (
            user.preferred_language
        )

        if current_language not in languages:

            current_language = "English"

        preferred_language = st.selectbox(
            "Preferred learning language",
            languages,
            index=languages.index(
                current_language
            ),
        )

        st.divider()

        # ====================================================
        # SAVE SETTINGS
        # ====================================================

        if st.button(
            "💾 Save Accessibility Settings",
            use_container_width=True,
        ):

            try:

                # --------------------------------------------
                # LEARNING PREFERENCES
                # --------------------------------------------

                user.simple_explanation = (
                    simple_explanation
                )

                user.step_by_step = (
                    step_by_step
                )

                user.repetition_support = (
                    repetition_support
                )

                user.visual_explanation = (
                    visual_explanation
                )

                # --------------------------------------------
                # COMMUNICATION
                # --------------------------------------------

                user.text_to_speech = (
                    text_to_speech
                )

                user.speech_to_text = (
                    speech_to_text
                )

                # --------------------------------------------
                # VISUAL ACCESSIBILITY
                # --------------------------------------------

                user.large_text = (
                    large_text
                )

                user.high_contrast = (
                    high_contrast
                )

                user.dyslexia_friendly = (
                    dyslexia_friendly
                )

                # --------------------------------------------
                # LANGUAGE
                # --------------------------------------------

                user.preferred_language = (
                    preferred_language
                )

                # --------------------------------------------
                # DATABASE COMMIT
                # --------------------------------------------

                db.commit()

                db.refresh(user)

                # --------------------------------------------
                # SESSION UPDATE
                # --------------------------------------------

                st.session_state.large_text = bool(
                    user.large_text
                )

                st.session_state.high_contrast = bool(
                    user.high_contrast
                )

                st.session_state.dyslexia_friendly = bool(
                    user.dyslexia_friendly
                )

                st.success(
                    "✅ Accessibility settings saved successfully!"
                )

                st.rerun()

            except Exception as e:

                db.rollback()

                st.error(
                    "❌ Failed to save accessibility settings."
                )

                st.exception(e)

    finally:

        db.close()