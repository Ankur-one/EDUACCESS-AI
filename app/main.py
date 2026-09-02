import importlib


# ============================================================
# AUTH SESSION
# ============================================================

from app.auth.session import (
    initialize_session,
    is_logged_in,
    logout_user,
    get_current_user_id,
)


# ============================================================
# DATABASE
# ============================================================

from app.database.database import SessionLocal
from app.database.models import User


# ============================================================
# UI MODULES
# ============================================================

from app.ui.login import show_login
from app.ui.dashboard import show_dashboard
from app.ai.tutor import show_tutor
from app.ui.history import show_history
from app.ui.settings import show_settings
from app.ui.accessibility import (
    apply_accessibility_styles,
)


# Load Streamlit dynamically so static analysis does not require the
# optional UI dependency to be installed in its analysis environment.
st = importlib.import_module("streamlit")


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
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    button {
        min-height: 42px;
    }

    p {
        line-height: 1.6;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOGIN CHECK
# ============================================================

if not is_logged_in():

    show_login()

    st.stop()


# ============================================================
# APPLY USER ACCESSIBILITY SETTINGS
# ============================================================

current_user_id = get_current_user_id()

if current_user_id:

    accessibility_db = SessionLocal()

    try:

        current_user = (
            accessibility_db.query(User)
            .filter(
                User.id == current_user_id
            )
            .first()
        )

        if current_user:

            apply_accessibility_styles(
                current_user
            )

    except Exception:

        # Do not stop the complete application if
        # accessibility CSS fails.

        st.warning(
            "⚠️ Accessibility preferences "
            "could not be applied."
        )

        # Keep the actual error hidden from normal users.

    finally:

        accessibility_db.close()


# ============================================================
# DEFAULT PAGE
# ============================================================

if "selected_page" not in st.session_state:

    st.session_state.selected_page = (
        "Dashboard"
    )


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    st.title("♿ EduAccess AI")

    st.caption(
        "Inclusive Educational Assistant"
    )

    st.divider()

    # ========================================================
    # AVAILABLE PAGES
    # ========================================================

    navigation_pages = [
        "Dashboard",
        "AI Tutor",
        "History",
        "Settings",
    ]

    # ========================================================
    # SAFETY CHECK
    # ========================================================

    if (
        st.session_state.selected_page
        not in navigation_pages
    ):

        st.session_state.selected_page = (
            "Dashboard"
        )

    # ========================================================
    # NAVIGATION
    # ========================================================

    page = st.radio(
        "Navigation",
        navigation_pages,
        index=navigation_pages.index(
            st.session_state.selected_page
        ),
        key="main_navigation",
    )

    # ========================================================
    # SAVE CURRENT PAGE
    # ========================================================

    st.session_state.selected_page = page

    st.divider()

    # ========================================================
    # ACCESSIBILITY INFORMATION
    # ========================================================

    st.caption(
        "♿ Accessibility support enabled"
    )

    st.caption(
        "Customize your experience from "
        "Settings."
    )

    st.divider()

    # ========================================================
    # LOGOUT
    # ========================================================

    if st.button(
        "🚪 Logout",
        use_container_width=True,
        key="main_logout_button",
    ):

        logout_user()

        # Reset selected page
        st.session_state.selected_page = (
            "Dashboard"
        )

        # Remove navigation widget state
        if "main_navigation" in st.session_state:

            del st.session_state[
                "main_navigation"
            ]

        st.rerun()


# ============================================================
# PAGE ROUTING
# ============================================================

if page == "Dashboard":

    show_dashboard()


elif page == "AI Tutor":

    show_tutor()


elif page == "History":

    show_history()


elif page == "Settings":

    show_settings()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "EduAccess AI • Inclusive Learning Platform"
)

st.caption(
    "Personalized • Accessible • AI-Powered"
)
