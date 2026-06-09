from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import json

from backend.agent.planner import Planner
from backend.agent.tools import TOOL_MAP
from backend.agent.memory import MemoryManager

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=os.getenv("GITHUB_TOKEN"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    temperature=0.2,
    streaming=True 
)

planner = Planner()
memory = MemoryManager()


def run_tool(tool_name, input_text):
    tool = TOOL_MAP.get(tool_name)
    if not tool:
        return None
    return tool.func(input_text)


# =========================
# STREAMING AGENT
# =========================
def agent_stream(user_input: str):

    semantic_context = memory.retrieve_semantic(user_input)
    profile = memory.get_profile()

    plan = planner.create_plan(user_input)
    tool_name = plan.get("tool")

    tool_result = None

    if tool_name == "search_product":
        tool_result = run_tool("search_product", user_input)

    elif tool_name == "weather":
        tool_result = run_tool("weather", user_input)

    prompt = f"""
Eres un asistente de compras de Ripley Chile.

CONTEXTO:
{semantic_context}

PERFIL:
{json.dumps(profile, ensure_ascii=False)}

TOOL RESULT:
{tool_result}

USUARIO:
{user_input}
"""

    full_response = ""

    for chunk in llm.stream(prompt):
        if chunk.content:
            full_response += chunk.content
            yield full_response

    memory.store_response(full_response)