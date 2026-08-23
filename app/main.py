import streamlit as st  # type: ignore[import-not-found]

# ============================================================
# AUTHENTICATION & SESSION
# ============================================================

from app.auth.session import (
    initialize_session,
    is_logged_in,
    logout_user,
)

# ============================================================
# UI PAGES
# ============================================================

from app.ui.login import show_login
from app.ui.register import show_register
from app.ui.tutor import show_tutor
from app.ui.history import show_history
from app.ui.accessibility import show_accessibility

# ============================================================
# ACCESSIBILITY STYLE
# ============================================================

from app.ui.accessibility_style import (
    apply_accessibility_style,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EduAccess AI",
    page_icon="♿",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# INITIALIZE SESSION
# ============================================================

initialize_session()


# ============================================================
# APPLY ACCESSIBILITY STYLE
# ============================================================

apply_accessibility_style()


# ============================================================
# LOGIN / REGISTER
# ============================================================

if not is_logged_in():

    st.title("♿ EduAccess AI")

    st.markdown(
        """
        ### Inclusive AI-Powered Education

        EduAccess AI is an AI-powered learning platform
        designed to support students with different
        disabilities and accessibility needs.
        """
    )

    st.divider()

    login_tab, register_tab = st.tabs(
        [
            "🔐 Login",
            "📝 Register",
        ]
    )

    with login_tab:

        show_login()

    with register_tab:

        show_register()


# ============================================================
# LOGGED-IN APPLICATION
# ============================================================

else:

    # ========================================================
    # SIDEBAR
    # ========================================================

    st.sidebar.title(
        "♿ EduAccess AI"
    )

    st.sidebar.caption(
        "Inclusive AI-Powered Education"
    )

    st.sidebar.divider()

    # --------------------------------------------------------
    # GET USER NAME
    # --------------------------------------------------------

    user_name = st.session_state.get(
        "user_name",
        "Student",
    )

    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🤖 AI Tutor",
            "📚 History",
            "♿ Accessibility",
        ],
    )

    st.sidebar.divider()

    st.sidebar.write(
        f"👤 **{user_name}**"
    )

    # ========================================================
    # LOGOUT
    # ========================================================

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True,
    ):

        logout_user()

        st.rerun()

    # ========================================================
    # DASHBOARD
    # ========================================================

    if page == "🏠 Dashboard":

        st.title(
            "🎓 EduAccess AI Dashboard"
        )

        st.subheader(
            f"Welcome, {user_name}! 👋"
        )

        st.write(
            "Your personalized accessible "
            "learning environment."
        )

        st.divider()

        # ----------------------------------------------------
        # PROFILE CARDS
        # ----------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.info(
                f"""
### 👤 Student

**{user_name}**
"""
            )

        with col2:

            disability_type = (
                st.session_state.get(
                    "disability_type",
                    "Not specified",
                )
            )

            st.info(
                f"""
### ♿ Accessibility

**{disability_type}**
"""
            )

        with col3:

            st.success(
                """
### 🤖 AI Tutor

**Available**
"""
            )

        st.divider()

        # ----------------------------------------------------
        # FEATURES
        # ----------------------------------------------------

        st.subheader(
            "🚀 EduAccess AI Features"
        )

        feature1, feature2, feature3 = st.columns(3)

        with feature1:

            st.markdown(
                """
### 🤖 AI Tutor

Ask questions and receive
personalized explanations.
"""
            )

        with feature2:

            st.markdown(
                """
### 📚 History

View your previous AI Tutor
questions and answers.
"""
            )

        with feature3:

            st.markdown(
                """
### ♿ Accessibility

Customize your learning
experience.
"""
            )

        st.divider()

        # ----------------------------------------------------
        # ACCESSIBILITY SUPPORT
        # ----------------------------------------------------

        st.subheader(
            "♿ Your Learning Support"
        )

        support1, support2, support3 = st.columns(3)

        with support1:

            st.markdown(
                """
🔊 **Audio Support**

Text-to-Speech can help
students who prefer listening.
"""
            )

        with support2:

            st.markdown(
                """
🧩 **Step-by-Step Learning**

Complex concepts can be
broken into smaller steps.
"""
            )

        with support3:

            st.markdown(
                """
🔎 **Readable Content**

Clear formatting and
accessible content improve readability.
"""
            )

        st.divider()

        st.info(
            """
💡 Use the sidebar to access:

**🤖 AI Tutor** → Ask educational questions.

**📚 History** → View previous conversations.

**♿ Accessibility** → Customize your learning experience.
"""
        )

    # ========================================================
    # AI TUTOR
    # ========================================================

    elif page == "🤖 AI Tutor":

        show_tutor()

    # ========================================================
    # HISTORY
    # ========================================================

    elif page == "📚 History":

        show_history()

    # ========================================================
    # ACCESSIBILITY
    # ========================================================

    elif page == "♿ Accessibility":

        show_accessibility()