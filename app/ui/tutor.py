import streamlit as st  # type: ignore[import-not-found]

from app.database.database import SessionLocal
from app.database.models import User
from app.auth.session import get_current_user_id

from app.ai.tutor_engine import ask_tutor

from app.audio.speech import (
    speech_to_text,
    text_to_speech,
)


# ============================================================
# AI TUTOR PAGE
# ============================================================

def show_tutor():

    st.title("🤖 EduAccess AI Tutor")

    st.markdown(
        """
        ### 📚 Your Personal AI Study Assistant

        Ask any educational question using **text or voice**.

        EduAccess AI can provide:
        - Simple explanations
        - Step-by-step explanations
        - Repeated explanations
        - Accessibility-friendly learning
        - Voice input
        - Voice output
        """
    )

    st.divider()

    # ========================================================
    # GET CURRENT USER
    # ========================================================

    user_id = get_current_user_id()

    if not user_id:

        st.warning(
            "⚠️ Please login first."
        )

        return

    # ========================================================
    # DATABASE SESSION
    # ========================================================

    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(
                User.id == user_id
            )
            .first()
        )

        if not user:

            st.error(
                "❌ User profile not found."
            )

            return

        # ====================================================
        # STUDENT INFORMATION
        # ====================================================

        st.info(
            f"""
👤 **Student:** {user.full_name}

♿ **Accessibility Need:** {user.disability_type}

🌐 **Language:** {user.preferred_language}
"""
        )

        st.divider()

        # ====================================================
        # VOICE INPUT
        # ====================================================

        st.subheader(
            "🎤 Ask Using Your Voice"
        )

        voice_question = ""

        if getattr(
            user,
            "speech_to_text",
            False,
        ):

            if st.button(
                "🎤 Speak Your Question",
                use_container_width=True,
            ):

                with st.spinner(
                    "🎤 Listening... Please speak."
                ):

                    voice_question = speech_to_text()

                if voice_question:

                    st.session_state[
                        "voice_question"
                    ] = voice_question

                    st.success(
                        f"🎤 You said: {voice_question}"
                    )

                    st.rerun()

                else:

                    st.warning(
                        "⚠️ I couldn't understand your voice. "
                        "Please try again."
                    )

        else:

            st.info(
                "🎤 Voice input is disabled in your "
                "Accessibility Settings."
            )

        # ====================================================
        # TEXT QUESTION
        # ====================================================

        st.subheader(
            "📝 Ask Your Question"
        )

        question = st.text_area(
            "What would you like to learn?",
            value=st.session_state.get(
                "voice_question",
                "",
            ),
            placeholder=(
                "Example: Explain Machine Learning "
                "in simple words."
            ),
            height=150,
        )

        # ====================================================
        # CLEAR VOICE QUESTION
        # ====================================================

        if st.session_state.get(
            "voice_question"
        ):

            if st.button(
                "🗑️ Clear Question"
            ):

                st.session_state[
                    "voice_question"
                ] = ""

                st.rerun()

        # ====================================================
        # LEARNING OPTIONS
        # ====================================================

        st.subheader(
            "🎯 Learning Preferences"
        )

        col1, col2 = st.columns(2)

        with col1:

            simple_mode = st.checkbox(
                "🧒 Simple Explanation",
                value=getattr(
                    user,
                    "simple_explanation",
                    True,
                ),
            )

            step_mode = st.checkbox(
                "🪜 Step-by-Step",
                value=getattr(
                    user,
                    "step_by_step",
                    True,
                ),
            )

        with col2:

            repetition_mode = st.checkbox(
                "🔁 Repeat Important Points",
                value=getattr(
                    user,
                    "repetition_support",
                    False,
                ),
            )

            visual_mode = st.checkbox(
                "📊 Use Examples",
                value=getattr(
                    user,
                    "visual_explanation",
                    True,
                ),
            )

        st.divider()

        # ====================================================
        # ASK GEMINI
        # ====================================================

        if st.button(
            "✨ Ask EduAccess AI",
            type="primary",
            use_container_width=True,
        ):

            if not question.strip():

                st.warning(
                    "⚠️ Please enter or speak a question."
                )

                return

            # -----------------------------------------------
            # BUILD ACCESSIBILITY INSTRUCTIONS
            # -----------------------------------------------

            accessibility_preferences = []

            if simple_mode:

                accessibility_preferences.append(
                    "Use very simple language."
                )

            if step_mode:

                accessibility_preferences.append(
                    "Explain the answer step by step."
                )

            if repetition_mode:

                accessibility_preferences.append(
                    "Repeat the most important points."
                )

            if visual_mode:

                accessibility_preferences.append(
                    "Use examples, bullet points, "
                    "and simple comparisons."
                )

            accessibility_text = "\n".join(
                accessibility_preferences
            )

            # -----------------------------------------------
            # GENERATE AI ANSWER
            # -----------------------------------------------

            with st.spinner(
                "🤖 EduAccess AI is thinking..."
            ):

                try:

                    answer = ask_tutor(
                        question=question,
                        user=user,
                        accessibility_preferences=(
                            accessibility_text
                        ),
                    )

                except TypeError:

                    # Compatibility fallback if your
                    # ask_tutor() currently accepts
                    # only question and user.

                    answer = ask_tutor(
                        question,
                        user,
                    )

                except Exception as e:

                    st.error(
                        f"❌ AI Tutor Error: {e}"
                    )

                    return

            # -----------------------------------------------
            # SAVE ANSWER IN SESSION
            # -----------------------------------------------

            st.session_state[
                "last_tutor_answer"
            ] = answer

            # Clear voice question after asking

            st.session_state[
                "voice_question"
            ] = ""

        # ====================================================
        # DISPLAY ANSWER
        # ====================================================

        answer = st.session_state.get(
            "last_tutor_answer",
            "",
        )

        if answer:

            st.divider()

            st.subheader(
                "🤖 EduAccess AI Answer"
            )

            st.markdown(
                answer
            )

            # =================================================
            # TEXT TO SPEECH
            # =================================================

            if getattr(
                user,
                "text_to_speech",
                False,
            ):

                st.divider()

                st.subheader(
                    "🔊 Listen to the Answer"
                )

                if st.button(
                    "🔊 Read Answer Aloud",
                    use_container_width=True,
                ):

                    with st.spinner(
                        "🔊 Preparing audio..."
                    ):

                        success = text_to_speech(
                            answer
                        )

                    if success:

                        st.success(
                            "🔊 Answer played successfully."
                        )

                    else:

                        st.error(
                            "❌ Unable to play the answer."
                        )

            else:

                st.info(
                    "🔊 Text-to-Speech is disabled "
                    "in your Accessibility Settings."
                )

    finally:

        db.close()