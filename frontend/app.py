import streamlit as st
from streamlit_option_menu import option_menu

from chatbot_page import render as chatbot_page
from agent_page import render as agent_page
from dashboard_page import render as dashboard_page

st.set_page_config(
    page_title="Ripley AI Platform",
    page_icon="🧠",
    layout="wide"
)

selected = option_menu(
    menu_title=None,
    options=[
        "Inicio",
        "Asistente Virtual",
        "Agente Inteligente",
        "Monitoreo"
    ],
    icons=[
        "house",
        "chat-dots",
        "robot",
        "bar-chart"
    ],
    orientation="horizontal"
)

# =========================
# HOME
# =========================
if selected == "Inicio":

    st.title("🧠 Ripley AI Platform")

    st.markdown("""
### Plataforma Inteligente de Asistencia

Sistema basado en Inteligencia Artificial para consultas,
automatización de atención, búsqueda de productos y observabilidad.
""")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("""
### 💬 Asistente Virtual
- Garantías
- Compras
- Despachos
- Devoluciones
""")

    with col2:
        st.success("""
### 🤖 Agente Inteligente
- Clima
- Productos
- Memoria
- Herramientas
""")

    with col3:
        st.warning("""
### 📊 Centro de Monitoreo
- Logs
- Latencia
- Errores
- Métricas
""")

    st.markdown("---")

    st.subheader("🚀 Pruebas sugeridas")

    col1, col2 = st.columns(2)

    with col1:
        st.code("""
¿Cómo devuelvo un producto?
¿Cuál es la garantía?
¿Cómo reviso mi pedido?
""")

    with col2:
        st.code("""
¿Cuál es el clima en Puerto Montt?
Lista los productos disponibles
¿Cuál es mi nombre?
""")

elif selected == "Asistente Virtual":
    chatbot_page()

elif selected == "Agente Inteligente":
    agent_page()

elif selected == "Monitoreo":
    dashboard_page()