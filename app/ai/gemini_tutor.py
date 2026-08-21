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

MODEL_NAME = "gemini-3.6-flash"


# ============================================================
# BUILD PERSONALIZED SYSTEM INSTRUCTION
# ============================================================

def build_student_instruction(user):

    instructions = []

    instructions.append(
        "You are EduAccess AI, an inclusive educational AI tutor."
    )

    instructions.append(
        "Your goal is to help students learn clearly, patiently, "
        "respectfully, and accessibly."
    )

    # --------------------------------------------------------
    # Disability
    # --------------------------------------------------------

    if user.disability_type:

        instructions.append(
            f"Student accessibility need: "
            f"{user.disability_type}."
        )

    # --------------------------------------------------------
    # Additional details
    # --------------------------------------------------------

    if user.disability_details:

        instructions.append(
            f"Additional accessibility information: "
            f"{user.disability_details}."
        )

    # --------------------------------------------------------
    # Language
    # --------------------------------------------------------

    if user.preferred_language:

        instructions.append(
            f"Respond primarily in "
            f"{user.preferred_language}."
        )

    # --------------------------------------------------------
    # Learning preferences
    # --------------------------------------------------------

    if user.simple_explanation:

        instructions.append(
            "Use simple and easy-to-understand explanations."
        )

    if user.step_by_step:

        instructions.append(
            "Explain difficult concepts step by step."
        )

    if user.repetition_support:

        instructions.append(
            "Repeat or summarize important concepts when useful."
        )

    if user.visual_explanation:

        instructions.append(
            "Use structured text, examples, tables, "
            "and text-based diagrams when useful."
        )

    if user.text_to_speech:

        instructions.append(
            "Keep responses suitable for text-to-speech "
            "and screen readers."
        )

    if user.speech_to_text:

        instructions.append(
            "Make responses easy to understand when the student "
            "uses speech-to-text."
        )

    if user.large_text:

        instructions.append(
            "Use clear headings and spacing for readability."
        )

    # --------------------------------------------------------
    # Educational behavior
    # --------------------------------------------------------

    instructions.append(
        "Do not make assumptions about the student's abilities."
    )

    instructions.append(
        "Never use insulting, discriminatory, or stigmatizing language."
    )

    instructions.append(
        "When teaching, give examples whenever possible."
    )

    instructions.append(
        "If the question is unclear, ask a simple clarification."
    )

    return "\n".join(instructions)


# ============================================================
# ASK GEMINI
# ============================================================

def ask_tutor(user, question):

    if not question or not question.strip():

        return "Please enter a question."

    student_instruction = build_student_instruction(
        user
    )

    prompt = f"""
{student_instruction}

Student's question:

{question}

Provide an educational answer that follows
the student's accessibility requirements.
"""

    try:

        response = client.models.generate_content(

            model=MODEL_NAME,

            contents=prompt
        )

        if response and response.text:

            return response.text

        return (
            "I could not generate a response. "
            "Please try again."
        )

    except Exception as e:

        return (
            "The AI Tutor is temporarily unavailable. "
            "Please try again shortly.\n\n"
            f"Technical information: {str(e)}"
        )