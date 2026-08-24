import streamlit as st  # type: ignore[import-not-found]

from app.auth.session import get_current_user_id
from app.database.database import SessionLocal
from app.database.models import User


# ============================================================
# GET CURRENT USER
# ============================================================

def get_current_accessibility_settings():
    """
    Return accessibility settings for the logged-in user.

    Returns:
        dict containing TTS, STT, language and visual settings.
    """

    user_id = get_current_user_id()

    if not user_id:

        return {
            "text_to_speech": False,
            "speech_to_text": False,
            "preferred_language": "English",
            "large_text": False,
            "high_contrast": False,
            "dyslexia_friendly": False,
            "simple_explanation": True,
            "step_by_step": True,
            "repetition_support": False,
            "visual_explanation": True,
        }

    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(
                User.id == user_id
            )
            .first()
        )

        if user is None:

            return {
                "text_to_speech": False,
                "speech_to_text": False,
                "preferred_language": "English",
                "large_text": False,
                "high_contrast": False,
                "dyslexia_friendly": False,
                "simple_explanation": True,
                "step_by_step": True,
                "repetition_support": False,
                "visual_explanation": True,
            }

        return {
            "text_to_speech": bool(
                user.text_to_speech
            ),
            "speech_to_text": bool(
                user.speech_to_text
            ),
            "preferred_language": (
                user.preferred_language
                or "English"
            ),
            "large_text": bool(
                user.large_text
            ),
            "high_contrast": bool(
                user.high_contrast
            ),
            "dyslexia_friendly": bool(
                user.dyslexia_friendly
            ),
            "simple_explanation": bool(
                user.simple_explanation
            ),
            "step_by_step": bool(
                user.step_by_step
            ),
            "repetition_support": bool(
                user.repetition_support
            ),
            "visual_explanation": bool(
                user.visual_explanation
            ),
        }

    except Exception:

        st.warning(
            "⚠️ Could not load accessibility preferences."
        )

        return {
            "text_to_speech": False,
            "speech_to_text": False,
            "preferred_language": "English",
            "large_text": False,
            "high_contrast": False,
            "dyslexia_friendly": False,
            "simple_explanation": True,
            "step_by_step": True,
            "repetition_support": False,
            "visual_explanation": True,
        }

    finally:

        db.close()


# ============================================================
# SHOW ACCESSIBILITY STATUS
# ============================================================

def show_tutor_accessibility_status():

    settings = (
        get_current_accessibility_settings()
    )

    col1, col2 = st.columns(2)

    with col1:

        if settings["speech_to_text"]:

            st.success(
                "🎤 Voice input enabled"
            )

        else:

            st.caption(
                "⌨️ Text input enabled"
            )

    with col2:

        if settings["text_to_speech"]:

            st.success(
                "🔊 Voice output enabled"
            )

        else:

            st.caption(
                "🔇 Voice output disabled"
            )

    return settings
