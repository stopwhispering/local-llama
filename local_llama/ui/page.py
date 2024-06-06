import streamlit as st


def set_page_header():
    st.set_page_config(
        page_title="Local Llama",
        page_icon="🦙",
    )
    st.title("Local Llama")
    st.markdown(
        "##### 🦙 built using [Streamlit](https://streamlit.io/) and "
        "[Ollama](https://github.com/ollama/ollama-python)"
    )
