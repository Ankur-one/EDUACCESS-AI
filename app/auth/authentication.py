from typing import Any

from app.auth.password import hash_password, verify_password
from app.database.database import SessionLocal
from app.database.models import User


# ============================================================
# REGISTER USER
# ============================================================

def register_user(
    full_name: str,
    email: str,
    password: str,
    disability_type: str = "No disability",
    disability_details: str = "",
    preferred_language: str = "English",
    simple_explanation: bool = False,
    step_by_step: bool = False,
    repetition_support: bool = False,
    visual_explanation: bool = False,
    text_to_speech: bool = False,
    speech_to_text: bool = False,
    large_text: bool = False,
):
    """
    Create a new EduAccess AI student account.
    """

    db: Any = SessionLocal()

    try:

        # ----------------------------------------------------
        # Check existing email
        # ----------------------------------------------------

        existing_user = (
            db.query(User)
            .filter(User.email == email.strip().lower())
            .first()
        )

        if existing_user:

            raise ValueError(
                "An account with this email already exists."
            )

        # ----------------------------------------------------
        # Hash password
        # ----------------------------------------------------

        password_hash = hash_password(password)

        # ----------------------------------------------------
        # Create user
        # ----------------------------------------------------

        user = User(
            full_name=full_name.strip(),

            email=email.strip().lower(),

            password_hash=password_hash,

            disability_type=disability_type,

            disability_details=disability_details,

            preferred_language=preferred_language,

            simple_explanation=simple_explanation,

            step_by_step=step_by_step,

            repetition_support=repetition_support,

            visual_explanation=visual_explanation,

            text_to_speech=text_to_speech,

            speech_to_text=speech_to_text,

            large_text=large_text,
        )

        # ----------------------------------------------------
        # Save
        # ----------------------------------------------------

        db.add(user)

        db.commit()

        db.refresh(user)

        return user

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


# ============================================================
# LOGIN USER
# ============================================================

def login_user(
    email: str,
    password: str,
):
    """
    Authenticate a student.
    """

    db: Any = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(
                User.email == email.strip().lower()
            )
            .first()
        )

        # ----------------------------------------------------
        # User doesn't exist
        # ----------------------------------------------------

        if not user:

            return None

        # ----------------------------------------------------
        # Verify password
        # ----------------------------------------------------

        if not verify_password(
            password,
            user.password_hash
        ):

            return None

        return user

    finally:

        db.close()


# ============================================================
# GET USER BY ID
# ============================================================

def get_user_by_id(
    user_id: int
):
    """
    Get a student by database ID.
    """

    db: Any = SessionLocal()

    try:

        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    finally:

        db.close()


# ============================================================
# GET USER BY EMAIL
# ============================================================

def get_user_by_email(
    email: str
):
    """
    Get a student by email.
    """

    db: Any = SessionLocal()

    try:

        return (
            db.query(User)
            .filter(
                User.email == email.strip().lower()
            )
            .first()
        )

    finally:

        db.close()