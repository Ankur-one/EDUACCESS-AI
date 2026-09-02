# ============================================================
# app/audio/__init__.py
# EduAccess AI - Audio Package
# ============================================================

"""
Audio package for EduAccess AI.

Provides:
    - Text-to-Speech (TTS)
    - Speech-to-Text (STT)
"""


# ============================================================
# TEXT TO SPEECH
# ============================================================

from app.audio.tts import (
    show_text_to_speech,
    get_tts_language,
    get_available_tts_voices,
    get_available_voices,
    test_voice,
    test_text_to_speech,
    stop_text_to_speech,
    validate_tts_settings,
)


# ============================================================
# SPEECH TO TEXT
# ============================================================

try:

    from app.audio.stt import (
        show_speech_to_text,
    )

except ImportError:

    show_speech_to_text = None


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [

    # TTS
    "show_text_to_speech",
    "get_tts_language",
    "get_available_tts_voices",
    "get_available_voices",
    "test_voice",
    "test_text_to_speech",
    "stop_text_to_speech",
    "validate_tts_settings",

    # STT
    "show_speech_to_text",

]
