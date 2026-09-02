# ============================================================
# app/ui/tutor.py
# EduAccess AI
# AI Tutor + TTS + STT + Database Preferences
# ============================================================

import importlib

from app.database.models import User
from app.database.database import SessionLocal

from app.audio.tts import (
    show_text_to_speech,
    get_tts_language,
    test_voice,
    get_available_tts_voices,
)

try:
    from app.audio.stt import (
        show_speech_to_text,
    )
except ImportError:
    show_speech_to_text = None

# NOTE: Backtick expressions are invalid Python syntax; keep string literals explicit.


# ============================================================
# STREAMLIT
# ============================================================

st = importlib.import_module("streamlit")


# ============================================================
# 1. INITIALIZE TUTOR SESSION STATE
# ============================================================

def initialize_tutor_state():
    """
    Initialize all Tutor-related Streamlit session state.
    """

    # --------------------------------------------------------
    # Conversation
    # --------------------------------------------------------

    if "messages" not in st.session_state:
        st.session_state.messages = []


    # --------------------------------------------------------
    # Tutor session
    # --------------------------------------------------------

    if "tutor_session_id" not in st.session_state:
        st.session_state.tutor_session_id = None


    # --------------------------------------------------------
    # Language
    # --------------------------------------------------------

    if "preferred_language" not in st.session_state:
        st.session_state.preferred_language = "English"


    # --------------------------------------------------------
    # Learning preferences
    # --------------------------------------------------------

    if "simple_explanation" not in st.session_state:
        st.session_state.simple_explanation = True

    if "step_by_step_learning" not in st.session_state:
        st.session_state.step_by_step_learning = True

    if "repetition_support" not in st.session_state:
        st.session_state.repetition_support = False

    if "visual_explanation" not in st.session_state:
        st.session_state.visual_explanation = True


    # --------------------------------------------------------
    # STT
    # --------------------------------------------------------

    if "stt_enabled" not in st.session_state:
        st.session_state.stt_enabled = False


    # ========================================================
    # TTS
    # ========================================================

    if "tts_enabled" not in st.session_state:
        st.session_state.tts_enabled = False

    if "tts_autoplay" not in st.session_state:
        st.session_state.tts_autoplay = False

    if "tts_voice" not in st.session_state:
        st.session_state.tts_voice = ""

    if "tts_rate" not in st.session_state:
        st.session_state.tts_rate = 0.9

    if "tts_volume" not in st.session_state:
        st.session_state.tts_volume = 1.0

    if "tts_pitch" not in st.session_state:
        st.session_state.tts_pitch = 1.0


    # --------------------------------------------------------
    # Database load flag
    # --------------------------------------------------------

    if "tts_preferences_loaded" not in st.session_state:
        st.session_state.tts_preferences_loaded = False


    # --------------------------------------------------------
    # Save status
    # --------------------------------------------------------

    if "tts_save_status" not in st.session_state:
        st.session_state.tts_save_status = "idle"


    # --------------------------------------------------------
    # Save error
    # --------------------------------------------------------

    if "tts_save_error" not in st.session_state:
        st.session_state.tts_save_error = ""


# ============================================================
# 2. LOAD TTS PREFERENCES FROM DATABASE
# ============================================================

