from sqlalchemy import inspect, text  # type: ignore[import-not-found]

from app.database.database import engine


# ============================================================
# ADD SESSION_ID TO TUTOR CONVERSATIONS
# ============================================================

def migrate_tutor_sessions():

    inspector = inspect(engine)

    # --------------------------------------------------------
    # CHECK TABLE
    # --------------------------------------------------------

    tables = inspector.get_table_names()

    if "tutor_conversations" not in tables:

        print(
            "❌ tutor_conversations table does not exist."
        )

        return

    # --------------------------------------------------------
    # CHECK EXISTING COLUMNS
    # --------------------------------------------------------

    columns = inspector.get_columns(
        "tutor_conversations"
    )

    column_names = {
        column["name"]
        for column in columns
    }

    # --------------------------------------------------------
    # ALREADY EXISTS
    # --------------------------------------------------------

    if "session_id" in column_names:

        print(
            "✅ session_id already exists."
        )

        return

    # --------------------------------------------------------
    # ADD COLUMN
    # --------------------------------------------------------

    with engine.begin() as connection:

        connection.execute(
            text(
                """
                ALTER TABLE tutor_conversations
                ADD COLUMN session_id VARCHAR(100)
                """
            )
        )

    print(
        "✅ session_id column added successfully."
    )


# ============================================================
# RUN MIGRATION
# ============================================================

if __name__ == "__main__":

    print(
        "🔄 Starting tutor session migration..."
    )

    migrate_tutor_sessions()

    print(
        "✅ Migration completed."
    )