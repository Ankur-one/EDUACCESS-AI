from collections import OrderedDict

import streamlit as st  # type: ignore[import-not-found]

from app.auth.session import get_current_user_id
from app.database.database import SessionLocal
from app.database.tutor_crud import (
    get_user_conversations,
    delete_tutor_conversation,
    delete_all_tutor_conversations,
)


# ============================================================
# GROUP CONVERSATIONS BY SESSION
# ============================================================

def group_conversations_by_session(conversations):

    grouped = OrderedDict()

    for conversation in conversations:

        session_id = getattr(
            conversation,
            "session_id",
            None,
        )

        if not session_id:
            session_id = "legacy"

        if session_id not in grouped:
            grouped[session_id] = []

        grouped[session_id].append(
            conversation
        )

    return grouped


# ============================================================
# SESSION TITLE
# ============================================================

def get_session_title(
    conversations,
    session_number,
):

    if not conversations:
        return f"Session {session_number}"

    question = str(
        conversations[0].question or ""
    ).strip()

    if not question:
        return f"Session {session_number}"

    if len(question) > 70:
        question = question[:70] + "..."

    return question


# ============================================================
# SESSION DATE
# ============================================================

def get_session_date(conversations):

    if not conversations:
        return "Unknown time"

    created_at = conversations[0].created_at

    if not created_at:
        return "Unknown time"

    return created_at.strftime(
        "%d %b %Y, %I:%M %p"
    )


# ============================================================
# SEARCH
# ============================================================

def search_conversations(
    conversations,
    search_text,
):

    if not search_text:
        return conversations

    search_text = (
        str(search_text)
        .strip()
        .lower()
    )

    if not search_text:
        return conversations

    results = []

    for conversation in conversations:

        question = str(
            conversation.question or ""
        ).lower()

        answer = str(
            conversation.answer or ""
        ).lower()

        if (
            search_text in question
            or search_text in answer
        ):

            results.append(
                conversation
            )

    return results


# ============================================================
# CONTINUE SESSION
# ============================================================

def continue_session(session_id):

    # Store the selected session.
    st.session_state.tutor_session_id = (
        session_id
    )

    # Tell tutor page that this is an existing
    # conversation being continued.
    st.session_state.continue_tutor_session = True

    # Clear any previous input safely.
    st.session_state.tutor_input_value = ""

    st.session_state.tutor_clear_input = True

    # Remove old temporary answer.
    st.session_state.tutor_answer = ""

    # Navigate to Tutor page.
    st.session_state.selected_page = (
        "🤖 AI Tutor"
    )

    st.rerun()


# ============================================================
# SHOW TUTOR HISTORY
# ============================================================

