import importlib


st = importlib.import_module("streamlit")


def apply_accessibility_style():
    """
    Apply accessibility preferences to the Streamlit UI.
    """

    # Default values
    large_text = st.session_state.get(
        "large_text",
        False
    )

    high_contrast = st.session_state.get(
        "high_contrast",
        False
    )

    dyslexia_friendly = st.session_state.get(
        "dyslexia_friendly",
        False
    )

    # ========================================================
    # LARGE TEXT
    # ========================================================

    large_text_css = ""

    if large_text:
        large_text_css = """
        .stApp {
            font-size: 20px !important;
        }

        p {
            font-size: 20px !important;
        }

        label {
            font-size: 18px !important;
        }

        input,
        textarea,
        button {
            font-size: 18px !important;
        }

        h1 {
            font-size: 38px !important;
        }

        h2 {
            font-size: 32px !important;
        }

        h3 {
            font-size: 27px !important;
        }
        """

    # ========================================================
    # HIGH CONTRAST
    # ========================================================

    high_contrast_css = ""

    if high_contrast:
        high_contrast_css = """
        .stApp {
            background-color: #000000 !important;
            color: #FFFFFF !important;
        }

        .stApp p,
        .stApp label,
        .stApp span,
        .stApp h1,
        .stApp h2,
        .stApp h3 {
            color: #FFFFFF !important;
        }

        .stButton button {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border: 2px solid #FFFFFF !important;
        }

        input,
        textarea {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            border: 2px solid #FFFFFF !important;
        }
        """

    # ========================================================
    # DYSLEXIA-FRIENDLY FONT
    # ========================================================

    dyslexia_css = ""

    if dyslexia_friendly:
        dyslexia_css = """
        .stApp {
            font-family: Arial, sans-serif !important;
            letter-spacing: 0.04em !important;
            line-height: 1.7 !important;
        }

        p,
        label,
        span,
        input,
        textarea,
        button {
            letter-spacing: 0.04em !important;
            line-height: 1.6 !important;
        }
        """

    # ========================================================
    # APPLY CSS
    # ========================================================

    st.markdown(
        f"""
        <style>

        {large_text_css}

        {high_contrast_css}

        {dyslexia_css}

        </style>
        """,
        unsafe_allow_html=True,
    )