from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from clients.open_meteo_client import fetch_open_meteo_data
from repositories.weather_repository import (
    get_latest_record,
    get_records_by_range,
    save_weather_records,
)

router = APIRouter()


@router.get("/health")
def health_check():
    """Endpoint obrigatório: Informa se o serviço está operacional."""
    return {"status": "ok", "service": "Weather Service API"}


@router.post("/weather/collect")
def collect_data():
    """Coleta dados da Open-Meteo e armazena localmente no SQLite."""
    try:
        records = fetch_open_meteo_data()
        save_weather_records(records)
        return {
            "message": "Coleta realizada com sucesso",
            "total_records": len(records),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao coletar dados: {str(e)}"
        )


@router.get("/weather/current")
def get_current_weather():
    """Endpoint obrigatório: Consulta a estimativa mais recente disponível."""
    latest = get_latest_record()
    if not latest:
        raise HTTPException(
            status_code=404, detail="Nenhum dado encontrado no banco."
        )
    return latest


@router.get("/weather/history")
def get_history(
    start_date: str = Query(..., description="Data inicial YYYY-MM-DD"),
    end_date: str = Query(..., description="Data final YYYY-MM-DD"),
):
    """Consulta dados históricos filtrados por período."""
    return get_records_by_range(start_date, end_date)


@router.get("/weather/forecast")
def get_forecast(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """Consulta previsões salvas."""
    today = datetime.now().strftime("%Y-%m-%d")
    s_date = start_date or today
    e_date = end_date or "2099-12-31"
    return get_records_by_range(s_date, e_date)


@router.get("/weather/stats")
def get_stats(
    start_date: str = Query(..., description="Data inicial YYYY-MM-DD"),
    end_date: str = Query(..., description="Data final YYYY-MM-DD"),
    metric: str = Query("temperature", description="Variável meteorológica"),
):
    """Retorna estatísticas básicas de uma métrica."""
    records = get_records_by_range(start_date, end_date)
    values = [r[metric] for r in records if r.get(metric) is not None]

    if not values:
        return {"count": 0, "mean": None, "max": None, "min": None}

    return {
        "metric": metric,
        "count": len(values),
        "mean": round(sum(values) / len(values), 2),
        "max": max(values),
        "min": min(values),
    }