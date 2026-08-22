from typing import Optional, Any

from google import genai

from app.config.settings import settings


# ============================================================
# EDUACCESS AI TUTOR ENGINE
# Stable version
# ============================================================


# ============================================================
# GEMINI MODEL
# ============================================================

GEMINI_MODEL = "gemini-3.6-flash"


# ============================================================
# GEMINI CLIENT
# ============================================================

def get_gemini_client():
    """
    Create Gemini client safely.
    """

    api_key = getattr(
        settings,
        "GEMINI_API_KEY",
        None,
    )

    if not api_key:

        raise ValueError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=api_key
    )


# ============================================================
# SAFE TEXT CONVERSION
# ============================================================

def safe_text(value: Any) -> str:
    """
    Convert input safely to text.

    IMPORTANT:
    Never call .strip() directly on unknown objects.
    """

    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    # Do NOT convert SQLAlchemy User objects into question text.
    if hasattr(value, "__table__"):

        return ""

    try:
        return str(value).strip()

    except Exception:
        return ""


# ============================================================
# DETECT USER OBJECT
# ============================================================

def looks_like_user(value: Any) -> bool:
    """
    Detect the logged-in SQLAlchemy User object.
    """

    if value is None:
        return False

    # SQLAlchemy model objects generally have these fields.
    user_fields = (
        "full_name",
        "email",
        "preferred_language",
        "disability_type",
    )

    matches = 0

    for field in user_fields:

        if hasattr(value, field):
            matches += 1

    return matches >= 2


# ============================================================
# PERSONALIZED LEARNING INSTRUCTIONS
# ============================================================

def build_learning_instruction(
    preferred_language: str = "English",
    simplified_language: bool = False,
    step_by_step_learning: bool = False,
    repetition_support: bool = False,
    visual_explanations: bool = False,
    large_text: bool = False,
    high_contrast: bool = False,
    dyslexia_friendly: bool = False,
) -> str:

    instructions = []

    instructions.append(
        f"Respond in {preferred_language}."
    )

    if simplified_language:

        instructions.append(
            "Use very simple and easy-to-understand language."
        )

    if step_by_step_learning:

        instructions.append(
            "Explain the topic step by step."
        )

    if repetition_support:

        instructions.append(
            "Repeat important concepts clearly when useful."
        )

    if visual_explanations:

        instructions.append(
            "Use tables, bullet points, ASCII diagrams, "
            "examples, and structured text when useful."
        )

    if large_text:

        instructions.append(
            "Use clear headings, short paragraphs, "
            "and generous spacing."
        )

    if high_contrast:

        instructions.append(
            "Keep the answer clean, structured, "
            "and free from unnecessary visual clutter."
        )

    if dyslexia_friendly:

        instructions.append(
            "Use short sentences, simple words, "
            "clear headings, bullet points, "
            "and generous spacing."
        )

    instructions.append(
        "Be patient, supportive, respectful, "
        "and encouraging."
    )

    return "\n".join(
        f"- {item}"
        for item in instructions
    )


# ============================================================
# CREATE TUTOR PROMPT
# ============================================================

def create_tutor_prompt(
    question: str,
    context: Optional[str] = None,
    preferred_language: str = "English",
    simplified_language: bool = False,
    step_by_step_learning: bool = False,
    repetition_support: bool = False,
    visual_explanations: bool = False,
    large_text: bool = False,
    high_contrast: bool = False,
    dyslexia_friendly: bool = False,
    disability_type: Optional[str] = None,
    disability_details: Optional[str] = None,
) -> str:

    instructions = build_learning_instruction(
        preferred_language=preferred_language,
        simplified_language=simplified_language,
        step_by_step_learning=step_by_step_learning,
        repetition_support=repetition_support,
        visual_explanations=visual_explanations,
        large_text=large_text,
        high_contrast=high_contrast,
        dyslexia_friendly=dyslexia_friendly,
    )

    accessibility_info = []

    if disability_type:

        accessibility_info.append(
            f"Student accessibility need: {disability_type}."
        )

    if disability_details:

        accessibility_info.append(
            f"Additional accessibility information: "
            f"{disability_details}."
        )

    accessibility_text = "\n".join(
        accessibility_info
    )

    if not accessibility_text:

        accessibility_text = (
            "No additional disability information provided."
        )

    prompt = f"""
You are EduAccess AI, an inclusive educational AI tutor.

Your purpose is to help students understand educational
topics clearly, patiently, and accessibly.

ACCESSIBILITY INFORMATION:

{accessibility_text}

LEARNING INSTRUCTIONS:

{instructions}

STUDENT QUESTION:

{question}

GENERAL TEACHING RULES:

1. Give accurate educational information.

2. Use simple language whenever possible.

3. Explain difficult concepts step by step.

4. Give examples when useful.

5. Do not assume advanced prior knowledge.

6. Use headings and bullet points.

7. Be patient and supportive.

8. For technical questions, explain the concept first.

9. For programming questions, explain the code clearly.

10. For mathematics, show calculation steps.

11. If the student makes a mistake, correct it politely.

12. Focus on understanding, not only the final answer.

13. Adapt the response to accessibility preferences.

14. Never make assumptions about a disability.

15. Keep the answer educational and student-friendly.

16. If conversation context is provided, use it to
    understand follow-up questions.

"""

    if context:

        prompt += f"""
CONVERSATION HISTORY:

{context}

"""

    prompt += """
Now answer the student's question.
"""

    return prompt.strip()


