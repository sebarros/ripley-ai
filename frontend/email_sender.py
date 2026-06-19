"""
email_sender.py — Ripley AI Platform
=====================================
Envío de reportes y promociones personalizadas vía SMTP (Gmail).
Soporta: resumen de conversación, clima + productos, y correo libre.
"""

import os
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime


# ══════════════════════════════════════════════════════
# CORE — ENVÍO SMTP
# ══════════════════════════════════════════════════════

def enviar_email(asunto: str, cuerpo_html: str, destinatario: str) -> dict:
    """
    Envía un correo HTML via Gmail SMTP.
    Retorna dict: { ok: bool, mensaje: str }
    """
    remitente = os.getenv("EMAIL_FROM", "")
    password  = os.getenv("EMAIL_PASSWORD", "")

    if not remitente or not password:
        return {
            "ok": False,
            "mensaje": "Faltan EMAIL_FROM o EMAIL_PASSWORD en el archivo .env"
        }

    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"]    = f"Ripley AI <{remitente}>"
    msg["To"]      = destinatario
    msg.set_content("Tu cliente de correo no soporta HTML.")
    msg.add_alternative(cuerpo_html, subtype="html")

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls(context=context)
            server.login(remitente, password)
            server.send_message(msg)
        return {"ok": True, "mensaje": f"Correo enviado a {destinatario}"}

    except smtplib.SMTPAuthenticationError:
        return {
            "ok": False,
            "mensaje": (
                "Error de autenticación Gmail. "
                "Asegúrate de usar una App Password: "
                "https://myaccount.google.com/security"
            )
        }
    except Exception as e:
        return {"ok": False, "mensaje": f"Error inesperado: {e}"}


# ══════════════════════════════════════════════════════
# PLANTILLA BASE HTML
# ══════════════════════════════════════════════════════

