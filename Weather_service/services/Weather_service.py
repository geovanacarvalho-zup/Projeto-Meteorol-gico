# ==============================================================================
# ⚙️ SERVICE: LÓGICA DE NEGÓCIO E INTEGRAÇÃO DE DADOS
# ==============================================================================

from repositories.weather_repository import init_db, save_weather_records, get_records_by_period
from clients.open_meteo_client import fetch_weather_data

# Garante que o banco e a tabela existam na inicialização do serviço
init_db()


def update_weather_data():
    """Busca os dados da API externa e salva no repositório."""
    records = fetch_weather_data()
    inserted_count = save_weather_records(records)
    return inserted_count


def calculate_period_stats(start_date: str, end_date: str, metric: str = "temperature"):
    """Calcula estatísticas (média, máx, mín) de uma métrica em um período."""
    records = get_records_by_period(start_date, end_date)
    values = [r[metric] for r in records if r.get(metric) is not None]

    if not values:
        return {"metric": metric, "mean": 0, "max": 0, "min": 0, "count": 0}

    return {
        "metric": metric,
        "mean": round(sum(values) / len(values), 2),
        "max": max(values),
        "min": min(values),
        "count": len(values)
    }