# ============================================================
# ASK GEMINI
# ============================================================

def ask_ai(
    question: str,
    context: Optional[str] = None,
    preferred_language: str = "English",
    simplified_language: bool = False,
    step_by_step_learning: bool = False,
    repetition_support: bool = False,
    visual_explanations: bool = False,
    large_text: bool = False,
    high_contrast: bool = False,
    dyslexia_friendly: bool = False,
    disability_type: Optional[str] = None,
    disability_details: Optional[str] = None,
) -> str:

    # --------------------------------------------------------
    # SAFE QUESTION VALIDATION
    # --------------------------------------------------------

    question = safe_text(question)

    if not question:

        return (
            "❌ Please enter a text question."
        )

    # --------------------------------------------------------
    # CREATE CLIENT
    # --------------------------------------------------------

    try:

        client = get_gemini_client()

    except Exception as e:

        return (
            "❌ Gemini configuration error:\n\n"
            f"{str(e)}"
        )

    # --------------------------------------------------------
    # CREATE PROMPT
    # --------------------------------------------------------

    prompt = create_tutor_prompt(
        question=question,
        context=context,
        preferred_language=preferred_language,
        simplified_language=simplified_language,
        step_by_step_learning=step_by_step_learning,
        repetition_support=repetition_support,
        visual_explanations=visual_explanations,
        large_text=large_text,
        high_contrast=high_contrast,
        dyslexia_friendly=dyslexia_friendly,
        disability_type=disability_type,
        disability_details=disability_details,
    )

    # --------------------------------------------------------
    # CALL GEMINI
    # --------------------------------------------------------

    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        if response is None:

            return (
                "⚠️ Gemini returned no response."
            )

        answer = getattr(
            response,
            "text",
            None,
        )

        answer = safe_text(answer)

        if answer:

            return answer

        return (
            "⚠️ Sorry, I could not generate an answer. "
            "Please try again."
        )

    except Exception as e:

        return (
            "❌ AI Tutor error:\n\n"
            f"{str(e)}"
        )


# ============================================================
# ASK TUTOR
# ============================================================

def ask_tutor(
    user=None,
    question=None,
    context=None,
) -> str:
    """
    MAIN PUBLIC FUNCTION USED BY tutor.py.

    Correct usage:

        ask_tutor(
            user=user,
            question=question
        )

    This function also protects against accidentally reversed
    arguments:

        ask_tutor(question, user)

    """

    # ========================================================
    # FIX REVERSED ARGUMENTS
    # ========================================================

    if (
        isinstance(user, str)
        and looks_like_user(question)
    ):

        real_question = user
        real_user = question

        user = real_user
        question = real_question

    # ========================================================
    # QUESTION VALIDATION
    # ========================================================

    question = safe_text(question)

    if not question:

        return (
            "❌ Please enter a text question."
        )

    # ========================================================
    # USER VALIDATION
    # ========================================================

    if user is None:

        return (
            "❌ User session not found. "
            "Please login again."
        )

    # ========================================================
    # GET USER SETTINGS
    # ========================================================

    preferred_language = (
        getattr(
            user,
            "preferred_language",
            None,
        )
        or "English"
    )

    simplified_language = bool(
        getattr(
            user,
            "simple_explanation",
            False,
        )
    )

    step_by_step_learning = bool(
        getattr(
            user,
            "step_by_step",
            False,
        )
    )

    repetition_support = bool(
        getattr(
            user,
            "repetition_support",
            False,
        )
    )

    visual_explanations = bool(
        getattr(
            user,
            "visual_explanation",
            False,
        )
    )

    large_text = bool(
        getattr(
            user,
            "large_text",
            False,
        )
    )

    high_contrast = bool(
        getattr(
            user,
            "high_contrast",
            False,
        )
    )

    dyslexia_friendly = bool(
        getattr(
            user,
            "dyslexia_friendly",
            False,
        )
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

    # ========================================================
    # SEND TO AI
    # ========================================================

    return ask_ai(
        question=question,
        context=context,
        preferred_language=preferred_language,
        simplified_language=simplified_language,
        step_by_step_learning=step_by_step_learning,
        repetition_support=repetition_support,
        visual_explanations=visual_explanations,
        large_text=large_text,
        high_contrast=high_contrast,
        dyslexia_friendly=dyslexia_friendly,
        disability_type=disability_type,
        disability_details=disability_details,
    )


# ============================================================
# TEST FUNCTION
# ============================================================

def test_tutor_engine():

    print("==========================================")
    print("EduAccess AI Tutor Engine")
    print("==========================================")

    print(f"Model: {GEMINI_MODEL}")

    api_key = getattr(
        settings,
        "GEMINI_API_KEY",
        None,
    )

    if api_key:

        print("Gemini API Key: CONFIGURED")

    else:

        print("Gemini API Key: NOT CONFIGURED")

    print("Tutor Engine: READY")


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":

    test_tutor_engine()