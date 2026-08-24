import streamlit as st  # type: ignore[import-not-found]

from app.auth.session import get_current_user_id
from app.database.database import SessionLocal
from app.database.tutor_crud import (
    get_user_conversations,
    delete_tutor_conversation,
    delete_all_tutor_conversations,
)


# ============================================================
# HISTORY PAGE
# ============================================================

def show_history():

    st.title("📚 Tutor History")

    st.caption(
        "View your previous EduAccess AI Tutor conversations."
    )

    st.divider()

    # ========================================================
    # GET CURRENT USER
    # ========================================================

    user_id = get_current_user_id()

    if not user_id:

        st.warning(
            "⚠️ User session not found. Please login again."
        )

        return

    # ========================================================
    # DATABASE
    # ========================================================

    db = SessionLocal()

    try:

        # ====================================================
        # LOAD CONVERSATIONS
        # ====================================================

        conversations = get_user_conversations(
            db=db,
            user_id=user_id,
            limit=100,
        )

        # ====================================================
        # EMPTY HISTORY
        # ====================================================

        if not conversations:

            st.info(
                "📭 No tutor history available."
            )

            st.write(
                "Go to **AI Tutor** and ask your first "
                "question."
            )

            return

        # ====================================================
        # TOP STATISTICS
        # ====================================================

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "💬 Questions",
                len(conversations),
            )

        with col2:

            # Count unique dates
            dates = set()

            for conversation in conversations:

                created_at = getattr(
                    conversation,
                    "created_at",
                    None,
                )

                if created_at:

                    dates.add(
                        created_at.date()
                    )

            st.metric(
                "📅 Active Days",
                len(dates),
            )

        with col3:

            st.metric(
                "🤖 AI Answers",
                len(conversations),
            )

        st.divider()

        # ====================================================
        # SEARCH
        # ====================================================

        search_text = st.text_input(
            "🔎 Search your tutor history",
            placeholder=(
                "Search by question or answer..."
            ),
            key="history_search",
        )

        # ====================================================
        # FILTER
        # ========================================================

        if search_text.strip():

            search_value = (
                search_text
                .strip()
                .lower()
            )

            filtered = []

            for conversation in conversations:

                question = (
                    conversation.question
                    or ""
                ).lower()

                answer = (
                    conversation.answer
                    or ""
                ).lower()

                if (
                    search_value in question
                    or search_value in answer
                ):

                    filtered.append(
                        conversation
                    )

        else:

            filtered = conversations

        # ====================================================
        # RESULT INFORMATION
        # ====================================================

        st.caption(
            f"Showing {len(filtered)} "
            f"of {len(conversations)} conversations"
        )

        st.divider()

        # ====================================================
        # GROUP BY DATE
        # ====================================================

        grouped = {}

        for conversation in filtered:

            created_at = getattr(
                conversation,
                "created_at",
                None,
            )

            if created_at:

                date_key = created_at.date()

            else:

                date_key = "Unknown Date"

            if date_key not in grouped:

                grouped[date_key] = []

            grouped[date_key].append(
                conversation
            )

        # ====================================================
        # DISPLAY GROUPS
        # ====================================================

        for date_key, items in grouped.items():

            # ------------------------------------------------
            # DATE HEADING
            # ------------------------------------------------

            if date_key != "Unknown Date":

                date_title = date_key.strftime(
                    "%A, %d %B %Y"
                )

            else:

                date_title = "Unknown Date"

            st.subheader(
                f"📅 {date_title}"
            )

            # ------------------------------------------------
            # CONVERSATIONS
            # ------------------------------------------------

            for conversation in items:

                question = (
                    conversation.question
                    or "Untitled Question"
                )

                created_at = getattr(
                    conversation,
                    "created_at",
                    None,
                )

                if created_at:

                    time_text = created_at.strftime(
                        "%I:%M %p"
                    )

                else:

                    time_text = "Time unavailable"

                # ------------------------------------------------
                # EXPANDER
                # ------------------------------------------------

                with st.expander(
                    f"💬 {question[:90]} "
                    f"  •  🕒 {time_text}"
                ):

                    # ============================================
                    # QUESTION
                    # ============================================

                    st.markdown(
                        "### 👤 Your Question"
                    )

                    st.info(
                        question
                    )

                    # ============================================
                    # ANSWER
                    # ============================================

                    st.markdown(
                        "### 🤖 EduAccess AI Answer"
                    )

                    answer = (
                        conversation.answer
                        or "No answer available."
                    )

                    st.markdown(
                        answer
                    )

                    st.divider()

                    # ============================================
                    # CONVERSATION ID
                    # ============================================

                    st.caption(
                        f"Conversation ID: "
                        f"{conversation.id}"
                    )

                    # ============================================
                    # DELETE
                    # ============================================

                    delete_key = (
                        f"delete_history_"
                        f"{conversation.id}"
                    )

                    if st.button(
                        "🗑️ Delete Conversation",
                        key=delete_key,
                        use_container_width=True,
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
                                "✅ Conversation deleted."
                            )

                            st.rerun()

                        else:

                            st.error(
                                "❌ Conversation could "
                                "not be deleted."
                            )

            st.divider()

        # ====================================================
        # DELETE ALL
        # ====================================================

        st.subheader(
            "⚠️ History Management"
        )

        st.write(
            "Deleting history permanently removes "
            "your saved tutor conversations."
        )

        if st.button(
            "🗑️ Delete All Tutor History",
            use_container_width=True,
            key="delete_all_history_button",
        ):

            st.session_state[
                "confirm_delete_all_history"
            ] = True

        # ====================================================
        # CONFIRMATION
        # ====================================================

        if st.session_state.get(
            "confirm_delete_all_history",
            False,
        ):

            st.warning(
                "⚠️ Are you sure you want to delete "
                "ALL tutor conversations?"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✅ Yes, Delete All",
                    use_container_width=True,
                    key="yes_delete_all_history",
                ):

                    count = (
                        delete_all_tutor_conversations(
                            db=db,
                            user_id=user_id,
                        )
                    )

                    st.session_state[
                        "confirm_delete_all_history"
                    ] = False

                    st.success(
                        f"✅ Successfully deleted "
                        f"{count} conversation(s)."
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "❌ Cancel",
                    use_container_width=True,
                    key="cancel_delete_all_history",
                ):

                    st.session_state[
                        "confirm_delete_all_history"
                    ] = False

                    st.rerun()

    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as error:

        st.error(
            "❌ Unable to load tutor history."
        )

        st.exception(error)

    # ========================================================
    # CLOSE DATABASE
    # ========================================================

    finally:

        db.close()