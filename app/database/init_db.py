# ============================================================
# app/database/init_db.py
# ============================================================

from app.database.database import (
    Base,
    engine,
)

# ============================================================
# INITIALIZE DATABASE
# ============================================================

def init_database():
    """
    Create database tables that do not already exist.
    """

    Base.metadata.create_all(
        bind=engine
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    init_database()
    print("✅ Database initialized successfully.")

