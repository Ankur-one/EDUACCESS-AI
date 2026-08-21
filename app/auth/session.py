import streamlit as st  # type: ignore[reportMissingImports]


# ============================================================
# INITIALIZE SESSION
# ============================================================

def initialize_session():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if "user_name" not in st.session_state:
        st.session_state.user_name = None

    if "user_email" not in st.session_state:
        st.session_state.user_email = None

    if "disability_type" not in st.session_state:
        st.session_state.disability_type = None


# ============================================================
# LOGIN SESSION
# ============================================================

def create_login_session(user):

    st.session_state.logged_in = True

    st.session_state.user_id = user.id

    st.session_state.user_name = user.full_name

    st.session_state.user_email = user.email

    st.session_state.disability_type = (
        user.disability_type
    )


# ============================================================
# LOGOUT
# ============================================================

def logout_user():

    st.session_state.logged_in = False

    st.session_state.user_id = None

    st.session_state.user_name = None

    st.session_state.user_email = None

    st.session_state.disability_type = None


# ============================================================
# CHECK LOGIN
# ============================================================

def is_logged_in():

    return st.session_state.get(
        "logged_in",
        False
    )


# ============================================================
# CURRENT USER ID
# ============================================================

def get_current_user_id():

    return st.session_state.get(
        "user_id"
    )


# ============================================================
# CURRENT USER NAME
# ============================================================

def get_current_user_name():

    return st.session_state.get(
        "user_name"
    )