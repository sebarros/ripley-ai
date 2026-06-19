import os
import csv
import re
from datetime import datetime

# =========================
# RUTA ÚNICA
# =========================

LOG_FILE = "data/logs/logs.csv"


# =========================
# ANONIMIZACIÓN
# =========================

def anonymize_text(text):

    if not text:
        return text

    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL]', text)
    text = re.sub(r'\b\d{8,11}\b', '[PHONE]', text)

    return text


# =========================
# INIT LOGS
# =========================

def init_logs():

    os.makedirs("data/logs", exist_ok=True)

    if not os.path.exists(LOG_FILE):

        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:

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

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([
            datetime.now().isoformat(),
            tipo,  # "agent" o "chatbot"
            pregunta,
            respuesta,
            intencion,
            round(latencia, 3),
            error
        ])