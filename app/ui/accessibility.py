import streamlit as st  # type: ignore[import-not-found]


# ============================================================
# APPLY ACCESSIBILITY STYLES
# ============================================================

def apply_accessibility_styles(user):
    """
    Apply accessibility settings without breaking
    Streamlit's existing theme.
    """

    if user is None:
        return

    # ========================================================
    # USER SETTINGS
    # ========================================================

    large_text = bool(
        getattr(
            user,
            "large_text",
            False,
        )
    )

    high_contrast = bool(
        getattr(
            user,
            "high_contrast",
            False,
        )
    )

    dyslexia_friendly = bool(
        getattr(
            user,
            "dyslexia_friendly",
            False,
        )
    )

    # ========================================================
    # CSS
    # ========================================================

    css = []

    # ========================================================
    # LARGE TEXT
    # ========================================================

    if large_text:

        css.append(
            """
            .main p,
            .main li,
            .main label {
                font-size: 1.12rem !important;
                line-height: 1.7 !important;
            }

            .main h1 {
                font-size: 2.35rem !important;
            }

            .main h2 {
                font-size: 1.95rem !important;
            }

            .main h3 {
                font-size: 1.55rem !important;
            }

            .main textarea {
                font-size: 1.1rem !important;
            }
            """
        )

    # ========================================================
    # HIGH CONTRAST
    # ========================================================

    if high_contrast:

        css.append(
            """
            /* High contrast accessibility mode */

            .main {
                filter: contrast(1.12);
            }

            .main input,
            .main textarea,
            .main select {
                border: 2px solid currentColor !important;
            }

            .main button {
                border: 2px solid currentColor !important;
            }

            .main a {
                text-decoration: underline !important;
                text-decoration-thickness: 2px !important;
            }

            .main [data-testid="stAlert"] {
                border: 2px solid currentColor !important;
            }
            """
        )

    # ========================================================
    # DYSLEXIA FRIENDLY
    # ========================================================

    if dyslexia_friendly:

        css.append(
            """
            .main p,
            .main li,
            .main label,
            .main textarea,
            .main input {
                letter-spacing: 0.035em !important;
                word-spacing: 0.08em !important;
                line-height: 1.8 !important;
            }
            """
        )

    # ========================================================
    # FOCUS VISIBILITY
    # ========================================================

    css.append(
        """
        /* Keyboard focus accessibility */

        .main button:focus-visible,
        .main input:focus-visible,
        .main textarea:focus-visible,
        .main select:focus-visible {
            outline: 3px solid #ff4b4b !important;
            outline-offset: 3px !important;
        }
        """
    )

    # ========================================================
    # APPLY
    # ========================================================

    if css:

        st.markdown(
            "<style>\n"
            + "\n".join(css)
            + "\n</style>",
            unsafe_allow_html=True,
        )
