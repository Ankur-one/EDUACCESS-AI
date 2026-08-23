import importlib

# Load Streamlit dynamically so static analyzers do not require the optional
# UI dependency to be installed in the current Python environment.
from app.auth.session import get_current_user
from app.database.database import SessionLocal
from app.database.tutor_crud import (
    get_user_conversations,
    delete_all_tutor_conversations,
    delete_tutor_conversation,
)

st = importlib.import_module("streamlit")


# ============================================================
# SHOW HISTORY PAGE
# ============================================================

def show_history():

    # ========================================================
    # CURRENT USER
    # ========================================================

    user = get_current_user()

    if user is None:

        st.warning(
            "⚠️ User session not found. "
            "Please login again."
        )

        return

    # ========================================================
    # USER ID
    # ========================================================

    user_id = getattr(
        user,
        "id",
        None,
    )

    if user_id is None:

        st.error(
            "❌ User ID not found."
        )

        return

    # ========================================================
    # HEADER
    # ========================================================

    st.title(
        "📚 AI Tutor History"
    )

    st.write(
        "Search, review, and manage your "
        "previous AI Tutor conversations."
    )

    st.divider()

    # ========================================================
    # LOAD CONVERSATIONS
    # ========================================================

    db = SessionLocal()

    try:

        conversations = get_user_conversations(
            db=db,
            user_id=user_id,
            limit=500,
        )

    except Exception as e:

        st.error(
            f"❌ Could not load history: {e}"
        )

        return

    finally:

        db.close()

    # ========================================================
    # NO HISTORY
    # ========================================================

    if not conversations:

        st.info(
            "💬 No AI Tutor conversations found."
        )

        st.write(
            "Go to **🤖 AI Tutor** and ask "
            "your first question."
        )

        return

    # ========================================================
    # SUMMARY
    # ========================================================

    st.success(
        f"📖 Total conversations: "
        f"**{len(conversations)}**"
    )

    st.divider()

    # ========================================================
    # SEARCH
    # ========================================================

    st.subheader(
        "🔎 Search Conversations"
    )

    search_text = st.text_input(
        "Search by question or answer:",
        placeholder=(
            "Example: Python, machine learning, CNN..."
        ),
        key="history_search",
    )

    # ========================================================
    # FILTER
    # ========================================================

    st.subheader(
        "📅 Filter"
    )

    filter_option = st.selectbox(
        "Show:",
        [
            "All conversations",
            "Last 7 conversations",
            "Last 30 conversations",
        ],
        key="history_filter",
    )

    # ========================================================
    # APPLY FILTER
    # ========================================================

    filtered_conversations = list(
        conversations
    )

    if filter_option == "Last 7 conversations":

        filtered_conversations = (
            filtered_conversations[-7:]
        )

    elif filter_option == "Last 30 conversations":

        filtered_conversations = (
            filtered_conversations[-30:]
        )

    # ========================================================
    # APPLY SEARCH
    # ========================================================

    if search_text:

        search_text = (
            search_text.strip().lower()
        )

        if search_text:

            results = []

            for conversation in (
                filtered_conversations
            ):

                question = getattr(
                    conversation,
                    "question",
                    "",
                )

                answer = getattr(
                    conversation,
                    "answer",
                    "",
                )

                if not isinstance(
                    question,
                    str,
                ):

                    question = str(
                        question
                    )

                if not isinstance(
                    answer,
                    str,
                ):

                    answer = str(
                        answer
                    )

                searchable_text = (
                    question
                    + " "
                    + answer
                ).lower()

                if search_text in searchable_text:

                    results.append(
                        conversation
                    )

            filtered_conversations = results

    # ========================================================
    # RESULT COUNT
    # ========================================================

    st.caption(
        f"Showing "
        f"{len(filtered_conversations)} "
        f"conversation(s)"
    )

    st.divider()

    # ========================================================
    # NO RESULTS
    # ========================================================

    if not filtered_conversations:

        st.warning(
            "🔎 No conversations matched your search."
        )

        return

    # ========================================================
    # DISPLAY CONVERSATIONS
    # ========================================================

    for number, conversation in enumerate(
        reversed(filtered_conversations),
        start=1,
    ):

        conversation_id = getattr(
            conversation,
            "id",
            None,
        )

        question = getattr(
            conversation,
            "question",
            "",
        )

        answer = getattr(
            conversation,
            "answer",
            "",
        )

        created_at = getattr(
            conversation,
            "created_at",
            None,
        )

        # ----------------------------------------------------
        # NORMALIZE
        # ----------------------------------------------------

        if not isinstance(
            question,
            str,
        ):

            question = str(
                question
            )

        if not isinstance(
            answer,
            str,
        ):

            answer = str(
                answer
            )

        question = question.strip()
        answer = answer.strip()

        # ----------------------------------------------------
        # DATE
        # ----------------------------------------------------

        if created_at:

            try:

                date_text = created_at.strftime(
                    "%d %B %Y, %I:%M %p"
                )

            except Exception:

                date_text = str(
                    created_at
                )

        else:

            date_text = "Unknown date"

        # ====================================================
        # CONVERSATION
        # ====================================================

        with st.expander(
            f"💬 Question {number} — {date_text}"
        ):

            st.markdown(
                "### 👤 Your Question"
            )

            st.info(
                question
            )

            st.markdown(
                "### 🤖 EduAccess AI Answer"
            )

            st.markdown(
                answer
            )

            st.caption(
                f"Conversation ID: "
                f"{conversation_id}"
            )

            st.divider()

            # ------------------------------------------------
            # DELETE INDIVIDUAL CONVERSATION
            # ------------------------------------------------

            delete_key = (
                f"delete_conversation_"
                f"{conversation_id}"
            )

            if st.button(
                "🗑️ Delete This Conversation",
                key=delete_key,
                use_container_width=True,
            ):

                db = SessionLocal()

                try:

                    deleted = (
                        delete_tutor_conversation(
                            db=db,
                            conversation_id=conversation_id,
                            user_id=user_id,
                        )
                    )

                    if deleted:

                        st.success(
                            "✅ Conversation deleted."
                        )

                    else:

                        st.warning(
                            "⚠️ Conversation was not found."
                        )

                except Exception as e:

                    st.error(
                        f"❌ Delete failed: {e}"
                    )

                finally:

                    db.close()

                st.rerun()

        st.divider()

    # ========================================================
    # DELETE ALL
    # ========================================================

    st.subheader(
        "🗑️ History Management"
    )

    if "confirm_delete_history" not in st.session_state:

        st.session_state[
            "confirm_delete_history"
        ] = False

    if not st.session_state[
        "confirm_delete_history"
    ]:

        if st.button(
            "🗑️ Delete All History",
            use_container_width=True,
        ):

            st.session_state[
                "confirm_delete_history"
            ] = True

            st.rerun()

    else:

        st.warning(
            "⚠️ This permanently deletes "
            "all your AI Tutor conversations."
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "✅ Yes, Delete Everything",
                use_container_width=True,
            ):

                db = SessionLocal()

                try:

                    deleted = (
                        delete_all_tutor_conversations(
                            db=db,
                            user_id=user_id,
                        )
                    )

                    st.session_state[
                        "confirm_delete_history"
                    ] = False

                    st.success(
                        f"✅ Deleted {deleted} "
                        "conversation(s)."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"❌ Delete failed: {e}"
                    )

                finally:

                    db.close()

        with col2:

            if st.button(
                "❌ Cancel",
                use_container_width=True,
            ):

                st.session_state[
                    "confirm_delete_history"
                ] = False

                st.rerun()

    # ========================================================
    # SECURITY NOTE
    # ========================================================

    st.divider()

    st.caption(
        "🔒 Your history is restricted to "
        "the currently logged-in account."
    )