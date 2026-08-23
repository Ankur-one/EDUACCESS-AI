import importlib


# Load Streamlit dynamically so this module can still be inspected in
# environments where the optional Streamlit dependency is not installed.
st = importlib.import_module("streamlit")


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

        # AI Tutor
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
    Create the login session using the authenticated User object.
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
    Preferred login function.
    """

    return create_login_session(user)


# ============================================================
# CHECK LOGIN
# ============================================================

def is_logged_in():
    """
    Check whether a valid user is logged in.
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
    Return the complete logged-in User object.
    """

    return st.session_state.get("user")


# ============================================================
# GET CURRENT USER ID
# ============================================================

def get_current_user_id():
    """
    Return the ID of the currently logged-in user.
    """

    # First use the stored session ID
    user_id = st.session_state.get("user_id")

    if user_id is not None:
        return user_id

    # Fallback: get ID from User object
    user = st.session_state.get("user")

    if user is not None:
        user_id = getattr(
            user,
            "id",
            None,
        )

        if user_id is not None:
            st.session_state["user_id"] = user_id

        return user_id

    return None


# ============================================================
# GET CURRENT USER NAME
# ============================================================

def get_current_user_name():
    """
    Return the current student's name.
    """

    user_name = st.session_state.get("user_name")

    if user_name:
        return user_name

    user = st.session_state.get("user")

    if user is not None:
        return getattr(
            user,
            "full_name",
            "Student",
        )

    return None


# ============================================================
# GET CURRENT DISABILITY TYPE
# ============================================================

def get_current_disability_type():
    """
    Return the current student's disability type.
    """

    disability_type = st.session_state.get(
        "disability_type"
    )

    if disability_type:
        return disability_type

    user = st.session_state.get("user")

    if user is not None:
        return getattr(
            user,
            "disability_type",
            None,
        )

    return None


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


# ============================================================
# CLEAR SESSION
# ============================================================

def clear_session():
    """
    Alias for logout_user().
    """

    logout_user()