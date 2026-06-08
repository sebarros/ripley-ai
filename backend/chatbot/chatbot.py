from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

import os
import time

from backend.observability.logger import log_interaction

# =========================
# CONFIGURACION MODELO
# =========================

llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("GITHUB_TOKEN"),
    model="gpt-4.1",
    temperature=0.3,
    max_tokens=250
)

# =========================
# MEMORIA
# =========================

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# =========================
# BASE DE CONOCIMIENTO
# =========================

documents = [
    "Las devoluciones en Ripley se pueden realizar dentro de 10 días con boleta y producto en buen estado.",
    "Los despachos demoran entre 2 y 5 días hábiles dependiendo de la región.",
    "Las compras online pueden ser retiradas en tienda sin costo adicional.",
    "Los productos cuentan con garantía legal de 6 meses.",
    "Puedes pagar con tarjeta Ripley, tarjetas de crédito y débito.",
    "Para seguimiento de pedidos debes ingresar a tu cuenta en ripley.cl.",
    "Los cambios de productos están sujetos a disponibilidad de stock."
]

# =========================
# CHUNKING
# =========================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=20
)

chunks = []
for doc in documents:
    chunks.extend(text_splitter.split_text(doc))

# =========================
# EMBEDDINGS
# =========================

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=os.getenv("GITHUB_TOKEN"),
    openai_api_base=os.getenv("OPENAI_BASE_URL")
)

vector_db = FAISS.from_texts(
    texts=chunks,
    embedding=embeddings
)

retriever = vector_db.as_retriever(
    search_kwargs={"k": 3}
)

# =========================
# CLASIFICADOR INTENCION
# =========================

def clasificar_intencion(mensaje):

    prompt = f"""
Clasifica la intención del usuario en UNA sola palabra:

- compra
- reclamo
- seguimiento
- informacion

Mensaje: {mensaje}

Respuesta:
"""

    try:
        respuesta = llm.invoke(
            [HumanMessage(content=prompt)]
        ).content

        return respuesta.strip().lower()

    except:
        return "informacion"

# =========================
# META PROMPTING
# =========================

def obtener_system_prompt(intencion):

    if "reclamo" in intencion:
        return (
            "Eres un asistente de atención al cliente de Ripley Chile. "
            "Responde con empatía y soluciones claras."
        )

    elif "compra" in intencion:
        return (
            "Eres un asistente de ventas de Ripley Chile. "
            "Ayuda a recomendar productos."
        )

    elif "seguimiento" in intencion:
        return (
            "Eres un asistente de seguimiento de pedidos de Ripley Chile."
        )

    else:
        return (
            "Eres un asistente virtual de atención al cliente de Ripley Chile."
        )

# =========================
# FUNCION PRINCIPAL (CON OBSERVABILIDAD)
# =========================

def responder(user_input, session_id="streamlit_user"):

    start_time = time.time()
    error = False
    response = ""
    intencion = "unknown"

    try:

        # =========================
        # MEMORIA
        # =========================
        history = get_session_history(session_id)

        # =========================
        # INTENCION
        # =========================
        intencion = clasificar_intencion(user_input)

        # =========================
        # RAG
        # =========================
        relevant_docs = retriever.invoke(user_input)

        if relevant_docs:
            context = "\n".join([doc.page_content for doc in relevant_docs])
        else:
            context = "No hay información relevante."

        # =========================
        # PROMPT FINAL
        # =========================
        system_prompt = obtener_system_prompt(intencion)

        rag_prompt = f"""
Contexto:
{context}

Historial:
{history.messages}

Pregunta:
{user_input}

Instrucciones:
- Usa el contexto si es útil
- Usa el historial si es necesario
- Si no sabes, dilo claramente
"""

        messages = [
            SystemMessage(content=system_prompt)
        ] + history.messages + [
            HumanMessage(content=rag_prompt)
        ]

        # =========================
        # LLM RESPONSE
        # =========================
        response = llm.invoke(messages).content

        # =========================
        # MEMORIA
        # =========================
        history.add_user_message(user_input)
        history.add_ai_message(response)

    except Exception as e:
        error = True
        response = f"Error: {str(e)}"

    # =========================
    # LATENCIA
    # =========================
    end_time = time.time()
    latency = round(end_time - start_time, 3)

    # =========================
    # LOG (OBSERVABILIDAD)
    # =========================
    log_interaction(
        tipo="chatbot",
        pregunta=user_input,
        respuesta=response,
        intencion=intencion,
        latencia=latency
    )

    # =========================
    # OUTPUT
    # =========================
    return {
        "respuesta": response,
        "intencion": intencion,
        "latencia": latency,
        "error": error
    }