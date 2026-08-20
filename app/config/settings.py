import os


class Settings:
    APP_NAME = os.getenv(
        "APP_NAME",
        "EduAccess AI"
    )

    APP_VERSION = os.getenv(
        "APP_VERSION",
        "1.0.0"
    )

    DEBUG = os.getenv(
        "DEBUG",
        "True"
    ).lower() == "true"

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./eduaccess.db"
    )


settings = Settings()