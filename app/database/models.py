from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String  # type: ignore[import-not-found]
from sqlalchemy.orm import Mapped, mapped_column  # type: ignore[import-not-found]

from app.database.database import Base


# ============================================================
# USER MODEL
# ============================================================

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


# ============================================================
# ACCESSIBILITY PROFILE MODEL
# ============================================================

class AccessibilityProfile(Base):
    __tablename__ = "accessibility_profiles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        nullable=False,
        index=True
    )

    # --------------------------------------------------------
    # Accessibility / Support Needs
    # --------------------------------------------------------

    visual_support: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    hearing_support: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    speech_support: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    motor_support: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    reading_support: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    learning_support: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    cognitive_support: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    multiple_support: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # --------------------------------------------------------
    # Interaction Preferences
    # --------------------------------------------------------

    voice_input: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    speech_to_text: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    text_to_speech: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    voice_navigation: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    keyboard_navigation: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    # --------------------------------------------------------
    # Visual Accessibility
    # --------------------------------------------------------

    large_text: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    high_contrast: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    reduced_animation: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # --------------------------------------------------------
    # Hearing Accessibility
    # --------------------------------------------------------

    captions: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    transcripts: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # --------------------------------------------------------
    # Learning Accessibility
    # --------------------------------------------------------

    simplified_language: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    step_by_step_learning: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    repetition_support: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    visual_explanations: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # --------------------------------------------------------
    # Communication Preferences
    # --------------------------------------------------------

    typing_support: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    aac_support: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # --------------------------------------------------------
    # Language
    # --------------------------------------------------------

    preferred_language: Mapped[str] = mapped_column(
        String(50),
        default="English",
        nullable=False
    )

    # --------------------------------------------------------
    # Learning Output Preference
    # --------------------------------------------------------

    preferred_input: Mapped[str] = mapped_column(
        String(50),
        default="Text",
        nullable=False
    )

    preferred_output: Mapped[str] = mapped_column(
        String(50),
        default="Text",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


# ============================================================
# STUDY PROGRESS MODEL
# ============================================================

class StudyProgress(Base):
    __tablename__ = "study_progress"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )

    topic: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    progress_percentage: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    quiz_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    study_minutes: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


# ============================================================
# QUIZ RESULT MODEL
# ============================================================

class QuizResult(Base):
    __tablename__ = "quiz_results"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )

    topic: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    total_questions: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    correct_answers: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    score_percentage: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


# ============================================================
# UPLOADED DOCUMENT MODEL
# ============================================================

class UploadedDocument(Base):
    __tablename__ = "uploaded_documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    processed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )