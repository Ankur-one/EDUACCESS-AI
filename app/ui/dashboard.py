from importlib import import_module

from app.auth.session import logout_user


# Load Streamlit dynamically so static analyzers do not report an unresolved
# import when the optional UI dependency is not installed in their environment.
st = import_module("streamlit")


def show_dashboard():

    st.title("🎓 EduAccess AI Dashboard")

    st.write(
        f"Welcome, **{st.session_state.user_name}** 👋"
    )

    st.divider()

    # ========================================================
    # Quick Navigation
    # ========================================================

    st.subheader("📚 Your Learning Space")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            "📖\n\n"
            "**AI Study Assistant**\n\n"
            "Ask questions and learn with AI."
        )

    with col2:
        st.info(
            "🎤\n\n"
            "**Voice Study**\n\n"
            "Learn using speech and audio."
        )

    with col3:
        st.info(
            "📄\n\n"
            "**Study Documents**\n\n"
            "Upload and learn from your notes."
        )

    st.divider()

    # ========================================================
    # Accessibility
    # ========================================================

    st.subheader("♿ Accessibility Support")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.success("🔊 Text-to-Speech")

    with col2:
        st.success("🎤 Speech-to-Text")

    with col3:
        st.success("📝 Captions")

    with col4:
        st.success("🔎 Large Text")

    st.divider()

    # ========================================================
    # Progress
    # ========================================================

    st.subheader("📊 Learning Progress")

    progress = 0

    st.progress(progress)

    st.write(
        f"Overall Progress: {progress}%"
    )

    st.divider()

    # ========================================================
    # Logout
    # ========================================================

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout_user()

        st.success("You have been logged out.")

        st.rerun()