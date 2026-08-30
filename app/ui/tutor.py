# ============================================================
# app/ui/tutor.py
# ============================================================
# EDUACCESS-AI
#
# Tutor UI
# TTS + Database Preference Management
#
# Features:
#   - Tutor session state
#   - TTS enabled/disabled
#   - Saved browser voice
#   - Autoplay
#   - Speech rate
#   - Volume
#   - Pitch
#   - Database loading
#   - Database saving
#   - TTS preference summary
#   - Test Voice
#   - Tutor answer speech
# ============================================================

import importlib


# ============================================================
# DATABASE
# ============================================================

from app.database.database import SessionLocal

from app.database.models import User


# ============================================================
# TTS
# ============================================================

from app.audio.tts import (
    show_text_to_speech,
    get_tts_language,
    get_available_voices,
    test_voice,
)


# ============================================================
# OPTIONAL STT
# ============================================================

try:

    from app.audio.stt import (
        show_speech_to_text,
    )

except ImportError:

    show_speech_to_text = None


# ============================================================
# STREAMLIT
# ============================================================

st = importlib.import_module(
    "streamlit"
)


# ============================================================
# DEFAULT TTS VALUES
# ============================================================

DEFAULT_TTS_ENABLED = False

DEFAULT_TTS_AUTOPLAY = False

DEFAULT_TTS_VOICE = ""

DEFAULT_TTS_RATE = 0.9

DEFAULT_TTS_VOLUME = 1.0

DEFAULT_TTS_PITCH = 1.0


# ============================================================
# 80.8.30.3
# INITIALIZE TUTOR STATE
# ============================================================

def initialize_tutor_state():
    """
    Initialize all Tutor-related Streamlit session-state
    variables.

    Database values are loaded separately through
    initialize_tts_preferences().
    """

    # ========================================================
    # CONVERSATION
    # ========================================================

    if "messages" not in st.session_state:

        st.session_state.messages = []


    # ========================================================
    # TUTOR SESSION
    # ========================================================

    if "tutor_session_id" not in st.session_state:

        st.session_state.tutor_session_id = None


    # ========================================================
    # LANGUAGE
    # ========================================================

    if "preferred_language" not in st.session_state:

        st.session_state.preferred_language = "English"


    # ========================================================
    # LEARNING PREFERENCES
    # ========================================================

    if "simple_explanation" not in st.session_state:

        st.session_state.simple_explanation = True


    if "step_by_step_learning" not in st.session_state:

        st.session_state.step_by_step_learning = True


    if "repetition_support" not in st.session_state:

        st.session_state.repetition_support = False


    if "visual_explanation" not in st.session_state:

        st.session_state.visual_explanation = True


    # ========================================================
    # STT
    # ========================================================

    if "stt_enabled" not in st.session_state:

        st.session_state.stt_enabled = False


    # ========================================================
    # TTS ENABLED
    # ========================================================

    if "tts_enabled" not in st.session_state:

        st.session_state.tts_enabled = (
            DEFAULT_TTS_ENABLED
        )


    # ========================================================
    # TTS AUTOPLAY
    # ========================================================

    if "tts_autoplay" not in st.session_state:

        st.session_state.tts_autoplay = (
            DEFAULT_TTS_AUTOPLAY
        )


    # ========================================================
    # TTS VOICE
    # ========================================================

    if "tts_voice" not in st.session_state:

        st.session_state.tts_voice = (
            DEFAULT_TTS_VOICE
        )


    # ========================================================
    # TTS RATE
    # ========================================================

    if "tts_rate" not in st.session_state:

        st.session_state.tts_rate = (
            DEFAULT_TTS_RATE
        )


    # ========================================================
    # TTS VOLUME
    # ========================================================

    if "tts_volume" not in st.session_state:

        st.session_state.tts_volume = (
            DEFAULT_TTS_VOLUME
        )


    # ========================================================
    # TTS PITCH
    # ========================================================

    if "tts_pitch" not in st.session_state:

        st.session_state.tts_pitch = (
            DEFAULT_TTS_PITCH
        )


    # ========================================================
    # DATABASE LOAD FLAG
    # ========================================================

    if "tts_preferences_loaded" not in st.session_state:

        st.session_state.tts_preferences_loaded = False


    # ========================================================
    # CURRENT USER ID
    # ========================================================

    if "tts_preferences_user_id" not in st.session_state:

        st.session_state.tts_preferences_user_id = None


    # ========================================================
    # SAVE STATUS
    # ========================================================

    if "tts_save_status" not in st.session_state:

        st.session_state.tts_save_status = "idle"


    # ========================================================
    # SAVE ERROR
    # ========================================================

    if "tts_save_error" not in st.session_state:

        st.session_state.tts_save_error = ""


