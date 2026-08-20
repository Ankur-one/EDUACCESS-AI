try:
    import streamlit as st  # pyright: ignore[reportMissingImports]
except ImportError:  # Allows non-Streamlit tooling to import this module.
    st = None


def initialize_session():
    """
    Initialize Streamlit session variables.
    """

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if "user_name" not in st.session_state:
        st.session_state.user_name = None

    if "user_email" not in st.session_state:
        st.session_state.user_email = None


def login_user(user):
    """
    Store authenticated user information.
    """

    st.session_state.logged_in = True
    st.session_state.user_id = user.id
    st.session_state.user_name = user.full_name
    st.session_state.user_email = user.email


def logout_user():
    """
    Clear the current user session.
    """

    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_name = None
    st.session_state.user_email = None


def is_logged_in():
    """
    Check whether a student is authenticated.
    """

    return st.session_state.get(
        "logged_in",
        False
    )