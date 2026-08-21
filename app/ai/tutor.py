from typing import Optional

from google import genai

from app.config.settings import settings


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
# PERSONALIZED LEARNING INSTRUCTIONS
# ============================================================

def build_learning_instruction(
    preferred_language: str = "English",
    simplified_language: bool = False,
    step_by_step_learning: bool = False,
    repetition_support: bool = False,
    visual_explanations: bool = False,
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
            "Repeat important concepts in a clear way "
            "when necessary."
        )

    if visual_explanations:
        instructions.append(
            "Use tables, structured points, ASCII diagrams, "
            "or simple visual descriptions when useful."
        )

    instructions.append(
        "Be patient, supportive, respectful, and encouraging."
    )

    return "\n".join(
        f"- {instruction}"
        for instruction in instructions
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
) -> str:

    instructions = build_learning_instruction(
        preferred_language=preferred_language,
        simplified_language=simplified_language,
        step_by_step_learning=step_by_step_learning,
        repetition_support=repetition_support,
        visual_explanations=visual_explanations,
    )

    prompt = f"""
You are EduAccess AI.

EduAccess AI is an inclusive educational assistant
designed to help students with different disabilities
and accessibility needs.

Your goal is to make education easier, clearer,
more accessible, and personalized.

LEARNING INSTRUCTIONS:

{instructions}

STUDENT QUESTION:

{question}
"""

    if context:

        prompt += f"""

STUDY CONTEXT:

{context}
"""

    prompt += """

GENERAL TEACHING RULES:

1. Give accurate educational information.

2. Use simple language whenever possible.

3. Explain difficult concepts step by step.

4. Give examples when useful.

5. Do not assume that the student already knows
   advanced concepts.

6. Use headings and bullet points to improve readability.

7. Be patient and supportive.

8. If the student asks a technical question,
   provide a practical explanation.

9. If the student makes a mistake,
   explain the mistake politely and show the correction.

10. Focus on helping the student understand the topic,
    not just giving the final answer.

11. For mathematics, show the calculation steps.

12. For programming questions, explain the code
    and provide corrected code when necessary.

13. Do not discriminate based on disability.

14. Adapt the explanation to the student's selected
    accessibility preferences.

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
) -> str:

    if not question or not question.strip():

        return "Please enter a question."

    client = get_gemini_client()

    prompt = create_tutor_prompt(
        question=question,
        context=context,
        preferred_language=preferred_language,
        simplified_language=simplified_language,
        step_by_step_learning=step_by_step_learning,
        repetition_support=repetition_support,
        visual_explanations=visual_explanations,
    )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    if not response.text:

        return (
            "Sorry, I could not generate an answer. "
            "Please try again."
        )

    return response.text