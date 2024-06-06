import logging

import pyperclip
import streamlit as st
import json

from local_llama.assistant import Assistant
from local_llama.entities import Message
from local_llama.history import get_conversations, get_previous_conversation
from local_llama.ui.page import set_page_header
from local_llama.ui.sidebar import get_sidebar_settings
from local_llama.util import CustomEncoder

logger = logging.getLogger(__name__)


def display_current_settings(assistant: Assistant):
    st.caption(f"UUID: {assistant.uuid}")
    st.caption(f"Model: {assistant.llm.model_id}")
    st.caption(f"Temperature: {assistant.temperature}")


def main():
    set_page_header()

    (
        new_model_name,
        new_temperature,
        new_system_instructions,
        create_new_conversation,
        selected_conversation,
        open_saved_conversation,
    ) = get_sidebar_settings()

    # new conversation on user request
    if create_new_conversation:
        assistant = Assistant.create(
            system_instructions=new_system_instructions,
            model_name=new_model_name,
            temperature=new_temperature,
        )
        logger.info(f"Created new conversation: {assistant.uuid}")
        conversations = get_conversations()
        st.session_state["conversations"] = conversations

    # open saved conversation on user request
    elif open_saved_conversation:
        logger.info(f"Loading saved conversation: {selected_conversation}")
        assistant = Assistant.load(selected_conversation["uuid"])

    # existing conversation in session
    elif "assistant" in st.session_state:
        assistant: Assistant = st.session_state["assistant"]

    # load previous run upon opening the app
    elif conversation := get_previous_conversation():
        logger.info(f"Loading previous conversation: {conversation['uuid']}")
        assistant = Assistant.load(conversation["uuid"])

    # very first run of the app with no previous run
    else:
        assistant = Assistant.create(
            system_instructions=new_system_instructions,
            model_name=new_model_name,
            temperature=new_temperature,
        )
        logger.info(f"Created first conversation: {assistant.uuid}")
        conversations = get_conversations()
        st.session_state["conversations"] = conversations

    # in any case, store assistant in session to avoid reloading
    st.session_state["assistant"] = assistant

    # display header plus conversation details at the top
    display_current_settings(assistant)

    # if we have a new user prompt, add it to the conversation
    if prompt := st.chat_input():
        message = Message(role="user", content=prompt)
        assistant.add_message(message)

    # display all messages in the conversation
    for message in assistant.get_messages():
        with st.chat_message(
            name=message.role, avatar="⚖" if message.role == "system" else None
        ):
            # st.write(message.format_content())
            resp_container = st.empty()
            resp_container.markdown(message.format_content())

    # if we have a new prompt, generate response and display it (chunk by chunk)
    if prompt:
        # generate llm response and display each yielded chunk
        # start = time.time()
        with st.chat_message(name="assistant"):
            resp_container = st.empty()
            response = ""
            ollama_request = assistant.request_response()
            for chunk in ollama_request.generate():
                response += chunk  # type: ignore
                resp_container.markdown(response)
            resp_container.markdown(ollama_request.response.format_content())
            assistant.add_message(ollama_request.response)

    if st.button("Copy"):
        pyperclip.copy(
            json.dumps(assistant.get_messages(), indent=4, cls=CustomEncoder)
        )
        st.success("Chat copied to clipboard!")


if __name__ == "__main__":
    main()
