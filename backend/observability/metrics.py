import pandas as pd

CHATBOT_LOG = "data/logs/chatbot_logs.csv"

def load_logs():
    return pd.read_csv(CHATBOT_LOG)


def get_avg_latency():
    df = load_logs()
    return df["latencia"].mean()


def get_total_questions():
    df = load_logs()
    return len(df)


def get_error_rate():
    df = load_logs()
    if len(df) == 0:
        return 0
    return df["error"].sum() / len(df)