# ============================================================
# LOAD USER TTS PREFERENCES
# ============================================================

def load_user_tts_preferences(
    user: User,
):
    """
    Load TTS preferences from a User database object
    into Streamlit session state.
    """

    if user is None:

        return


    # ========================================================
    # TTS ENABLED
    # ========================================================

    st.session_state.tts_enabled = bool(
        getattr(
            user,
            "text_to_speech",
            DEFAULT_TTS_ENABLED,
        )
    )


    # ========================================================
    # VOICE
    # ========================================================

    saved_voice = getattr(
        user,
        "tts_voice",
        DEFAULT_TTS_VOICE,
    )


    if saved_voice is None:

        saved_voice = DEFAULT_TTS_VOICE


    st.session_state.tts_voice = str(
        saved_voice
    )


    # ========================================================
    # AUTOPLAY
    # ========================================================

    autoplay = getattr(
        user,
        "tts_autoplay",
        DEFAULT_TTS_AUTOPLAY,
    )


    st.session_state.tts_autoplay = bool(
        autoplay
    )


    # ========================================================
    # RATE
    # ========================================================

    try:

        st.session_state.tts_rate = float(
            getattr(
                user,
                "tts_rate",
                DEFAULT_TTS_RATE,
            )
        )

    except (
        TypeError,
        ValueError,
    ):

        st.session_state.tts_rate = (
            DEFAULT_TTS_RATE
        )


    # ========================================================
    # VOLUME
    # ========================================================

    try:

        st.session_state.tts_volume = float(
            getattr(
                user,
                "tts_volume",
                DEFAULT_TTS_VOLUME,
            )
        )

    except (
        TypeError,
        ValueError,
    ):

        st.session_state.tts_volume = (
            DEFAULT_TTS_VOLUME
        )


    # ========================================================
    # PITCH
    # ========================================================

    try:

        st.session_state.tts_pitch = float(
            getattr(
                user,
                "tts_pitch",
                DEFAULT_TTS_PITCH,
            )
        )

    except (
        TypeError,
        ValueError,
    ):

        st.session_state.tts_pitch = (
            DEFAULT_TTS_PITCH
        )


    # ========================================================
    # MARK AS LOADED
    # ========================================================

    st.session_state.tts_preferences_loaded = True

    st.session_state.tts_preferences_user_id = (
        user.id
    )


# ============================================================
# INITIALIZE TTS PREFERENCES
# ============================================================

def initialize_tts_preferences(
    user: User,
):
    """
    Load database TTS preferences once for the current user.

    If another user logs in during the same Streamlit session,
    the preferences are loaded again for that user.
    """

    if user is None:

        return


    # ========================================================
    # CURRENT USER ID
    # ========================================================

    current_user_id = getattr(
        user,
        "id",
        None,
    )


    # ========================================================
    # PREVIOUS USER ID
    # ========================================================

    loaded_user_id = st.session_state.get(
        "tts_preferences_user_id",
        None,
    )


    # ========================================================
    # ALREADY LOADED FOR THIS USER
    # ========================================================

    if (
        st.session_state.get(
            "tts_preferences_loaded",
            False,
        )
        and loaded_user_id == current_user_id
    ):

        return


    # ========================================================
    # LOAD
    # ========================================================

    load_user_tts_preferences(
        user
    )