def load_user_tts_preferences(
    user: User,
):
    """
    Load TTS preferences from User database object.
    """

    if user is None:
        return


    # --------------------------------------------------------
    # TTS enabled
    # --------------------------------------------------------

    st.session_state.tts_enabled = bool(
        getattr(
            user,
            "text_to_speech",
            False,
        )
    )


    # --------------------------------------------------------
    # Voice
    # --------------------------------------------------------

    saved_voice = getattr(
        user,
        "tts_voice",
        "",
    )

    if saved_voice is None:
        saved_voice = ""

    st.session_state.tts_voice = str(
        saved_voice
    )


    # --------------------------------------------------------
    # Autoplay
    # --------------------------------------------------------

    st.session_state.tts_autoplay = bool(
        getattr(
            user,
            "tts_autoplay",
            False,
        )
    )


    # --------------------------------------------------------
    # Rate
    # --------------------------------------------------------

    try:

        st.session_state.tts_rate = float(
            getattr(
                user,
                "tts_rate",
                0.9,
            )
        )

    except (
        TypeError,
        ValueError,
    ):

        st.session_state.tts_rate = 0.9


    # --------------------------------------------------------
    # Volume
    # --------------------------------------------------------

    try:

        st.session_state.tts_volume = float(
            getattr(
                user,
                "tts_volume",
                1.0,
            )
        )

    except (
        TypeError,
        ValueError,
    ):

        st.session_state.tts_volume = 1.0


    # --------------------------------------------------------
    # Pitch
    # --------------------------------------------------------

    try:

        st.session_state.tts_pitch = float(
            getattr(
                user,
                "tts_pitch",
                1.0,
            )
        )

    except (
        TypeError,
        ValueError,
    ):

        st.session_state.tts_pitch = 1.0


    # --------------------------------------------------------
    # Mark loaded
    # --------------------------------------------------------

    st.session_state.tts_preferences_loaded = True


# ============================================================
# 3. INITIALIZE DATABASE TTS PREFERENCES
# ============================================================

def initialize_tts_preferences(
    user: User,
):
    """
    Load database TTS preferences once.
    """

    if user is None:
        return


    if st.session_state.get(
        "tts_preferences_loaded",
        False,
    ):
        return


    load_user_tts_preferences(
        user
    )


# ============================================================
# 4. SAVE TTS PREFERENCES
# ============================================================

