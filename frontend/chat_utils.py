import streamlit as st
import streamlit.components.v1 as components
import time
import html as html_lib
import re


def is_dark_mode() -> bool:
    return st.get_option("theme.base") == "dark"


def _md_to_html(text: str) -> str:
    """Convierte markdown básico a HTML: negritas, listas, saltos de línea."""
    text = html_lib.escape(text)
    # Negrita **texto**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Itálica *texto*
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Listas con guión
    lines = text.split('\n')
    result = []
    in_list = False
    for line in lines:
        stripped = line.strip()
        if re.match(r'^- (.+)', stripped):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append('<li>' + re.sub(r'^- ', '', stripped) + '</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(line)
    if in_list:
        result.append('</ul>')
    text = '\n'.join(result)
    # Saltos de línea fuera de tags de lista
    text = re.sub(r'\n(?!<(?:li|ul|/ul))', '<br>', text)
    return text


def _build_chat_html(messages: list, dark: bool = False) -> str:
    bg     = "#0F0A1E" if dark else "#F9F7FF"
    bot_bg = "#221840" if dark else "#FFFFFF"
    text   = "#EDE9FE" if dark else "#1E1B2E"
    border = "rgba(167,139,202,0.2)" if dark else "rgba(107,33,168,0.14)"

    bubbles = ""
    for m in messages:
        role    = m["role"]
        content = _md_to_html(m["content"])
        if role == "user":
            bubbles += f"""
            <div class="row user">
                <div class="avatar user">👤</div>
                <div class="bubble user">{content}</div>
            </div>"""
        else:
            bubbles += f"""
            <div class="row bot">
                <div class="avatar bot">🛍️</div>
                <div class="bubble bot">{content}</div>
            </div>"""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{
      font-family: 'Inter','Segoe UI',sans-serif;
      background: {bg};
      padding: 10px 6px 6px;
  }}
  @keyframes pop {{
      from {{ opacity:0; transform:translateY(7px) scale(0.98); }}
      to   {{ opacity:1; transform:translateY(0)   scale(1);    }}
  }}
  .row {{
      display: flex;
      align-items: flex-end;
      gap: 12px;
      margin: 10px 0;
      animation: pop 0.2s ease;
  }}
  .row.user {{ flex-direction: row-reverse; }}
  .row.bot  {{ flex-direction: row; }}
  .avatar {{
      width: 40px; height: 40px;
      border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      font-size: 19px; flex-shrink: 0;
  }}
  .avatar.user {{ background: linear-gradient(135deg,#6B21A8,#9333EA); box-shadow: 0 2px 8px rgba(107,33,168,0.35); }}
  .avatar.bot  {{ background: {bot_bg}; border: 1.5px solid {border}; }}
  .bubble {{
      max-width: 80%;
      padding: 14px 20px;
      font-size: 15px;
      line-height: 1.7;
      word-wrap: break-word;
      border-radius: 24px;
  }}
  .bubble.user {{
      background: linear-gradient(135deg,#6B21A8,#9333EA);
      color: #fff;
      border-bottom-right-radius: 5px;
      box-shadow: 0 4px 16px rgba(107,33,168,0.30);
  }}
  .bubble.bot {{
      background: {bot_bg};
      color: {text};
      border: 1.5px solid {border};
      border-bottom-left-radius: 5px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.07);
  }}
  .bubble.bot ul {{
      padding-left: 1.2rem;
      margin: 6px 0;
  }}
  .bubble.bot li {{
      margin-bottom: 3px;
  }}
  .bubble.bot strong {{
      font-weight: 700;
      color: inherit;
  }}
</style>
</head>
<body>{bubbles}</body>
</html>"""


def _estimate_height(messages: list) -> int:
    if not messages:
        return 60
    total_chars = sum(len(m["content"]) for m in messages)
    base  = len(messages) * 90
    extra = (total_chars // 80) * 22
    return min(base + extra + 30, 520)


def render_chat(messages: list):
    """Renderiza el historial completo en un iframe con scroll."""
    if not messages:
        return
    dark   = is_dark_mode()
    html   = _build_chat_html(messages, dark=dark)
    height = _estimate_height(messages)
    components.html(html, height=height, scrolling=True)


def stream_response(generator, delay: float = 0.012) -> str:
    dark   = is_dark_mode()
    bot_bg = "#221840" if dark else "#FFFFFF"
    text   = "#EDE9FE" if dark else "#1E1B2E"
    border = "rgba(167,139,202,0.2)" if dark else "rgba(107,33,168,0.14)"

    placeholder = st.empty()
    full_text   = ""
    displayed   = ""

    for chunk in generator:
        full_text = chunk
        new_chars = full_text[len(displayed):]
        for char in new_chars:
            displayed += char
            placeholder.markdown(
                f"<div style='"
                f"background:{bot_bg};"
                f"color:{text};"
                f"padding:14px 20px;"
                f"border-radius:24px 24px 24px 5px;"
                f"font-size:15px;"
                f"line-height:1.7;"
                f"max-width:80%;"
                f"border:1.5px solid {border};"
                f"box-shadow:0 2px 10px rgba(0,0,0,0.15);"
                f"font-family:Inter,sans-serif;"
                f"'>{html_lib.escape(displayed)}▌</div>",
                unsafe_allow_html=True
            )
            time.sleep(delay)

    placeholder.empty()
    return full_text