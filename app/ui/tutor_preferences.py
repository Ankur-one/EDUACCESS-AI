from app.auth.session import (
    get_accessibility_preferences,
    get_learning_preferences,
    get_preferred_language,
)


# ============================================================
# GET ALL TUTOR PREFERENCES
# ============================================================

def get_tutor_preferences():
    """
    Get all preferences currently loaded for the
    logged-in student.
    """

    accessibility = (
        get_accessibility_preferences()
    )

    learning = (
        get_learning_preferences()
    )

    return {
        # ----------------------------------------------------
        # LANGUAGE
        # ----------------------------------------------------

        "preferred_language": (
            get_preferred_language()
        ),

        # ----------------------------------------------------
        # LEARNING
        # ----------------------------------------------------

        "simple_explanation": (
            learning["simple_explanation"]
        ),

        "step_by_step": (
            learning["step_by_step"]
        ),

        "repetition_support": (
            learning["repetition_support"]
        ),

        "visual_explanation": (
            learning["visual_explanation"]
        ),

        # ----------------------------------------------------
        # COMMUNICATION
        # ----------------------------------------------------

        "text_to_speech": (
            accessibility["text_to_speech"]
        ),

        "speech_to_text": (
            accessibility["speech_to_text"]
        ),

        # ----------------------------------------------------
        # VISUAL ACCESSIBILITY
        # ----------------------------------------------------

        "large_text": (
            accessibility["large_text"]
        ),

        "high_contrast": (
            accessibility["high_contrast"]
        ),

        "dyslexia_friendly": (
            accessibility["dyslexia_friendly"]
        ),
    }


# ============================================================
# BUILD AI TUTOR INSTRUCTIONS
# ============================================================

def build_tutor_instructions():
    """
    Convert the student's preferences into instructions
    that can be passed to the AI Tutor engine.
    """

    preferences = get_tutor_preferences()

    instructions = []

    # ========================================================
    # LANGUAGE
    # ========================================================

    language = preferences[
        "preferred_language"
    ]

    if language == "Hindi":

        instructions.append(
            "Answer primarily in Hindi."
        )

    elif language == "Hinglish":

        instructions.append(
            "Answer in simple Hinglish using "
            "Hindi and English naturally."
        )

    else:

        instructions.append(
            "Answer in clear English."
        )

    # ========================================================
    # SIMPLE EXPLANATION
    # ========================================================

    if preferences[
        "simple_explanation"
    ]:

        instructions.append(
            "Use simple and easy-to-understand "
            "language. Avoid unnecessary jargon."
        )

    # ========================================================
    # STEP BY STEP
    # ========================================================

    if preferences[
        "step_by_step"
    ]:

        instructions.append(
            "Explain difficult concepts "
            "step by step."
        )

    # ========================================================
    # REPETITION
    # ========================================================

    if preferences[
        "repetition_support"
    ]:

        instructions.append(
            "At the end, briefly repeat the "
            "most important points."
        )

    # ========================================================
    # VISUAL EXPLANATION
    # ========================================================

    if preferences[
        "visual_explanation"
    ]:

        instructions.append(
            "When useful, use simple examples, "
            "structured lists, tables, or text-based "
            "visual explanations."
        )

    # ========================================================
    # ACCESSIBILITY
    # ========================================================

    if preferences[
        "large_text"
    ]:

        instructions.append(
            "Keep responses clearly structured "
            "with short sections and readable spacing."
        )

    if preferences[
        "dyslexia_friendly"
    ]:

        instructions.append(
            "Use short paragraphs, clear headings, "
            "simple sentences, and generous spacing."
        )

    # ========================================================
    # RETURN FINAL INSTRUCTIONS
    # ========================================================

    return "\n".join(
        f"- {instruction}"
        for instruction in instructions
    )


# ============================================================
# SHOW CURRENT TUTOR PREFERENCES
# ============================================================

def show_tutor_preference_status():
    """
    Display the student's currently active Tutor
    accessibility settings.
    """

    # Import lazily so this preferences module can also be used in
    # environments where the optional Streamlit UI dependency is absent.
    from importlib import import_module

    st = import_module("streamlit")

    preferences = get_tutor_preferences()

    with st.expander(
        "♿ Active Learning & Accessibility Settings"
    ):

        # ----------------------------------------------------
        # LANGUAGE
        # ----------------------------------------------------

        st.write(
            f"🌐 **Language:** "
            f"{preferences['preferred_language']}"
        )

        # ----------------------------------------------------
        # LEARNING
        # ----------------------------------------------------

        learning_items = []

        if preferences["simple_explanation"]:

            learning_items.append(
                "👨‍🏫 Simple explanations"
            )

        if preferences["step_by_step"]:

            learning_items.append(
                "📚 Step-by-step explanations"
            )

        if preferences["repetition_support"]:

            learning_items.append(
                "🔁 Repetition support"
            )

        if preferences["visual_explanation"]:

            learning_items.append(
                "📊 Examples / visual explanations"
            )

        if learning_items:

            st.write(
                "**Learning:** "
                + ", ".join(learning_items)
            )

        # ----------------------------------------------------
        # VOICE
        # ----------------------------------------------------

        voice_items = []

        if preferences["speech_to_text"]:

            voice_items.append(
                "🎤 Speech-to-text"
            )

        if preferences["text_to_speech"]:

            voice_items.append(
                "🔊 Text-to-speech"
            )

        if voice_items:

            st.write(
                "**Voice:** "
                + ", ".join(voice_items)
            )

        else:

            st.write(
                "**Voice:** Text mode"
            )

        # ----------------------------------------------------
        # VISUAL
        # ----------------------------------------------------

        visual_items = []

        if preferences["large_text"]:

            visual_items.append(
                "🔎 Large text"
            )

        if preferences["high_contrast"]:

            visual_items.append(
                "⚫ High contrast"
            )

        if preferences["dyslexia_friendly"]:

            visual_items.append(
                "📖 Dyslexia-friendly"
            )

        if visual_items:

            st.write(
                "**Visual:** "
                + ", ".join(visual_items)
            )
