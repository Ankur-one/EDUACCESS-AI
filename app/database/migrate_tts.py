import sqlite3
from pathlib import Path


# ============================================================
# DATABASE PATH
# ============================================================

DATABASE_PATH = Path("eduaccess.db")


# ============================================================
# TTS COLUMNS
# ============================================================

TTS_COLUMNS = {

    "tts_voice": """
        ALTER TABLE users
        ADD COLUMN tts_voice
        VARCHAR(200)
        NOT NULL
        DEFAULT ''
    """,

    "tts_autoplay": """
        ALTER TABLE users
        ADD COLUMN tts_autoplay
        BOOLEAN
        NOT NULL
        DEFAULT 0
    """,

    "tts_rate": """
        ALTER TABLE users
        ADD COLUMN tts_rate
        FLOAT
        NOT NULL
        DEFAULT 0.9
    """,

    "tts_volume": """
        ALTER TABLE users
        ADD COLUMN tts_volume
        FLOAT
        NOT NULL
        DEFAULT 1.0
    """,

    "tts_pitch": """
        ALTER TABLE users
        ADD COLUMN tts_pitch
        FLOAT
        NOT NULL
        DEFAULT 1.0
    """,
}


# ============================================================
# MIGRATION
# ============================================================

def migrate():

    print()
    print("=" * 60)
    print("EduAccess-AI TTS Database Migration")
    print("=" * 60)
    print()


    # ========================================================
    # DATABASE CHECK
    # ========================================================

    if not DATABASE_PATH.exists():

        print(
            "❌ Database file was not found:"
        )

        print(
            DATABASE_PATH
        )

        print()

        print(
            "Create/initialize the database first."
        )

        return


    # ========================================================
    # CONNECT
    # ========================================================

    connection = sqlite3.connect(
        DATABASE_PATH
    )


    cursor = connection.cursor()


    try:

        # ====================================================
        # GET EXISTING COLUMNS
        # ====================================================

        cursor.execute(
            "PRAGMA table_info(users)"
        )

        existing_columns = {

            row[1]

            for row in cursor.fetchall()

        }


        print(
            "Existing users table columns:"
        )

        for column in sorted(
            existing_columns
        ):

            print(
                f"  ✓ {column}"
            )

        print()


        # ====================================================
        # ADD TTS COLUMNS
        # ====================================================

        for column_name, sql in TTS_COLUMNS.items():

            if column_name in existing_columns:

                print(
                    f"✓ {column_name} already exists"
                )

                continue


            print(
                f"→ Adding {column_name}..."
            )


            cursor.execute(
                sql
            )


            print(
                f"  ✓ {column_name} added"
            )


        # ====================================================
        # COMMIT
        # ====================================================

        connection.commit()


        print()

        print(
            "✅ TTS database migration completed."
        )


    except Exception as error:

        connection.rollback()

        print()

        print(
            "❌ Migration failed."
        )

        print(
            f"Error: {error}"
        )

        raise


    finally:

        cursor.close()

        connection.close()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    migrate()