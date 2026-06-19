import streamlit as st
from backend.router import route_request


def render():

    st.title("💬 Asistente Virtual")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # =========================
    # HISTORIAL
    # =========================
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # =========================
    # INPUT
    # =========================
    msg = st.chat_input("Escribe tu consulta")

    if msg:

        with st.chat_message("user"):
            st.markdown(msg)

        st.session_state.messages.append({
            "role": "user",
            "content": msg
        })

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""

            for chunk in route_request(msg, mode="chatbot"):
                full_response = chunk
                placeholder.markdown(full_response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })

        st.rerun()