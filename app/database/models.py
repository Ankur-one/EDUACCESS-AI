from datetime import datetime

from sqlalchemy import (  # type: ignore[import-not-found]
    Column,
    Integer,
    String,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship  # type: ignore[import-not-found]

from app.database.database import Base


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
    # RELATIONSHIP WITH TUTOR CONVERSATIONS
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
    # STUDENT QUESTION
    # ========================================================

    question = Column(
        Text,
        nullable=False,
    )

    # ========================================================
    # AI ANSWER
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