def show_tutor_history():

    st.title("📚 Tutor History")

    st.caption(
        "Search, review, and continue your "
        "previous AI Tutor sessions."
    )

    st.divider()

    # ========================================================
    # CURRENT USER
    # ========================================================

    user_id = get_current_user_id()

    if not user_id:

        st.warning(
            "⚠️ User session not found. "
            "Please login again."
        )

        return

    # ========================================================
    # DATABASE
    # ========================================================

    db = SessionLocal()

    try:

        conversations = get_user_conversations(
            db=db,
            user_id=user_id,
            limit=500,
        )

        # ====================================================
        # EMPTY HISTORY
        # ====================================================

        if not conversations:

            st.info(
                "📭 No tutor history found yet."
            )

            st.write(
                "Ask a question in AI Tutor "
                "to create your first session."
            )

            return

        # ====================================================
        # SEARCH
        # ====================================================

        st.subheader(
            "🔍 Search Tutor History"
        )

        search_text = st.text_input(
            "Search questions or answers",
            placeholder=(
                "Example: Python, CNN, "
                "machine learning..."
            ),
        )

        filtered_conversations = (
            search_conversations(
                conversations,
                search_text,
            )
        )

        # ====================================================
        # GROUP
        # ====================================================

        grouped_sessions = (
            group_conversations_by_session(
                filtered_conversations
            )
        )

        # ====================================================
        # STATISTICS
        # ====================================================

        total_questions = len(
            filtered_conversations
        )

        total_sessions = len(
            grouped_sessions
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "📚 Sessions",
                total_sessions,
            )

        with col2:

            st.metric(
                "💬 Questions",
                total_questions,
            )

        st.divider()

        # ====================================================
        # NO SEARCH RESULT
        # ====================================================

        if (
            search_text
            and not filtered_conversations
        ):

            st.warning(
                f'🔎 No results found for '
                f'"{search_text}".'
            )

            return

        # ====================================================
        # MANAGE HISTORY
        # ====================================================

        with st.expander(
            "⚠️ Manage Tutor History"
        ):

            st.warning(
                "Deleting all history cannot be undone."
            )

            if st.button(
                "🗑️ Delete All Tutor History",
                use_container_width=True,
            ):

                deleted = (
                    delete_all_tutor_conversations(
                        db=db,
                        user_id=user_id,
                    )
                )

                st.success(
                    f"Deleted {deleted} conversation(s)."
                )

                st.rerun()

        st.divider()

        # ====================================================
        # SESSION LIST
        # ====================================================

        st.subheader(
            "🗂️ Your Tutor Sessions"
        )

        # ====================================================
        # DISPLAY SESSIONS
        # ====================================================

        for session_number, (
            session_id,
            session_conversations,
        ) in enumerate(
            grouped_sessions.items(),
            start=1,
        ):

            session_title = get_session_title(
                session_conversations,
                session_number,
            )

            session_date = get_session_date(
                session_conversations
            )

            question_count = len(
                session_conversations
            )

            # ------------------------------------------------
            # SESSION HEADER
            # ------------------------------------------------

            if session_id == "legacy":

                session_label = (
                    f"📁 Session {session_number} "
                    f"• Legacy History"
                )

            else:

                session_label = (
                    f"📁 Session {session_number} "
                    f"• {session_title}"
                )

            with st.expander(
                session_label,
                expanded=False,
            ):

                # --------------------------------------------
                # SESSION INFORMATION
                # --------------------------------------------

                col1, col2 = st.columns(2)

                with col1:

                    st.caption(
                        f"🕒 Started: {session_date}"
                    )

                with col2:

                    st.caption(
                        f"💬 {question_count} "
                        f"question(s)"
                    )

                # --------------------------------------------
                # CONTINUE BUTTON
                # --------------------------------------------

                if session_id != "legacy":

                    continue_key = (
                        "continue_session_"
                        f"{session_id}"
                    )

                    if st.button(
                        "▶️ Continue This Session",
                        key=continue_key,
                        use_container_width=True,
                        type="primary",
                    ):

                        continue_session(
                            session_id
                        )

                else:

                    st.info(
                        "This is older history without "
                        "a session ID, so it cannot be "
                        "continued as a session."
                    )

                st.divider()

                # --------------------------------------------
                # CONVERSATIONS
                # --------------------------------------------

                for index, conversation in enumerate(
                    session_conversations,
                    start=1,
                ):

                    created_at = (
                        conversation.created_at
                    )

                    if created_at:

                        time_text = (
                            created_at.strftime(
                                "%d %b %Y, %I:%M %p"
                            )
                        )

                    else:

                        time_text = "Unknown time"

                    st.markdown(
                        f"### 👤 Question {index}"
                    )

                    st.caption(
                        f"🕒 {time_text}"
                    )

                    st.write(
                        conversation.question
                    )

                    st.markdown(
                        "### 🤖 AI Tutor Answer"
                    )

                    st.markdown(
                        conversation.answer
                    )

                    # ----------------------------------------
                    # DELETE
                    # ----------------------------------------

                    delete_key = (
                        "delete_history_"
                        f"{conversation.id}"
                    )

                    if st.button(
                        "🗑️ Delete This Conversation",
                        key=delete_key,
                    ):

                        deleted = (
                            delete_tutor_conversation(
                                db=db,
                                conversation_id=(
                                    conversation.id
                                ),
                                user_id=user_id,
                            )
                        )

                        if deleted:

                            st.success(
                                "Conversation deleted."
                            )

                        else:

                            st.error(
                                "Conversation could not "
                                "be deleted."
                            )

                        st.rerun()

                    st.divider()

    except Exception as e:

        st.error(
            "❌ Unable to load tutor history."
        )

        st.exception(e)

    finally:

        db.close()
