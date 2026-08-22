"""Session-state helpers with an optional Streamlit dependency."""

try:
    import importlib

    st = importlib.import_module("streamlit")
except ModuleNotFoundError:
    class _SessionState(dict):
        """Minimal fallback used when this module is imported outside Streamlit."""

    class _StreamlitFallback:
        session_state = _SessionState()

    st = _StreamlitFallback()


# ============================================================
# INITIALIZE SESSION
# ============================================================

def initialize_session():
    """
    Initialize all Streamlit session variables.
    """

    defaults = {
        "logged_in": False,
        "user": None,
        "user_id": None,
        "user_name": None,
        "disability_type": None,
        "chat_history": [],
        "conversation_history": [],
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


# ============================================================
# CREATE LOGIN SESSION
# ============================================================

def create_login_session(user):
    """
    Create a complete login session for the authenticated user.

    This function is kept for compatibility with the existing
    app/ui/login.py.
    """

    if user is None:
        return False

    # Store complete User object
    st.session_state["user"] = user

    # Login status
    st.session_state["logged_in"] = True

    # User ID
    st.session_state["user_id"] = getattr(
        user,
        "id",
        None,
    )

    # User name
    st.session_state["user_name"] = getattr(
        user,
        "full_name",
        "Student",
    )

    # Disability
    st.session_state["disability_type"] = getattr(
        user,
        "disability_type",
        None,
    )

    return True


# ============================================================
# LOGIN USER
# ============================================================

def login_user(user):
    """
    New preferred login function.

    Internally uses create_login_session() so both old and
    new code work correctly.
    """

    return create_login_session(user)


# ============================================================
# CHECK LOGIN
# ============================================================

def is_logged_in():
    """
    Return True only when a valid User object exists.
    """

    user = st.session_state.get("user")

    return (
        st.session_state.get("logged_in", False)
        and user is not None
    )


# ============================================================
# GET CURRENT USER
# ============================================================

def get_current_user():
    """
    Return the currently logged-in User object.
    """

    return st.session_state.get("user")


# ============================================================
# LOGOUT
# ============================================================

def logout_user():
    """
    Completely clear the current login session.
    """

    st.session_state["logged_in"] = False

    st.session_state["user"] = None

    st.session_state["user_id"] = None

    st.session_state["user_name"] = None

    st.session_state["disability_type"] = None

    # Clear AI Tutor history
    st.session_state["chat_history"] = []

    st.session_state["conversation_history"] = []