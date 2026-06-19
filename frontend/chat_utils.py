import streamlit as st
import streamlit.components.v1 as components
import time
import os
import base64
import html as html_lib
import re

def is_dark_mode() -> bool:
    return st.get_option("theme.base") == "dark"


# ══════════════════════════════════════════════════════
# LOGO — busca un logo propio en /assets, si no existe usa emoji
# ══════════════════════════════════════════════════════

_ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
_LOGO_CANDIDATES = ["ripley_logo.png", "ripley_logo.svg", "ripley_logo.jpg", "ripley_logo.jpeg"]


def _find_logo_path():
    for name in _LOGO_CANDIDATES:
        p = os.path.join(_ASSET_DIR, name)
        if os.path.exists(p):
            return p
    return None


def get_logo_html(size: int = 40) -> str:
    """
    Devuelve un <img> con el logo si existe en /assets/ripley_logo.(png|svg|jpg),
    o un emoji de respaldo si el usuario aún no ha subido uno.
    """
    path = _find_logo_path()
    if path:
        ext = path.rsplit(".", 1)[-1].lower()
        mime = "image/svg+xml" if ext == "svg" else f"image/{'jpeg' if ext == 'jpg' else ext}"
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return (
            f'<img src="data:{mime};base64,{b64}" '
            f'style="height:{size}px;width:auto;border-radius:8px;vertical-align:middle;" '
            f'alt="Ripley">'
        )
    return f'<span style="font-size:{int(size * 0.95)}px;line-height:1;">🛍️</span>'


# ══════════════════════════════════════════════════════
# PANTALLA DE BIENVENIDA — centrada, estilo "primer mensaje"
# ══════════════════════════════════════════════════════

def render_welcome_screen(title: str, subtitle: str):
    logo_html = get_logo_html(size=46)
    st.markdown(f"""
    <div class="welcome-wrap">
        <div class="welcome-icon">{logo_html}</div>
        <h1 class="welcome-title">{title}</h1>
        <p class="welcome-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def use_inline_chat_input():
    """
    Anula el anclaje fijo del chat_input de Streamlit para que, mientras no
    haya conversación, el input aparezca dentro del flujo normal de la
    página (debajo del saludo) en vez de pegado abajo del todo. En cuanto
    exista historial, esta función deja de llamarse y el input vuelve a
    su comportamiento normal (anclado abajo).
    """
    st.markdown("""
    <style>
    [data-testid="stBottom"] {
        position: relative !important;
        inset: auto !important;
        padding: 6px 0 4px !important;
    }
    [data-testid="stBottom"] > div { max-width: 640px !important; }
    </style>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# HISTORIAL DE CHATS — barra lateral
# ══════════════════════════════════════════════════════

def render_sidebar_history():
    """
    Muestra en la barra lateral el registro de la conversación de cada
    sección (Agente / Asistente) por separado, sin mezclarlas, con acceso
    directo y opción para limpiar cada una.
    """
    with st.sidebar:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;margin:2px 0 22px;">
            {get_logo_html(34)}
            <div>
                <p style="margin:0;font-weight:700;font-size:15px;color:#fff;">Ripley AI</p>
                <p style="margin:0;font-size:11px;color:rgba(255,255,255,0.65);">Registro de chats</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        _render_history_section("🤖 Agente Inteligente", "agent", nav_index=2)
        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        _render_history_section("💬 Asistente Virtual", "messages", nav_index=1)


def _render_history_section(label: str, session_key: str, nav_index: int):
    msgs = st.session_state.get(session_key, [])
    st.markdown(f'<p class="sidebar-section-title">{label}</p>', unsafe_allow_html=True)

    if not msgs:
        st.markdown(
            '<div class="chat-history-item empty">Aún no hay conversación</div>',
            unsafe_allow_html=True
        )
        return

    first_user = next((m["content"] for m in msgs if m["role"] == "user"), "Conversación")
    preview = (first_user[:34] + "…") if len(first_user) > 34 else first_user

    col_a, col_b = st.columns([5, 1])
    with col_a:
        if st.button(f"💭 {preview}", key=f"hist_{session_key}", use_container_width=True):
            st.session_state.nav_jump = nav_index
            st.rerun()
    with col_b:
        if st.button("🗑️", key=f"hist_del_{session_key}"):
            st.session_state[session_key] = []
            st.rerun()

    st.markdown(
        f'<p class="chat-history-meta">{len(msgs)} mensajes</p>',
        unsafe_allow_html=True
    )


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


def _store_tool_metadata(meta: dict):
    """
    Guarda en session_state el resultado de la herramienta (clima o
    productos) que el agente haya usado en el último turno, para que
    el correo de 'Promoción con productos/clima' use datos reales.
    """
    tipo = meta.get("type")
    data = meta.get("data")

    if tipo == "weather" and isinstance(data, dict):
        st.session_state["ultimo_clima"] = data
    elif tipo == "products" and isinstance(data, list):
        st.session_state["ultimos_productos"] = data


def stream_response(generator, delay: float = 0.012) -> str:
    dark   = is_dark_mode()
    bot_bg = "#221840" if dark else "#FFFFFF"
    text   = "#EDE9FE" if dark else "#1E1B2E"
    border = "rgba(167,139,202,0.2)" if dark else "rgba(107,33,168,0.14)"

    placeholder = st.empty()
    full_text   = ""
    displayed   = ""

    for chunk in generator:

        # El agente puede entregar, al final, un "chunk" especial (dict)
        # con el resultado de una herramienta (clima/productos) en vez de
        # texto. Se guarda aparte y no se muestra en la burbuja del chat.
        if isinstance(chunk, dict):
            if chunk.get("__meta__"):
                _store_tool_metadata(chunk)
            continue

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