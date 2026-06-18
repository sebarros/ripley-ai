import os
import csv
import re
from datetime import datetime

# =========================
# RUTAS
# =========================

CHATBOT_LOG = "data/logs/chatbot_logs.csv"
AGENT_LOG = "data/logs/agent_logs.csv"


# =========================
# ANONIMIZACIÓN
# =========================

def anonymize_text(text):

    if not text:
        return text

    # Correos
    text = re.sub(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        '[EMAIL]',
        text
    )

    # Teléfonos (8-11 dígitos)
    text = re.sub(
        r'\b\d{8,11}\b',
        '[PHONE]',
        text
    )

    return text


# =========================
# INIT LOGS
# =========================

def init_logs():

    os.makedirs("data/logs", exist_ok=True)

    if not os.path.exists(CHATBOT_LOG):

        with open(CHATBOT_LOG, "w", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)

            writer.writerow([
                "timestamp",
                "tipo",
                "pregunta",
                "respuesta",
                "intencion",
                "latencia",
                "error"
            ])

    if not os.path.exists(AGENT_LOG):

        with open(AGENT_LOG, "w", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)

            writer.writerow([
                "timestamp",
                "tipo",
                "pregunta",
                "respuesta",
                "intencion",
                "latencia",
                "error"
            ])


# =========================
# LOG PRINCIPAL
# =========================

def log_interaction(
    tipo: str,
    pregunta: str,
    respuesta: str,
    intencion: str,
    latencia: float,
    error: bool = False
):

    init_logs()

    pregunta = anonymize_text(pregunta)
    respuesta = anonymize_text(respuesta)

    file_path = CHATBOT_LOG if tipo == "chatbot" else AGENT_LOG

    with open(file_path, "a", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([
            datetime.now().isoformat(),
            tipo,
            pregunta,
            respuesta,
            intencion,
            round(latencia, 3),
            error
        ])