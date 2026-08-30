import sqlite3
from pathlib import Path


# ============================================================
# DATABASE LOCATION
# ============================================================

DATABASE_FILE = Path("eduaccess.db")


# ============================================================
# TTS COLUMNS
# ============================================================

TTS_COLUMNS = {

    "tts_voice": (
        "VARCHAR(255) DEFAULT ''"
    ),

    "tts_autoplay": (
        "BOOLEAN DEFAULT 0"
    ),

    "tts_rate": (
        "FLOAT DEFAULT 0.9"
    ),

    "tts_volume": (
        "FLOAT DEFAULT 1.0"
    ),

    "tts_pitch": (
        "FLOAT DEFAULT 1.0"
    ),

}


# ============================================================
# MAIN
# ============================================================

def update_database():

    # ========================================================
    # CHECK DATABASE
    # ========================================================

    if not DATABASE_FILE.exists():

        print(
            "Database file not found:"
        )

        print(
            DATABASE_FILE.resolve()
        )

        return


    # ========================================================
    # CONNECT
    # ========================================================

    connection = sqlite3.connect(
        DATABASE_FILE
    )


    cursor = connection.cursor()


    # ========================================================
    # GET EXISTING COLUMNS
    # ========================================================

    cursor.execute(
        "PRAGMA table_info(users)"
    )


    existing_columns = {

        row[1]

        for row in cursor.fetchall()

    }


    print(
        "Existing users columns:"
    )

    for column in sorted(
        existing_columns
    ):

        print(
            f"  - {column}"
        )


    # ========================================================
    # ADD MISSING TTS COLUMNS
    # ========================================================

    for column_name, definition in (
        TTS_COLUMNS.items()
    ):

        if column_name in existing_columns:

            print(
                f"✓ {column_name} already exists"
            )

            continue


        sql = (
            f"ALTER TABLE users "
            f"ADD COLUMN {column_name} "
            f"{definition}"
        )


        print(
            f"+ Adding {column_name}..."
        )


        cursor.execute(
            sql
        )


        print(
            f"✓ Added {column_name}"
        )


    # ========================================================
    # COMMIT
    # ========================================================

    connection.commit()


    # ========================================================
    # CLOSE
    # ========================================================

    connection.close()


    print()
    print(
        "======================================"
    )

    print(
        "TTS database update completed."
    )

    print(
        "======================================"
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    update_database()