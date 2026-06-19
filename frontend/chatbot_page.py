import streamlit as st
from backend.router import route_request
from chat_utils import render_chat, stream_response, render_welcome_screen, use_inline_chat_input
from email_page import render_email_button


SUGERENCIAS = [
    "¿Cómo devuelvo un producto?",
    "¿Cuál es la garantía?",
    "¿Cómo reviso mi pedido?",
    "Necesito contactar soporte",
]


def _render_header():
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


def render():

    if "messages" not in st.session_state:
        st.session_state.messages = []

    had_history = bool(st.session_state.messages)
    msg_chip = None

    if had_history:
        _render_header()
    else:
        use_inline_chat_input()
        render_welcome_screen(
            title="💬 ¿En qué puedo ayudarte?",
            subtitle="Resuelvo tus dudas sobre compras, garantías y despachos."
        )
        st.markdown(
            '<p class="welcome-pill-label">✨ Consultas frecuentes</p>',
            unsafe_allow_html=True
        )
        cols = st.columns(len(SUGERENCIAS))
        for i, sug in enumerate(SUGERENCIAS):
            with cols[i]:
                if st.button(sug, key=f"chip_{i}", use_container_width=True):
                    msg_chip = sug

    msg_typed = st.chat_input("Escribe tu consulta a Ripley...")

    msg = msg_chip or msg_typed

    if msg:
        st.session_state.messages.append({"role": "user", "content": msg})
        if not had_history:
            _render_header()

    # Se pinta el historial UNA sola vez, ya con el mensaje nuevo incluido
    # (si lo hay), para que el burbuja del usuario aparezca de inmediato
    # y no recién cuando el asistente termine de responder.
    if st.session_state.messages:
        render_chat(st.session_state.messages)

    if msg:
        full_response = stream_response(
            route_request(msg, mode="chatbot"),
            delay=0.012
        )
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.rerun()

    # ── Email ────────────────────────────────────────────────
    if st.session_state.messages:
        st.markdown("<br>", unsafe_allow_html=True)
        render_email_button(
            messages   = st.session_state.messages,
            modo       = "chatbot",
            key_prefix = "chatbot"
        )