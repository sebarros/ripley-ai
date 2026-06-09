import os
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime


# =========================
# ENVIO DE EMAIL
# =========================
def enviar_promocion(asunto: str, cuerpo_html: str, destinatario: str = None):

    remitente = os.getenv("EMAIL_FROM", "ripley.bot@gmail.com")
    password = os.getenv("EMAIL_PASSWORD", "")
    destino_default = os.getenv("EMAIL_TO", "cliente@correo.com")
    destino = destinatario or destino_default

    if not password:
        return "[!] EMAIL_PASSWORD no configurado en .env"

    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = destino

    msg.set_content("Tu cliente de correo no soporta HTML.")
    msg.add_alternative(cuerpo_html, subtype="html")

    try:
        context = ssl.create_default_context()

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(remitente, password)
            server.send_message(msg)

        return f"[OK] Promoción enviada a {destino}"

    except Exception as e:
        return f"[!] Error enviando correo: {e}"


# =========================
# GENERADOR HTML
# =========================
def generar_email_ripley(cliente: str, clima: dict = None, productos: list = None):

    ahora = datetime.now().strftime("%d/%m/%Y %H:%M")

    clima_html = ""
    if clima:
        clima_html = f"""
        <div style="background:#e3f2fd;padding:15px;border-radius:10px;margin-bottom:20px;">
            <h3>🌤️ Clima</h3>
            <p>{clima.get('city')} → {clima.get('temperature')}°C | viento {clima.get('windspeed')} km/h</p>
        </div>
        """

    productos_html = ""
    if productos:
        cards = ""
        for p in productos[:5]:
            cards += f"""
            <div style="border:1px solid #eee;padding:10px;margin:10px 0;">
                <b>{p.get('title')}</b><br>
                ${p.get('price')}
            </div>
            """

        productos_html = f"""
        <h3>🛍️ Productos</h3>
        {cards}
        """

    return f"""
    <html>
    <body style="font-family:Arial">

        <h2>Hola {cliente}</h2>
        <p>{ahora}</p>

        {clima_html}

        {productos_html}

        <br><br>
        <a href="https://www.ripley.cl">Ver ofertas</a>

    </body>
    </html>
    """