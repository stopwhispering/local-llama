import streamlit as st

from local_llama import settings
from local_llama.history import get_conversations


def get_sidebar_settings() -> tuple[str, float, str, bool, str, bool]:
    # Inject custom CSS to set the width of the sidebar
    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
                width: 400px !important; # Set the width to your desired value
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    with st.sidebar.form(key="new_conversation_form"):
        st.caption("Model")
        selected_model = st.dataframe(  # no default selection possible
            settings.available_models,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
        )
        if len(selected_model["selection"]["rows"]) == 1:
            row_no = selected_model["selection"]["rows"][0]
            model_name = settings.available_models[row_no]["model"]
        else:
            model_name = None

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
        st.caption("Conversation")
        selected_conversation = st.dataframe(  # no default selection possible
            conversations,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
        )
        if len(selected_conversation["selection"]["rows"]) == 1:
            row_no = selected_conversation["selection"]["rows"][0]
            conversation_uuid = conversations[row_no]["uuid"]
        else:
            conversation_uuid = None

        open_saved_conversation = st.form_submit_button("Open Conversation")

    return (
        model_name,
        temperature,
        system_instructions,
        create_new_conversation,
        conversation_uuid,
        open_saved_conversation,
    )
