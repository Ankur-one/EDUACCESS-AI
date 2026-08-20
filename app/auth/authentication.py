from typing import Any

from app.auth.password import hash_password
from app.database.crud import (
    create_accessibility_profile,
    create_user,
    get_user_by_email,
)


def register_user(
    db: Any,
    full_name: str,
    email: str,
    password: str
):
    """
    Register a new EduAccess AI student.
    """

    # Clean input
    full_name = full_name.strip()
    email = email.strip().lower()

    # Check if email already exists
    existing_user = get_user_by_email(
        db,
        email
    )

    if existing_user:
        return None, "Email is already registered."

    # Hash password
    password_hash = hash_password(password)

    # Create user
    user = create_user(
        db=db,
        full_name=full_name,
        email=email,
        password_hash=password_hash
    )

    # Automatically create accessibility profile
    create_accessibility_profile(
        db=db,
        user_id=user.id
    )

    return user, "Registration successful."


def authenticate_user(
    db: Any,
    email: str,
    password: str
):
    """
    Authenticate an existing student.
    """

    from app.auth.password import verify_password

    email = email.strip().lower()

    user = get_user_by_email(
        db,
        email
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.password_hash
    ):
        return None

    if not user.is_active:
        return None

    return user