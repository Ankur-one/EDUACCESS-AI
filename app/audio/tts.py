# ============================================================
# app/audio/tts.py
# EduAccess AI
# Browser Text-to-Speech
# ============================================================

import importlib
import json


# ============================================================
# STREAMLIT
# ============================================================

try:
    st = importlib.import_module("streamlit")
except ModuleNotFoundError:
    st = None


# ============================================================
# LANGUAGE MAP
# ============================================================

TTS_LANGUAGE_MAP = {
    "English": "en-US",
    "Hindi": "hi-IN",
    "Punjabi": "pa-IN",
    "Bengali": "bn-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Marathi": "mr-IN",
    "Gujarati": "gu-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Urdu": "ur-IN",
}


# ============================================================
# DEFAULT VALUES
# ============================================================

DEFAULT_LANGUAGE = "en-US"
DEFAULT_RATE = 0.9
DEFAULT_VOLUME = 1.0
DEFAULT_PITCH = 1.0


def _require_streamlit():
    """Ensure Streamlit is available before rendering HTML."""

    if st is None:
        raise RuntimeError(
            "streamlit is required to display browser TTS output."
        )

    return st


# ============================================================
# KNOWN BROWSER VOICE NAMES
#
# IMPORTANT:
# These are only suggestions/options.
#
# The browser decides whether a particular voice exists.
# ============================================================

KNOWN_VOICE_NAMES = [
    "Microsoft David",
    "Microsoft Zira",
    "Microsoft Mark",
    "Microsoft Heera",
    "Microsoft Ravi",
    "Microsoft Swara",
    "Microsoft Kalpana",
    "Google US English",
    "Google UK English Female",
    "Google UK English Male",
    "Google हिन्दी",
    "Google हिंदी",
    "Google Deutsch",
    "Google français",
    "Google español",
    "Samantha",
    "Alex",
    "Daniel",
    "Karen",
    "Moira",
    "Veena",
]


# ============================================================
# GET TTS LANGUAGE
# ============================================================

def get_tts_language(
    language_name: str,
) -> str:
    """
    Convert application language to browser
    SpeechSynthesis language code.
    """

    if not language_name:

        return DEFAULT_LANGUAGE


    language_name = str(
        language_name
    ).strip()


    return TTS_LANGUAGE_MAP.get(
        language_name,
        DEFAULT_LANGUAGE,
    )


# ============================================================
# SAFE FLOAT
# ============================================================

def _safe_float(
    value,
    default,
    minimum,
    maximum,
):
    """
    Safely convert a value into a float.
    """

    try:

        value = float(value)

    except (
        TypeError,
        ValueError,
    ):

        value = default


    return max(
        minimum,
        min(
            maximum,
            value,
        ),
    )


# ============================================================
# GET AVAILABLE TTS VOICES
# ============================================================

def get_available_tts_voices():
    """
    Return known browser voice names.

    Actual browser voice availability is determined
    by JavaScript in the user's browser.
    """

    return [
        {
            "name": voice_name,
        }
        for voice_name in KNOWN_VOICE_NAMES
    ]


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def get_available_voices():
    """
    Backward-compatible alias.
    """

    return get_available_tts_voices()


# ============================================================
# BUILD TTS HTML
# ============================================================

def _build_tts_html(
    text: str,
    autoplay: bool,
    language: str,
    selected_voice: str,
    speech_rate: float,
    volume: float,
    pitch: float,
):
    """
    Generate browser-side SpeechSynthesis JavaScript.
    """

    text_json = json.dumps(
        text,
        ensure_ascii=False,
    )

    language_json = json.dumps(
        language,
        ensure_ascii=False,
    )

    voice_json = json.dumps(
        selected_voice,
        ensure_ascii=False,
    )

    autoplay_json = json.dumps(
        bool(autoplay)
    )

    rate_json = json.dumps(
        speech_rate
    )

    volume_json = json.dumps(
        volume
    )

    pitch_json = json.dumps(
        pitch
    )


    html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<style>

body {{
    margin: 0;
    padding: 0;
    overflow: hidden;
    font-family: Arial, sans-serif;
}}

.tts-container {{
    display: flex;
    gap: 8px;
    align-items: center;
}}

.tts-button {{
    border: 1px solid #888;
    border-radius: 6px;
    padding: 8px 14px;
    background: white;
    cursor: pointer;
    font-size: 14px;
}}

