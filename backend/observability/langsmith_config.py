import os
from langsmith import Client

def setup_langsmith():
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "ripley-chatbot"

    if not os.getenv("LANGCHAIN_API_KEY"):
        print("⚠️ Falta LANGCHAIN_API_KEY")

    return Client()