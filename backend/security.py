import re
import time
from collections import defaultdict

# =========================
# CONFIG
# =========================

MAX_INPUT_LENGTH = 1000
MAX_REQUESTS_PER_MINUTE = 20

# =========================
# RATE LIMIT
# =========================

user_requests = defaultdict(list)

def rate_limit(user_id: str):

    now = time.time()

    user_requests[user_id] = [
        t for t in user_requests[user_id]
        if now - t < 60
    ]

    if len(user_requests[user_id]) >= MAX_REQUESTS_PER_MINUTE:
        return False

    user_requests[user_id].append(now)
    return True


# =========================
# SANITIZE INPUT
# =========================

def sanitize_input(text: str):

    text = re.sub(r"<.*?>", "", text)

    text = text.replace("{", "")
    text = text.replace("}", "")

    return text.strip()


# =========================
# PROMPT INJECTION
# =========================

BLOCKED_PATTERNS = [

    "ignore previous instructions",
    "ignora todas las instrucciones",
    "ignora instrucciones",

    "system prompt",
    "prompt completo",

    "revela tus instrucciones",
    "show your instructions",

    "actua como",
    "actúa como",

    "eres chatgpt",
    "you are chatgpt",

    "developer message",
    "mensaje del desarrollador",

    "reveal system prompt",
    "show hidden prompt",

    "bypass",
    "jailbreak"
]

def detect_prompt_injection(text: str):

    text = text.lower()

    for pattern in BLOCKED_PATTERNS:
        if pattern in text:
            return True

    return False


# =========================
# VALIDATE INPUT
# =========================

def validate_input(text: str):

    if not text:
        return False, "Mensaje vacío."

    if len(text) > MAX_INPUT_LENGTH:
        return False, "El mensaje excede el límite permitido."

    if detect_prompt_injection(text):
        return False, "Solicitud bloqueada por razones de seguridad."

    return True, ""