import streamlit as st
import pandas as pd
import plotly.express as px
import os


def render():

    st.title("📊 Centro de Monitoreo")
    st.caption("Monitoreo en tiempo real del rendimiento del sistema.")

    LOG_FILE = "data/logs/chatbot_logs.csv"

    @st.cache_data
    def load():

        if not os.path.exists(LOG_FILE):
            return pd.DataFrame()

        df = pd.read_csv(LOG_FILE)

        if df.empty:
            return df

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["latencia"] = pd.to_numeric(df["latencia"])
        df["error"] = df["error"].astype(int)

        return df

    df = load()

    if df.empty:
        st.warning("No hay datos aún.")
        return

    col1, col2, col3 = st.columns(3)

    col1.metric("🧠 Consultas", len(df))
    col2.metric("⚡ Latencia", round(df["latencia"].mean(), 3))
    col3.metric("❌ Errores", int(df["error"].sum()))

    error_rate = round((df["error"].sum() / len(df)) * 100, 2)

    st.info(f"""
Consultas registradas: {len(df)}

Latencia promedio: {round(df['latencia'].mean(), 3)} segundos

Tasa de error: {error_rate}%
""")

    st.markdown("---")

    st.subheader("📈 Rendimiento")

    st.plotly_chart(
        px.line(df, x="timestamp", y="latencia", markers=True),
        use_container_width=True
    )

    st.subheader("📊 Actividad")

    activity = (
        df.groupby(df["timestamp"].dt.date)
        .size()
        .reset_index(name="consultas")
    )

    st.plotly_chart(
        px.bar(activity, x="timestamp", y="consultas"),
        use_container_width=True
    )

    st.subheader("❌ Errores")

    errors = (
        df.groupby(df["timestamp"].dt.date)["error"]
        .sum()
        .reset_index()
    )

    st.plotly_chart(
        px.bar(errors, x="timestamp", y="error"),
        use_container_width=True
    )

    st.subheader("📋 Logs")

    st.dataframe(
        df.sort_values("timestamp", ascending=False),
        use_container_width=True
    )