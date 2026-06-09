from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv
import os
import time

from backend.observability.logger import log_interaction

load_dotenv()

# =========================
# LLM
# =========================
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("GITHUB_TOKEN"),
    model="gpt-4.1",
    temperature=0.3,
    max_tokens=250,
    streaming=True
)

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


# =========================
# STREAMING RESPONSE
# =========================
def responder_stream(user_input, session_id="streamlit_user"):

    history = get_session_history(session_id)

    messages = [
        SystemMessage(content="Eres un asistente de atención al cliente de Ripley Chile."),
        *history.messages,
        HumanMessage(content=user_input)
    ]

    full_response = ""

    for chunk in llm.stream(messages):
        if chunk.content:
            full_response += chunk.content
            yield full_response

    history.add_user_message(user_input)
    history.add_ai_message(full_response)