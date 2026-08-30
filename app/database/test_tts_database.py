from app.database.database import SessionLocal
from app.database.tts_preferences import (
    load_tts_preferences,
    save_tts_preferences,
)


# ============================================================
# TEST USER ID
# ============================================================

USER_ID = 1


# ============================================================
# DATABASE SESSION
# ============================================================

db = SessionLocal()


try:

    print()
    print("=" * 60)
    print("TTS DATABASE TEST")
    print("=" * 60)
    print()


    # ========================================================
    # LOAD CURRENT SETTINGS
    # ========================================================

    print("1. Loading current TTS preferences...")

    current = load_tts_preferences(

        db=db,

        user_id=USER_ID,

    )


    print(
        "Current preferences:"
    )

    print(
        current
    )

    print()


    # ========================================================
    # USER CHECK
    # ========================================================

    if current is None:

        print(
            f"❌ User ID {USER_ID} was not found."
        )

        print(
            "Change USER_ID to an existing user ID."
        )

    else:

        print(
            "✅ User found."
        )

        print()


        # ====================================================
        # SAVE TEST VALUES
        # ====================================================

        print(
            "2. Saving test TTS preferences..."
        )


        success = save_tts_preferences(

            db=db,

            user_id=USER_ID,

            tts_voice="",

            tts_autoplay=True,

            tts_rate=0.7,

            tts_volume=0.8,

            tts_pitch=1.1,

        )


        if success:

            print(
                "✅ Preferences saved."
            )

        else:

            print(
                "❌ Preferences could not be saved."
            )


        print()


        # ====================================================
        # LOAD AGAIN
        # ====================================================

        print(
            "3. Loading preferences again..."
        )


        updated = load_tts_preferences(

            db=db,

            user_id=USER_ID,

        )


        print(
            "Updated preferences:"
        )

        print(
            updated
        )

        print()


        # ====================================================
        # VERIFY
        # ====================================================

        if (

            updated is not None

            and updated["tts_autoplay"] is True

            and updated["tts_rate"] == 0.7

            and updated["tts_volume"] == 0.8

            and updated["tts_pitch"] == 1.1

        ):

            print(
                "✅ TTS persistence test PASSED."
            )

        else:

            print(
                "❌ TTS persistence test FAILED."
            )


finally:

    db.close()


print()
print("=" * 60)
print("TEST COMPLETE")
print("=" * 60)