from backend.chatbot.chatbot import responder_stream
from backend.agent.ripley_agent import agent_stream

def route_request(user_input, mode="chatbot"):

    if mode == "agent":
        return agent_stream(user_input)

    return responder_stream(user_input)