.tts-button:hover {{
    background: #eeeeee;
}}

</style>

</head>


<body>

<div class="tts-container">

<button
    class="tts-button"
    onclick="speakText()"
>
🔊 Speak
</button>

<button
    class="tts-button"
    onclick="stopSpeech()"
>
⏹ Stop
</button>

</div>


<script>

(function() {{

    const text = {text_json};

    const language = {language_json};

    const selectedVoiceName = {voice_json};

    const autoplay = {autoplay_json};

    const speechRate = {rate_json};

    const speechVolume = {volume_json};

    const speechPitch = {pitch_json};


    // ========================================================
    // STOP
    // ========================================================

    window.stopSpeech = function() {{

        if (
            "speechSynthesis" in window
        ) {{

            window.speechSynthesis.cancel();

        }}

    }};


    // ========================================================
    // GET BROWSER VOICES
    // ========================================================

    function getBrowserVoices() {{

        if (
            !("speechSynthesis" in window)
        ) {{

            return [];

        }}


        return window.speechSynthesis
            .getVoices();

    }}


    // ========================================================
    // FIND VOICE
    // ========================================================

    function findVoice() {{

        const voices =
            getBrowserVoices();


        if (
            !voices ||
            voices.length === 0
        ) {{

            return null;

        }}


        // ----------------------------------------------------
        // EXACT NAME MATCH
        // ----------------------------------------------------

        if (selectedVoiceName) {{

            const exact =
                voices.find(
                    function(voice) {{

                        return (
                            voice.name ===
                            selectedVoiceName
                        );

                    }}
                );


            if (exact) {{

                return exact;

            }}


            // ------------------------------------------------
            // PARTIAL NAME MATCH
            // ------------------------------------------------

            const partial =
                voices.find(
                    function(voice) {{

                        return voice.name
                            .toLowerCase()
                            .includes(
                                selectedVoiceName
                                    .toLowerCase()
                            );

                    }}
                );


            if (partial) {{

                return partial;

            }}

        }}


        // ----------------------------------------------------
        // LANGUAGE MATCH
        // ----------------------------------------------------

        const languagePrefix =
            language
                .toLowerCase()
                .split("-")[0];


        const languageVoice =
            voices.find(
                function(voice) {{

                    if (!voice.lang) {{

                        return false;

                    }}


                    return voice.lang
                        .toLowerCase()
                        .startsWith(
                            languagePrefix
                        );

                }}
            );


        if (languageVoice) {{

            return languageVoice;

        }}


        // ----------------------------------------------------
        // DEFAULT
        // ----------------------------------------------------

        return voices[0];

    }}


    // ========================================================
    // SPEAK
    // ========================================================

    window.speakText = function() {{

        if (
            !("speechSynthesis" in window)
        ) {{

            console.error(
                "SpeechSynthesis is not supported."
            );

            return;

        }}


        window.speechSynthesis.cancel();


        const utterance =
            new SpeechSynthesisUtterance(
                text
            );


        utterance.lang = language;

        utterance.rate = speechRate;

        utterance.volume = speechVolume;

        utterance.pitch = speechPitch;


        const selectedVoice =
            findVoice();


        if (selectedVoice) {{

            utterance.voice =
                selectedVoice;

        }}


        window.speechSynthesis.speak(
            utterance
        );

    }};


    // ========================================================
    // LOAD VOICES
    // ========================================================

    function loadVoices() {{

        if (
            !("speechSynthesis" in window)
        ) {{

            return;

        }}


        window.speechSynthesis
            .getVoices();

    }}


    loadVoices();


    // ========================================================
    // VOICES CHANGED
    // ========================================================

    if (
        "speechSynthesis" in window
    ) {{

        window.speechSynthesis
            .addEventListener(
                "voiceschanged",
                loadVoices
            );

    }}


    // ========================================================
    // AUTOPLAY
    // ========================================================

    if (autoplay) {{

        setTimeout(
            function() {{

                window.speakText();

            }},
            700
        );

    }}

}})();

</script>

</body>

