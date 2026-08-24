from typing import Any

from app.auth.password import (
    hash_password,
    verify_password,
)

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

    # --------------------------------------------------------
    # LEARNING PREFERENCES
    # --------------------------------------------------------

    simple_explanation: bool = True,
    step_by_step: bool = True,
    repetition_support: bool = False,
    visual_explanation: bool = True,

    # --------------------------------------------------------
    # COMMUNICATION ACCESSIBILITY
    # --------------------------------------------------------

    text_to_speech: bool = False,
    speech_to_text: bool = False,

    # --------------------------------------------------------
    # VISUAL ACCESSIBILITY
    # --------------------------------------------------------

    large_text: bool = False,
    high_contrast: bool = False,
    dyslexia_friendly: bool = False,
):
    """
    Create a new EduAccess AI student account.

    All learning and accessibility preferences are stored
    permanently in the database.
    """

    db: Any = SessionLocal()

    try:

        # ====================================================
        # CLEAN INPUT
        # ====================================================

        full_name = str(full_name).strip()
        email = str(email).strip().lower()
        password = str(password)

        disability_type = (
            str(disability_type).strip()
            or "No disability"
        )

        disability_details = (
            str(disability_details).strip()
        )

        preferred_language = (
            str(preferred_language).strip()
            or "English"
        )

        # ====================================================
        # VALIDATION
        # ====================================================

        if not full_name:

            raise ValueError(
                "Full name is required."
            )

        if not email:

            raise ValueError(
                "Email is required."
            )

        if "@" not in email:

            raise ValueError(
                "Please enter a valid email address."
            )

        if len(password) < 6:

            raise ValueError(
                "Password must contain at least 6 characters."
            )

        # ====================================================
        # CHECK EXISTING EMAIL
        # ====================================================

        existing_user = (
            db.query(User)
            .filter(
                User.email == email
            )
            .first()
        )

        if existing_user:

            raise ValueError(
                "An account with this email already exists."
            )

        # ====================================================
        # HASH PASSWORD
        # ====================================================

        password_hash = hash_password(
            password
        )

        # ====================================================
        # CREATE USER
        # ====================================================

        user = User(

            # ------------------------------------------------
            # BASIC INFORMATION
            # ------------------------------------------------

            full_name=full_name,

            email=email,

            password_hash=password_hash,

            # ------------------------------------------------
            # DISABILITY INFORMATION
            # ------------------------------------------------

            disability_type=disability_type,

            disability_details=disability_details,

            # ------------------------------------------------
            # LANGUAGE
            # ------------------------------------------------

            preferred_language=preferred_language,

            # ------------------------------------------------
            # LEARNING PREFERENCES
            # ------------------------------------------------

            simple_explanation=bool(
                simple_explanation
            ),

            step_by_step=bool(
                step_by_step
            ),

            repetition_support=bool(
                repetition_support
            ),

            visual_explanation=bool(
                visual_explanation
            ),

            # ------------------------------------------------
            # COMMUNICATION ACCESSIBILITY
            # ------------------------------------------------

            text_to_speech=bool(
                text_to_speech
            ),

            speech_to_text=bool(
                speech_to_text
            ),

            # ------------------------------------------------
            # VISUAL ACCESSIBILITY
            # ------------------------------------------------

            large_text=bool(
                large_text
            ),

            high_contrast=bool(
                high_contrast
            ),

            dyslexia_friendly=bool(
                dyslexia_friendly
            ),
        )

        # ====================================================
        # SAVE
        # ====================================================

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
    Authenticate a student using email and password.
    """

    db: Any = SessionLocal()

    try:

        email = str(email).strip().lower()

        user = (
            db.query(User)
            .filter(
                User.email == email
            )
            .first()
        )

        # ----------------------------------------------------
        # USER NOT FOUND
        # ----------------------------------------------------

        if user is None:

            return None

        # ----------------------------------------------------
        # VERIFY PASSWORD
        # ----------------------------------------------------

        if not verify_password(
            password,
            user.password_hash,
        ):

            return None

        return user

    finally:

        db.close()


# ============================================================
# GET USER BY ID
# ============================================================

def get_user_by_id(
    user_id: int,
):
    """
    Return a user by database ID.
    """

    db: Any = SessionLocal()

    try:

        return (
            db.query(User)
            .filter(
                User.id == user_id
            )
            .first()
        )

    finally:

        db.close()


# ============================================================
# GET USER BY EMAIL
# ============================================================

def get_user_by_email(
    email: str,
):
    """
    Return a user by email.
    """

    db: Any = SessionLocal()

    try:

        email = str(email).strip().lower()

        return (
            db.query(User)
            .filter(
                User.email == email
            )
            .first()
        )

    finally:

        db.close()
