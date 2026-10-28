# ==============================================================================
# 🌐 CLIENTE HTTP DO ANALISADOR
# ==============================================================================

import requests

BASE_URL = "http://127.0.0.1:8000/weather"


def trigger_collection():
    try:
        response = requests.post(f"{BASE_URL}/collect", timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erro ao disparar coleta: {e}")
        return None


def fetch_history(start_date: str, end_date: str):
    try:
        response = requests.get(
            f"{BASE_URL}/history",
            params={"start_date": start_date, "end_date": end_date},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erro ao buscar histórico: {e}")
        return []


def fetch_forecast(start_date: str, end_date: str):
    try:
        response = requests.get(
            f"{BASE_URL}/forecast",
            params={"start_date": start_date, "end_date": end_date},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erro ao buscar previsão: {e}")
        return []


def fetch_stats(start_date: str, end_date: str, metric: str = "temperature"):
    try:
        response = requests.get(
            f"{BASE_URL}/stats",
            params={"start_date": start_date, "end_date": end_date, "metric": metric},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erro ao buscar estatísticas: {e}")
        return {}