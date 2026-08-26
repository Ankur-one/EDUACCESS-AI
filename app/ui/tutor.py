import uuid

import streamlit as st  # type: ignore[import-not-found]

from app.auth.session import get_current_user_id
from app.database.database import SessionLocal
from app.database.models import User
from app.database.tutor_crud import (
    save_tutor_conversation,
    get_session_conversations,
)
from app.ai.tutor_engine import ask_tutor


# ============================================================
# INITIALIZE TUTOR STATE
# ============================================================

def initialize_tutor_state():
    """
    Initialize all Tutor-related Streamlit session variables.
    """

    if "tutor_session_id" not in st.session_state:
        st.session_state.tutor_session_id = str(
            uuid.uuid4()
        )

    if "tutor_answer" not in st.session_state:
        st.session_state.tutor_answer = ""

    if "continue_tutor_session" not in st.session_state:
        st.session_state.continue_tutor_session = False


# ============================================================
# CREATE NEW TUTOR SESSION
# ============================================================

def create_new_tutor_session():
    """
    Start a completely new AI Tutor session.
    """

    st.session_state.tutor_session_id = str(
        uuid.uuid4()
    )

    st.session_state.tutor_answer = ""

    st.session_state.continue_tutor_session = False


# ============================================================
# LOAD CURRENT USER
# ============================================================

def get_current_user(db, user_id):
    """
    Load the currently logged-in user from the database.
    """

    return (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )


# ============================================================
# SHOW ACCESSIBILITY INFORMATION
# ============================================================

def show_accessibility_information(user):
    """
    Display the student's saved accessibility preferences.
    """

    st.subheader(
        "♿ Accessibility & Learning Preferences"
    )

    st.write(
        "🌐 Language: "
        f"**{user.preferred_language or 'English'}**"
    )

    preferences = []

    if user.simple_explanation:
        preferences.append(
            "✓ Simple explanations"
        )

    if user.step_by_step:
        preferences.append(
            "✓ Step-by-step learning"
        )

    if user.repetition_support:
        preferences.append(
            "✓ Repetition support"
        )

    if user.visual_explanation:
        preferences.append(
            "✓ Visual explanations"
        )

    if user.text_to_speech:
        preferences.append(
            "✓ Text-to-speech"
        )

    if user.speech_to_text:
        preferences.append(
            "✓ Speech-to-text"
        )

    if user.large_text:
        preferences.append(
            "✓ Large text"
        )

    if user.high_contrast:
        preferences.append(
            "✓ High contrast"
        )

    if user.dyslexia_friendly:
        preferences.append(
            "✓ Dyslexia friendly"
        )

    if preferences:

        for preference in preferences:
            st.write(preference)

    else:

        st.caption(
            "No additional accessibility preferences "
            "are currently enabled."
        )


# ============================================================
# DISPLAY CONVERSATION
# ============================================================

def show_conversation(conversations):
    """
    Display the current Tutor session conversation.
    """

    st.subheader(
        "💬 Current Conversation"
    )

    if not conversations:

        st.info(
            "👋 This is a new Tutor session. "
            "Ask your first question below."
        )

        return

    for conversation in conversations:

        question = str(
            getattr(
                conversation,
                "question",
                "",
            )
            or ""
        ).strip()

        answer = str(
            getattr(
                conversation,
                "answer",
                "",
            )
            or ""
        ).strip()

        if question:

            with st.chat_message("user"):

                st.markdown(question)

        if answer:

            with st.chat_message("assistant"):

                st.markdown(answer)


# ============================================================
# SHOW TUTOR
# ============================================================

