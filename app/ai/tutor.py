import streamlit as st  # type: ignore

from app.ai.tutor_engine import ask_tutor


# ============================================================
# TEXT TO SPEECH
# ============================================================

def speak_text(text: str):
    try:
        import pyttsx3  # type: ignore

        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        engine.setProperty("volume", 1.0)

        engine.say(text)
        engine.runAndWait()

    except Exception as e:
        st.warning(
            f"🔊 Text-to-Speech unavailable: {e}"
        )


# ============================================================
# INITIALIZE SESSION STATE
# ============================================================

def initialize_tutor_state():

    if "tutor_history" not in st.session_state:
        st.session_state.tutor_history = []

    if "tutor_question" not in st.session_state:
        st.session_state.tutor_question = ""


# ============================================================
# AI TUTOR PAGE
# ============================================================

def show_tutor():

    initialize_tutor_state()

    # ========================================================
    # HEADER
    # ========================================================

    st.title("🤖 EduAccess AI Tutor")

    st.markdown(
        """
        ### Your Personalized Learning Assistant

        Ask educational questions using text or voice.
        EduAccess AI will provide an accessible,
        personalized explanation.
        """
    )

    st.divider()

    # ========================================================
    # SIDEBAR
    # ========================================================

    with st.sidebar:

        st.subheader("⚙️ Tutor Controls")

        if st.button(
            "🗑️ Clear Conversation",
            use_container_width=True,
        ):

            st.session_state.tutor_history = []
            st.session_state.tutor_question = ""

            st.rerun()

        st.divider()

        st.write(
            f"💬 Questions asked: "
            f"{len(st.session_state.tutor_history)}"
        )

    # ========================================================
    # CONVERSATION HISTORY
    # ========================================================

    if st.session_state.tutor_history:

        st.subheader("💬 Conversation")

        for index, chat in enumerate(
            st.session_state.tutor_history
        ):

            with st.chat_message("user"):

                st.markdown(
                    chat["question"]
                )

            with st.chat_message("assistant"):

                st.markdown(
                    chat["answer"]
                )

                if st.button(
                    "🔊 Read Answer",
                    key=f"tts_answer_{index}",
                ):

                    speak_text(
                        chat["answer"]
                    )

        st.divider()

    else:

        st.info(
            "💡 No conversation yet. "
            "Ask your first question below."
        )

    # ========================================================
    # QUESTION INPUT
    # ========================================================

    st.subheader("📝 Ask Your Question")

    question = st.text_area(
        "Type your question:",
        value=st.session_state.tutor_question,
        placeholder=(
            "Example: Explain machine learning "
            "in simple language."
        ),
        height=120,
        key="tutor_question_box",
    )

    # ========================================================
    # IMPORTANT:
    # SAVE THE CURRENT TEXT IMMEDIATELY
    # ========================================================

    st.session_state.tutor_question = question

    # ========================================================
    # VOICE INPUT
    # ========================================================

    st.subheader("🎤 Voice Input")

    audio = st.audio_input(
        "Click here and speak your question"
    )

    if audio is not None:

        st.audio(
            audio,
            format="audio/wav",
        )

        st.info(
            "🎤 Voice recording received."
        )

    # ========================================================
    # ASK BUTTON
    # ========================================================

    st.divider()

    ask_clicked = st.button(
        "🤖 Ask EduAccess AI",
        type="primary",
        use_container_width=True,
    )

    if not ask_clicked:
        return

    # ========================================================
    # GET QUESTION FROM SESSION STATE
    # ========================================================

    question = st.session_state.get(
        "tutor_question",
        "",
    )

    # Ensure question is a string
    if question is None:
        question = ""

    if not isinstance(question, str):

        question = str(question)

    question = question.strip()

    # ========================================================
    # VALIDATE QUESTION
    # ========================================================

    if not question:

        st.warning(
            "⚠️ Please enter a question first."
        )

        return

    # ========================================================
    # GET LOGGED-IN USER
    # ========================================================

    user = st.session_state.get(
        "user"
    )

    if user is None:

        st.error(
            "❌ User session not found. "
            "Please login again."
        )

        return

    # ========================================================
    # BUILD CONVERSATION CONTEXT
    # ========================================================

    conversation_context = ""

    for chat in st.session_state.tutor_history:

        old_question = str(
            chat.get(
                "question",
                "",
            )
        )

        old_answer = str(
            chat.get(
                "answer",
                "",
            )
        )

        conversation_context += (
            f"Student: {old_question}\n"
            f"EduAccess AI: {old_answer}\n\n"
        )

    # ========================================================
    # ASK GEMINI
    # ========================================================

    with st.spinner(
        "🤖 EduAccess AI is thinking..."
    ):

        try:

            answer = ask_tutor(
                user=user,
                question=question,
                context=conversation_context,
            )

        except TypeError:

            # ------------------------------------------------
            # Compatibility fallback:
            # If an older tutor_engine.py does not support
            # context, still answer the question.
            # ------------------------------------------------

            answer = ask_tutor(
                user,
                question,
            )

        except Exception as e:

            st.error(
                "❌ AI Tutor error:\n\n"
                f"{str(e)}"
            )

            return

    # ========================================================
    # ENSURE ANSWER IS TEXT
    # ========================================================

    if answer is None:

        answer = (
            "⚠️ Sorry, no answer was generated."
        )

    elif not isinstance(answer, str):

        answer = str(answer)

    answer = answer.strip()

    # ========================================================
    # SAVE CONVERSATION
    # ========================================================

    st.session_state.tutor_history.append(
        {
            "question": question,
            "answer": answer,
        }
    )

    # ========================================================
    # CLEAR QUESTION AFTER SUCCESS
    # ========================================================

    st.session_state.tutor_question = ""

    # ========================================================
    # SHOW RESULT
    # ========================================================

    st.rerun()