import importlib
from io import BytesIO

from app.auth.session import get_current_user
from app.ai.tutor_engine import ask_tutor

# Load Streamlit dynamically so static analyzers do not require the optional
# dependency to be installed in the editor's selected Python environment.
st = importlib.import_module("streamlit")

# Load gTTS dynamically because it is an optional runtime dependency.
gTTS = importlib.import_module("gtts").gTTS


# ============================================================
# TEXT TO SPEECH
# ============================================================

def generate_speech(text, language="en"):
    """
    Convert text into MP3 speech.

    Returns:
        bytes | None
    """

    if text is None:
        return None

    # IMPORTANT:
    # Always convert the answer to string.
    # This prevents .strip() errors.
    if not isinstance(text, str):
        text = str(text)

    text = text.strip()

    if not text:
        return None

    try:

        audio_buffer = BytesIO()

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
# GET TTS LANGUAGE
# ============================================================

def get_tts_language(user):
    """
    Convert user's preferred language
    into a gTTS language code.
    """

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
# INITIALIZE CONVERSATION
# ============================================================

def initialize_chat_history():

    if "conversation_history" not in st.session_state:

        st.session_state[
            "conversation_history"
        ] = []


# ============================================================
# BUILD CONVERSATION CONTEXT
# ============================================================

def build_conversation_context():

    history = st.session_state.get(
        "conversation_history",
        [],
    )

    if not history:
        return None

    context_parts = []

    # Keep latest 10 messages
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
# CLEAR CHAT
# ============================================================

def clear_chat():

    st.session_state[
        "conversation_history"
    ] = []

    if "chat_history" in st.session_state:

        st.session_state[
            "chat_history"
        ] = []

    # Clear current question
    st.session_state[
        "tutor_question"
    ] = ""

    st.rerun()


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

def display_chat_history():

    history = st.session_state.get(
        "conversation_history",
        [],
    )

    for index, item in enumerate(history):

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
# AI TUTOR
# ============================================================

def show_tutor():

    # --------------------------------------------------------
    # Initialize
    # --------------------------------------------------------

    initialize_chat_history()

    # --------------------------------------------------------
    # Get current user
    # --------------------------------------------------------

    user = get_current_user()

    if user is None:

        st.warning(
            "⚠️ User session not found. "
            "Please login again."
        )

        return

    # ========================================================
    # HEADER
    # ========================================================

    st.title(
        "🤖 EduAccess AI Tutor"
    )

    st.write(
        "Ask educational questions using text or voice. "
        "EduAccess AI provides personalized and accessible "
        "explanations."
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
        # CLEAR CHAT
        # ----------------------------------------------------

        if st.button(
            "🗑️ Clear Conversation",
            use_container_width=True,
        ):

            clear_chat()

    # ========================================================
    # VOICE OUTPUT SETTING
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
            "🔊 Automatic voice output is enabled. "
            "AI answers will be converted to speech."
        )

    else:

        st.caption(
            "Automatic voice output is disabled. "
            "You can manually click "
            "'Read Answer Aloud'."
        )

    st.divider()

    # ========================================================
    # PREVIOUS CONVERSATION
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
    # PERMANENT QUESTION VALIDATION
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
    # BUILD CONTEXT BEFORE ADDING NEW MESSAGE
    # ========================================================

    context = build_conversation_context()

    # ========================================================
    # SHOW USER QUESTION
    # ========================================================

    with st.chat_message("user"):

        st.markdown(
            question
        )

    # ========================================================
    # ASK GEMINI
    # ========================================================

    with st.chat_message("assistant"):

        with st.spinner(
            "🤖 EduAccess AI is thinking..."
        ):

            try:

                # Preferred version
                answer = ask_tutor(
                    user=user,
                    question=question,
                    context=context,
                )

            except TypeError as e:

                # Compatibility with older ask_tutor()
                # that does not accept context.
                if "context" in str(e):

                    answer = ask_tutor(
                        user=user,
                        question=question,
                    )

                else:

                    answer = (
                        "❌ AI Tutor error:\n\n"
                        f"{str(e)}"
                    )

            except Exception as e:

                answer = (
                    "❌ AI Tutor error:\n\n"
                    f"{str(e)}"
                )

        # ----------------------------------------------------
        # Guarantee answer is text
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # Display answer
        # ----------------------------------------------------

        st.markdown(
            answer
        )

    # ========================================================
    # SAVE USER MESSAGE
    # ========================================================

    st.session_state[
        "conversation_history"
    ].append(
        {
            "role": "user",
            "content": question,
        }
    )

    # ========================================================
    # SAVE AI ANSWER
    # ========================================================

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

    # --------------------------------------------------------
    # Get language
    # --------------------------------------------------------

    tts_language = get_tts_language(
        user
    )

    # ========================================================
    # AUTOMATIC VOICE OUTPUT
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

            st.success(
                "🔊 AI answer is ready to play."
            )

        else:

            st.warning(
                "⚠️ Voice output could not be generated."
            )

    # ========================================================
    # MANUAL VOICE OUTPUT
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

                st.success(
                    "🔊 Audio is ready."
                )

            else:

                st.warning(
                    "⚠️ Could not generate audio. "
                    "Please try again."
                )

    # ========================================================
    # CLEAR INPUT
    # ========================================================

    st.session_state[
        "tutor_question"
    ] = ""