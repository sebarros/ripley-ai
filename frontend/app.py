import streamlit as st
from streamlit_option_menu import option_menu
import os

from chatbot_page import render as chatbot_page
from agent_page import render as agent_page
from dashboard_page import render as dashboard_page

st.set_page_config(
    page_title="Ripley AI Platform",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_css(path: str):
    with open(path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css(os.path.join(os.path.dirname(__file__), "styles.css"))

is_dark = st.get_option("theme.base") == "dark"

st.markdown(
    f"<script>document.documentElement.setAttribute('data-theme', '{'dark' if is_dark else 'light'}');</script>",
    unsafe_allow_html=True,
)

# JS para fijar el navbar al hacer scroll
st.markdown("""
<script>
(function() {
    function fixNav() {
        var nav = document.querySelector('[data-testid="stAppViewContainer"] > section > div:first-child');
        if (nav) {
            nav.style.position = 'sticky';
            nav.style.top = '0';
            nav.style.zIndex = '9999';
            nav.style.backdropFilter = 'blur(12px)';
            nav.style.webkitBackdropFilter = 'blur(12px)';
        }
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fixNav);
    } else {
        fixNav();
    }
    setTimeout(fixNav, 800);
})();
</script>
""", unsafe_allow_html=True)

nav_bg   = "#1A1230" if is_dark else "#FFFFFF"
nav_text = "#C084FC" if is_dark else "#6B7280"
nav_icon = "#C084FC" if is_dark else "#9333EA"

selected = option_menu(
    menu_title=None,
    options=["Inicio", "Asistente Virtual", "Agente Inteligente", "Monitoreo"],
    icons=["house-fill", "chat-dots-fill", "robot", "bar-chart-fill"],
    orientation="horizontal",
    default_index=0,
    styles={
        "container": {
            "padding": "8px",
            "background-color": nav_bg,
            "border-radius": "16px",
            "border": "1px solid rgba(107,33,168,0.18)",
            "box-shadow": "0 2px 10px rgba(107,33,168,0.10)",
            "margin-bottom": "1.5rem",
        },
        "icon":         {"color": nav_icon, "font-size": "18px"},
        "nav-link":     {"font-size": "16px", "font-weight": "500",
                         "color": nav_text, "border-radius": "12px", "padding": "11px 26px"},
        "nav-link-selected": {"background-color": "#6B21A8", "color": "white", "font-weight": "700"},
    },
)

if selected == "Inicio":

    st.markdown("""
    <div class="hero-banner">
        <h1>🛍️ Ripley AI Platform</h1>
        <p>Plataforma de Inteligencia Artificial para atención al cliente,
        automatización de consultas y monitoreo operacional en tiempo real.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">💬</span>
            <h3>Asistente Virtual</h3>
            <ul>
                <li>Consultas de garantías</li>
                <li>Estado de compras</li>
                <li>Seguimiento de despachos</li>
                <li>Gestión de devoluciones</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🤖</span>
            <h3>Agente Inteligente</h3>
            <ul>
                <li>Consulta del clima</li>
                <li>Búsqueda de productos</li>
                <li>Memoria de sesión</li>
                <li>Herramientas integradas</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">📊</span>
            <h3>Centro de Monitoreo</h3>
            <ul>
                <li>Logs en tiempo real</li>
                <li>Latencia del sistema</li>
                <li>Tasa de errores</li>
                <li>Métricas de uso</li>
            </ul>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💡 Pruebas sugeridas")

    col_a, col_b = st.columns(2, gap="medium")
    with col_a:
        st.markdown("""
        <div class="suggestion-block">
            <p style="font-size:13px; font-weight:600; color:#9333EA; margin-bottom:8px;">💬 Asistente Virtual</p>
            <code>¿Cómo devuelvo un producto?</code><br>
            <code>¿Cuál es la garantía de mi TV?</code><br>
            <code>¿Cómo reviso el estado de mi pedido?</code>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="suggestion-block">
            <p style="font-size:13px; font-weight:600; color:#9333EA; margin-bottom:8px;">🤖 Agente Inteligente</p>
            <code>¿Cuál es el clima en Puerto Montt?</code><br>
            <code>Lista los productos disponibles</code><br>
            <code>¿Cuál es mi nombre?</code>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🟢 Estado del sistema")

    s1, s2, s3, s4 = st.columns(4)
    for col, label in zip([s1, s2, s3], ["Asistente Virtual", "Agente Inteligente", "Sistema de Logs"]):
        with col:
            st.markdown(f"""
            <div class="ripley-card" style="text-align:center;">
                <div class="badge badge-online" style="margin:0 auto 6px;">● Operativo</div>
                <p style="font-size:12px; margin:0;">{label}</p>
            </div>""", unsafe_allow_html=True)
    with s4:
        st.markdown("""
        <div class="ripley-card" style="text-align:center;">
            <div class="badge badge-purple" style="margin:0 auto 6px;">🛍️ Ripley AI</div>
            <p style="font-size:12px; margin:0;">v1.0.0</p>
        </div>""", unsafe_allow_html=True)

elif selected == "Asistente Virtual":
    chatbot_page()

elif selected == "Agente Inteligente":
    agent_page()

elif selected == "Monitoreo":
    dashboard_page()