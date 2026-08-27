import io
import importlib


# ============================================================
# LOAD OPTIONAL DEPENDENCIES
# ============================================================

mic_recorder = importlib.import_module(
    "streamlit_mic_recorder"
).mic_recorder


st = importlib.import_module(
    "streamlit"
)


sr = importlib.import_module(
    "speech_recognition"
)


# ============================================================
# SPEECH TO TEXT
# ============================================================

def transcribe_audio(
    audio_bytes: bytes,
    language: str = "en-IN",
) -> str:
    """
    Convert recorded WAV audio into text.

    Parameters
    ----------
    audio_bytes:
        Recorded WAV audio bytes.

    language:
        Speech recognition language code.

    Returns
    -------
    str
        Recognized speech text.
    """

    # ========================================================
    # VALIDATE AUDIO
    # ========================================================

    if not audio_bytes:
        return ""

    recognizer = sr.Recognizer()

    try:

        # ====================================================
        # CONVERT BYTES TO FILE-LIKE OBJECT
        # ====================================================

        audio_file = io.BytesIO(
            audio_bytes
        )

        # ====================================================
        # READ WAV AUDIO
        # ====================================================

        with sr.AudioFile(
            audio_file
        ) as source:

            audio = recognizer.record(
                source
            )

        # ====================================================
        # GOOGLE SPEECH RECOGNITION
        # ====================================================

        text = recognizer.recognize_google(
            audio,
            language=language,
        )

        return text.strip()

    # ========================================================
    # SPEECH COULD NOT BE UNDERSTOOD
    # ========================================================

    except sr.UnknownValueError:

        return ""

    # ========================================================
    # SPEECH RECOGNITION SERVICE ERROR
    # ========================================================

    except sr.RequestError as error:

        raise RuntimeError(
            "The speech recognition service is "
            "temporarily unavailable. Please check "
            "your internet connection and try again."
        ) from error

    # ========================================================
    # GENERAL AUDIO PROCESSING ERROR
    # ========================================================

    except Exception as error:

        raise RuntimeError(
            "The voice recording could not be processed. "
            "Please try recording again."
        ) from error


# ============================================================
# MICROPHONE
# ============================================================

def show_speech_to_text(
    language: str = "en-IN",
):
    """
    Display the microphone recorder and convert
    the recording into text.

    Parameters
    ----------
    language:
        Speech recognition language code.

    Returns
    -------
    str
        Recognized speech text.
    """

    # ========================================================
    # HEADER
    # ========================================================

    st.markdown(
        "### 🎤 Voice Question"
    )

    st.caption(
        "Click Start Recording, speak clearly, "
        "then click Stop Recording."
    )

    # ========================================================
    # ACTIVE LANGUAGE
    # ========================================================

    st.info(
        f"🌐 Recognition language: **{language}**"
    )

    # ========================================================
    # MICROPHONE RECORDER
    # ========================================================

    audio_data = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹️ Stop Recording",
        just_once=True,
        use_container_width=True,
        format="wav",
        key="tutor_microphone",
    )

    # ========================================================
    # NO RECORDING
    # ========================================================

    if not audio_data:

        return ""

    # ========================================================
    # GET AUDIO BYTES
    # ========================================================

    audio_bytes = audio_data.get(
        "bytes"
    )

    if not audio_bytes:

        st.warning(
            "⚠️ No audio was received. "
            "Please record your question again."
        )

        return ""

    # ========================================================
    # AUDIO PLAYER
    # ========================================================

    st.audio(
        audio_bytes,
        format="audio/wav",
    )

    # ========================================================
    # TRANSCRIBE AUDIO
    # ========================================================

    with st.spinner(
        "🎤 Converting your speech to text..."
    ):

        try:

            text = transcribe_audio(
                audio_bytes=audio_bytes,
                language=language,
            )

        except RuntimeError as error:

            st.error(
                f"❌ {error}"
            )

            st.info(
                "💡 Try recording again after checking "
                "your microphone and internet connection."
            )

            return ""

    # ========================================================
    # SPEECH NOT UNDERSTOOD
    # ========================================================

    if not text:

        st.warning(
            "⚠️ I couldn't understand the recording."
        )

        st.info(
            "💡 Tips:\n\n"
            "- Speak a little more slowly.\n"
            "- Keep the microphone close to you.\n"
            "- Reduce background noise.\n"
            "- Make sure you selected the correct language.\n"
            "- Try recording again."
        )

        return ""

    # ========================================================
    # SUCCESS
    # ========================================================

    st.success(
        "✅ Your question was recognized."
    )

    # ========================================================
    # DISPLAY RECOGNIZED QUESTION
    # ========================================================

    st.markdown(
        "#### 📝 Recognized Question"
    )

    st.info(
        text
    )

    # ========================================================
    # RETURN RECOGNIZED TEXT
    # ========================================================

    return text