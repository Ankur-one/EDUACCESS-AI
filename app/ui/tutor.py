import importlib


# ============================================================
# TTS
# ============================================================

from app.audio.tts import (
    show_text_to_speech
)


# ============================================================
# STT
# ============================================================

from app.audio.stt import (
    show_speech_to_text
)


# ============================================================
# OPTIONAL TUTOR PROMPT BUILDER
# ============================================================

try:

    build_tutor_prompt = getattr(
        importlib.import_module("app.tutor.prompt_builder"),
        "build_tutor_prompt",
        None,
    )

except ImportError:

    build_tutor_prompt = None


# ============================================================
# STREAMLIT
# ============================================================

st = importlib.import_module("streamlit")


# ============================================================
# LANGUAGE MAPPING
# ============================================================

LANGUAGE_MAPPING = {

    "English": "en-IN",

    "English (India)": "en-IN",

    "Hindi": "hi-IN",

    "Punjabi": "pa-IN",

}


# ============================================================
# INITIALIZE TUTOR STATE
# ============================================================

def initialize_tutor_state():

    """
    Initialize all Tutor session-state values.
    """

    # ========================================================
    # QUESTION
    # ========================================================

    if "tutor_question" not in st.session_state:

        st.session_state.tutor_question = ""


    # ========================================================
    # ANSWER
    # ========================================================

    if "tutor_answer" not in st.session_state:

        st.session_state.tutor_answer = ""


    # ========================================================
    # HISTORY
    # ========================================================

    if "tutor_history" not in st.session_state:

        st.session_state.tutor_history = []


    # ========================================================
    # TTS AUTOPLAY
    # ========================================================

    if "tts_autoplay" not in st.session_state:

        st.session_state.tts_autoplay = False


    # ========================================================
    # TTS VOICE
    # ========================================================

    if "tts_voice" not in st.session_state:

        st.session_state.tts_voice = ""


    # ========================================================
    # TTS RATE
    # ========================================================

    if "tts_rate" not in st.session_state:

        st.session_state.tts_rate = 0.9


    # ========================================================
    # TTS VOLUME
    # ========================================================

    if "tts_volume" not in st.session_state:

        st.session_state.tts_volume = 1.0


    # ========================================================
    # TTS PITCH
    # ========================================================

    if "tts_pitch" not in st.session_state:

        st.session_state.tts_pitch = 1.0


# ============================================================
# GET STUDENT LANGUAGE
# ============================================================

def get_student_language():

    """
    Get the student's preferred language.

    Returns:
        Language code such as en-IN, hi-IN, pa-IN.
    """

    language = st.session_state.get(
        "preferred_language",
        "English"
    )


    # ========================================================
    # ALREADY A LANGUAGE CODE
    # ========================================================

    if language in LANGUAGE_MAPPING.values():

        return language


    # ========================================================
    # LANGUAGE NAME -> CODE
    # ========================================================

    return LANGUAGE_MAPPING.get(
        language,
        "en-IN"
    )


# ============================================================
# 80.3.2 — TTS VOICE SELECTOR
# ============================================================

def show_tts_voice_selector():

    """
    Display the Streamlit TTS voice selector.

    The selected voice is stored in:

        st.session_state.tts_voice
    """

    # ========================================================
    # COMMON BROWSER VOICES
    # ========================================================

    common_voices = [

        "Default browser voice",

        "Google US English",

        "Google UK English Female",

        "Google UK English Male",

        "Microsoft David",

        "Microsoft Zira",

        "Microsoft Mark",

        "Microsoft Ravi",

        "Microsoft Heera",

        "Microsoft Kalpana",

        "Microsoft Hemant",

    ]


    # ========================================================
    # CURRENT VOICE
    # ========================================================

    current_voice = (
        st.session_state.get(
            "tts_voice",
            ""
        )
    )


    # ========================================================
    # DEFAULT INDEX
    # ========================================================

    if current_voice in common_voices:

        default_index = (
            common_voices.index(
                current_voice
            )
        )

    else:

        default_index = 0


    # ========================================================
    # SELECT VOICE
    # ========================================================

    selected_voice = st.selectbox(

        "🎙️ TTS Voice",

        options=common_voices,

        index=default_index,

        key="tts_voice_selector",

        help=(
            "Select the voice that the AI Tutor "
            "should use when reading answers."
        ),
    )


    # ========================================================
    # SAVE SELECTED VOICE
    # ========================================================

    if selected_voice == (
        "Default browser voice"
    ):

        st.session_state.tts_voice = ""

    else:

        st.session_state.tts_voice = (
            selected_voice
        )


    # ========================================================
    # SHOW CURRENT VOICE
    # ========================================================

    if st.session_state.tts_voice:

        st.caption(
            "🎙️ Selected voice: "
            f"{st.session_state.tts_voice}"
        )

    else:

        st.caption(
            "🎙️ Selected voice: "
            "Default browser voice"
        )


    return st.session_state.tts_voice


