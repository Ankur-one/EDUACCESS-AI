from sqlalchemy.orm import Session

from app.database.models import (
    AccessibilityProfile,
    StudyProgress,
    User,
)


# ============================================================
# USER OPERATIONS
# ============================================================

def create_user(
    db: Session,
    full_name: str,
    email: str,
    password_hash: str
):
    user = User(
        full_name=full_name,
        email=email.lower().strip(),
        password_hash=password_hash
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_email(
    db: Session,
    email: str
):
    return (
        db.query(User)
        .filter(
            User.email == email.lower().strip()
        )
        .first()
    )


def get_user_by_id(
    db: Session,
    user_id: int
):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


# ============================================================
# ACCESSIBILITY PROFILE
# ============================================================

def create_accessibility_profile(
    db: Session,
    user_id: int
):
    profile = AccessibilityProfile(
        user_id=user_id
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


def get_accessibility_profile(
    db: Session,
    user_id: int
):
    return (
        db.query(AccessibilityProfile)
        .filter(
            AccessibilityProfile.user_id == user_id
        )
        .first()
    )


# ============================================================
# STUDY PROGRESS
# ============================================================

def create_study_progress(
    db: Session,
    user_id: int,
    topic: str
):
    progress = StudyProgress(
        user_id=user_id,
        topic=topic
    )

    db.add(progress)
    db.commit()
    db.refresh(progress)

    return progress