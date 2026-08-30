# ============================================================
# app/database/database.py
# ============================================================

try:
    from sqlalchemy import create_engine  # type: ignore[reportMissingImports]
    from sqlalchemy.orm import declarative_base, sessionmaker  # type: ignore[reportMissingImports]
except ImportError as e:
    raise ImportError("SQLAlchemy is required. Install it with: pip install sqlalchemy") from e

from app.config.settings import settings


# ============================================================
# DATABASE URL
# ============================================================

DATABASE_URL = settings.DATABASE_URL


# ============================================================
# ENGINE
# ============================================================

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
)


# ============================================================
# SESSION
# ============================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ============================================================
# BASE
# ============================================================

Base = declarative_base()
