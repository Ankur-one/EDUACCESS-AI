import sqlite3


# ============================================================
# DATABASE
# ============================================================

DATABASE_FILE = "eduaccess.db"


# ============================================================
# MAIN TEST
# ============================================================

def main():

    print()
    print("=" * 60)
    print("EDUACCESS-AI TTS DATABASE TEST")
    print("=" * 60)
    print()


    # ========================================================
    # CONNECT
    # ========================================================

    try:

        connection = sqlite3.connect(
            DATABASE_FILE
        )

        cursor = connection.cursor()

        print("✅ Database connection successful.")

    except Exception as error:

        print(
            f"❌ Database connection failed: {error}"
        )

        return


    # ========================================================
    # CHECK USERS TABLE
    # ========================================================

    try:

        cursor.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='users'"
        )

        result = cursor.fetchone()


        if result:

            print("✅ users table exists.")

        else:

            print("❌ users table does not exist.")

            connection.close()

            return

    except Exception as error:

        print(
            f"❌ Could not check users table: {error}"
        )

        connection.close()

        return


    # ========================================================
    # CHECK TTS COLUMNS
    # ========================================================

    required_columns = [

        "tts_voice",

        "tts_autoplay",

        "tts_rate",

        "tts_volume",

        "tts_pitch",

    ]


    try:

        cursor.execute(
            "PRAGMA table_info(users)"
        )

        columns = cursor.fetchall()

        column_names = [
            column[1]
            for column in columns
        ]


        print()
        print("TTS columns:")
        print()


        all_present = True


        for column in required_columns:

            if column in column_names:

                print(
                    f"✅ {column}"
                )

            else:

                print(
                    f"❌ {column}"
                )

                all_present = False


    except Exception as error:

        print(
            f"❌ Could not inspect database columns: {error}"
        )

        connection.close()

        return


    # ========================================================
    # READ USERS
    # ========================================================

    try:

        cursor.execute(
            """
            SELECT
                id,
                full_name,
                email,
                tts_voice,
                tts_autoplay,
                tts_rate,
                tts_volume,
                tts_pitch
            FROM users
            """
        )

        users = cursor.fetchall()


    except Exception as error:

        print()
        print(
            f"❌ Could not read TTS settings: {error}"
        )

        connection.close()

        return


    # ========================================================
    # DISPLAY USERS
    # ========================================================

    print()
    print("=" * 60)
    print("SAVED TTS SETTINGS")
    print("=" * 60)
    print()


    if not users:

        print(
            "⚠️ No users found."
        )

    else:

        for user in users:

            (
                user_id,
                full_name,
                email,
                tts_voice,
                tts_autoplay,
                tts_rate,
                tts_volume,
                tts_pitch,
            ) = user


            print(
                f"User ID      : {user_id}"
            )

            print(
                f"Name         : {full_name}"
            )

            print(
                f"Email        : {email}"
            )

            print(
                f"TTS Voice    : {tts_voice or 'Automatic browser voice'}"
            )

            print(
                f"Autoplay     : {'ON' if tts_autoplay else 'OFF'}"
            )

            print(
                f"Speech Rate  : {tts_rate}"
            )

            print(
                f"Volume       : {tts_volume}"
            )

            print(
                f"Pitch        : {tts_pitch}"
            )

            print(
                "-" * 60
            )


    # ========================================================
    # RESULT
    # ========================================================

    print()

    if all_present:

        print(
            "✅ TTS database structure is ready."
        )

    else:

        print(
            "❌ One or more TTS columns are missing."
        )


    # ========================================================
    # CLOSE
    # ========================================================

    connection.close()

    print()
    print(
        "Database connection closed."
    )

    print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()
