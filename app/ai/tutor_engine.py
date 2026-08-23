from typing import Optional

from google import genai

from app.config.settings import settings


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

GEMINI_MODEL = "gemini-3.6-flash"


# ============================================================
# GEMINI CLIENT
# ============================================================

def get_gemini_client():
    if not settings.GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=settings.GEMINI_API_KEY
    )


# ============================================================
# LEARNING INSTRUCTIONS
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

    instructions = [
        f"Respond in {preferred_language}."
    ]

    if simplified_language:
        instructions.append(
            "Use very simple and easy-to-understand language."
        )

    if step_by_step_learning:
        instructions.append(
            "Explain difficult concepts step by step."
        )

    if repetition_support:
        instructions.append(
            "Repeat important concepts and provide a short summary."
        )

    if visual_explanations:
        instructions.append(
            "Use bullet points, tables, examples, "
            "ASCII diagrams, or structured text when useful."
        )

    if large_text:
        instructions.append(
            "Use clear headings, short paragraphs, "
            "and generous spacing."
        )

    if high_contrast:
        instructions.append(
            "Keep the response clean and highly structured."
        )

    if dyslexia_friendly:
        instructions.append(
            "Use short sentences, simple words, "
            "clear headings, bullet points, and spacing."
        )

    instructions.append(
        "Be patient, supportive, respectful, and encouraging."
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
            f"Accessibility need: {disability_type}"
        )

    if disability_details:
        accessibility_info.append(
            f"Additional information: {disability_details}"
        )

    accessibility_text = "\n".join(
        f"- {item}"
        for item in accessibility_info
    )

    prompt = f"""
You are EduAccess AI, an inclusive educational tutor.

Your purpose is to help students learn independently
using clear, accessible, personalized explanations.

ACCESSIBILITY INFORMATION:

{accessibility_text or "- No additional information provided."}

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
9. For programming questions, explain the code.
10. For mathematics, show calculation steps.
11. Correct mistakes politely.
12. Focus on understanding, not only the final answer.
13. Never make assumptions beyond the accessibility
    information provided.
14. Adapt the answer to the student's preferences.

"""

    if context:
        prompt += f"""
PREVIOUS CONVERSATION:

{context}

"""

    prompt += """
Now answer the student's question.
"""

    return prompt.strip()


# ============================================================
# ASK AI
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
    # Validate question
    # --------------------------------------------------------

    if question is None:
        return "Please enter a question."

    if not isinstance(question, str):
        question = str(question)

    question = question.strip()

    if not question:
        return "Please enter a question."

    # --------------------------------------------------------
    # Gemini client
    # --------------------------------------------------------

    try:
        client = get_gemini_client()

    except Exception as e:
        return (
            "❌ Gemini configuration error:\n\n"
            f"{str(e)}"
        )

    # --------------------------------------------------------
    # Prompt
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
    # Gemini request
    # --------------------------------------------------------

    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        if response and response.text:

            return response.text.strip()

        return (
            "⚠️ Gemini did not return an answer. "
            "Please try again."
        )

    except Exception as e:

        error_text = str(e)

        if "503" in error_text or "UNAVAILABLE" in error_text:

            return (
                "⚠️ Gemini is temporarily busy.\n\n"
                "Please wait a few seconds and try again."
            )

        if "429" in error_text:

            return (
                "⚠️ Gemini request limit reached.\n\n"
                "Please wait a little and try again."
            )

        if "404" in error_text:

            return (
                "❌ Gemini model is unavailable for this API key.\n\n"
                f"Configured model: {GEMINI_MODEL}"
            )

        return (
            "❌ AI Tutor error:\n\n"
            f"{error_text}"
        )


# ============================================================
# ASK TUTOR
# ============================================================

def ask_tutor(
    user,
    question: str,
    context: Optional[str] = None,
) -> str:
    """
    Main function used by the Tutor UI.

    IMPORTANT:
        ask_tutor(user, question, context)
    """

    # --------------------------------------------------------
    # Validate user
    # --------------------------------------------------------

    if user is None:

        return (
            "⚠️ User session not found.\n\n"
            "Please login again."
        )

    # --------------------------------------------------------
    # Safely convert question to text
    # --------------------------------------------------------

    if question is None:

        return "Please enter a question."

    if not isinstance(question, str):

        question = str(question)

    question = question.strip()

    if not question:

        return "Please enter a question."

    # --------------------------------------------------------
    # Get user preferences safely
    # --------------------------------------------------------

    preferred_language = getattr(
        user,
        "preferred_language",
        None,
    ) or "English"

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

    # --------------------------------------------------------
    # Ask AI
    # --------------------------------------------------------

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