from app.database.database import Base, engine

# Import all models so SQLAlchemy knows about the tables
from app.database.models import (
    StudyProgress,  # noqa: F401 — imported to register the model with SQLAlchemy
    UploadedDocument,  # noqa: F401 — imported to register the model with SQLAlchemy
)


def init_database():
    """
    Create all database tables.
    """

    Base.metadata.create_all(bind=engine)

    print("========================================")
    print("   EduAccess AI Database Initialized")
    print("========================================")
    print("Tables created:")
    print("✓ users")
    print("✓ accessibility_profiles")
    print("✓ study_progress")
    print("✓ quiz_results")
    print("✓ uploaded_documents")
    print("========================================")


if __name__ == "__main__":
    init_database()