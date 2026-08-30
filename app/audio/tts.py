# ============================================================
# app/audio/tts.py
# EDUACCESS-AI — TEXT TO SPEECH
# ============================================================
# NOTE: This file must not contain Markdown code fences such as
# ```python ... ``` . If copied from documentation, strip them
# before saving or the Python parser will fail on the opening tick.

import json

try:
    import streamlit as st  # type: ignore
    import streamlit.components.v1 as components  # type: ignore
except ImportError:  # pragma: no cover
    class _MissingStreamlitModule:
        def __getattr__(self, _name):
            raise RuntimeError("streamlit is required to run EduAccess-AI TTS.")

    class _MissingComponentsModule:
        @staticmethod
        def html(*args, **kwargs):
            raise RuntimeError("streamlit is required to run EduAccess-AI TTS.")

    st = _MissingStreamlitModule()
    components = _MissingComponentsModule()


# ============================================================
# LANGUAGE MAPPING
# ============================================================

TTS_LANGUAGES = {
    "English": "en-US",
    "Hindi": "hi-IN",
    "Punjabi": "pa-IN",
}


def _strip_markdown_fences(code: str) -> str:
    """
    Remove accidental Markdown code fences from copied/pasted snippets.
    This prevents Python syntax errors caused by stray backticks at the
    start of a file or script block.
    """
    if not isinstance(code, str):
        return code

    cleaned = code.strip()

    if not cleaned.startswith("```"):
        return cleaned

    lines = cleaned.splitlines()

    if lines and lines[0].startswith("```"):
        lines = lines[1:]

    if lines and lines[-1].rstrip().endswith("```"):
        lines[-1] = lines[-1].rstrip()
        if lines[-1].endswith("```"):
            lines[-1] = lines[-1][:-3].rstrip()

    cleaned = "\n".join(lines).strip()

    if cleaned.startswith("python"):
        cleaned = cleaned[6:].lstrip()

    return cleaned


# ============================================================
# GET TTS LANGUAGE
# ============================================================

def get_tts_language(language_name: str) -> str:
    """
    Convert application language name to browser TTS language code.
    """

    if not language_name:
        return "en-US"

    return TTS_LANGUAGES.get(
        str(language_name),
        "en-US",
    )


# ============================================================
# GET AVAILABLE TTS VOICES
# ============================================================

def get_available_tts_voices():
    """
    Return an empty list on the Python side.

    Browser speech voices are actually discovered by JavaScript
    inside the user's browser.

    This function is kept for compatibility with tutor.py.
    """

    return []


# ============================================================
# BACKWARD-COMPATIBILITY ALIAS
# ============================================================

def get_available_voices():
    """
    Compatibility alias used by older tutor.py versions.
    """

    return get_available_tts_voices()


# ============================================================
# BUILD TTS JAVASCRIPT
# ============================================================

def _build_tts_javascript(
    text: str,
    language: str = "en-US",
    selected_voice: str = "",
    speech_rate: float = 0.9,
    volume: float = 1.0,
    pitch: float = 1.0,
    autoplay: bool = True,
) -> str:
    """
    Build browser JavaScript for SpeechSynthesis.
    """

    safe_text = json.dumps(
        str(text)
    )

    safe_language = json.dumps(
        str(language or "en-US")
    )

    safe_voice = json.dumps(
        str(selected_voice or "")
    )

    try:
        rate = float(speech_rate)
    except (TypeError, ValueError):
        rate = 0.9

    try:
        vol = float(volume)
    except (TypeError, ValueError):
        vol = 1.0

    try:
        pt = float(pitch)
    except (TypeError, ValueError):
        pt = 1.0

    # Keep browser values within safe ranges.
    rate = max(0.1, min(10.0, rate))
    vol = max(0.0, min(1.0, vol))
    pt = max(0.0, min(2.0, pt))

    autoplay_value = (
        "true"
        if autoplay
        else "false"
    )

    return f"""
<script>

(function() {{

    const text = {safe_text};
    const language = {safe_language};
    const selectedVoiceName = {safe_voice};

    const speechRate = {rate};
    const speechVolume = {vol};
    const speechPitch = {pt};

    const autoplay = {autoplay_value};


    function speakText() {{

        if (!text || !text.trim()) {{
            return;
        }}


        if (!("speechSynthesis" in window)) {{
            console.warn(
                "Speech synthesis is not supported by this browser."
            );
            return;
        }}


        window.speechSynthesis.cancel();


        const utterance =
            new SpeechSynthesisUtterance(text);


        utterance.lang = language;

        utterance.rate = speechRate;

        utterance.volume = speechVolume;

        utterance.pitch = speechPitch;


        const voices =
            window.speechSynthesis.getVoices();


        let selectedVoice = null;


        // ----------------------------------------------------
        // FIRST: EXACT VOICE NAME
        // ----------------------------------------------------

        if (selectedVoiceName) {{

            selectedVoice = voices.find(
                function(voice) {{
                    return voice.name === selectedVoiceName;
                }}
            );

        }}


        // ----------------------------------------------------
        // SECOND: LANGUAGE MATCH
        // ----------------------------------------------------

        if (!selectedVoice) {{

            selectedVoice = voices.find(
                function(voice) {{

                    return voice.lang &&
                        voice.lang.toLowerCase() ===
                        language.toLowerCase();

                }}
            );

        }}


        // ----------------------------------------------------
        // THIRD: LANGUAGE PREFIX MATCH
        // ----------------------------------------------------

        if (!selectedVoice) {{

            const languagePrefix =
                language
                    .toLowerCase()
                    .split("-")[0];


            selectedVoice = voices.find(
                function(voice) {{

                    return voice.lang &&
                        voice.lang
                            .toLowerCase()
                            .startsWith(
                                languagePrefix
                            );

                }}
            );

        }}


        // ----------------------------------------------------
        // APPLY VOICE
        // ----------------------------------------------------

        if (selectedVoice) {{
            utterance.voice = selectedVoice;
        }}


        // ----------------------------------------------------
        // SPEECH EVENTS
        // ----------------------------------------------------

        utterance.onstart = function() {{

            console.log(
                "EduAccess-AI TTS started."
            );

        }};


        utterance.onend = function() {{

            console.log(
                "EduAccess-AI TTS finished."
            );

        }};


        utterance.onerror = function(event) {{

            console.warn(
                "EduAccess-AI TTS error:",
                event
            );

        }};


        window.speechSynthesis.speak(
            utterance
        );

    }}


    // --------------------------------------------------------
    // BROWSER VOICES MAY LOAD ASYNCHRONOUSLY
    // --------------------------------------------------------

    if (
        window.speechSynthesis
    ) {{

        const voices =
            window.speechSynthesis.getVoices();


        if (
            voices &&
            voices.length > 0
        ) {{

            if (autoplay) {{
                speakText();
            }}

        }} else {{

            window.speechSynthesis.onvoiceschanged =
                function() {{

                    if (autoplay) {{
                        speakText();
                    }}

                }};

        }}

    }}

}})();

</script>
"""


