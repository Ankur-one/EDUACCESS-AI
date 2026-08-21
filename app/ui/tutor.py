import streamlit as st  # pyright: ignore[reportMissingImports]

from app.auth.session import get_current_user_id
from app.database.database import SessionLocal
from app.database.models import User

from app.ai.gemini_tutor import ask_tutor


def show_tutor():

    st.title("🤖 EduAccess AI Tutor")

    st.write(
        "Ask your personalized AI tutor anything "
        "about your studies."
    )

    st.divider()

    # ========================================================
    # GET CURRENT USER
    # ========================================================

    user_id = get_current_user_id()

    if not user_id:

        st.error(
            "User session not found."
        )

        return

    db = SessionLocal()

    try:

        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if not user:

            st.error(
                "Student profile could not be found."
            )

            return

        # ====================================================
        # STUDENT PROFILE
        # ====================================================

        st.info(
            f"♿ Accessibility profile: "
            f"**{user.disability_type}**"
        )

        # ====================================================
        # QUESTION
        # ====================================================

        question = st.text_area(
            "Ask your question",
            placeholder=(
                "Example: Explain machine learning "
                "in simple words."
            ),
            height=150,
        )

        # ====================================================
        # ASK BUTTON
        # ====================================================

        if st.button(
            "🤖 Ask AI Tutor",
            use_container_width=True,
        ):

            if not question.strip():

                st.warning(
                    "Please enter a question first."
                )

                return

            with st.spinner(
                "EduAccess AI is preparing your answer..."
            ):

                answer = ask_tutor(
                    user=user,
                    question=question,
                )

            st.divider()

            st.subheader(
                "📖 AI Tutor Response"
            )

            st.markdown(answer)

    finally:

        db.close()