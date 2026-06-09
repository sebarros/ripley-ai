import streamlit as st
from backend.router import route_request

st.title("💬 Ripley Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

msg = st.chat_input("Escribe tu consulta")

if msg:

    st.session_state.messages.append({"role": "user", "content": msg})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        for chunk in route_request(msg):
            full_response = chunk
            placeholder.markdown(full_response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })