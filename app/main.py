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
from app.ui.dashboard import show_dashboard
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
# LOGGED-IN USER
# ============================================================

else:

    # --------------------------------------------------------
    # GET USER
    # --------------------------------------------------------

    user = st.session_state.get("user")

    # --------------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------------

    with st.sidebar:

        st.title("♿ EduAccess AI")

        if user:

            user_name = getattr(
                user,
                "full_name",
                "Student",
            )

            st.write(
                f"👤 **{user_name}**"
            )

        st.divider()

        # ----------------------------------------------------
        # NAVIGATION
        # ----------------------------------------------------

        st.subheader("📚 Navigation")

        page = st.radio(
            "Select Page",
            [
                "🏠 Dashboard",
                "🤖 AI Tutor",
                "♿ Accessibility",
            ],
            label_visibility="collapsed",
        )

        st.divider()

        # ----------------------------------------------------
        # LOGOUT
        # ----------------------------------------------------

        if st.button(
            "🚪 Logout",
            use_container_width=True,
        ):

            logout_user()

            st.rerun()

    # ========================================================
    # DASHBOARD
    # ========================================================

    if page == "🏠 Dashboard":

        show_dashboard()

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