# ============================================================
# app/audio/__init__.py
# ============================================================

from app.audio.tts import (
    show_text_to_speech,
    get_tts_language,
)


__all__ = [
    "show_text_to_speech",
    "get_tts_language",
]
