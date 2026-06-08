import streamlit as st

st.set_page_config(
    page_title="Ripley AI Platform",
    page_icon="🧠",
    layout="wide"
)

# ===== SIDEBAR =====
st.sidebar.title("🧠 Ripley AI")

page = st.sidebar.radio(
    "Navegación",
    ["💬 Chatbot", "🤖 Agente", "📊 Observabilidad", "ℹ️ Info"]
)

st.markdown("# Ripley AI Platform")
st.markdown("Sistema interno de asistencia inteligente")

st.markdown("---")

st.markdown("Selecciona una sección en la barra lateral 👈")

# routing manual simple
st.session_state.page = page