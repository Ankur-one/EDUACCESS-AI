from sqlalchemy import (  # type: ignore[import-not-found]
    Column,
    Integer,
    String,
    Boolean,
)

from app.database.database import Base


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