import streamlit as st

from local_llama import settings
from local_llama.history import get_conversations


def get_sidebar_settings() -> tuple[str, float, str, bool, dict, bool]:
    with st.sidebar.form(key="new_conversation_form"):
        model_name = st.selectbox(
            "Select Model",
            options=[m["model_name"] for m in settings.available_models],
        )

        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            key="current_temperature",
        )

        system_instructions = st.text_area(
            "System Instructions",
            (
                "You are an AI assistant designed to answer simple questions."
                "Please restrict your answer to the exact question asked."
            ),
            height=300,
        )

        create_new_conversation = st.form_submit_button("New Conversation")

    # get conversations list either from session or from disk
    if "conversations" not in st.session_state:
        conversations = get_conversations()
        st.session_state["conversations"] = conversations
    else:
        conversations = st.session_state["conversations"]

    with st.sidebar.form(key="open_conversation_form"):
        selected_conversation = st.selectbox(
            label="Assistant",
            options=conversations,
            index=0,
        )
        open_saved_conversation = st.form_submit_button("Open Conversation")

    return (
        model_name,
        temperature,
        system_instructions,
        create_new_conversation,
        selected_conversation,
        open_saved_conversation,
    )
