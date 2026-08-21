from sqlalchemy import create_engine  # type: ignore[reportMissingImports]
from sqlalchemy.orm import declarative_base  # type: ignore[reportMissingImports]
from sqlalchemy.orm import sessionmaker  # type: ignore[reportMissingImports]

from app.config.settings import settings


# ============================================================
# DATABASE URL
# ============================================================

DATABASE_URL = settings.DATABASE_URL


# ============================================================
# ENGINE
# ============================================================

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
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