</html>
"""


    return html


# ============================================================
# SHOW TEXT TO SPEECH
# ============================================================

def show_text_to_speech(
    text: str,
    autoplay: bool = False,
    language: str = DEFAULT_LANGUAGE,
    selected_voice: str = "",
    speech_rate: float = DEFAULT_RATE,
    volume: float = DEFAULT_VOLUME,
    pitch: float = DEFAULT_PITCH,
):
    """
    Display the browser TTS controls.
    """

    if text is None:

        return


    text = str(
        text
    ).strip()


    if not text:

        return


    # ========================================================
    # NORMALIZE SETTINGS
    # ========================================================

    language = (
        str(language)
        if language
        else DEFAULT_LANGUAGE
    )


    selected_voice = (
        str(selected_voice)
        if selected_voice
        else ""
    )


    speech_rate = _safe_float(
        speech_rate,
        DEFAULT_RATE,
        0.5,
        2.0,
    )


    volume = _safe_float(
        volume,
        DEFAULT_VOLUME,
        0.0,
        1.0,
    )


    pitch = _safe_float(
        pitch,
        DEFAULT_PITCH,
        0.5,
        2.0,
    )


    # ========================================================
    # CREATE HTML
    # ========================================================

    html = _build_tts_html(
        text=text,
        autoplay=autoplay,
        language=language,
        selected_voice=selected_voice,
        speech_rate=speech_rate,
        volume=volume,
        pitch=pitch,
    )


    # ========================================================
    # DISPLAY
    # ========================================================

    st.components.v1.html(
        html,
        height=60,
        scrolling=False,
    )


# ============================================================
# TEST VOICE
# ============================================================

def test_voice(
    language: str = DEFAULT_LANGUAGE,
    selected_voice: str = "",
    speech_rate: float = DEFAULT_RATE,
    volume: float = DEFAULT_VOLUME,
    pitch: float = DEFAULT_PITCH,
):
    """
    Test the currently selected voice.
    """

    # --------------------------------------------------------
    # Language-specific test sentence
    # --------------------------------------------------------

    if language == "hi-IN":

        test_text = (
            "नमस्ते। यह EduAccess AI की "
            "टेक्स्ट टू स्पीच आवाज़ का परीक्षण है।"
        )

    elif language == "pa-IN":

        test_text = (
            "ਸਤ ਸ੍ਰੀ ਅਕਾਲ। ਇਹ EduAccess AI "
            "ਦੀ ਟੈਕਸਟ ਟੂ ਸਪੀਚ ਆਵਾਜ਼ ਦਾ ਟੈਸਟ ਹੈ।"
        )

    else:

        test_text = (
            "Hello. This is a test of the "
            "EduAccess AI text to speech system."
        )


    show_text_to_speech(
        text=test_text,
        autoplay=True,
        language=language,
        selected_voice=selected_voice,
        speech_rate=speech_rate,
        volume=volume,
        pitch=pitch,
    )


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def test_text_to_speech(
    language: str = DEFAULT_LANGUAGE,
    selected_voice: str = "",
    speech_rate: float = DEFAULT_RATE,
    volume: float = DEFAULT_VOLUME,
    pitch: float = DEFAULT_PITCH,
):
    """
    Backward-compatible test function.
    """

    return test_voice(
        language=language,
        selected_voice=selected_voice,
        speech_rate=speech_rate,
        volume=volume,
        pitch=pitch,
    )


# ============================================================
# STOP SPEECH
# ============================================================

def stop_text_to_speech():
    """
    Stop browser speech.
    """

    html = """
<script>

if ("speechSynthesis" in window) {

    window.speechSynthesis.cancel();

}

</script>
"""


    st.components.v1.html(
        html,
        height=0,
        scrolling=False,
    )


# ============================================================
# VALIDATE SETTINGS
# ============================================================

def validate_tts_settings(
    language: str = DEFAULT_LANGUAGE,
    selected_voice: str = "",
    speech_rate: float = DEFAULT_RATE,
    volume: float = DEFAULT_VOLUME,
    pitch: float = DEFAULT_PITCH,
):
    """
    Return validated TTS settings.
    """

    return {

        "language": (
            str(language)
            if language
            else DEFAULT_LANGUAGE
        ),

        "selected_voice": (
            str(selected_voice)
            if selected_voice
            else ""
        ),

        "speech_rate": _safe_float(
            speech_rate,
            DEFAULT_RATE,
            0.5,
            2.0,
        ),

        "volume": _safe_float(
            volume,
            DEFAULT_VOLUME,
            0.0,
            1.0,
        ),

        "pitch": _safe_float(
            pitch,
            DEFAULT_PITCH,
            0.5,
            2.0,
        ),

    }


# ============================================================
# END OF TTS MODULE
# ============================================================
