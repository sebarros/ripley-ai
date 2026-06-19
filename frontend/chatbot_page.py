import streamlit as st
from backend.router import route_request
from chat_utils import render_chat, stream_response


SUGERENCIAS = [
    "¿Cómo devuelvo un producto?",
    "¿Cuál es la garantía?",
    "¿Cómo reviso mi pedido?",
    "Necesito contactar soporte",
]


def render():

    col_title, col_badge = st.columns([6, 1])
    with col_title:
        st.markdown("""
        <h1 style="margin-bottom:2px;">💬 Asistente Virtual</h1>
        <p style="font-size:14px; margin-top:0;">
            Resuelve tus dudas sobre compras, garantías y despachos.
        </p>
        """, unsafe_allow_html=True)
    with col_badge:
        st.markdown("""
        <div style="text-align:right; padding-top:14px;">
            <span class="badge badge-online">● En línea</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    msg_chip = None
    if not st.session_state.messages:
        st.markdown('<p style="font-size:13px;color:#9333EA;font-weight:600;margin-bottom:6px;">✨ Consultas frecuentes</p>', unsafe_allow_html=True)
        cols = st.columns(len(SUGERENCIAS))
        for i, sug in enumerate(SUGERENCIAS):
            with cols[i]:
                if st.button(sug, key=f"chip_{i}", use_container_width=True):
                    msg_chip = sug
        st.markdown("<br>", unsafe_allow_html=True)

    msg_typed = st.chat_input("Escribe tu consulta a Ripley...")

    msg = msg_chip or msg_typed

    if msg:
        st.session_state.messages.append({"role": "user", "content": msg})

    render_chat(st.session_state.messages)

    if msg:
        full_response = stream_response(
            route_request(msg, mode="chatbot"),
            delay=0.012
        )
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.rerun()