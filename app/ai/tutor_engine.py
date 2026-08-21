from google import genai

from app.config.settings import settings


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


# ============================================================
# MODEL
# ============================================================

GEMINI_MODEL = "gemini-3.6-flash"


# ============================================================
# BUILD ACCESSIBLE PROMPT
# ============================================================

def build_accessibility_prompt(
    user,
    question: str,
) -> str:

    instructions = []

    # --------------------------------------------------------
    # Disability
    # --------------------------------------------------------

    if user.disability_type:

        instructions.append(
            f"Student accessibility need: "
            f"{user.disability_type}."
        )

    # --------------------------------------------------------
    # Disability Details
    # --------------------------------------------------------

    if user.disability_details:

        instructions.append(
            f"Additional accessibility information: "
            f"{user.disability_details}."
        )

    # --------------------------------------------------------
    # Simple Explanation
    # --------------------------------------------------------

    if user.simple_explanation:

        instructions.append(
            "Use very simple and easy-to-understand "
            "language."
        )

    # --------------------------------------------------------
    # Step-by-Step
    # --------------------------------------------------------

    if user.step_by_step:

        instructions.append(
            "Explain the answer step-by-step."
        )

    # --------------------------------------------------------
    # Repetition
    # --------------------------------------------------------

    if user.repetition_support:

        instructions.append(
            "Repeat important concepts and summarize "
            "the key points."
        )

    # --------------------------------------------------------
    # Visual Explanation
    # --------------------------------------------------------

    if user.visual_explanation:

        instructions.append(
            "Use structured text, bullet points, "
            "tables, examples, and simple text diagrams "
            "when useful."
        )

    # --------------------------------------------------------
    # Large Text
    # --------------------------------------------------------

    if user.large_text:

        instructions.append(
            "Use clear headings, short paragraphs, "
            "and well-spaced content."
        )

    # --------------------------------------------------------
    # High Contrast
    # --------------------------------------------------------

    if user.high_contrast:

        instructions.append(
            "Keep the response clean and structured "
            "with clear headings and minimal visual clutter."
        )

    # --------------------------------------------------------
    # Dyslexia Friendly
    # --------------------------------------------------------

    if user.dyslexia_friendly:

        instructions.append(
            "Use short sentences, simple words, "
            "clear headings, bullet points, and generous "
            "spacing. Avoid unnecessarily complicated "
            "sentence structures."
        )

    # --------------------------------------------------------
    # Language
    # --------------------------------------------------------

    language = user.preferred_language or "English"

    instructions.append(
        f"Respond in {language}."
    )

    # --------------------------------------------------------
    # FINAL PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are EduAccess AI, an inclusive AI study tutor.

Your goal is to help students with different
accessibility needs learn independently.

ACCESSIBILITY INSTRUCTIONS:

{chr(10).join("- " + item for item in instructions)}

IMPORTANT RULES:

1. Never make assumptions about the student's
   disability beyond the information provided.

2. Focus on teaching and learning.

3. Do not use unnecessarily difficult language.

4. Give examples whenever they improve understanding.

5. If the question is technical, explain the concept
   first and then provide the technical details.

6. If the student asks for a solution, explain the
   reasoning instead of only giving the final answer.

7. Make the response accessible and easy to follow.

STUDENT QUESTION:

{question}

Now provide the best possible educational answer.
"""

    return prompt


# ============================================================
# ASK GEMINI
# ============================================================

def ask_tutor(
    user,
    question: str,
) -> str:

    if not settings.GEMINI_API_KEY:

        return (
            "❌ Gemini API key is not configured."
        )

    if not question.strip():

        return (
            "Please enter a question."
        )

    prompt = build_accessibility_prompt(
        user=user,
        question=question,
    )

    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        if response.text:

            return response.text

        return (
            "⚠️ Gemini did not return an answer."
        )

    except Exception as e:

        return (
            "❌ AI Tutor error:\n\n"
            f"{str(e)}"
        )