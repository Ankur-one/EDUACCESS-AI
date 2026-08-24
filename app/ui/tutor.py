import uuid

import streamlit as st  # pyright: ignore[reportMissingImports]

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

    if "tutor_session_id" not in st.session_state:

        st.session_state.tutor_session_id = str(
            uuid.uuid4()
        )

    if "tutor_answer" not in st.session_state:

        st.session_state.tutor_answer = ""

    if "tutor_input_value" not in st.session_state:

        st.session_state.tutor_input_value = ""

    if "tutor_clear_input" not in st.session_state:

        st.session_state.tutor_clear_input = False

    if "continue_tutor_session" not in st.session_state:

        st.session_state.continue_tutor_session = False


# ============================================================
# CREATE NEW TUTOR SESSION
# ============================================================

def create_new_tutor_session():

    st.session_state.tutor_session_id = str(
        uuid.uuid4()
    )

    st.session_state.tutor_answer = ""

    st.session_state.tutor_input_value = ""

    st.session_state.tutor_clear_input = True

    st.session_state.continue_tutor_session = False


# ============================================================
# SHOW TUTOR
# ============================================================

def show_tutor():

    # ========================================================
    # INITIALIZE SESSION STATE
    # ========================================================

    initialize_tutor_state()

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.title("🤖 EduAccess AI Tutor")

    st.caption(
        "Ask questions using text or voice and receive "
        "personalized accessible explanations."
    )

    st.divider()

    # ========================================================
    # GET CURRENT USER
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
        # CURRENT SESSION ID
        # ====================================================

        session_id = (
            st.session_state.tutor_session_id
        )

        # ====================================================
        # SIDEBAR
        # ====================================================

        with st.sidebar:

            st.subheader(
                "🤖 AI Tutor"
            )

            st.write(
                f"👤 **{user.full_name}**"
            )

            st.divider()

            # ------------------------------------------------
            # NEW SESSION
            # ------------------------------------------------

            if st.button(
                "➕ New Tutor Session",
                use_container_width=True,
                key="new_tutor_session_button",
            ):

                create_new_tutor_session()

                st.rerun()

            # ------------------------------------------------
            # SESSION INFORMATION
            # ------------------------------------------------

            st.caption(
                "Current Session"
            )

            st.code(
                session_id,
                language=None,
            )

            # ------------------------------------------------
            # CONTINUE SESSION MESSAGE
            # ------------------------------------------------

            if st.session_state.get(
                "continue_tutor_session",
                False,
            ):

                st.success(
                    "▶️ Continuing this tutor session."
                )

                st.session_state.continue_tutor_session = (
                    False
                )

            st.divider()

            # ------------------------------------------------
            # ACCESSIBILITY
            # ------------------------------------------------

            st.subheader(
                "♿ Accessibility"
            )

            st.write(
                "Language: "
                f"**{user.preferred_language or 'English'}**"
            )

            if user.simple_explanation:

                st.write(
                    "✓ Simple explanations"
                )

            if user.step_by_step:

                st.write(
                    "✓ Step-by-step learning"
                )

            if user.repetition_support:

                st.write(
                    "✓ Repetition support"
                )

            if user.visual_explanation:

                st.write(
                    "✓ Visual explanations"
                )

            if user.text_to_speech:

                st.write(
                    "✓ Text-to-speech"
                )

            if user.speech_to_text:

                st.write(
                    "✓ Speech-to-text"
                )

            if user.large_text:

                st.write(
                    "✓ Large text"
                )

            if user.high_contrast:

                st.write(
                    "✓ High contrast"
                )

            if user.dyslexia_friendly:

                st.write(
                    "✓ Dyslexia friendly"
                )

        # ====================================================
        # LOAD CURRENT SESSION CONVERSATION
        # ====================================================

        conversations = get_session_conversations(
            db=db,
            user_id=user_id,
            session_id=session_id,
            limit=100,
        )

        # ====================================================
        # CURRENT CONVERSATION
        # ====================================================

        st.subheader(
            "💬 Current Conversation"
        )

        if conversations:

            for conversation in conversations:

                # --------------------------------------------
                # STUDENT MESSAGE
                # --------------------------------------------

                with st.chat_message(
                    "user"
                ):

                    st.markdown(
                        conversation.question
                    )

                # --------------------------------------------
                # AI MESSAGE
                # --------------------------------------------

                with st.chat_message(
                    "assistant"
                ):

                    st.markdown(
                        conversation.answer
                    )

        else:

            st.info(
                "👋 This is a new tutor session. "
                "Ask your first question below."
            )

        st.divider()

        # ====================================================
        # QUESTION SECTION
        # ====================================================

        st.subheader(
            "📝 Ask your question"
        )

        # ====================================================
        # SAFE INPUT CLEAR
        #
        # IMPORTANT:
        # We NEVER directly modify
        # st.session_state.tutor_question
        # after the widget is instantiated.
        # ========================================================

        if st.session_state.tutor_clear_input:

            st.session_state.tutor_input_value = ""

            st.session_state.tutor_clear_input = False

        # ====================================================
        # TEXT INPUT
        # ====================================================

        question = st.text_area(
            "Enter your question:",
            value=st.session_state.tutor_input_value,
            height=120,
            placeholder=(
                "Example: Explain machine learning "
                "in simple language."
            ),
            key="tutor_question",
        )

        # ====================================================
        # STORE CURRENT INPUT
        # ====================================================

        st.session_state.tutor_input_value = question

        # ====================================================
        # BUTTONS
        # ====================================================

        col1, col2 = st.columns(2)

        with col1:

            ask_button = st.button(
                "🤖 Ask AI Tutor",
                use_container_width=True,
                type="primary",
                key="ask_tutor_button",
            )

        with col2:

            clear_button = st.button(
                "🗑️ Clear",
                use_container_width=True,
                key="clear_tutor_button",
            )

        # ====================================================
        # CLEAR INPUT
        # ====================================================

        if clear_button:

            st.session_state.tutor_input_value = ""

            st.session_state.tutor_clear_input = True

            st.rerun()

        # ====================================================
        # ASK AI
        # ====================================================

        if ask_button:

            # ------------------------------------------------
            # VALIDATE QUESTION
            # ------------------------------------------------

            if not isinstance(
                question,
                str,
            ):

                st.error(
                    "❌ Invalid question. "
                    "Please enter a text question."
                )

                return

            clean_question = question.strip()

            if not clean_question:

                st.warning(
                    "⚠️ Please enter a question first."
                )

                return

            # ------------------------------------------------
            # RELOAD SESSION HISTORY
            #
            # This ensures the newest database state is
            # passed to Gemini.
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
            # GENERATE AI ANSWER
            #
            # IMPORTANT:
            # Previous conversation is passed here.
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
            # CHECK ANSWER
            # ------------------------------------------------

            if not answer:

                st.error(
                    "❌ AI Tutor did not return an answer."
                )

                return

            # ------------------------------------------------
            # SAVE CONVERSATION
            # ------------------------------------------------

            try:

                save_tutor_conversation(
                    db=db,
                    user_id=user_id,
                    question=clean_question,
                    answer=answer,
                    session_id=session_id,
                )

                # The CRUD function already commits.
                # No second commit is required.

            except Exception as save_error:

                db.rollback()

                st.error(
                    "⚠️ AI generated an answer, "
                    "but the conversation could not "
                    "be saved."
                )

                st.exception(
                    save_error
                )

                return

            # ------------------------------------------------
            # STORE LATEST ANSWER
            # ------------------------------------------------

            st.session_state.tutor_answer = answer

            # ------------------------------------------------
            # CLEAR INPUT SAFELY
            # ------------------------------------------------

            st.session_state.tutor_input_value = ""

            st.session_state.tutor_clear_input = True

            # ------------------------------------------------
            # REFRESH
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

    except Exception as e:

        st.error(
            "❌ AI Tutor encountered an error."
        )

        st.exception(e)

    # ========================================================
    # CLOSE DATABASE
    # ========================================================

    finally:

        db.close()
