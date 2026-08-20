import streamlit as st  # type: ignore

from app.auth.session import initialize_session
from app.ui.register import show_register


st.set_page_config(
    page_title="EduAccess AI",
    page_icon="♿",
    layout="wide"
)


initialize_session()


st.title("♿ EduAccess AI")

st.subheader(
    "AI-Powered Inclusive Learning Assistant"
)


show_register()