from typing import Optional, Dict, Any

from sqlalchemy.orm import Session  # type: ignore[import-not-found]

from app.database.models import User


# ============================================================
# DEFAULT TTS VALUES
# ============================================================

DEFAULT_TTS_VOICE = ""

DEFAULT_TTS_AUTOPLAY = False

DEFAULT_TTS_RATE = 0.9

DEFAULT_TTS_VOLUME = 1.0

DEFAULT_TTS_PITCH = 1.0


# ============================================================
# LOAD TTS PREFERENCES
# ============================================================

def load_tts_preferences(
    db: Session,
    user_id: int,
) -> Optional[Dict[str, Any]]:
    """
    Load a student's TTS preferences from the database.

    Parameters
    ----------
    db:
        SQLAlchemy database session.

    user_id:
        ID of the logged-in student.

    Returns
    -------
    dict | None
        TTS preferences or None if the user does not exist.
    """

    # ========================================================
    # FIND USER
    # ========================================================

    user = (
        db.query(User)
        .filter(
            User.id == int(user_id)
        )
        .first()
    )


    # ========================================================
    # USER NOT FOUND
    # ========================================================

    if user is None:

        return None


    # ========================================================
    # RETURN PREFERENCES
    # ========================================================

    return {

        "tts_voice": (
            user.tts_voice
            if user.tts_voice is not None
            else DEFAULT_TTS_VOICE
        ),

        "tts_autoplay": (
            bool(user.tts_autoplay)
            if user.tts_autoplay is not None
            else DEFAULT_TTS_AUTOPLAY
        ),

        "tts_rate": (
            float(user.tts_rate)
            if user.tts_rate is not None
            else DEFAULT_TTS_RATE
        ),

        "tts_volume": (
            float(user.tts_volume)
            if user.tts_volume is not None
            else DEFAULT_TTS_VOLUME
        ),

        "tts_pitch": (
            float(user.tts_pitch)
            if user.tts_pitch is not None
            else DEFAULT_TTS_PITCH
        ),

    }


# ============================================================
# SAVE TTS PREFERENCES
# ============================================================

def save_tts_preferences(
    db: Session,
    user_id: int,
    tts_voice: str = DEFAULT_TTS_VOICE,
    tts_autoplay: bool = DEFAULT_TTS_AUTOPLAY,
    tts_rate: float = DEFAULT_TTS_RATE,
    tts_volume: float = DEFAULT_TTS_VOLUME,
    tts_pitch: float = DEFAULT_TTS_PITCH,
) -> bool:
    """
    Save a student's TTS preferences.

    Returns
    -------
    bool
        True when successfully saved.
    """

    # ========================================================
    # FIND USER
    # ========================================================

    user = (
        db.query(User)
        .filter(
            User.id == int(user_id)
        )
        .first()
    )


    # ========================================================
    # USER NOT FOUND
    # ========================================================

    if user is None:

        return False


    # ========================================================
    # VALIDATE VOICE
    # ========================================================

    if tts_voice is None:

        tts_voice = DEFAULT_TTS_VOICE

    else:

        tts_voice = str(
            tts_voice
        )


    # ========================================================
    # VALIDATE AUTOPLAY
    # ========================================================

    tts_autoplay = bool(
        tts_autoplay
    )


    # ========================================================
    # VALIDATE RATE
    # ========================================================

    try:

        tts_rate = float(
            tts_rate
        )

    except (
        TypeError,
        ValueError,
    ):

        tts_rate = DEFAULT_TTS_RATE


    # ========================================================
    # VALIDATE VOLUME
    # ========================================================

    try:

        tts_volume = float(
            tts_volume
        )

    except (
        TypeError,
        ValueError,
    ):

        tts_volume = DEFAULT_TTS_VOLUME


    # ========================================================
    # VALIDATE PITCH
    # ========================================================

    try:

        tts_pitch = float(
            tts_pitch
        )

    except (
        TypeError,
        ValueError,
    ):

        tts_pitch = DEFAULT_TTS_PITCH


    # ========================================================
    # LIMIT RATE
    # ========================================================

    tts_rate = max(
        0.1,
        min(
            tts_rate,
            2.0,
        ),
    )


    # ========================================================
    # LIMIT VOLUME
    # ========================================================

    tts_volume = max(
        0.0,
        min(
            tts_volume,
            1.0,
        ),
    )


    # ========================================================
    # LIMIT PITCH
    # ========================================================

    tts_pitch = max(
        0.0,
        min(
            tts_pitch,
            2.0,
        ),
    )


    # ========================================================
    # UPDATE USER
    # ========================================================

    user.tts_voice = tts_voice

    user.tts_autoplay = tts_autoplay

    user.tts_rate = tts_rate

    user.tts_volume = tts_volume

    user.tts_pitch = tts_pitch


    # ========================================================
    # COMMIT
    # ========================================================

    try:

        db.commit()

        db.refresh(
            user
        )

        return True


    except Exception:

        db.rollback()

        return False