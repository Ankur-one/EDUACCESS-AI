from pathlib import Path
from os import environ


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

ENV_FILE = PROJECT_ROOT / ".env"


# ============================================================
# APPLICATION SETTINGS
# ============================================================

class Settings:

    APP_NAME: str = "EduAccess AI"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True

    DATABASE_URL: str = "sqlite:///./eduaccess.db"

    GEMINI_API_KEY: str = ""

    def __init__(self):
        if ENV_FILE.is_file():
            for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    environ.setdefault(key.strip(), value.strip().strip('"\''))

        self.APP_NAME = environ.get("APP_NAME", self.APP_NAME)
        self.APP_VERSION = environ.get("APP_VERSION", self.APP_VERSION)
        self.DEBUG = environ.get("DEBUG", str(self.DEBUG)).lower() in {
            "1", "true", "yes", "on"
        }
        self.DATABASE_URL = environ.get("DATABASE_URL", self.DATABASE_URL)
        self.GEMINI_API_KEY = environ.get("GEMINI_API_KEY", self.GEMINI_API_KEY)


# ============================================================
# SETTINGS INSTANCE
# ============================================================

settings = Settings()