def save_user_tts_preferences(
    db,
    user: User,
):
    """
    Save current TTS settings into the database.
    """

    st.session_state.tts_save_status = "idle"
    st.session_state.tts_save_error = ""


    if db is None:

        st.session_state.tts_save_status = "error"

        st.session_state.tts_save_error = (
            "Database session is not available."
        )

        return False


    if user is None:

        st.session_state.tts_save_status = "error"

        st.session_state.tts_save_error = (
            "Logged-in user is not available."
        )

        return False


    try:

        # ----------------------------------------------------
        # TTS enabled
        # ----------------------------------------------------

        user.text_to_speech = bool(
            st.session_state.get(
                "tts_enabled",
                False,
            )
        )


        # ----------------------------------------------------
        # Voice
        # ----------------------------------------------------

        user.tts_voice = str(
            st.session_state.get(
                "tts_voice",
                "",
            ) or ""
        )


        # ----------------------------------------------------
        # Autoplay
        # ----------------------------------------------------

        if hasattr(
            user,
            "tts_autoplay",
        ):

            user.tts_autoplay = bool(
                st.session_state.get(
                    "tts_autoplay",
                    False,
                )
            )


        # ----------------------------------------------------
        # Rate
        # ----------------------------------------------------

        if hasattr(
            user,
            "tts_rate",
        ):

            user.tts_rate = str(
                st.session_state.get(
                    "tts_rate",
                    0.9,
                )
            )


        # ----------------------------------------------------
        # Volume
        # ----------------------------------------------------

        if hasattr(
            user,
            "tts_volume",
        ):

            user.tts_volume = str(
                st.session_state.get(
                    "tts_volume",
                    1.0,
                )
            )


        # ----------------------------------------------------
        # Pitch
        # ----------------------------------------------------

        if hasattr(
            user,
            "tts_pitch",
        ):

            user.tts_pitch = str(
                st.session_state.get(
                    "tts_pitch",
                    1.0,
                )
            )


        # ----------------------------------------------------
        # Commit
        # ----------------------------------------------------

        db.commit()


        # ----------------------------------------------------
        # Refresh
        # ----------------------------------------------------

        db.refresh(
            user
        )


        # ----------------------------------------------------
        # Synchronize session state
        # ----------------------------------------------------

        st.session_state.tts_enabled = bool(
            user.text_to_speech
        )

        st.session_state.tts_voice = str(
            user.tts_voice or ""
        )

        st.session_state.tts_autoplay = bool(
            getattr(
                user,
                "tts_autoplay",
                False,
            )
        )


        try:

            st.session_state.tts_rate = float(
                getattr(
                    user,
                    "tts_rate",
                    0.9,
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            st.session_state.tts_rate = 0.9


        try:

            st.session_state.tts_volume = float(
                getattr(
                    user,
                    "tts_volume",
                    1.0,
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            st.session_state.tts_volume = 1.0


        try:

            st.session_state.tts_pitch = float(
                getattr(
                    user,
                    "tts_pitch",
                    1.0,
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            st.session_state.tts_pitch = 1.0


        # ----------------------------------------------------
        # Success
        # ----------------------------------------------------

        st.session_state.tts_save_status = "saved"
        st.session_state.tts_save_error = ""

        return True


    except Exception as error:

        db.rollback()

        st.session_state.tts_save_status = "error"

        st.session_state.tts_save_error = str(
            error
        )

        return False


# ============================================================
# 5. TEST CURRENT VOICE
# ============================================================

def test_current_tts_voice():
    """
    Test the currently selected TTS voice.
    """

    language_name = st.session_state.get(
        "preferred_language",
        "English",
    )


    try:

        language_code = get_tts_language(
            language_name
        )

    except Exception:

        language_code = "en-US"


    selected_voice = st.session_state.get(
        "tts_voice",
        "",
    )


    speech_rate = st.session_state.get(
        "tts_rate",
        0.9,
    )


    volume = st.session_state.get(
        "tts_volume",
        1.0,
    )


    pitch = st.session_state.get(
        "tts_pitch",
        1.0,
    )


    try:

        test_voice(
            language=language_code,
            selected_voice=selected_voice,
            speech_rate=speech_rate,
            volume=volume,
            pitch=pitch,
        )

        return True

    except Exception as error:

        st.error(
            f"❌ Voice test failed: {error}"
        )

        return False


# ============================================================
# 6. SAVE BUTTON
# ============================================================

def show_tts_save_button(
    db,
    user: User,
):
    """
    Display Save and Test Voice buttons.
    """

    st.markdown(
        "#### 💾 Save TTS Preferences"
    )


    # --------------------------------------------------------
    # Current voice
    # --------------------------------------------------------

    current_voice = st.session_state.get(
        "tts_voice",
        "",
    )


    if current_voice:

        st.caption(
            f"🎙️ Selected voice: {current_voice}"
        )

    else:

        st.caption(
            "🎙️ Selected voice: Automatic browser voice"
        )


    # --------------------------------------------------------
    # Save button
    # --------------------------------------------------------

    save_clicked = st.button(
        "💾 Save Voice Settings",
        key="save_tts_preferences_button",
        use_container_width=True,
    )


    # --------------------------------------------------------
    # Test button
    # --------------------------------------------------------

    test_clicked = st.button(
        "🔊 Test Voice",
        key="test_tts_voice_button",
        use_container_width=True,
    )


    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    if save_clicked:

        saved = save_user_tts_preferences(
            db=db,
            user=user,
        )


        if saved:

            st.success(
                "✅ TTS preferences saved successfully."
            )

        else:

            error_message = st.session_state.get(
                "tts_save_error",
                "",
            )

            if error_message:

                st.error(
                    f"❌ Unable to save TTS preferences: "
                    f"{error_message}"
                )

            else:

                st.error(
                    "❌ Unable to save TTS preferences."
                )


    # --------------------------------------------------------
    # Test voice
    # --------------------------------------------------------

    if test_clicked:

        test_current_tts_voice()


    # --------------------------------------------------------
    # Saved status
    # --------------------------------------------------------

    if (
        not save_clicked
        and st.session_state.get(
            "tts_save_status",
            "idle",
        ) == "saved"
    ):

        st.success(
            "✅ TTS preferences are saved."
        )


# ============================================================
# 7. TTS SETTINGS PANEL
# ============================================================

def show_tts_settings_panel(
    db,
    current_user: User,
):
    """
    Display complete TTS settings.
    """

    with st.expander(
        "🔊 Text-to-Speech Settings",
        expanded=False,
    ):

        # ====================================================
        # ENABLE
        # ====================================================

        st.checkbox(
            "Enable Text-to-Speech",
            key="tts_enabled",
        )


        # ====================================================
        # AUTOPLAY
        # ====================================================

        st.checkbox(
            "Automatically speak Tutor answers",
            key="tts_autoplay",
        )


        # ====================================================
        # VOICE
        # ====================================================

        st.markdown(
            "#### 🎙️ Voice"
        )


        # ----------------------------------------------------
        # Get available voices
        # ----------------------------------------------------

        try:

            available_voices = (
                get_available_tts_voices()
            )

        except Exception:

            available_voices = []


        # ----------------------------------------------------
        # Voice names
        # ----------------------------------------------------

        voice_names = []


        for voice in available_voices:

            if isinstance(
                voice,
                dict,
            ):

                voice_name = voice.get(
                    "name",
                    "",
                )

            else:

                voice_name = getattr(
                    voice,
                    "name",
                    str(voice),
                )


            if voice_name:

                voice_names.append(
                    str(voice_name)
                )


        # ----------------------------------------------------
        # Remove duplicates
        # ----------------------------------------------------

        voice_names = list(
            dict.fromkeys(
                voice_names
            )
        )


        # ----------------------------------------------------
        # Current voice
        # ----------------------------------------------------

        current_voice = st.session_state.get(
            "tts_voice",
            "",
        )


        # ----------------------------------------------------
        # Options
        # ----------------------------------------------------

        options = [
            "",
            *voice_names,
        ]


        # ----------------------------------------------------
        # Add saved voice if not in known list
        #
        # This is important:
        # A saved browser voice must never disappear
        # from the selector.
        # ----------------------------------------------------

        if (
            current_voice
            and current_voice not in options
        ):

            options.insert(
                1,
                current_voice,
            )


        # ----------------------------------------------------
        # Current index
        # ----------------------------------------------------

        if current_voice in options:

            current_index = options.index(
                current_voice
            )

        else:

            current_index = 0


        # ----------------------------------------------------
        # Voice selector
        # ----------------------------------------------------

        st.selectbox(
            "Select voice",
            options=options,
            index=current_index,
            format_func=lambda value: (
                "Automatic browser voice"
                if value == ""
                else value
            ),
            key="tts_voice",
        )


        # ====================================================
        # RATE
        # ====================================================

        st.slider(
            "Speech Rate",
            min_value=0.5,
            max_value=2.0,
            step=0.1,
            key="tts_rate",
        )


        # ====================================================
        # VOLUME
        # ====================================================

        st.slider(
            "Volume",
            min_value=0.0,
            max_value=1.0,
            step=0.1,
            key="tts_volume",
        )


        # ====================================================
        # PITCH
        # ====================================================

        st.slider(
            "Pitch",
            min_value=0.5,
            max_value=2.0,
            step=0.1,
            key="tts_pitch",
        )


        # ====================================================
        # CURRENT SETTINGS
        # ====================================================

        st.markdown("---")

        selected_voice = st.session_state.get(
            "tts_voice",
            "",
        )


        if selected_voice:

            st.write(
                f"🎙️ **Selected voice:** "
                f"{selected_voice}"
            )

        else:

            st.write(
                "🎙️ **Selected voice:** "
                "Automatic browser voice"
            )


        # ====================================================
        # SAVE SECTION
        # ====================================================

        show_tts_save_button(
            db=db,
            user=current_user,
        )


# ============================================================
# 8. SPEAK TUTOR ANSWER
# ============================================================

def speak_tutor_answer(
    answer: str,
):
    """
    Speak the Tutor answer using the current
    saved TTS settings.
    """

    if not answer:

        return


    # --------------------------------------------------------
    # TTS enabled?
    # --------------------------------------------------------

    if not st.session_state.get(
        "tts_enabled",
        False,
    ):

        return


    # --------------------------------------------------------
    # Language
    # --------------------------------------------------------

    language_name = st.session_state.get(
        "preferred_language",
        "English",
    )


    try:

        language_code = get_tts_language(
            language_name
        )

    except Exception:

        language_code = "en-US"


    # --------------------------------------------------------
    # Saved voice
    # --------------------------------------------------------

    selected_voice = st.session_state.get(
        "tts_voice",
        "",
    )


    # --------------------------------------------------------
    # Settings
    # --------------------------------------------------------

    speech_rate = st.session_state.get(
        "tts_rate",
        0.9,
    )

    volume = st.session_state.get(
        "tts_volume",
        1.0,
    )

    pitch = st.session_state.get(
        "tts_pitch",
        1.0,
    )

    autoplay = st.session_state.get(
        "tts_autoplay",
        False,
    )


    # --------------------------------------------------------
    # Speak
    # --------------------------------------------------------

    try:

        show_text_to_speech(

            text=answer,

            autoplay=autoplay,

            language=language_code,

            selected_voice=selected_voice,

            speech_rate=speech_rate,

            volume=volume,

            pitch=pitch,

        )

    except Exception as error:

        st.warning(
            f"TTS could not be started: {error}"
        )


# ============================================================
# 9. GET TTS SETTINGS
# ============================================================

def get_tts_settings():
    """
    Return current TTS settings.
    """

    return {

        "enabled": st.session_state.get(
            "tts_enabled",
            False,
        ),

        "autoplay": st.session_state.get(
            "tts_autoplay",
            False,
        ),

        "voice": st.session_state.get(
            "tts_voice",
            "",
        ),

        "rate": float(
            st.session_state.get(
                "tts_rate",
                0.9,
            )
        ),

        "volume": float(
            st.session_state.get(
                "tts_volume",
                1.0,
            )
        ),

        "pitch": float(
            st.session_state.get(
                "tts_pitch",
                1.0,
            )
        ),

    }


# ============================================================
# 10. TTS SUMMARY
# ============================================================

def show_tts_preference_summary():
    """
    Display current TTS settings.
    """

    settings = get_tts_settings()


    st.markdown(
        "#### 🔊 TTS Preference Summary"
    )


    # --------------------------------------------------------
    # Enabled
    # --------------------------------------------------------

    if settings["enabled"]:

        st.write(
            "🔊 **TTS:** Enabled"
        )

    else:

        st.write(
            "🔇 **TTS:** Disabled"
        )


    # --------------------------------------------------------
    # Voice
    # --------------------------------------------------------

    if settings["voice"]:

        st.write(
            f"🎙️ **Voice:** "
            f"{settings['voice']}"
        )

    else:

        st.write(
            "🎙️ **Voice:** "
            "Automatic browser voice"
        )


    # --------------------------------------------------------
    # Autoplay
    # --------------------------------------------------------

    if settings["autoplay"]:

        st.write(
            "▶️ **Autoplay:** Enabled"
        )

    else:

        st.write(
            "⏸️ **Autoplay:** Disabled"
        )


    # --------------------------------------------------------
    # Rate
    # --------------------------------------------------------

    st.write(
        f"⚡ **Rate:** "
        f"{settings['rate']:.1f}"
    )


    # --------------------------------------------------------
    # Volume
    # --------------------------------------------------------

    st.write(
        f"🔊 **Volume:** "
        f"{settings['volume']:.1f}"
    )


    # --------------------------------------------------------
    # Pitch
    # --------------------------------------------------------

    st.write(
        f"🎵 **Pitch:** "
        f"{settings['pitch']:.1f}"
    )


# ============================================================
# 11. DATABASE SESSION
# ============================================================

def get_tts_database_session():
    """
    Create SQLAlchemy database session.
    """

    return SessionLocal()


# ============================================================
# 12. INITIALIZE TUTOR FOR USER
# ============================================================

def initialize_tutor_for_user(
    current_user: User,
):
    """
    Initialize Tutor and load user preferences.
    """

    initialize_tutor_state()

    initialize_tts_preferences(
        current_user
    )


# ============================================================
# 13. TUTOR PAGE INITIALIZATION
# ============================================================

def initialize_tutor_page(
    current_user: User,
):
    """
    Convenience Tutor initialization function.
    """

    initialize_tutor_for_user(
        current_user
    )


# ============================================================
# END OF TUTOR MODULE
# ============================================================
