import streamlit as st  # type: ignore[import-unresolved]
from io import BytesIO

from importlib import import_module

from app.auth.session import get_current_user
from app.database.database import SessionLocal
from app.database.tutor_crud import (
    save_tutor_conversation,
    get_user_conversations,
    delete_all_tutor_conversations,
)
from app.ai.tutor_engine import ask_tutor


# ============================================================
# TEXT TO SPEECH
# ============================================================

def generate_speech(text, language="en"):
    """
    Convert AI answer into MP3 audio.
    """

    if text is None:
        return None

    if not isinstance(text, str):
        text = str(text)

    text = text.strip()

    if not text:
        return None

    try:

        audio_buffer = BytesIO()

        # Import lazily so the tutor UI can load even when gTTS is unavailable.
        gTTS = import_module("gtts").gTTS

        tts = gTTS(
            text=text,
            lang=language,
            slow=False,
        )

        tts.write_to_fp(audio_buffer)

        audio_buffer.seek(0)

        return audio_buffer.read()

    except Exception as e:

        st.error(
            f"❌ Text-to-Speech error: {e}"
        )

        return None


# ============================================================
# TTS LANGUAGE
# ============================================================

def get_tts_language(user):

    preferred_language = getattr(
        user,
        "preferred_language",
        "English",
    )

    if not isinstance(
        preferred_language,
        str,
    ):
        preferred_language = "English"

    preferred_language = (
        preferred_language.strip()
    )

    language_map = {
        "English": "en",
        "Hindi": "hi",
        "Punjabi": "pa",
        "Bengali": "bn",
        "Gujarati": "gu",
        "Marathi": "mr",
        "Tamil": "ta",
        "Telugu": "te",
        "Kannada": "kn",
        "Malayalam": "ml",
        "Urdu": "ur",
    }

    return language_map.get(
        preferred_language,
        "en",
    )


# ============================================================
# INITIALIZE SESSION HISTORY
# ============================================================

def initialize_chat_history():

    if "conversation_history" not in st.session_state:

        st.session_state[
            "conversation_history"
        ] = []


# ============================================================
# LOAD DATABASE HISTORY
# ============================================================

def load_database_history(user_id):

    db = SessionLocal()

    try:

        conversations = get_user_conversations(
            db=db,
            user_id=user_id,
            limit=50,
        )

        history = []

        for conversation in conversations:

            history.append(
                {
                    "role": "user",
                    "content": conversation.question,
                }
            )

            history.append(
                {
                    "role": "assistant",
                    "content": conversation.answer,
                }
            )

        return history

    except Exception as e:

        st.error(
            f"❌ Could not load conversation history: {e}"
        )

        return []

    finally:

        db.close()


# ============================================================
# LOAD HISTORY ONLY ONCE
# ============================================================

def initialize_database_history(user_id):

    history_key = (
        f"database_history_loaded_{user_id}"
    )

    if history_key not in st.session_state:

        database_history = load_database_history(
            user_id
        )

        st.session_state[
            "conversation_history"
        ] = database_history

        st.session_state[
            history_key
        ] = True


# ============================================================
# BUILD AI CONTEXT
# ============================================================

def build_conversation_context():

    history = st.session_state.get(
        "conversation_history",
        [],
    )

    if not history:
        return None

    context_parts = []

    recent_history = history[-10:]

    for item in recent_history:

        role = item.get(
            "role",
            "",
        )

        content = item.get(
            "content",
            "",
        )

        if not isinstance(
            content,
            str,
        ):
            content = str(content)

        content = content.strip()

        if not content:
            continue

        if role == "user":

            context_parts.append(
                f"Student: {content}"
            )

        elif role == "assistant":

            context_parts.append(
                f"EduAccess AI: {content}"
            )

    if not context_parts:
        return None

    return "\n\n".join(
        context_parts
    )


# ============================================================
# DISPLAY HISTORY
# ============================================================