# ============================================================
# SAVE USER TTS PREFERENCES
# ============================================================

def save_user_tts_preferences(
    db,
    user: User,
):
    """
    Save all TTS preferences from Streamlit session state
    into the database.
    """

    # ========================================================
    # RESET STATUS
    # ========================================================

    st.session_state.tts_save_status = "idle"

    st.session_state.tts_save_error = ""


    # ========================================================
    # VALIDATE DATABASE
    # ========================================================

    if db is None:

        st.session_state.tts_save_status = "error"

        st.session_state.tts_save_error = (
            "Database session is not available."
        )

        return False


    # ========================================================
    # VALIDATE USER
    # ========================================================

    if user is None:

        st.session_state.tts_save_status = "error"

        st.session_state.tts_save_error = (
            "Logged-in user is not available."
        )

        return False


    # ========================================================
    # SAVE
    # ========================================================

    try:

        # ====================================================
        # ENABLED
        # ====================================================

        user.text_to_speech = bool(
            st.session_state.get(
                "tts_enabled",
                DEFAULT_TTS_ENABLED,
            )
        )


        # ====================================================
        # VOICE
        # ====================================================

        selected_voice = st.session_state.get(
            "tts_voice",
            DEFAULT_TTS_VOICE,
        )


        if selected_voice is None:

            selected_voice = DEFAULT_TTS_VOICE


        user.tts_voice = str(
            selected_voice
        )


        # ====================================================
        # AUTOPLAY
        # ====================================================

        if hasattr(
            user,
            "tts_autoplay",
        ):

            user.tts_autoplay = bool(
                st.session_state.get(
                    "tts_autoplay",
                    DEFAULT_TTS_AUTOPLAY,
                )
            )


        # ====================================================
        # RATE
        # ====================================================

        if hasattr(
            user,
            "tts_rate",
        ):

            user.tts_rate = str(
                st.session_state.get(
                    "tts_rate",
                    DEFAULT_TTS_RATE,
                )
            )


        # ====================================================
        # VOLUME
        # ====================================================

        if hasattr(
            user,
            "tts_volume",
        ):

            user.tts_volume = str(
                st.session_state.get(
                    "tts_volume",
                    DEFAULT_TTS_VOLUME,
                )
            )


        # ====================================================
        # PITCH
        # ====================================================

        if hasattr(
            user,
            "tts_pitch",
        ):

            user.tts_pitch = str(
                st.session_state.get(
                    "tts_pitch",
                    DEFAULT_TTS_PITCH,
                )
            )


        # ====================================================
        # COMMIT
        # ====================================================

        db.commit()


        # ====================================================
        # REFRESH
        # ====================================================

        db.refresh(
            user
        )


        # ====================================================
        # SYNCHRONIZE SESSION STATE
        # ====================================================

        st.session_state.tts_enabled = bool(
            user.text_to_speech
        )


        st.session_state.tts_voice = (
            user.tts_voice or ""
        )


        if hasattr(
            user,
            "tts_autoplay",
        ):

            st.session_state.tts_autoplay = bool(
                user.tts_autoplay
            )


        try:

            st.session_state.tts_rate = float(
                user.tts_rate
            )

        except (
            TypeError,
            ValueError,
        ):

            st.session_state.tts_rate = (
                DEFAULT_TTS_RATE
            )


        try:

            st.session_state.tts_volume = float(
                user.tts_volume
            )

        except (
            TypeError,
            ValueError,
        ):

            st.session_state.tts_volume = (
                DEFAULT_TTS_VOLUME
            )


        try:

            st.session_state.tts_pitch = float(
                user.tts_pitch
            )

        except (
            TypeError,
            ValueError,
        ):

            st.session_state.tts_pitch = (
                DEFAULT_TTS_PITCH
            )


        # ====================================================
        # MARK CURRENT USER AS LOADED
        # ====================================================

        st.session_state.tts_preferences_loaded = True

        st.session_state.tts_preferences_user_id = (
            user.id
        )


        # ====================================================
        # SUCCESS
        # ====================================================

        st.session_state.tts_save_status = "saved"

        st.session_state.tts_save_error = ""


        return True


    except Exception as error:

        # ====================================================
        # ROLLBACK
        # ====================================================

        db.rollback()


        # ====================================================
        # ERROR
        # ====================================================

        st.session_state.tts_save_status = "error"

        st.session_state.tts_save_error = str(
            error
        )


        return False


