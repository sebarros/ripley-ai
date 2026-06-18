import streamlit as st
from backend.router import route_request


def render():

    st.title("🤖 Agente Inteligente")

    if "agent" not in st.session_state:
        st.session_state.agent = []

    # =========================
    # HISTORIAL
    # =========================
    for m in st.session_state.agent:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # =========================
    # INPUT
    # =========================
    msg = st.chat_input("Ej: clima en Puerto Montt, lista productos...")

    if msg:

        with st.chat_message("user"):
            st.markdown(msg)

        st.session_state.agent.append({
            "role": "user",
            "content": msg
        })

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""

            for chunk in route_request(msg, mode="agent"):
                full_response = chunk
                placeholder.markdown(full_response)

        st.session_state.agent.append({
            "role": "assistant",
            "content": full_response
        })

        st.rerun()