def display_chat_history():

    history = st.session_state.get(
        "conversation_history",
        [],
    )

    if not history:

        st.info(
            "💬 No previous conversation yet."
        )

        return

    st.subheader(
        "💬 Conversation History"
    )

    for item in history:

        role = item.get(
            "role",
            "",
        )

        content = item.get(
            "content",
            "",
        )

        if not isinstance(
            content,
            str,
        ):
            content = str(content)

        content = content.strip()

        if not content:
            continue

        if role == "user":

            with st.chat_message("user"):

                st.markdown(
                    content
                )

        elif role == "assistant":

            with st.chat_message("assistant"):

                st.markdown(
                    content
                )


# ============================================================
# CLEAR PERMANENT HISTORY
# ============================================================

def clear_permanent_history(user_id):

    db = SessionLocal()

    try:

        deleted_count = (
            delete_all_tutor_conversations(
                db=db,
                user_id=user_id,
            )
        )

        st.session_state[
            "conversation_history"
        ] = []

        history_key = (
            f"database_history_loaded_{user_id}"
        )

        if history_key in st.session_state:

            del st.session_state[
                history_key
            ]

        st.success(
            f"✅ Deleted {deleted_count} conversation(s)."
        )

    except Exception as e:

        st.error(
            f"❌ Could not delete conversations: {e}"
        )

    finally:

        db.close()


# ============================================================
# SHOW TUTOR
# ============================================================