def _base_template(titulo: str, subtitulo: str, cuerpo: str) -> str:
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M")
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo}</title>
</head>
<body style="margin:0;padding:0;background:#F3F0FB;font-family:'Segoe UI',Arial,sans-serif;">
<div style="max-width:620px;margin:28px auto;background:#fff;border-radius:18px;overflow:hidden;
            box-shadow:0 6px 32px rgba(107,33,168,0.13);">

  <!-- HEADER -->
  <div style="background:linear-gradient(135deg,#3B0764 0%,#7C3AED 60%,#A855F7 100%);
              padding:28px 28px 22px;text-align:center;">
    <div style="font-size:38px;margin-bottom:8px;">🛍️</div>
    <h1 style="margin:0;color:#fff;font-size:22px;font-weight:700;letter-spacing:-0.3px;">
      Ripley AI Platform
    </h1>
    <p style="margin:6px 0 0;color:rgba(255,255,255,0.82);font-size:14px;">{subtitulo}</p>
  </div>

  <!-- CUERPO -->
  <div style="padding:28px 28px 20px;">
    {cuerpo}
  </div>

  <!-- FOOTER -->
  <div style="background:#F9F7FF;border-top:1px solid #EDE9FE;
              padding:16px 28px;text-align:center;">
    <p style="margin:0;font-size:12px;color:#9CA3AF;">
      Generado el {ahora} · Ripley Chile © 2026
    </p>
    <a href="https://www.ripley.cl"
       style="display:inline-block;margin-top:10px;
              background:linear-gradient(135deg,#6B21A8,#9333EA);
              color:#fff;padding:10px 24px;border-radius:20px;
              text-decoration:none;font-size:13px;font-weight:600;">
      Ver ofertas en Ripley →
    </a>
  </div>
</div>
</body>
</html>"""


# ══════════════════════════════════════════════════════
# PLANTILLA 1 — REPORTE DE CONVERSACIÓN
# ══════════════════════════════════════════════════════

def generar_email_reporte(cliente: str, mensajes: list, modo: str = "chatbot") -> str:
    """
    Genera HTML con el resumen de la conversación del chat.
    mensajes: lista de {"role": "user"|"assistant", "content": "..."}
    """
    icono_modo = "💬" if modo == "chatbot" else "🤖"
    nombre_modo = "Asistente Virtual" if modo == "chatbot" else "Agente Inteligente"

    burbujas = ""
    for m in mensajes:
        role    = m.get("role", "user")
        content = m.get("content", "").replace("\n", "<br>")

        if role == "user":
            burbujas += f"""
            <div style="display:flex;justify-content:flex-end;margin:8px 0;">
              <div style="background:linear-gradient(135deg,#6B21A8,#9333EA);
                          color:#fff;padding:11px 16px;border-radius:18px 18px 4px 18px;
                          max-width:75%;font-size:14px;line-height:1.6;">
                {content}
              </div>
            </div>"""
        else:
            burbujas += f"""
            <div style="display:flex;justify-content:flex-start;margin:8px 0;">
              <div style="background:#F3F0FB;color:#1E1B2E;
                          border:1.5px solid rgba(107,33,168,0.14);
                          padding:11px 16px;border-radius:18px 18px 18px 4px;
                          max-width:75%;font-size:14px;line-height:1.6;">
                {content}
              </div>
            </div>"""

    cuerpo = f"""
    <p style="color:#4B5563;font-size:15px;margin:0 0 16px;">
      Hola <strong style="color:#6B21A8;">{cliente}</strong>, aquí tienes el resumen
      de tu conversación con el {icono_modo} <strong>{nombre_modo}</strong>.
    </p>

    <div style="background:#F9F7FF;border:1px solid #EDE9FE;border-radius:14px;
                padding:16px;margin-bottom:20px;">
      <p style="margin:0 0 12px;font-size:12px;font-weight:600;
                color:#9333EA;text-transform:uppercase;letter-spacing:0.5px;">
        Conversación
      </p>
      {burbujas}
    </div>
    """

    return _base_template(
        titulo    = f"Reporte de conversación — Ripley AI",
        subtitulo = f"Resumen de tu sesión con {nombre_modo}",
        cuerpo    = cuerpo
    )


# ══════════════════════════════════════════════════════
# PLANTILLA 2 — PROMOCIÓN (CLIMA + PRODUCTOS)
# ══════════════════════════════════════════════════════

def generar_email_promocion(cliente: str, clima: dict = None, productos: list = None) -> str:
    """
    Genera HTML con recomendaciones basadas en clima y/o productos.
    """
    clima_html = ""
    if clima:
        temp      = clima.get("temperature", "?")
        ciudad    = clima.get("city", "")
        viento    = clima.get("windspeed", "?")
        condicion = clima.get("description", "")

        if isinstance(temp, (int, float)) and temp < 12:
            tip = "🧥 ¡Día frío! Te recomendamos ropa de abrigo y calefacción."
        elif isinstance(temp, (int, float)) and temp > 24:
            tip = "☀️ ¡Día caluroso! Ideal para ropa liviana y ventiladores."
        else:
            tip = "🌤️ Clima templado, perfecto para salir."

        clima_html = f"""
        <div style="background:linear-gradient(135deg,#EDE9FE,#F3F0FB);
                    border:1px solid #DDD6FE;border-radius:14px;
                    padding:16px 20px;margin-bottom:20px;">
          <p style="margin:0 0 4px;font-size:13px;font-weight:600;color:#6B21A8;">
            🌡️ Clima en {ciudad}
          </p>
          <p style="margin:0;font-size:20px;font-weight:700;color:#1E1B2E;">
            {temp}°C &nbsp;·&nbsp; <span style="font-size:14px;color:#6B7280;">{condicion}</span>
          </p>
          <p style="margin:8px 0 0;font-size:13px;color:#4B5563;">
            Viento {viento} km/h &nbsp;·&nbsp; {tip}
          </p>
        </div>"""

    productos_html = ""
    if productos:
        cards = ""
        for i, p in enumerate(productos[:4]):
            titulo = (
                p.get("title")
                or p.get("name")
                or p.get("nombre")
                or p.get("producto")
                or "Producto"
            )
            precio = p.get("price") or p.get("precio") or ""
            cat    = p.get("category") or p.get("categoria") or ""
            accent = ["#6B21A8", "#7C3AED", "#9333EA", "#A855F7"][i % 4]

            cards += f"""
            <div style="border:1px solid #EDE9FE;border-radius:12px;
                        padding:14px 16px;margin:8px 0;
                        border-left:4px solid {accent};">
              <p style="margin:0 0 2px;font-size:14px;font-weight:600;color:#1E1B2E;">
                {titulo}
              </p>
              <p style="margin:0;font-size:12px;color:#9CA3AF;">{cat}</p>
              <p style="margin:6px 0 0;font-size:16px;font-weight:700;color:{accent};">
                ${precio:,} CLP
              </p>
            </div>""" if isinstance(precio, (int, float)) else f"""
            <div style="border:1px solid #EDE9FE;border-radius:12px;
                        padding:14px 16px;margin:8px 0;
                        border-left:4px solid {accent};">
              <p style="margin:0 0 2px;font-size:14px;font-weight:600;color:#1E1B2E;">
                {titulo}
              </p>
              <p style="margin:0;font-size:12px;color:#9CA3AF;">{cat}</p>
              <p style="margin:6px 0 0;font-size:16px;font-weight:700;color:{accent};">
                {precio}
              </p>
            </div>"""

        productos_html = f"""
        <div style="margin-bottom:20px;">
          <p style="margin:0 0 10px;font-size:13px;font-weight:600;color:#6B21A8;">
            🛍️ Recomendaciones para ti
          </p>
          {cards}
        </div>"""

    cuerpo = f"""
    <p style="color:#4B5563;font-size:15px;margin:0 0 18px;">
      Hola <strong style="color:#6B21A8;">{cliente}</strong>,
      preparamos recomendaciones especiales basadas en tu consulta.
    </p>
    {clima_html}
    {productos_html}
    """

    return _base_template(
        titulo    = "Ofertas personalizadas — Ripley",
        subtitulo = "Recomendaciones basadas en tu consulta al agente",
        cuerpo    = cuerpo
    )