def show_tutor():
    """
    Main AI Tutor interface.
    """

    # ========================================================
    # INITIALIZE STATE
    # ========================================================

    initialize_tutor_state()

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.title(
        "🤖 EduAccess AI Tutor"
    )

    st.caption(
        "Ask questions using text or voice and receive "
        "personalized accessible explanations."
    )

    st.divider()

    # ========================================================
    # CURRENT USER ID
    # ========================================================

    user_id = get_current_user_id()

    if user_id is None:

        st.warning(
            "⚠️ User session not found. "
            "Please login again."
        )

        return

    # ========================================================
    # CURRENT SESSION ID
    # ========================================================

    session_id = (
        st.session_state.tutor_session_id
    )

    # ========================================================
    # DATABASE
    # ========================================================

    db = SessionLocal()

    try:

        # ====================================================
        # LOAD USER
        # ====================================================

        user = get_current_user(
            db=db,
            user_id=user_id,
        )

        if user is None:

            st.error(
                "❌ User account could not be found."
            )

            return

        # ====================================================
        # SESSION CONTROLS
        # ====================================================

        col1, col2 = st.columns(2)

        with col1:

            new_session_button = st.button(
                "🆕 New Tutor Session",
                use_container_width=True,
                key="new_tutor_session_button",
            )

        with col2:

            continue_session_button = st.button(
                "↩️ Continue Current Session",
                use_container_width=True,
                key="continue_tutor_session_button",
            )

        # ====================================================
        # NEW SESSION
        # ====================================================

        if new_session_button:

            create_new_tutor_session()

            st.rerun()

        # ====================================================
        # CONTINUE SESSION
        # ========================================================

        if continue_session_button:

            st.session_state.continue_tutor_session = True

        # ====================================================
        # ACCESSIBILITY
        # ====================================================

        with st.expander(
            "♿ Accessibility Settings",
            expanded=False,
        ):

            show_accessibility_information(
                user
            )

        st.divider()

        # ====================================================
        # LOAD CONVERSATIONS
        # ====================================================

        conversations = get_session_conversations(
            db=db,
            user_id=user_id,
            session_id=session_id,
            limit=100,
        )

        # ====================================================
        # SHOW CONVERSATION
        # ====================================================

        show_conversation(
            conversations
        )

        st.divider()

        # ====================================================
        # QUESTION SECTION
        # ====================================================

        st.subheader(
            "❓ Ask the AI Tutor"
        )

        st.caption(
            "Type your question below."
        )

        # ====================================================
        # QUESTION FORM
        #
        # Using a form prevents us from modifying the
        # widget's session state after it has been created.
        # ====================================================

        with st.form(
            key="tutor_question_form",
            clear_on_submit=True,
        ):

            question = st.text_area(
                "Your question",
                placeholder=(
                    "Example: Explain inheritance in Java "
                    "with a simple example."
                ),
                height=150,
                key="tutor_question",
            )

            ask_button = st.form_submit_button(
                "🤖 Ask AI Tutor",
                use_container_width=True,
            )

        # ====================================================
        # PROCESS QUESTION
        # ====================================================

        if ask_button:

            clean_question = (
                question.strip()
                if isinstance(
                    question,
                    str,
                )
                else ""
            )

            # ------------------------------------------------
            # VALIDATION
            # ------------------------------------------------

            if not clean_question:

                st.warning(
                    "⚠️ Please enter a question first."
                )

                return

            # ------------------------------------------------
            # RELOAD CONVERSATION HISTORY
            # ------------------------------------------------

            conversation_history = (
                get_session_conversations(
                    db=db,
                    user_id=user_id,
                    session_id=session_id,
                    limit=100,
                )
            )

            # ------------------------------------------------
            # ASK AI
            # ------------------------------------------------

            with st.spinner(
                "🤖 EduAccess AI is thinking..."
            ):

                answer = ask_tutor(
                    user=user,
                    question=clean_question,
                    conversation_history=conversation_history,
                )

            # ------------------------------------------------
            # VALIDATE ANSWER
            # ------------------------------------------------

            if not answer:

                st.error(
                    "❌ The AI Tutor did not return an answer."
                )

                return

            # ------------------------------------------------
            # SAVE CONVERSATION
            # ------------------------------------------------

            try:

                save_tutor_conversation(
                    db=db,
                    user_id=user_id,
                    session_id=session_id,
                    question=clean_question,
                    answer=str(answer),
                )

            except Exception as save_error:

                db.rollback()

                st.error(
                    "⚠️ The AI answered, but the "
                    "conversation could not be saved."
                )

                st.exception(
                    save_error
                )

                return

            # ------------------------------------------------
            # STORE LATEST ANSWER
            # ------------------------------------------------

            st.session_state.tutor_answer = str(
                answer
            )

            # ------------------------------------------------
            # REFRESH PAGE
            #
            # clear_on_submit=True already clears the form.
            # We do NOT modify st.session_state.tutor_question.
            # ------------------------------------------------

            st.rerun()

        # ====================================================
        # LATEST ANSWER
        # ====================================================

        if st.session_state.tutor_answer:

            st.divider()

            st.subheader(
                "🤖 Latest AI Answer"
            )

            st.markdown(
                st.session_state.tutor_answer
            )

    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as error:

        st.error(
            "❌ AI Tutor encountered an error."
        )

        st.exception(
            error
        )

    finally:

        db.close()
