# ============================================================
# app/database/crud.py
# ============================================================
# EDUACCESS-AI
# Database CRUD Operations
# ============================================================

from sqlalchemy.orm import Session  # type: ignore

from app.database.models import (
    User,
)


# ============================================================
# USER OPERATIONS
# ============================================================

def create_user(
    db: Session,
    full_name: str,
    email: str,
    password_hash: str,
    disability_type: str = "None",
    disability_details: str = "",
):
    """
    Create a new EduAccess user.

    The additional fields have defaults so existing
    authentication code remains compatible.
    """

    user = User(
        full_name=full_name.strip(),
        email=email.lower().strip(),
        password_hash=password_hash,
        disability_type=disability_type,
        disability_details=disability_details,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# ============================================================
# GET USER BY EMAIL
# ============================================================

def get_user_by_email(
    db: Session,
    email: str,
):
    """
    Find a user by email address.
    """

    if not email:
        return None

    return (
        db.query(User)
        .filter(
            User.email == email.lower().strip()
        )
        .first()
    )


# ============================================================
# GET USER BY ID
# ============================================================

def get_user_by_id(
    db: Session,
    user_id: int,
):
    """
    Find a user by primary key.
    """

    if user_id is None:
        return None

    return (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )


# ============================================================
# UPDATE USER
# ============================================================

def update_user(
    db: Session,
    user: User,
    **updates,
):
    """
    Update allowed User fields.

    Example:

        update_user(
            db,
            user,
            preferred_language="Hindi",
            text_to_speech=True,
        )
    """

    if user is None:
        return None

    for field, value in updates.items():

        if hasattr(user, field):

            setattr(
                user,
                field,
                value,
            )

    db.commit()
    db.refresh(user)

    return user


# ============================================================
# UPDATE USER ACCESSIBILITY SETTINGS
# ============================================================

def update_accessibility_settings(
    db: Session,
    user: User,
    **settings,
):
    """
    Update accessibility preferences directly on User.

    The current EduAccess database stores accessibility
    preferences in the users table.
    """

    if user is None:
        return None

    allowed_fields = {
        "simple_explanation",
        "step_by_step",
        "repetition_support",
        "visual_explanation",
        "text_to_speech",
        "speech_to_text",
        "large_text",
        "high_contrast",
        "dyslexia_friendly",
    }

    for field, value in settings.items():

        if field in allowed_fields:

            setattr(
                user,
                field,
                bool(value),
            )

    db.commit()
    db.refresh(user)

    return user


# ============================================================
# UPDATE TTS SETTINGS
# ============================================================

def update_tts_preferences(
    db: Session,
    user: User,
    tts_enabled=None,
    tts_voice=None,
    tts_autoplay=None,
    tts_rate=None,
    tts_volume=None,
    tts_pitch=None,
):
    """
    Update the complete TTS preference set.

    This matches the TTS implementation currently used
    by app.ui.tutor.
    """

    if user is None:
        return None

    # --------------------------------------------------------
    # TTS ENABLED
    # --------------------------------------------------------

    if tts_enabled is not None:

        user.text_to_speech = bool(
            tts_enabled
        )

    # --------------------------------------------------------
    # VOICE
    # --------------------------------------------------------

    if tts_voice is not None:

        user.tts_voice = str(
            tts_voice
        )

    # --------------------------------------------------------
    # AUTOPLAY
    # --------------------------------------------------------

    if tts_autoplay is not None:

        user.tts_autoplay = bool(
            tts_autoplay
        )

    # --------------------------------------------------------
    # RATE
    # --------------------------------------------------------

    if tts_rate is not None:

        user.tts_rate = str(
            tts_rate
        )

    # --------------------------------------------------------
    # VOLUME
    # --------------------------------------------------------

    if tts_volume is not None:

        user.tts_volume = str(
            tts_volume
        )

    # --------------------------------------------------------
    # PITCH
    # --------------------------------------------------------

    if tts_pitch is not None:

        user.tts_pitch = str(
            tts_pitch
        )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    db.commit()
    db.refresh(user)

    return user


# ============================================================
# DELETE USER
# ============================================================

def delete_user(
    db: Session,
    user: User,
):
    """
    Delete a user from the database.
    """

    if user is None:
        return False

    db.delete(user)
    db.commit()

    return True


# ============================================================
# GET ALL USERS
# ============================================================

def get_all_users(
    db: Session,
):
    """
    Return all registered users.
    """

    return (
        db.query(User)
        .order_by(
            User.id.asc()
        )
        .all()
    )


# ============================================================
# TUTOR CONVERSATION OPERATIONS
# ============================================================

def create_tutor_conversation(
    db: Session,
    user_id: int,
    question: str,
    answer: str,
    session_id: str = None,
):
    """
    Store one Tutor question and answer.
    """

    from app.database.models import (
        TutorConversation,
    )

    conversation = TutorConversation(
        user_id=user_id,
        session_id=session_id,
        question=question,
        answer=answer,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


# ============================================================
# GET TUTOR CONVERSATIONS
# ============================================================

def get_tutor_conversations(
    db: Session,
    user_id: int,
    limit: int = 100,
):
    """
    Return Tutor conversations for a user.
    """

    from app.database.models import (
        TutorConversation,
    )

    return (
        db.query(TutorConversation)
        .filter(
            TutorConversation.user_id == user_id
        )
        .order_by(
            TutorConversation.created_at.desc()
        )
        .limit(limit)
        .all()
    )


# ============================================================
# GET TUTOR SESSION
# ============================================================

def get_tutor_session(
    db: Session,
    user_id: int,
    session_id: str,
):
    """
    Return conversations belonging to a particular
    Tutor session.
    """

    from app.database.models import (
        TutorConversation,
    )

    return (
        db.query(TutorConversation)
        .filter(
            TutorConversation.user_id == user_id,
            TutorConversation.session_id == session_id,
        )
        .order_by(
            TutorConversation.created_at.asc()
        )
        .all()
    )


# ============================================================
# END
# ============================================================