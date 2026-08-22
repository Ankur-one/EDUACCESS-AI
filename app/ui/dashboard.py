import streamlit as st  # type: ignore[reportMissingImports]


# ============================================================
# EDUACCESS AI — STUDENT DASHBOARD
# ============================================================

def show_dashboard():
    """
    Main student dashboard for EduAccess AI.
    """

    user = st.session_state.get("user")

    if user is None:
        st.error("⚠️ User session not found. Please login again.")
        return

    # ========================================================
    # HEADER
    # ========================================================

    st.title("🎓 EduAccess AI Dashboard")

    user_name = getattr(
        user,
        "full_name",
        "Student",
    )

    st.subheader(
        f"Welcome, {user_name}! 👋"
    )

    st.write(
        "Your personalized accessible learning environment."
    )

    st.divider()

    # ========================================================
    # BASIC USER INFORMATION
    # ========================================================

    disability_type = getattr(
        user,
        "disability_type",
        None,
    ) or "Not specified"

    preferred_language = getattr(
        user,
        "preferred_language",
        None,
    ) or "English"

    # ========================================================
    # PROFILE CARDS
    # ========================================================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            f"""
### 👤 Student

**{user_name}**

Language: **{preferred_language}**
"""
        )

    with col2:
        st.info(
            f"""
### ♿ Accessibility

**{disability_type}**

Personalized support enabled.
"""
        )

    with col3:
        st.success(
            """
### 🤖 AI Tutor

**Available**

Ask questions anytime.
"""
        )

    st.divider()

    # ========================================================
    # LEARNING FEATURES
    # ========================================================

    st.subheader("🚀 Learning Features")

    feature1, feature2, feature3 = st.columns(3)

    with feature1:
        st.markdown(
            """
### 🤖 AI Tutor

Ask educational questions and
receive personalized explanations.
"""
        )

        if st.button(
            "Open AI Tutor",
            use_container_width=True,
        ):
            st.session_state["page"] = "AI Tutor"
            st.rerun()

    with feature2:
        st.markdown(
            """
### ♿ Accessibility

Customize your learning experience
according to your accessibility needs.
"""
        )

        if st.button(
            "Accessibility Settings",
            use_container_width=True,
        ):
            st.session_state["page"] = "Accessibility"
            st.rerun()

    with feature3:
        st.markdown(
            """
### 🔊 Voice Support

Use speech input and listen to
AI-generated educational answers.
"""
        )

        st.success("Voice features available")

    st.divider()

    # ========================================================
    # ACCESSIBILITY SUPPORT
    # ========================================================

    st.subheader("♿ Your Accessibility Support")

    support1, support2, support3, support4 = st.columns(4)

    simple_explanation = bool(
        getattr(
            user,
            "simple_explanation",
            False,
        )
    )

    step_by_step = bool(
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

    visual_explanation = bool(
        getattr(
            user,
            "visual_explanation",
            False,
        )
    )

    with support1:
        if simple_explanation:
            st.success("✅ Simple\nExplanation")
        else:
            st.info("○ Simple\nExplanation")

    with support2:
        if step_by_step:
            st.success("✅ Step-by-Step")
        else:
            st.info("○ Step-by-Step")

    with support3:
        if repetition_support:
            st.success("✅ Repetition\nSupport")
        else:
            st.info("○ Repetition\nSupport")

    with support4:
        if visual_explanation:
            st.success("✅ Visual\nExplanation")
        else:
            st.info("○ Visual\nExplanation")

    st.divider()

    # ========================================================
    # LEARNING ACTIVITY
    # ========================================================

    st.subheader("📊 Learning Activity")

    history = st.session_state.get(
        "tutor_history",
        [],
    )

    question_count = len(history)

    activity1, activity2, activity3 = st.columns(3)

    with activity1:
        st.metric(
            "Questions Asked",
            question_count,
        )

    with activity2:
        st.metric(
            "AI Tutor",
            "Available",
        )

    with activity3:
        st.metric(
            "Accessibility",
            "Enabled",
        )

    st.divider()

    # ========================================================
    # RECENT QUESTIONS
    # ========================================================

    st.subheader("📝 Recent Questions")

    if history:

        # Display latest questions first
        recent_history = history[-5:][::-1]

        for index, item in enumerate(
            recent_history,
            start=1,
        ):

            if isinstance(item, dict):

                question = item.get(
                    "question",
                    "Unknown question",
                )

            else:

                question = str(item)

            st.markdown(
                f"""
**{index}.** {question}
"""
            )

    else:

        st.info(
            "No questions asked yet. "
            "Start learning with the AI Tutor!"
        )

    st.divider()

    # ========================================================
    # QUICK ACTION
    # ========================================================

    st.subheader("⚡ Quick Start")

    st.write(
        "Ready to learn? Ask EduAccess AI a question."
    )

    if st.button(
        "✨ Start Learning",
        use_container_width=True,
    ):

        st.session_state["page"] = "AI Tutor"

        st.rerun()