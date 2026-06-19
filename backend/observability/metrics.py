import pandas as pd
import os

LOG_FILE = "data/logs/logs.csv"


def load_logs():

    if not os.path.exists(LOG_FILE):
        return pd.DataFrame()

    df = pd.read_csv(LOG_FILE)

    if df.empty:
        return pd.DataFrame()

    return df


def get_avg_latency():

    df = load_logs()

    if df.empty:
        return 0

    return df["latencia"].mean()


def get_total_questions():

    df = load_logs()

    return len(df)


def get_error_rate():

    df = load_logs()

    if df.empty:
        return 0

    if "error" not in df.columns:
        return 0

    return df["error"].sum() / len(df)