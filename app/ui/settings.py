import streamlit as st  # type: ignore[import-not-found]

from app.auth.session import get_current_user_id
from app.database.database import SessionLocal
from app.database.models import User


# ============================================================
# SHOW SETTINGS
# ============================================================


def show_settings():
    """Render and persist the current user's accessibility settings."""

    st.title("⚙️ Accessibility Settings")

    st.caption(
        "Customize EduAccess AI according to your learning "
        "and accessibility preferences."
    )

    st.divider()

    # ========================================================
    # CURRENT USER
    # ========================================================

    user_id = get_current_user_id()

    if not user_id:

        st.warning(
            "⚠️ User session not found. Please login again."
        )

        return

    # ========================================================
    # DATABASE
    # ========================================================

    db = None

    try:

        db = SessionLocal()

        # ====================================================
        # GET USER
        # ====================================================

        user = (
            db.query(User)
            .filter(
                User.id == user_id
            )
            .first()
        )

        if user is None:

            st.error(
                "❌ User account could not be found."
            )

            return

        # ====================================================
        # LANGUAGE
        # ====================================================

        st.subheader(
            "🌐 Language"
        )

        languages = [
            "English",
            "Hindi",
            "Hinglish",
            "Punjabi",
        ]

        current_language = (
            user.preferred_language
            or "English"
        )

        if current_language not in languages:

            languages.append(
                current_language
            )

        selected_language = st.selectbox(
            "Preferred learning language",
            languages,
            index=languages.index(
                current_language
            ),
            key="settings_language",
        )

        st.divider()

        # ====================================================
        # LEARNING PREFERENCES
        # ====================================================

        st.subheader(
            "📚 Learning Preferences"
        )

        simple_explanation = st.checkbox(
            "📝 Simple explanations",
            value=bool(
                user.simple_explanation
            ),
            help=(
                "Use easier words and simpler explanations."
            ),
            key="settings_simple",
        )

        step_by_step = st.checkbox(
            "👣 Step-by-step learning",
            value=bool(
                user.step_by_step
            ),
            help=(
                "Explain difficult topics one step at a time."
            ),
            key="settings_step",
        )

        repetition_support = st.checkbox(
            "🔁 Repetition support",
            value=bool(
                user.repetition_support
            ),
            help=(
                "Repeat important concepts when useful."
            ),
            key="settings_repetition",
        )

        visual_explanation = st.checkbox(
            "👁️ Visual explanations",
            value=bool(
                user.visual_explanation
            ),
            help=(
                "Use tables, diagrams, and structured "
                "visual explanations."
            ),
            key="settings_visual",
        )

        st.divider()

        # ====================================================
        # COMMUNICATION ACCESSIBILITY
        # ====================================================

        st.subheader(
            "🗣️ Communication Accessibility"
        )

        text_to_speech = st.checkbox(
            "🔊 Text-to-speech",
            value=bool(
                user.text_to_speech
            ),
            help=(
                "Read AI Tutor answers aloud."
            ),
            key="settings_tts",
        )

        speech_to_text = st.checkbox(
            "🎤 Speech-to-text",
            value=bool(
                user.speech_to_text
            ),
            help=(
                "Allow voice input for tutor questions."
            ),
            key="settings_stt",
        )

        st.divider()

        # ====================================================
        # VISUAL ACCESSIBILITY
        # ====================================================

        st.subheader(
            "👁️ Visual Accessibility"
        )

        large_text = st.checkbox(
            "🔠 Large text",
            value=bool(
                user.large_text
            ),
            help=(
                "Use larger and more readable text."
            ),
            key="settings_large_text",
        )

        high_contrast = st.checkbox(
            "◐ High contrast",
            value=bool(
                user.high_contrast
            ),
            help=(
                "Use a cleaner high-contrast interface."
            ),
            key="settings_high_contrast",
        )

        dyslexia_friendly = st.checkbox(
            "📖 Dyslexia-friendly mode",
            value=bool(
                user.dyslexia_friendly
            ),
            help=(
                "Use short sentences, clear headings, "
                "and improved spacing."
            ),
            key="settings_dyslexia",
        )

        st.divider()

        # ====================================================
        # SAVE BUTTON
        # ========================================================

        if st.button(
            "💾 Save Accessibility Settings",
            type="primary",
            use_container_width=True,
            key="save_accessibility_settings",
        ):

            # ================================================
            # UPDATE USER
            # ================================================

            user.preferred_language = (
                selected_language
            )

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

            user.text_to_speech = (
                text_to_speech
            )

            user.speech_to_text = (
                speech_to_text
            )

            user.large_text = (
                large_text
            )

            user.high_contrast = (
                high_contrast
            )

            user.dyslexia_friendly = (
                dyslexia_friendly
            )

            # ================================================
            # SAVE
            # ================================================

            db.commit()

            db.refresh(
                user
            )

            st.success(
                "✅ Accessibility settings saved successfully."
            )

            st.rerun()

    # ========================================================
    # ERROR
    # ========================================================

    except Exception as error:

        if db is not None:
            db.rollback()

        st.error(
            "❌ Could not save accessibility settings."
        )

        st.exception(error)

    # ========================================================
    # CLOSE DATABASE
    # ========================================================

    finally:

        if db is not None:

            db.close()
