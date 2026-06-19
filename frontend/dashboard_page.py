import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from streamlit_autorefresh import st_autorefresh

# Paleta violeta Ripley para Plotly
RIPLEY_COLORS = [
    "#6B21A8", "#9333EA", "#A855F7",
    "#C084FC", "#DDD6FE", "#7C3AED"
]


def render():

    is_dark   = st.get_option("theme.base") == "dark"
    text_clr  = "#EDE9FE" if is_dark else "#1E1B2E"

    # =========================
    # ENCABEZADO
    # =========================
    col_title, col_refresh = st.columns([5, 2])

    with col_title:
        st.markdown("""
        <h1 style="margin-bottom:2px;">📊 Centro de Monitoreo</h1>
        <p style="color:var(--muted); font-size:14px; margin-top:0;">
            Rendimiento y operación del sistema en tiempo real.
        </p>
        """, unsafe_allow_html=True)

    with col_refresh:
        st.markdown("<br>", unsafe_allow_html=True)
        auto = st.toggle("🔄 Auto-refresh (3s)", value=True, key="autorefresh_toggle")

    if auto:
        st_autorefresh(interval=3000, key="refresh")

    st.markdown("<hr>", unsafe_allow_html=True)

    LOG_FILE = "data/logs/logs.csv"

    # =========================
    # CARGA DE DATOS
    # =========================
    def load():
        if not os.path.exists(LOG_FILE):
            return pd.DataFrame()
        try:
            df = pd.read_csv(LOG_FILE)
        except pd.errors.EmptyDataError:
            return pd.DataFrame()

        if df.empty:
            return df

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["latencia"]  = pd.to_numeric(df["latencia"], errors="coerce")
        df["error"]     = pd.to_numeric(df["error"], errors="coerce").fillna(0).astype(int)

        return df

    df = load()

    if df.empty:
        st.markdown("""
        <div class="ripley-card" style="text-align:center; padding:3rem;">
            <span style="font-size:48px;">📭</span><br><br>
            <p style="color:var(--muted); font-size:15px;">
                Aún no hay datos de monitoreo registrados.<br>
                Comienza a usar el asistente para generar logs.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    # =========================
    # MÉTRICAS SUPERIORES
    # =========================
    total     = len(df)
    avg_lat   = round(df["latencia"].mean(), 3)
    total_err = int(df["error"].sum())
    err_rate  = round((total_err / total) * 100, 1) if total else 0.0

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("🧠 Consultas totales", total)
    m2.metric("⚡ Latencia promedio", f"{avg_lat}s")
    m3.metric("❌ Errores", total_err)
    m4.metric("📉 Tasa de error", f"{err_rate}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # FILA 1 — LATENCIA + ACTIVIDAD
    # =========================
    col_lat, col_act = st.columns(2, gap="medium")

    with col_lat:
        st.markdown("#### 📈 Latencia en el tiempo")

        fig_lat = px.line(
            df.sort_values("timestamp"),
            x="timestamp",
            y="latencia",
            markers=True,
            color_discrete_sequence=["#9333EA"],
        )
        fig_lat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=False, title=None),
            yaxis=dict(
                gridcolor="rgba(107,33,168,0.08)",
                title=dict(text="seg.", font=dict(size=12))
            ),
            font=dict(family="Inter", color=text_clr),
            height=280,
        )
        fig_lat.update_traces(
            line=dict(width=2.5),
            marker=dict(size=6, color="#6B21A8"),
            fill="tozeroy",
            fillcolor="rgba(147,51,234,0.08)"
        )
        st.plotly_chart(fig_lat, use_container_width=True)

    with col_act:
        st.markdown("#### 📊 Consultas por día")

        activity = (
            df.groupby(df["timestamp"].dt.date)
            .size()
            .reset_index(name="consultas")
        )

        fig_act = px.bar(
            activity,
            x="timestamp",
            y="consultas",
            color_discrete_sequence=["#7C3AED"],
        )
        fig_act.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=False, title=None),
            yaxis=dict(gridcolor="rgba(107,33,168,0.08)", title="N° consultas"),
            font=dict(family="Inter", color=text_clr),
            height=280,
        )
        fig_act.update_traces(
            marker_line_width=0,
            marker_color="#9333EA",
        )
        st.plotly_chart(fig_act, use_container_width=True)

    # =========================
    # FILA 2 — ERRORES + DISTRIBUCIÓN
    # =========================
    col_err, col_dist = st.columns(2, gap="medium")

    with col_err:
        st.markdown("#### ❌ Errores por día")

        errors = (
            df.groupby(df["timestamp"].dt.date)["error"]
            .sum()
            .reset_index()
        )

        fig_err = px.bar(
            errors,
            x="timestamp",
            y="error",
            color_discrete_sequence=["#DC2626"],
        )
        fig_err.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=False, title=None),
            yaxis=dict(gridcolor="rgba(107,33,168,0.08)", title="Errores"),
            font=dict(family="Inter", color=text_clr),
            height=260,
        )
        st.plotly_chart(fig_err, use_container_width=True)

    with col_dist:
        st.markdown("#### 🍩 Distribución OK vs Error")

        ok_count  = total - total_err
        pie_data  = pd.DataFrame({
            "estado": ["Exitosas", "Con error"],
            "count":  [ok_count, total_err]
        })

        fig_pie = px.pie(
            pie_data,
            names="estado",
            values="count",
            hole=0.55,
            color_discrete_sequence=["#9333EA", "#DC2626"],
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
            font=dict(family="Inter", color=text_clr),
            legend=dict(orientation="h", y=-0.1),
            height=260,
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_pie, use_container_width=True)

    # =========================
    # RESUMEN TEXTUAL
    # =========================
    st.markdown("<br>", unsafe_allow_html=True)

    col_sum, col_dl = st.columns([5, 1])

    with col_sum:
        st.markdown(f"""
        <div class="ripley-card ripley-card-accent">
            <strong style="color:#6B21A8; font-size:14px;">📋 Resumen del período</strong><br><br>
            <span style="color:var(--muted); font-size:13px;">
                Se registraron <strong style="color:var(--text);">{total}</strong> consultas con una
                latencia promedio de <strong style="color:var(--text);">{avg_lat}s</strong>.
                Se detectaron <strong style="color:#DC2626;">{total_err}</strong> errores,
                equivalente al <strong style="color:#DC2626;">{err_rate}%</strong> del total.
            </span>
        </div>
        """, unsafe_allow_html=True)

    with col_dl:
        st.markdown("<br>", unsafe_allow_html=True)
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Exportar CSV",
            data=csv_data,
            file_name="ripley_logs.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # TABLA DE LOGS
    # =========================
    st.markdown("#### 📋 Logs recientes")

    st.dataframe(
        df.sort_values("timestamp", ascending=False).head(50),
        use_container_width=True,
        hide_index=True,
    )