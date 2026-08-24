import importlib

from app.auth.session import get_current_user_id
from app.database.database import SessionLocal
from app.database.models import User
from app.database.tutor_crud import get_user_conversations

st = importlib.import_module("streamlit")


# ============================================================
# SHOW DASHBOARD
# ============================================================

def show_dashboard():

    st.title("🏠 EduAccess AI Dashboard")

    st.caption(
        "Your personalized learning and accessibility dashboard."
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
        # GET USER
        # ====================================================

        user = (
            db.query(User)
            .filter(
                User.id == user_id
            )
            .first()
        )

        if user is None:

            st.error(
                "❌ User account could not be found."
            )

            return

        # ====================================================
        # GET TUTOR HISTORY
        # ====================================================

        conversations = get_user_conversations(
            db=db,
            user_id=user_id,
            limit=100,
        )

        # ====================================================
        # WELCOME
        # ====================================================

        st.subheader(
            f"👋 Welcome, {user.full_name}!"
        )

        st.write(
            "EduAccess AI is ready to help you learn "
            "in a way that matches your accessibility "
            "preferences."
        )

        st.divider()

        # ====================================================
        # STATISTICS
        # ====================================================

        total_questions = len(
            conversations
        )

        active_dates = set()

        for conversation in conversations:

            created_at = getattr(
                conversation,
                "created_at",
                None,
            )

            if created_at:

                active_dates.add(
                    created_at.date()
                )

        active_days = len(
            active_dates
        )

        # ====================================================
        # STAT CARDS
        # ====================================================

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "💬 Questions",
                total_questions,
            )

        with col2:

            st.metric(
                "🤖 AI Answers",
                total_questions,
            )

        with col3:

            st.metric(
                "📅 Active Days",
                active_days,
            )

        with col4:

            st.metric(
                "♿ Accessibility",
                "Enabled",
            )

        st.divider()

        # ====================================================
        # QUICK ACTIONS
        # ====================================================

        st.subheader(
            "🚀 Quick Actions"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "🤖 Open AI Tutor",
                use_container_width=True,
                type="primary",
                key="dashboard_open_tutor",
            ):

                st.session_state[
                    "selected_page"
                ] = "AI Tutor"

                st.rerun()

        with col2:

            if st.button(
                "📚 View Tutor History",
                use_container_width=True,
                key="dashboard_open_history",
            ):

                st.session_state[
                    "selected_page"
                ] = "History"

                st.rerun()

        st.divider()

        # ====================================================
        # ACCESSIBILITY PROFILE
        # ====================================================

        st.subheader(
            "♿ Your Accessibility Preferences"
        )

        preferences = []

        if user.simple_explanation:

            preferences.append(
                "Simple explanations"
            )

        if user.step_by_step:

            preferences.append(
                "Step-by-step learning"
            )

        if user.repetition_support:

            preferences.append(
                "Repetition support"
            )

        if user.visual_explanation:

            preferences.append(
                "Visual explanations"
            )

        if user.text_to_speech:

            preferences.append(
                "Text-to-speech"
            )

        if user.speech_to_text:

            preferences.append(
                "Speech-to-text"
            )

        if user.large_text:

            preferences.append(
                "Large text"
            )

        if user.high_contrast:

            preferences.append(
                "High contrast"
            )

        if user.dyslexia_friendly:

            preferences.append(
                "Dyslexia-friendly mode"
            )

        if preferences:

            for preference in preferences:

                st.write(
                    f"✓ {preference}"
                )

        else:

            st.info(
                "No additional accessibility "
                "preferences are enabled."
            )

        st.divider()

        # ====================================================
        # LANGUAGE
        # ====================================================

        st.subheader(
            "🌐 Learning Language"
        )

        st.info(
            user.preferred_language
            or "English"
        )

        st.divider()

        # ====================================================
        # RECENT ACTIVITY
        # ====================================================

        st.subheader(
            "🕒 Recent Learning Activity"
        )

        if not conversations:

            st.info(
                "📭 No learning activity yet."
            )

            st.write(
                "Start by asking a question in "
                "the AI Tutor."
            )

        else:

            # Latest five conversations
            recent = list(
                reversed(
                    conversations[-5:]
                )
            )

            for conversation in recent:

                created_at = getattr(
                    conversation,
                    "created_at",
                    None,
                )

                if created_at:

                    time_text = created_at.strftime(
                        "%d %b %Y, %I:%M %p"
                    )

                else:

                    time_text = (
                        "Date unavailable"
                    )

                question = (
                    conversation.question
                    or "Question unavailable"
                )

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"**💬 {question}**"
                    )

                    st.caption(
                        f"🕒 {time_text}"
                    )

                    answer = (
                        conversation.answer
                        or ""
                    )

                    if answer:

                        preview = answer.strip()

                        if len(preview) > 180:

                            preview = (
                                preview[:180]
                                + "..."
                            )

                        st.write(
                            preview
                        )

        st.divider()

        # ====================================================
        # DISABILITY INFORMATION
        # ====================================================

        st.subheader(
            "ℹ️ Accessibility Profile"
        )

        disability_type = getattr(
            user,
            "disability_type",
            None,
        )

        disability_details = getattr(
            user,
            "disability_details",
            None,
        )

        if disability_type:

            st.write(
                f"**Accessibility need:** "
                f"{disability_type}"
            )

        if disability_details:

            st.write(
                f"**Additional information:** "
                f"{disability_details}"
            )

        if not disability_type and not disability_details:

            st.info(
                "No additional accessibility "
                "information provided."
            )

    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as error:

        st.error(
            "❌ Unable to load dashboard."
        )

        st.exception(error)

    # ========================================================
    # CLOSE DATABASE
    # ========================================================

    finally:

        db.close()
