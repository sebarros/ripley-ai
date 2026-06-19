"""
email_page.py — Panel de envío de correos desde el chat
"""
import streamlit as st
from email_sender import enviar_email, generar_email_reporte, generar_email_promocion


def render_email_button(messages: list, modo: str = "chatbot", key_prefix: str = "email"):
    """
    Muestra un botón 'Enviar por correo' con un formulario emergente (expander).
    Se llama desde chatbot_page o agent_page cuando hay mensajes.
    """
    if not messages:
        return

    with st.expander("📧 Enviar conversación por correo", expanded=False):
        st.markdown("""
        <p style="font-size:13px;color:#6B7280;margin:0 0 12px;">
            Recibe el resumen de esta conversación directo en tu correo.
        </p>
        """, unsafe_allow_html=True)

        col_name, col_email = st.columns(2)

        with col_name:
            nombre = st.text_input(
                "Tu nombre",
                placeholder="Ej: Sebastián",
                key=f"{key_prefix}_nombre"
            )

        with col_email:
            correo = st.text_input(
                "Tu correo",
                placeholder="ejemplo@gmail.com",
                key=f"{key_prefix}_correo"
            )

        if modo == "agent":
            tipo = st.radio(
                "Tipo de reporte",
                ["📋 Resumen de conversación", "🛍️ Promoción con productos/clima"],
                horizontal=True,
                key=f"{key_prefix}_tipo"
            )
        else:
            tipo = "📋 Resumen de conversación"

        if st.button("📤 Enviar correo", key=f"{key_prefix}_send", use_container_width=False):
            if not nombre.strip():
                st.warning("Por favor ingresa tu nombre.")
                return
            if not correo.strip() or "@" not in correo:
                st.warning("Por favor ingresa un correo válido.")
                return

            with st.spinner("Enviando..."):
                if "Resumen" in tipo:
                    html = generar_email_reporte(
                        cliente  = nombre,
                        mensajes = messages,
                        modo     = modo
                    )
                    asunto = f"Tu conversación con Ripley AI — {nombre}"
                else:
                    # Extraer clima y productos del session_state si existen
                    clima     = st.session_state.get("ultimo_clima", None)
                    productos = st.session_state.get("ultimos_productos", None)

                    if not clima and not productos:
                        st.warning(
                            "Aún no tengo datos de clima ni productos en esta sesión. "
                            "Pídele primero al Agente algo como '¿cuál es el clima en Puerto Montt?' "
                            "o 'lista los productos disponibles' y luego intenta enviar este correo."
                        )
                        return

                    html = generar_email_promocion(
                        cliente   = nombre,
                        clima     = clima,
                        productos = productos
                    )
                    asunto = f"Recomendaciones personalizadas de Ripley para {nombre}"

                resultado = enviar_email(asunto, html, correo)

            if resultado["ok"]:
                st.success(f"✅ {resultado['mensaje']}")
            else:
                st.error(f"❌ {resultado['mensaje']}")