def show_tutor():

    # --------------------------------------------------------
    # Initialize
    # --------------------------------------------------------

    initialize_chat_history()

    # --------------------------------------------------------
    # Current user
    # --------------------------------------------------------

    user = get_current_user()

    if user is None:

        st.warning(
            "⚠️ User session not found. "
            "Please login again."
        )

        return

    # --------------------------------------------------------
    # User ID
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Load permanent database history
    # --------------------------------------------------------

    initialize_database_history(
        user_id
    )

    # ========================================================
    # HEADER
    # ========================================================

    st.title(
        "🤖 EduAccess AI Tutor"
    )

    st.write(
        "Ask questions using text or voice. "
        "Your AI Tutor conversation history is "
        "saved securely for your account."
    )

    st.divider()

    # ========================================================
    # SIDEBAR
    # ========================================================

    with st.sidebar:

        st.subheader(
            "🤖 AI Tutor"
        )

        student_name = getattr(
            user,
            "full_name",
            "Student",
        )

        if not isinstance(
            student_name,
            str,
        ):
            student_name = "Student"

        st.write(
            f"Student: **{student_name}**"
        )

        st.divider()

        st.subheader(
            "♿ Accessibility"
        )

        preferred_language = getattr(
            user,
            "preferred_language",
            "English",
        )

        st.write(
            f"Language: **{preferred_language}**"
        )

        disability_type = getattr(
            user,
            "disability_type",
            None,
        )

        if disability_type:

            st.write(
                f"Support: **{disability_type}**"
            )

        st.divider()

        # ----------------------------------------------------
        # DELETE HISTORY
        # ----------------------------------------------------

        if st.button(
            "🗑️ Delete Conversation History",
            use_container_width=True,
        ):

            clear_permanent_history(
                user_id
            )

            st.rerun()

    # ========================================================
    # VOICE OUTPUT
    # ========================================================

    st.subheader(
        "🔊 Voice Output"
    )

    automatic_voice = st.checkbox(
        "🔊 Automatically read AI answers aloud",
        value=st.session_state.get(
            "voice_output_enabled",
            False,
        ),
        key="voice_output_enabled",
    )

    if automatic_voice:

        st.info(
            "🔊 Automatic voice output is enabled."
        )

    else:

        st.caption(
            "Automatic voice output is disabled. "
            "You can manually read answers aloud."
        )

    st.divider()

    # ========================================================
    # DISPLAY HISTORY
    # ========================================================

    display_chat_history()

    st.divider()

    # ========================================================
    # QUESTION INPUT
    # ========================================================

    st.subheader(
        "💬 Ask your question"
    )

    question = st.text_area(
        "Enter your question:",
        key="tutor_question",
        height=120,
        placeholder=(
            "Example: Explain machine learning "
            "in simple language."
        ),
    )

    st.caption(
        "🎤 Voice input can place recognized speech "
        "into this question box."
    )

    # ========================================================
    # ASK BUTTON
    # ========================================================

    ask_button = st.button(
        "🤖 Ask Question",
        type="primary",
        use_container_width=True,
    )

    if not ask_button:

        return

    # ========================================================
    # VALIDATE QUESTION
    # ========================================================

    if question is None:

        question = ""

    elif not isinstance(
        question,
        str,
    ):

        question = str(question)

    question = question.strip()

    if not question:

        st.warning(
            "⚠️ Please enter a question first."
        )

        return

    # ========================================================
    # BUILD CONTEXT
    # ========================================================

    context = build_conversation_context()

    # ========================================================
    # ASK GEMINI
    # ========================================================

    with st.spinner(
        "🤖 EduAccess AI is thinking..."
    ):

        try:

            # ------------------------------------------------
            # Try current tutor_engine API
            # ------------------------------------------------

            try:

                answer = ask_tutor(
                    user=user,
                    question=question,
                    context=context,
                )

            except TypeError as e:

                # ------------------------------------------------
                # Compatibility with older ask_tutor()
                # ------------------------------------------------

                if "context" in str(e):

                    answer = ask_tutor(
                        user=user,
                        question=question,
                    )

                else:

                    raise e

        except Exception as e:

            answer = (
                "❌ AI Tutor error:\n\n"
                f"{str(e)}"
            )

    # ========================================================
    # NORMALIZE ANSWER
    # ========================================================

    if answer is None:

        answer = (
            "⚠️ Sorry, I could not generate "
            "an answer."
        )

    if not isinstance(
        answer,
        str,
    ):

        answer = str(answer)

    answer = answer.strip()

    # ========================================================
    # DISPLAY NEW RESPONSE
    # ========================================================

    with st.chat_message("user"):

        st.markdown(
            question
        )

    with st.chat_message("assistant"):

        st.markdown(
            answer
        )

    # ========================================================
    # SAVE TO DATABASE
    # ========================================================

    db = SessionLocal()

    try:

        save_tutor_conversation(
            db=db,
            user_id=user_id,
            question=question,
            answer=answer,
        )

    except Exception as e:

        st.error(
            "⚠️ Answer generated, but conversation "
            f"could not be saved: {e}"
        )

    finally:

        db.close()

    # ========================================================
    # SAVE TO STREAMLIT SESSION
    # ========================================================

    st.session_state[
        "conversation_history"
    ].append(
        {
            "role": "user",
            "content": question,
        }
    )

    st.session_state[
        "conversation_history"
    ].append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    # ========================================================
    # TEXT TO SPEECH
    # ========================================================

    st.divider()

    st.subheader(
        "🔊 Listen to Answer"
    )

    tts_language = get_tts_language(
        user
    )

    # ========================================================
    # AUTOMATIC TTS
    # ========================================================

    if automatic_voice:

        with st.spinner(
            "🔊 Preparing voice output..."
        ):

            audio_data = generate_speech(
                answer,
                language=tts_language,
            )

        if audio_data:

            st.audio(
                audio_data,
                format="audio/mp3",
                autoplay=True,
            )

        else:

            st.warning(
                "⚠️ Voice output could not be generated."
            )

    # ========================================================
    # MANUAL TTS
    # ========================================================

    else:

        speak_button = st.button(
            "🔊 Read Answer Aloud",
            key=(
                "speak_answer_"
                + str(
                    len(
                        st.session_state[
                            "conversation_history"
                        ]
                    )
                )
            ),
            use_container_width=True,
        )

        if speak_button:

            with st.spinner(
                "🔊 Preparing audio..."
            ):

                audio_data = generate_speech(
                    answer,
                    language=tts_language,
                )

            if audio_data:

                st.audio(
                    audio_data,
                    format="audio/mp3",
                )

            else:

                st.warning(
                    "⚠️ Could not generate audio."
                )