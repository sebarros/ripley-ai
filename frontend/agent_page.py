import streamlit as st
from backend.router import route_request
from chat_utils import render_chat, stream_response, render_welcome_screen, use_inline_chat_input
from email_page import render_email_button


SUGERENCIAS_AGENTE = [
    "¿Cuál es el clima en Puerto Montt?",
    "Lista los productos disponibles",
    "¿Cuál es mi nombre?",
    "Busca laptops en el catálogo",
]


def _render_header():
    col_title, col_badge = st.columns([6, 1])
    with col_title:
        st.markdown("""
        <h1 style="margin-bottom:2px;">🤖 Agente Inteligente</h1>
        <p style="font-size:14px; margin-top:0;">
            Accede a herramientas, clima, productos y más con IA avanzada.
        </p>
        """, unsafe_allow_html=True)
    with col_badge:
        st.markdown("""
        <div style="text-align:right; padding-top:14px;">
            <span class="badge badge-purple">🧠 Agente</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    with st.expander("🔧 ¿Qué puede hacer este agente?", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
            <div class="ripley-card ripley-card-accent">
                <strong style="color:#9333EA;">🌤️ Clima</strong><br>
                <span style="font-size:13px;">Consulta el tiempo en cualquier ciudad.</span>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class="ripley-card ripley-card-accent">
                <strong style="color:#9333EA;">🛍️ Productos</strong><br>
                <span style="font-size:13px;">Busca en el catálogo de Ripley.</span>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown("""
            <div class="ripley-card ripley-card-accent">
                <strong style="color:#9333EA;">🧠 Memoria</strong><br>
                <span style="font-size:13px;">Recuerda el contexto de la sesión.</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


def render():

    if "agent" not in st.session_state:
        st.session_state.agent = []

    had_history = bool(st.session_state.agent)
    msg_chip = None

    if had_history:
        _render_header()
    else:
        use_inline_chat_input()
        render_welcome_screen(
            title="🤖 ¿En qué puedo ayudarte hoy?",
            subtitle="Pregúntame por el clima, busca productos en el catálogo o solo conversemos."
        )
        st.markdown(
            '<p class="welcome-pill-label">✨ Prueba el agente</p>',
            unsafe_allow_html=True
        )
        cols = st.columns(len(SUGERENCIAS_AGENTE))
        for i, sug in enumerate(SUGERENCIAS_AGENTE):
            with cols[i]:
                if st.button(sug, key=f"agent_chip_{i}", use_container_width=True):
                    msg_chip = sug

    msg_typed = st.chat_input("Ej: clima en Puerto Montt, lista productos...")

    msg = msg_chip or msg_typed

    if msg:
        st.session_state.agent.append({"role": "user", "content": msg})
        if not had_history:
            _render_header()

    # Se pinta el historial UNA sola vez, ya con el mensaje nuevo incluido
    # (si lo hay), para que la burbuja del usuario aparezca de inmediato
    # y no recién cuando el agente termine de responder.
    if st.session_state.agent:
        render_chat(st.session_state.agent)

    if msg:
        full_response = stream_response(
            route_request(msg, mode="agent"),
            delay=0.012
        )
        st.session_state.agent.append({"role": "assistant", "content": full_response})
        st.rerun()

    # ── Email ────────────────────────────────────────────────
    if st.session_state.agent:
        st.markdown("<br>", unsafe_allow_html=True)
        render_email_button(
            messages   = st.session_state.agent,
            modo       = "agent",
            key_prefix = "agent"
        )