import streamlit as st
from backend.router import route_request

st.title("🤖 Agente Inteligente Ripley")

if "agent" not in st.session_state:
    st.session_state.agent = []

for m in st.session_state.agent:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

msg = st.chat_input("Ej: envía un correo, busca producto, etc.")

if msg:

    st.session_state.agent.append({"role": "user", "content": msg})

    with st.chat_message("assistant"):

        result = route_request(msg)
        response = result.get("respuesta", str(result))

        st.markdown(response)

    st.session_state.agent.append({"role": "assistant", "content": response})