# ============================================================
# app/database/models.py
# ============================================================

from datetime import datetime

from sqlalchemy import (  # type: ignore
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship  # type: ignore

from app.database.database import Base

"""Database models for the EduAccess application."""


# ============================================================
# USER MODEL
# ============================================================


class User(Base):
    __tablename__ = "users"

    # ========================================================
    # BASIC USER INFORMATION
    # ========================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    full_name = Column(
        String(150),
        nullable=False,
    )

    email = Column(
        String(150),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    # ========================================================
    # DISABILITY INFORMATION
    # ========================================================

    disability_type = Column(
        String(100),
        nullable=False,
    )

    disability_details = Column(
        String(500),
        nullable=True,
    )

    # ========================================================
    # LANGUAGE
    # ========================================================

    preferred_language = Column(
        String(50),
        default="English",
    )

    # ========================================================
    # LEARNING PREFERENCES
    # ========================================================

    simple_explanation = Column(
        Boolean,
        default=True,
    )

    step_by_step = Column(
        Boolean,
        default=True,
    )

    repetition_support = Column(
        Boolean,
        default=False,
    )

    visual_explanation = Column(
        Boolean,
        default=True,
    )

    # ========================================================
    # COMMUNICATION ACCESSIBILITY
    # ========================================================

    text_to_speech = Column(
        Boolean,
        default=False,
    )

    speech_to_text = Column(
        Boolean,
        default=False,
    )

    # ========================================================
    # TTS VOICE
    #
    # Stores the browser voice name selected by the student.
    # Empty string means browser automatic/default voice.
    # ========================================================

    tts_voice = Column(
        String(255),
        nullable=True,
        default="",
    )

    # ========================================================
    # TTS AUTOPLAY
    # ========================================================

    tts_autoplay = Column(
        Boolean,
        default=False,
    )

    # ========================================================
    # TTS SPEECH RATE
    #
    # Stored as String so existing SQLite database values
    # remain compatible with the current schema.
    # Default: 0.9
    # ========================================================

    tts_rate = Column(
        String(20),
        default="0.9",
        nullable=True,
    )

    # ========================================================
    # TTS VOLUME
    #
    # Range normally used by the UI:
    # 0.0 - 1.0
    # ========================================================

    tts_volume = Column(
        String(20),
        default="1.0",
        nullable=True,
    )

    # ========================================================
    # TTS PITCH
    #
    # Default: 1.0
    # ========================================================

    tts_pitch = Column(
        String(20),
        default="1.0",
        nullable=True,
    )

    # ========================================================
    # VISUAL ACCESSIBILITY
    # ========================================================

    large_text = Column(
        Boolean,
        default=False,
    )

    high_contrast = Column(
        Boolean,
        default=False,
    )

    dyslexia_friendly = Column(
        Boolean,
        default=False,
    )

    # ========================================================
    # TUTOR CONVERSATIONS
    # ========================================================

    tutor_conversations = relationship(
        "TutorConversation",
        back_populates="user",
        cascade="all, delete-orphan",
    )


# ============================================================
# TUTOR CONVERSATION MODEL
# ============================================================


class TutorConversation(Base):
    __tablename__ = "tutor_conversations"

    # ========================================================
    # PRIMARY KEY
    # ========================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ========================================================
    # USER ID
    # ========================================================

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ========================================================
    # SESSION ID
    # ========================================================

    session_id = Column(
        String(100),
        nullable=True,
        index=True,
    )

    # ========================================================
    # QUESTION
    # ========================================================

    question = Column(
        Text,
        nullable=False,
    )

    # ========================================================
    # ANSWER
    # ========================================================

    answer = Column(
        Text,
        nullable=False,
    )

    # ========================================================
    # CREATED TIME
    # ========================================================

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # ========================================================
    # RELATIONSHIP
    # ========================================================

    user = relationship(
        "User",
        back_populates="tutor_conversations",
    )