# ============================================================
# SHOW TEXT TO SPEECH
# ============================================================

def show_text_to_speech(
    text: str,
    autoplay: bool = False,
    language: str = "en-US",
    selected_voice: str = "",
    speech_rate: float = 0.9,
    volume: float = 1.0,
    pitch: float = 1.0,
):
    """
    Display browser-based Text-to-Speech.

    Parameters
    ----------
    text:
        Text that should be spoken.

    autoplay:
        Automatically start speaking when True.

    language:
        Browser language code such as en-US, hi-IN, pa-IN.

    selected_voice:
        Saved browser voice name.

    speech_rate:
        Speech speed.

    volume:
        Speech volume.

    pitch:
        Speech pitch.
    """

    if not text:
        return


    javascript = _build_tts_javascript(
        text=text,
        language=language,
        selected_voice=selected_voice,
        speech_rate=speech_rate,
        volume=volume,
        pitch=pitch,
        autoplay=autoplay,
    )


    components.html(
        javascript,
        height=0,
        scrolling=False,
    )


# ============================================================
# TEST TEXT TO SPEECH
# ============================================================

def test_text_to_speech(
    language: str = "en-US",
    selected_voice: str = "",
    speech_rate: float = 0.9,
    volume: float = 1.0,
    pitch: float = 1.0,
):
    """
    Test the current TTS settings.
    """

    test_messages = {

        "en-US":
            "Hello. This is the EduAccess AI text to speech test.",

        "hi-IN":
            "नमस्ते। यह EduAccess AI टेक्स्ट टू स्पीच टेस्ट है।",

        "pa-IN":
            "ਸਤ ਸ੍ਰੀ ਅਕਾਲ। ਇਹ EduAccess AI ਟੈਕਸਟ ਟੂ ਸਪੀਚ ਟੈਸਟ ਹੈ।",

    }


    text = test_messages.get(
        language,
        test_messages["en-US"],
    )


    show_text_to_speech(
        text=text,
        autoplay=True,
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
    Stop currently running browser speech.
    """

    components.html(
        """
<script>

if ("speechSynthesis" in window) {
    window.speechSynthesis.cancel();
}

</script>
        """,
        height=0,
        scrolling=False,
    )


# ============================================================
# SIMPLE TTS STATUS
# ============================================================

def is_tts_supported():
    """
    Return True because the implementation uses the browser's
    SpeechSynthesis API.

    Actual browser support is checked by JavaScript.
    """

    return True
```python
# ============================================================
# TEST VOICE
# ============================================================

def test_voice(
    language: str = "en-US",
    selected_voice: str = "",
    speech_rate: float = 0.9,
    volume: float = 1.0,
    pitch: float = 1.0,
):
    """
    Compatibility wrapper for tutor.py.

    Tests the currently selected browser TTS voice
    using the current TTS settings.
    """

    test_text_to_speech(
        language=language,
        selected_voice=selected_voice,
        speech_rate=speech_rate,
        volume=volume,
        pitch=pitch,
    )
```

Then update the `__all__` section to:

```python
# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    "show_text_to_speech",
    "get_tts_language",
    "test_text_to_speech",
    "test_voice",
    "get_available_tts_voices",
    "get_available_voices",
    "stop_text_to_speech",
    "is_tts_supported",
]
```



# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    "show_text_to_speech",
    "get_tts_language",
    "test_text_to_speech",
    "get_available_tts_voices",
    "get_available_voices",
    "stop_text_to_speech",
    "is_tts_supported",
]
