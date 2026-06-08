from backend.chatbot.chatbot import responder as chatbot_responder
from backend.agent.ripley_agent import run_agent


def route_request(user_input, session_id="default"):
    """
    Decide si usar chatbot o agente
    """

    # regla simple (puedes mejorar después)
    agent_keywords = ["comprar", "buscar producto", "recomendar", "cotizar"]

    if any(word in user_input.lower() for word in agent_keywords):
        return run_agent(user_input)

    return chatbot_responder(user_input, session_id)