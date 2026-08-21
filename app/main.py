import streamlit as st  # pyright: ignore[reportMissingImports]

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
# NOT LOGGED IN
# ============================================================

if not is_logged_in():

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # LOGIN / REGISTER
    # --------------------------------------------------------

    login_tab, register_tab = st.tabs(
        [
            "🔐 Login",
            "📝 Register",
        ]
    )

    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    with login_tab:

        show_login()

    # --------------------------------------------------------
    # REGISTER
    # --------------------------------------------------------

    with register_tab:

        show_register()


# ============================================================
# LOGGED IN
# ============================================================

else:

    # ========================================================
    # SIDEBAR
    # ========================================================

    st.sidebar.title("♿ EduAccess AI")

    st.sidebar.success(
        f"Welcome, {st.session_state.user_name}"
    )

    st.sidebar.divider()

    # --------------------------------------------------------
    # USER INFORMATION
    # --------------------------------------------------------

    st.sidebar.markdown(
        "### 👤 Student"
    )

    st.sidebar.write(
        st.session_state.user_name
    )

    st.sidebar.markdown(
        "### 📧 Email"
    )

    st.sidebar.write(
        st.session_state.user_email
    )

    st.sidebar.markdown(
        "### ♿ Accessibility"
    )

    st.sidebar.write(
        st.session_state.disability_type
    )

    st.sidebar.divider()

    # ========================================================
    # NAVIGATION
    # ========================================================

    page = st.sidebar.radio(
        "📚 Navigation",
        [
            "🏠 Dashboard",
            "🤖 AI Tutor",
            "♿ Accessibility",
        ],
    )

    st.sidebar.divider()

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
            f"Welcome, {st.session_state.user_name}! 👋"
        )

        st.write(
            "Your personalized accessible learning environment."
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

**{st.session_state.user_name}**
"""
            )

        with col2:

            st.info(
                f"""
### ♿ Accessibility

**{st.session_state.disability_type}**
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
### ♿ Accessibility

Customize learning according
to your accessibility needs.
"""
            )

        with feature3:

            st.markdown(
                """
### 📚 Smart Learning

Learn using simple,
structured and adaptive content.
"""
            )

        st.divider()

        # ----------------------------------------------------
        # ACCESSIBILITY SUMMARY
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
🪜 **Step-by-Step Learning**

Complex concepts can be
broken into smaller steps.
"""
            )

        with support3:

            st.markdown(
                """
🔎 **Readable Content**

Large text and accessible
formatting improve readability.
"""
            )

        st.divider()

        st.info(
            """
💡 Use the sidebar to access:

**🤖 AI Tutor** → Ask educational questions.

**♿ Accessibility** → Customize your learning
experience.
"""
        )

    # ========================================================
    # AI TUTOR
    # ========================================================

    elif page == "🤖 AI Tutor":

        show_tutor()

    # ========================================================
    # ACCESSIBILITY
    # ========================================================

    elif page == "♿ Accessibility":

        show_accessibility()