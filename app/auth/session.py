import streamlit as st  # type: ignore[import-not-found]


# ============================================================
# STREAMLIT
# ============================================================

# ============================================================
# INITIALIZE SESSION
# ============================================================

def initialize_session():
    """
    Initialize all EduAccess AI Streamlit session variables.
    """

    defaults = {

        # ----------------------------------------------------
        # AUTHENTICATION
        # ----------------------------------------------------

        "logged_in": False,
        "user": None,
        "user_id": None,
        "user_name": None,
        "disability_type": None,

        # ----------------------------------------------------
        # USER PREFERENCES
        # ----------------------------------------------------

        "preferred_language": "English",

        "simple_explanation": True,

        "step_by_step": True,

        "repetition_support": False,

        "visual_explanation": True,

        # ----------------------------------------------------
        # COMMUNICATION ACCESSIBILITY
        # ----------------------------------------------------

        "text_to_speech": False,

        "speech_to_text": False,

        # ----------------------------------------------------
        # VISUAL ACCESSIBILITY
        # ----------------------------------------------------

        "large_text": False,

        "high_contrast": False,

        "dyslexia_friendly": False,

        # ----------------------------------------------------
        # AI TUTOR
        # ----------------------------------------------------

        "chat_history": [],

        "conversation_history": [],

        "tutor_question": "",

        "selected_page": "Dashboard",
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# ============================================================
# CREATE LOGIN SESSION
# ============================================================

def create_login_session(user):
    """
    Create a complete login session from the authenticated
    User database object.

    This also loads all saved accessibility and learning
    preferences into Streamlit session state.
    """

    if user is None:

        return False

    # ========================================================
    # BASIC USER INFORMATION
    # ========================================================

    st.session_state["user"] = user

    st.session_state["logged_in"] = True

    st.session_state["user_id"] = getattr(
        user,
        "id",
        None,
    )

    st.session_state["user_name"] = getattr(
        user,
        "full_name",
        "Student",
    )

    st.session_state["disability_type"] = getattr(
        user,
        "disability_type",
        None,
    )

    # ========================================================
    # LANGUAGE
    # ========================================================

    st.session_state["preferred_language"] = (
        getattr(
            user,
            "preferred_language",
            None,
        )
        or "English"
    )

    # ========================================================
    # LEARNING PREFERENCES
    # ========================================================

    st.session_state["simple_explanation"] = bool(
        getattr(
            user,
            "simple_explanation",
            True,
        )
    )

    st.session_state["step_by_step"] = bool(
        getattr(
            user,
            "step_by_step",
            True,
        )
    )

    st.session_state["repetition_support"] = bool(
        getattr(
            user,
            "repetition_support",
            False,
        )
    )

    st.session_state["visual_explanation"] = bool(
        getattr(
            user,
            "visual_explanation",
            True,
        )
    )

    # ========================================================
    # COMMUNICATION ACCESSIBILITY
    # ========================================================

    st.session_state["text_to_speech"] = bool(
        getattr(
            user,
            "text_to_speech",
            False,
        )
    )

    st.session_state["speech_to_text"] = bool(
        getattr(
            user,
            "speech_to_text",
            False,
        )
    )

    # ========================================================
    # VISUAL ACCESSIBILITY
    # ========================================================

    st.session_state["large_text"] = bool(
        getattr(
            user,
            "large_text",
            False,
        )
    )

    st.session_state["high_contrast"] = bool(
        getattr(
            user,
            "high_contrast",
            False,
        )
    )

    st.session_state["dyslexia_friendly"] = bool(
        getattr(
            user,
            "dyslexia_friendly",
            False,
        )
    )

    # ========================================================
    # RESET TUTOR STATE FOR NEW LOGIN
    # ========================================================

    st.session_state["chat_history"] = []

    st.session_state["conversation_history"] = []

    st.session_state["tutor_question"] = ""

    # ========================================================
    # START AT DASHBOARD
    # ========================================================

    st.session_state["selected_page"] = "Dashboard"

    return True


# ============================================================
# LOGIN USER SESSION
# ============================================================

def login_user(user):
    """
    Compatibility wrapper.

    This function creates the Streamlit login session.
    """

    return create_login_session(user)


# ============================================================
# CHECK LOGIN
# ============================================================

def is_logged_in():
    """
    Return True only when a valid user session exists.
    """

    return bool(
        st.session_state.get(
            "logged_in",
            False,
        )
        and st.session_state.get(
            "user",
            None,
        ) is not None
    )


# ============================================================
# GET CURRENT USER
# ============================================================

def get_current_user():
    """
    Return the currently logged-in User object.
    """

    return st.session_state.get(
        "user"
    )


# ============================================================
# GET CURRENT USER ID
# ============================================================

def get_current_user_id():
    """
    Return the currently logged-in user's database ID.
    """

    user_id = st.session_state.get(
        "user_id"
    )

    if user_id is not None:

        return user_id

    user = st.session_state.get(
        "user"
    )

    if user is not None:

        user_id = getattr(
            user,
            "id",
            None,
        )

        if user_id is not None:

            st.session_state["user_id"] = (
                user_id
            )

        return user_id

    return None


# ============================================================
# GET CURRENT USER NAME
# ============================================================

def get_current_user_name():
    """
    Return the logged-in student's name.
    """

    user_name = st.session_state.get(
        "user_name"
    )

    if user_name:

        return user_name

    user = st.session_state.get(
        "user"
    )

    if user is not None:

        return getattr(
            user,
            "full_name",
            "Student",
        )

    return None


# ============================================================
# GET DISABILITY TYPE
# ============================================================

def get_current_disability_type():
    """
    Return the logged-in student's disability type.
    """

    disability_type = st.session_state.get(
        "disability_type"
    )

    if disability_type:

        return disability_type

    user = st.session_state.get(
        "user"
    )

    if user is not None:

        return getattr(
            user,
            "disability_type",
            None,
        )

    return None


# ============================================================
# GET PREFERRED LANGUAGE
# ============================================================

def get_preferred_language():
    """
    Return the student's preferred language.
    """

    return st.session_state.get(
        "preferred_language",
        "English",
    )


# ============================================================
# GET ACCESSIBILITY PREFERENCES
# ============================================================

def get_accessibility_preferences():
    """
    Return all accessibility preferences currently
    loaded into the student's session.
    """

    return {

        "text_to_speech": bool(
            st.session_state.get(
                "text_to_speech",
                False,
            )
        ),

        "speech_to_text": bool(
            st.session_state.get(
                "speech_to_text",
                False,
            )
        ),

        "large_text": bool(
            st.session_state.get(
                "large_text",
                False,
            )
        ),

        "high_contrast": bool(
            st.session_state.get(
                "high_contrast",
                False,
            )
        ),

        "dyslexia_friendly": bool(
            st.session_state.get(
                "dyslexia_friendly",
                False,
            )
        ),
    }


# ============================================================
# GET LEARNING PREFERENCES
# ============================================================

def get_learning_preferences():
    """
    Return all learning preferences currently
    loaded into the student's session.
    """

    return {

        "simple_explanation": bool(
            st.session_state.get(
                "simple_explanation",
                True,
            )
        ),

        "step_by_step": bool(
            st.session_state.get(
                "step_by_step",
                True,
            )
        ),

        "repetition_support": bool(
            st.session_state.get(
                "repetition_support",
                False,
            )
        ),

        "visual_explanation": bool(
            st.session_state.get(
                "visual_explanation",
                True,
            )
        ),

        "preferred_language": (
            st.session_state.get(
                "preferred_language",
                "English",
            )
        ),
    }


# ============================================================
# LOGOUT
# ============================================================

def logout_user():
    """
    Completely clear the current student's session.
    """

    # --------------------------------------------------------
    # AUTHENTICATION
    # --------------------------------------------------------

    st.session_state["logged_in"] = False

    st.session_state["user"] = None

    st.session_state["user_id"] = None

    st.session_state["user_name"] = None

    st.session_state["disability_type"] = None

    # --------------------------------------------------------
    # LANGUAGE
    # --------------------------------------------------------

    st.session_state["preferred_language"] = (
        "English"
    )

    # --------------------------------------------------------
    # LEARNING PREFERENCES
    # --------------------------------------------------------

    st.session_state["simple_explanation"] = True

    st.session_state["step_by_step"] = True

    st.session_state["repetition_support"] = False

    st.session_state["visual_explanation"] = True

    # --------------------------------------------------------
    # ACCESSIBILITY
    # --------------------------------------------------------

    st.session_state["text_to_speech"] = False

    st.session_state["speech_to_text"] = False

    st.session_state["large_text"] = False

    st.session_state["high_contrast"] = False

    st.session_state["dyslexia_friendly"] = False

    # --------------------------------------------------------
    # AI TUTOR
    # --------------------------------------------------------

    st.session_state["chat_history"] = []

    st.session_state["conversation_history"] = []

    st.session_state["tutor_question"] = ""

    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    st.session_state["selected_page"] = "Dashboard"


# ============================================================
# CLEAR SESSION
# ============================================================

def clear_session():
    """
    Compatibility alias for logout_user().
    """

    logout_user()
