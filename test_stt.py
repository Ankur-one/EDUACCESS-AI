import importlib

from app.audio.stt import show_speech_to_text

# Load Streamlit dynamically so editors do not report a missing static import
# when the selected Python environment does not provide package type metadata.
st = importlib.import_module("streamlit")


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EduAccess AI - STT Test",
    page_icon="🎤",
    layout="centered",
)


# ============================================================
# HEADER
# ============================================================

st.title(
    "🎤 EduAccess AI - Speech-to-Text Test"
)

st.caption(
    "Standalone test for microphone and "
    "multilingual speech recognition."
)

st.divider()


# ============================================================
# LANGUAGE OPTIONS
# ============================================================

language_options = {
    "English (India)": "en-IN",
    "Hindi (India)": "hi-IN",
    "Punjabi (India)": "pa-IN",
    "Bengali (India)": "bn-IN",
    "Tamil (India)": "ta-IN",
    "Telugu (India)": "te-IN",
    "Marathi (India)": "mr-IN",
    "Gujarati (India)": "gu-IN",
    "Kannada (India)": "kn-IN",
    "Malayalam (India)": "ml-IN",
    "Odia (India)": "or-IN",
    "Assamese (India)": "as-IN",
    "Urdu (India)": "ur-IN",
}


# ============================================================
# LANGUAGE SELECTION
# ============================================================

st.subheader(
    "🌐 Speech Recognition Language"
)

selected_language_name = st.selectbox(
    "Select the language you will speak:",
    options=list(
        language_options.keys()
    ),
    index=0,
)


selected_language_code = (
    language_options[
        selected_language_name
    ]
)


# ============================================================
# SHOW SELECTED LANGUAGE
# ============================================================

st.info(
    f"""
🌐 **Selected Language:** {selected_language_name}

🔤 **Recognition Code:** `{selected_language_code}`
"""
)


st.divider()


# ============================================================
# INSTRUCTIONS
# ============================================================

st.subheader(
    "🎙️ Microphone Test"
)

st.write(
    """
Follow these steps:

1. Click **Start Recording**.
2. Allow microphone access when the browser asks.
3. Speak clearly.
4. Click **Stop Recording**.
5. Wait for speech recognition.
6. Check the recognized text below.
"""
)


# ============================================================
# SPEECH TO TEXT
# ============================================================

recognized_text = ""

try:

    recognized_text = show_speech_to_text(
        language=selected_language_code
    )

except Exception as error:

    st.error(
        "❌ Speech-to-text test failed."
    )

    st.exception(
        error
    )


# ============================================================
# RECOGNIZED RESULT
# ============================================================

if recognized_text:

    st.divider()

    st.subheader(
        "📝 Recognized Text"
    )

    st.success(
        "✅ Speech recognized successfully!"
    )

    st.text_area(
        "Your speech:",
        value=recognized_text,
        height=120,
        disabled=True,
        key="stt_test_result",
    )

    # --------------------------------------------------------
    # CHARACTER / WORD INFORMATION
    # --------------------------------------------------------

    word_count = len(
        recognized_text.split()
    )

    character_count = len(
        recognized_text
    )

    st.write(
        f"**Words:** {word_count}"
    )

    st.write(
        f"**Characters:** {character_count}"
    )

else:

    st.divider()

    st.caption(
        "🎤 No speech has been recognized yet."
    )


# ============================================================
# STATUS
# ============================================================

st.divider()

st.subheader(
    "🔍 STT Test Status"
)

st.write(
    "Speech-to-text module: ✅ Loaded"
)

st.write(
    f"Language: **{selected_language_name}**"
)

st.write(
    f"Language code: **{selected_language_code}**"
)

st.write(
    "Mode: **Standalone Test**"
)