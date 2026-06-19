from backend.chatbot.chatbot import responder_stream
from backend.agent.ripley_agent import agent_stream

from backend.security import (
    validate_input,
    sanitize_input,
    rate_limit
)


def route_request(user_input, mode="agent"):

    user_id = "streamlit_user"

    # =========================
    # RATE LIMIT
    # =========================
    if not rate_limit(user_id):
        return iter([
            "Demasiadas solicitudes. Intenta nuevamente en unos minutos."
        ])

    # =========================
    # VALIDACIÓN
    # =========================
    valid, msg = validate_input(user_input)

    if not valid:
        return iter([msg])

    # =========================
    # SANITIZACIÓN
    # =========================
    user_input = sanitize_input(user_input)

    # =========================
    # ROUTING
    # =========================
    if mode == "agent":
        return agent_stream(user_input)

    return responder_stream(user_input)