# ============================================================
# TTS SAVE BUTTON
# ============================================================

def show_tts_save_button(
    db,
    user: User,
):
    """
    Display the Save TTS Preferences button.
    """

    st.markdown(
        "#### 💾 Save TTS Preferences"
    )


    # ========================================================
    # CURRENT VOICE
    # ========================================================

    current_voice = st.session_state.get(
        "tts_voice",
        DEFAULT_TTS_VOICE,
    )


    if current_voice:

        st.caption(
            f"🎙️ Selected voice: {current_voice}"
        )

    else:

        st.caption(
            "🎙️ Selected voice: Automatic browser voice"
        )


    # ========================================================
    # CURRENT STATUS
    # ========================================================

    if st.session_state.get(
        "tts_enabled",
        False,
    ):

        st.caption(
            "🔊 Text-to-Speech: Enabled"
        )

    else:

        st.caption(
            "🔇 Text-to-Speech: Disabled"
        )


    # ========================================================
    # SAVE BUTTON
    # ========================================================

    save_clicked = st.button(
        "💾 Save Voice Settings",
        key="save_tts_preferences_button",
        use_container_width=True,
    )


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
                    "❌ Unable to save TTS preferences: "
                    f"{error_message}"
                )

            else:

                st.error(
                    "❌ Unable to save TTS preferences."
                )


    # ========================================================
    # PERSISTENT STATUS
    # ========================================================

    elif st.session_state.get(
        "tts_save_status",
        "idle",
    ) == "saved":

        st.success(
            "✅ TTS preferences are saved."
        )


    elif st.session_state.get(
        "tts_save_status",
        "idle",
    ) == "error":

        error_message = st.session_state.get(
            "tts_save_error",
            "",
        )


        if error_message:

            st.error(
                f"❌ {error_message}"
            )


# ============================================================
# VOICE NAME EXTRACTION
# ============================================================

def _get_voice_names(
    voices,
):
    """
    Convert the voice objects returned by the TTS module
    into unique voice names.
    """

    names = []


    for voice in voices or []:

        if isinstance(
            voice,
            dict,
        ):

            name = voice.get(
                "name",
                "",
            )

        else:

            name = getattr(
                voice,
                "name",
                voice,
            )


        if name:

            names.append(
                str(name)
            )


    return list(
        dict.fromkeys(
            names
        )
    )


# ============================================================
# TEST CURRENT VOICE
# ============================================================

def show_tts_test_voice(
):
    """
    Display a Test Voice button using the current TTS
    session-state settings.
    """

    st.markdown(
        "#### 🔊 Test Voice"
    )


    if st.button(
        "🔊 Test Selected Voice",
        key="test_tts_voice_button",
        use_container_width=True,
    ):

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
            DEFAULT_TTS_VOICE,
        )


        speech_rate = st.session_state.get(
            "tts_rate",
            DEFAULT_TTS_RATE,
        )


        volume = st.session_state.get(
            "tts_volume",
            DEFAULT_TTS_VOLUME,
        )


        pitch = st.session_state.get(
            "tts_pitch",
            DEFAULT_TTS_PITCH,
        )


        try:

            test_voice(
                language=language_code,
                selected_voice=selected_voice,
                speech_rate=speech_rate,
                volume=volume,
                pitch=pitch,
            )

        except Exception as error:

            st.error(
                f"❌ Unable to test voice: {error}"
            )