# ============================================================
# 80.3.3 — TTS ACCESSIBILITY SETTINGS
# ============================================================

def show_tts_accessibility_settings():

    """
    Display all TTS accessibility settings.
    """

    with st.expander(

        "🔊 TTS Accessibility Settings",

        expanded=False,

    ):

        st.caption(
            "Customize how the AI Tutor speaks to you."
        )


        # ====================================================
        # TTS VOICE
        # ====================================================

        show_tts_voice_selector()


        # ====================================================
        # AUTOPLAY
        # ====================================================

        autoplay_enabled = st.checkbox(

            "🔊 Automatically read AI answers",

            value=(
                st.session_state.tts_autoplay
            ),

            key="tts_autoplay_control",

            help=(
                "Automatically read the AI Tutor "
                "answer after it is generated."
            ),
        )


        st.session_state.tts_autoplay = (
            autoplay_enabled
        )


        # ====================================================
        # SPEECH SPEED
        # ====================================================

        speech_rate = st.slider(

            "🐢 Speech speed",

            min_value=0.5,

            max_value=1.5,

            value=float(
                st.session_state.tts_rate
            ),

            step=0.1,

            key="tts_rate_control",

            help=(
                "Lower values make speech slower. "
                "Higher values make speech faster."
            ),
        )


        st.session_state.tts_rate = (
            speech_rate
        )


        # ====================================================
        # VOLUME
        # ====================================================

        speech_volume = st.slider(

            "🔊 Speech volume",

            min_value=0.0,

            max_value=1.0,

            value=float(
                st.session_state.tts_volume
            ),

            step=0.1,

            key="tts_volume_control",

            help=(
                "Controls the volume of the AI Tutor voice."
            ),
        )


        st.session_state.tts_volume = (
            speech_volume
        )


        # ====================================================
        # PITCH
        # ====================================================

        speech_pitch = st.slider(

            "🎵 Voice pitch",

            min_value=0.5,

            max_value=1.5,

            value=float(
                st.session_state.tts_pitch
            ),

            step=0.1,

            key="tts_pitch_control",

            help=(
                "Controls the pitch of the AI Tutor voice."
            ),
        )


        st.session_state.tts_pitch = (
            speech_pitch
        )


        # ====================================================
        # CURRENT SETTINGS
        # ====================================================

        st.markdown(
            "### Current TTS Settings"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(

                "Speed",

                f"{st.session_state.tts_rate:.1f}x",

            )


        with col2:

            st.metric(

                "Volume",

                f"{int(st.session_state.tts_volume * 100)}%",

            )


        with col3:

            st.metric(

                "Pitch",

                f"{st.session_state.tts_pitch:.1f}",

            )


        # ====================================================
        # ACCESSIBILITY PRESET
        # ====================================================

        st.markdown(
            "### ♿ Accessibility Preset"
        )


        if st.button(

            "♿ Enable Easy Listening",

            use_container_width=True,

            key="easy_listening_button",

        ):

            st.session_state.tts_rate = 0.7

            st.session_state.tts_volume = 1.0

            st.session_state.tts_pitch = 1.0


            # ------------------------------------------------
            # CLEAR SLIDER WIDGET STATE
            # ------------------------------------------------

            st.session_state.pop(
                "tts_rate_control",
                None,
            )

            st.session_state.pop(
                "tts_volume_control",
                None,
            )

            st.session_state.pop(
                "tts_pitch_control",
                None,
            )


            st.success(
                "♿ Easy Listening enabled."
            )


            st.rerun()


        # ====================================================
        # RESET
        # ====================================================

        if st.button(

            "🔄 Reset TTS Settings",

            use_container_width=True,

            key="reset_tts_button",

        ):

            # ------------------------------------------------
            # RESET VALUES
            # ------------------------------------------------

            st.session_state.tts_voice = ""

            st.session_state.tts_rate = 0.9

            st.session_state.tts_volume = 1.0

            st.session_state.tts_pitch = 1.0

            st.session_state.tts_autoplay = False


            # ------------------------------------------------
            # CLEAR WIDGET STATE
            # ------------------------------------------------

            st.session_state.pop(
                "tts_voice_selector",
                None,
            )

            st.session_state.pop(
                "tts_autoplay_control",
                None,
            )

            st.session_state.pop(
                "tts_rate_control",
                None,
            )

            st.session_state.pop(
                "tts_volume_control",
                None,
            )

            st.session_state.pop(
                "tts_pitch_control",
                None,
            )


            st.success(
                "🔄 TTS settings have been reset."
            )


            st.rerun()


# ============================================================
# TUTOR PAGE
# ============================================================

def show_tutor():

    """
    Display the AI Tutor.
    """

    # ========================================================
    # INITIALIZE
    # ========================================================

    initialize_tutor_state()


    # ========================================================
    # TITLE
    # ========================================================

    st.title(
        "🤖 AI Tutor"
    )


    st.caption(
        "Ask questions using text or your voice."
    )


    # ========================================================
    # LANGUAGE
    # ========================================================

    preferred_language = (
        get_student_language()
    )


    # ========================================================
    # ACTIVE LANGUAGE
    # ========================================================

    st.info(

        f"🌐 Active language: "
        f"**{preferred_language}**"

    )


    # ========================================================
    # TTS SETTINGS
    # ========================================================

    show_tts_accessibility_settings()


    # ========================================================
    # VOICE QUESTION
    # ========================================================

    st.subheader(
        "🎤 Ask by Voice"
    )


    voice_question = (
        show_speech_to_text(
            language=preferred_language
        )
    )


    # ========================================================
    # TEXT QUESTION
    # ========================================================

    st.subheader(
        "⌨️ Ask by Text"
    )


    text_question = st.text_area(

        "Enter your question:",

        value=(
            st.session_state.tutor_question
        ),

        height=120,

        placeholder=(
            "Example: Explain photosynthesis "
            "in simple words."
        ),

    )


    # ========================================================
    # SELECT QUESTION
    # ========================================================

    question = ""


    # ========================================================
    # VOICE QUESTION
    # ========================================================

    if voice_question:

        question = voice_question

        st.success(

            f"🎤 Voice question detected: "
            f"{voice_question}"

        )


    # ========================================================
    # TEXT QUESTION
    # ========================================================

    elif text_question.strip():

        question = (
            text_question.strip()
        )


    # ========================================================
    # ASK BUTTON
    # ========================================================

    ask_button = st.button(

        "🤖 Ask AI Tutor",

        type="primary",

        use_container_width=True,

    )


    # ========================================================
    # PROCESS QUESTION
    # ========================================================

    if ask_button:

        # ----------------------------------------------------
        # EMPTY QUESTION
        # ----------------------------------------------------

        if not question:

            st.warning(

                "Please enter a question "
                "or ask using the microphone."

            )

            return


        # ----------------------------------------------------
        # SAVE QUESTION
        # ----------------------------------------------------

        st.session_state.tutor_question = (
            question
        )


        # ----------------------------------------------------
        # BUILD PROMPT
        # ----------------------------------------------------

        if build_tutor_prompt:

            try:

                prompt = build_tutor_prompt(

                    question=question,

                    language=preferred_language,

                )

            except TypeError:

                prompt = build_tutor_prompt(
                    question
                )

        else:

            prompt = f"""
You are an inclusive AI Tutor.

Answer the student's question clearly.

Student language:
{preferred_language}

Student question:
{question}

Requirements:

- Explain concepts simply.
- Use step-by-step explanations when useful.
- Repeat important concepts when useful.
- Use examples.
- Avoid unnecessary complexity.
- Be supportive and accessible.
"""


        # ----------------------------------------------------
        # GENERATE ANSWER
        # ----------------------------------------------------

        with st.spinner(
            "🤖 AI Tutor is thinking..."
        ):

            try:

                answer = generate_tutor_response(
                    prompt
                )

            except Exception as error:

                st.error(
                    "Unable to generate the Tutor answer."
                )

                st.exception(
                    error
                )

                return


        # ----------------------------------------------------
        # SAVE ANSWER
        # ----------------------------------------------------

        st.session_state.tutor_answer = (
            answer
        )


        # ----------------------------------------------------
        # SAVE HISTORY
        # ----------------------------------------------------

        st.session_state.tutor_history.append(

            {
                "question": question,

                "answer": answer,
            }

        )


    # ========================================================
    # DISPLAY ANSWER
    # ========================================================

    if st.session_state.tutor_answer:

        st.divider()


        st.subheader(
            "📚 AI Tutor Answer"
        )


        st.markdown(
            st.session_state.tutor_answer
        )


        # ====================================================
        # TTS
        # ====================================================

        show_text_to_speech(

            text=(
                st.session_state.tutor_answer
            ),

            language=(
                preferred_language
            ),

            autoplay=(
                st.session_state.tts_autoplay
            ),

            selected_voice=(
                st.session_state.tts_voice
            ),

            speech_rate=(
                st.session_state.tts_rate
            ),

            volume=(
                st.session_state.tts_volume
            ),

            pitch=(
                st.session_state.tts_pitch
            ),

        )


# ============================================================
# AI RESPONSE
# ============================================================

def generate_tutor_response(
    prompt: str
) -> str:

    """
    Generate the AI Tutor response.
    """

    # ========================================================
    # EXISTING AI MODULE
    # ========================================================

    try:

        ai_module = importlib.import_module(
            "app.ai.gemini"
        )


        # ----------------------------------------------------
        # generate_response
        # ----------------------------------------------------

        if hasattr(
            ai_module,
            "generate_response"
        ):

            response = (
                ai_module.generate_response(
                    prompt
                )
            )

            return str(
                response
            )


        # ----------------------------------------------------
        # generate_content
        # ----------------------------------------------------

        if hasattr(
            ai_module,
            "generate_content"
        ):

            response = (
                ai_module.generate_content(
                    prompt
                )
            )

            return str(
                response
            )


        # ----------------------------------------------------
        # ask_gemini
        # ----------------------------------------------------

        if hasattr(
            ai_module,
            "ask_gemini"
        ):

            response = (
                ai_module.ask_gemini(
                    prompt
                )
            )

            return str(
                response
            )


    except ImportError:

        pass


    # ========================================================
    # GOOGLE GENAI FALLBACK
    # ========================================================

    try:

        genai = importlib.import_module(
            "google.genai"
        )


        # ----------------------------------------------------
        # API KEY
        # ----------------------------------------------------

        api_key = ""


        try:

            api_key = st.secrets.get(
                "GEMINI_API_KEY",
                ""
            )

        except Exception:

            api_key = ""


        if not api_key:

            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )


        # ----------------------------------------------------
        # CLIENT
        # ----------------------------------------------------

        client = genai.Client(
            api_key=api_key
        )


        # ----------------------------------------------------
        # GENERATE RESPONSE
        # ----------------------------------------------------

        response = (
            client.models.generate_content(

                model="gemini-3.6-flash",

                contents=prompt,

            )
        )


        # ----------------------------------------------------
        # RETURN TEXT
        # ----------------------------------------------------

        if hasattr(
            response,
            "text"
        ):

            return response.text


        return str(
            response
        )


    except Exception as error:

        raise RuntimeError(
            "Unable to generate AI Tutor response."
        ) from error


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    show_tutor()