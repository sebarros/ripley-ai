import streamlit as st
from backend.chatbot.chatbot import responder

st.title("💬 Chatbot Ripley")

if "chatbot" not in st.session_state:
    st.session_state.chatbot = []

for m in st.session_state.chatbot:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

msg = st.chat_input("Escribe aquí...")

if msg:

    st.session_state.chatbot.append({"role": "user", "content": msg})

    with st.chat_message("user"):
        st.markdown(msg)

    with st.chat_message("assistant"):

        response = responder(msg)["respuesta"]
        st.markdown(response)

    st.session_state.chatbot.append({"role": "assistant", "content": response})