# ============================================================
# TTS SETTINGS PANEL
# ============================================================

def show_tts_settings_panel(
    db,
    current_user: User,
):
    """
    Display the complete TTS settings panel.
    """

    if current_user is None:

        st.warning(
            "Please log in to manage TTS preferences."
        )

        return


    with st.expander(
        "🔊 Text-to-Speech Settings",
        expanded=False,
    ):

        # ====================================================
        # ENABLE TTS
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


        # ====================================================
        # GET VOICES
        # ====================================================

        try:

            available_voices = (
                get_available_voices()
            )

        except Exception:

            available_voices = []


        voice_names = _get_voice_names(
            available_voices
        )


        # ====================================================
        # CURRENT VOICE
        # ====================================================

        current_voice = st.session_state.get(
            "tts_voice",
            DEFAULT_TTS_VOICE,
        )


        # ====================================================
        # VOICE SELECTOR
        # ====================================================

        if voice_names:

            options = [
                "",
                *voice_names,
            ]


            if current_voice in options:

                current_index = options.index(
                    current_voice
                )

            else:

                current_index = 0


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

        else:

            st.info(
                "Browser voices are detected when speech "
                "is played. You can still use the browser's "
                "default voice or enter a saved voice later."
            )


        # ====================================================
        # RATE
        # ====================================================

        st.slider(
            "Speech Rate",
            min_value=0.5,
            max_value=2.0,
            value=float(
                st.session_state.get(
                    "tts_rate",
                    DEFAULT_TTS_RATE,
                )
            ),
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
            value=float(
                st.session_state.get(
                    "tts_volume",
                    DEFAULT_TTS_VOLUME,
                )
            ),
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
            value=float(
                st.session_state.get(
                    "tts_pitch",
                    DEFAULT_TTS_PITCH,
                )
            ),
            step=0.1,
            key="tts_pitch",
        )


        # ====================================================
        # CURRENT SETTINGS
        # ====================================================

        st.markdown(
            "---"
        )


        selected_voice = st.session_state.get(
            "tts_voice",
            DEFAULT_TTS_VOICE,
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
        # TEST VOICE
        # ====================================================

        show_tts_test_voice()


        # ====================================================
        # SAVE
        # ====================================================

        show_tts_save_button(
            db=db,
            user=current_user,
        )


# ============================================================
# SPEAK TUTOR ANSWER
# ============================================================

def speak_tutor_answer(
    answer: str,
):
    """
    Speak a Tutor answer using the current saved TTS
    preferences stored in Streamlit session state.
    """

    # ========================================================
    # EMPTY ANSWER
    # ========================================================

    if not answer:

        return


    # ========================================================
    # TTS ENABLED
    # ========================================================

    if not st.session_state.get(
        "tts_enabled",
        False,
    ):

        return


    # ========================================================
    # LANGUAGE
    # ========================================================

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


    # ========================================================
    # SAVED VOICE
    # ========================================================

    selected_voice = st.session_state.get(
        "tts_voice",
        DEFAULT_TTS_VOICE,
    )


    # ========================================================
    # RATE
    # ========================================================

    speech_rate = st.session_state.get(
        "tts_rate",
        DEFAULT_TTS_RATE,
    )


    # ========================================================
    # VOLUME
    # ========================================================

    volume = st.session_state.get(
        "tts_volume",
        DEFAULT_TTS_VOLUME,
    )


    # ========================================================
    # PITCH
    # ========================================================

    pitch = st.session_state.get(
        "tts_pitch",
        DEFAULT_TTS_PITCH,
    )


    # ========================================================
    # AUTOPLAY
    # ========================================================

    autoplay = st.session_state.get(
        "tts_autoplay",
        DEFAULT_TTS_AUTOPLAY,
    )


    # ========================================================
    # SPEAK
    # ========================================================

    show_text_to_speech(
        text=answer,
        autoplay=autoplay,
        language=language_code,
        selected_voice=selected_voice,
        speech_rate=speech_rate,
        volume=volume,
        pitch=pitch,
    )


# ============================================================
# GET TTS SETTINGS
# ============================================================

def get_tts_settings():
    """
    Return the current TTS settings.
    """

    return {

        "enabled": bool(
            st.session_state.get(
                "tts_enabled",
                DEFAULT_TTS_ENABLED,
            )
        ),

        "autoplay": bool(
            st.session_state.get(
                "tts_autoplay",
                DEFAULT_TTS_AUTOPLAY,
            )
        ),

        "voice": st.session_state.get(
            "tts_voice",
            DEFAULT_TTS_VOICE,
        ),

        "rate": float(
            st.session_state.get(
                "tts_rate",
                DEFAULT_TTS_RATE,
            )
        ),

        "volume": float(
            st.session_state.get(
                "tts_volume",
                DEFAULT_TTS_VOLUME,
            )
        ),

        "pitch": float(
            st.session_state.get(
                "tts_pitch",
                DEFAULT_TTS_PITCH,
            )
        ),
    }


# ============================================================
# TTS PREFERENCE SUMMARY
# ============================================================

def show_tts_preference_summary():
    """
    Display the current TTS preference summary.
    """

    settings = get_tts_settings()


    st.markdown(
        "#### 🔊 TTS Preference Summary"
    )


    # ========================================================
    # STATUS
    # ========================================================

    if settings["enabled"]:

        st.write(
            "🔊 **TTS:** Enabled"
        )

    else:

        st.write(
            "🔇 **TTS:** Disabled"
        )


    # ========================================================
    # VOICE
    # ========================================================

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


    # ========================================================
    # AUTOPLAY
    # ========================================================

    if settings["autoplay"]:

        st.write(
            "▶️ **Autoplay:** Enabled"
        )

    else:

        st.write(
            "⏸️ **Autoplay:** Disabled"
        )


    # ========================================================
    # RATE
    # ========================================================

    st.write(
        f"⚡ **Rate:** "
        f"{settings['rate']:.1f}"
    )


    # ========================================================
    # VOLUME
    # ========================================================

    st.write(
        f"🔊 **Volume:** "
        f"{settings['volume']:.1f}"
    )


    # ========================================================
    # PITCH
    # ========================================================

    st.write(
        f"🎵 **Pitch:** "
        f"{settings['pitch']:.1f}"
    )


# ============================================================
# DATABASE SESSION
# ============================================================

def get_tts_database_session():
    """
    Create a SQLAlchemy database session.
    """

    return SessionLocal()


# ============================================================
# INITIALIZE TUTOR FOR LOGGED-IN USER
# ============================================================

def initialize_tutor_for_user(
    current_user: User,
):
    """
    Initialize Tutor state and load the logged-in user's
    TTS preferences.
    """

    initialize_tutor_state()

    initialize_tts_preferences(
        current_user
    )


# ============================================================
# TUTOR PAGE ENTRY
# ============================================================

def initialize_tutor_page(
    current_user: User,
):
    """
    Optional complete Tutor initialization helper.

    Use this when the Tutor page needs to initialize TTS
    settings and display the settings panel.
    """

    if current_user is None:

        st.warning(
            "No logged-in user was provided."
        )

        return


    # ========================================================
    # INITIALIZE
    # ========================================================

    initialize_tutor_for_user(
        current_user
    )


    # ========================================================
    # DATABASE
    # ========================================================

    db = get_tts_database_session()


    try:

        # ====================================================
        # SETTINGS
        # ====================================================

        show_tts_settings_panel(
            db=db,
            current_user=current_user,
        )


        # ====================================================
        # SUMMARY
        # ====================================================

        show_tts_preference_summary()


    finally:

        db.close()


# ============================================================
# END OF app/ui/tutor.py
# ============================================================
