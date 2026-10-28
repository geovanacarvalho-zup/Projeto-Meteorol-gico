import sys
import os

# Adiciona o analisador ao caminho para conseguir importar o analysis.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../weather_analyzer")))

from analysis import (
    calcular_resumo_periodo,
    analisar_precipitacao,
    analisar_umidade_temperatura,
    analisar_extremos_previsao
)


def test_calcular_resumo_periodo():
    """Testa se a média, mínima e máxima de temperatura estão certas."""
    dados_falsos = [
        {"datetime": "2026-10-01T00:00", "temperature": 10.0},
        {"datetime": "2026-10-01T01:00", "temperature": 20.0},
        {"datetime": "2026-10-01T02:00", "temperature": 30.0},
    ]
    resultado = calcular_resumo_periodo(dados_falsos)

    assert resultado["media"] == 20.0
    assert resultado["min"] == 10.0
    assert resultado["max"] == 30.0
    assert resultado["total"] == 3


def test_analisar_precipitacao():
    """Testa o cálculo de chuva acumulada e o dia mais chuvoso."""
    dados_falsos = [
        {"datetime": "2026-10-01T10:00", "precipitation": 5.0},
        {"datetime": "2026-10-01T12:00", "precipitation": 10.0},
        {"datetime": "2026-10-02T10:00", "precipitation": 2.0},
    ]
    resultado = analisar_precipitacao(dados_falsos)

    # Dia 01 teve 15mm, Dia 02 teve 2mm -> Total 17mm
    assert resultado["total_acumulado_mm"] == 17.0
    assert resultado["dia_mais_chuvoso"] == "2026-10-01"
    assert resultado["chuva_no_dia_mm"] == 15.0


def test_analisar_umidade_temperatura():
    """Testa o comparativo de médias."""
    dados_falsos = [
        {"datetime": "2026-10-01T10:00", "temperature": 20.0, "relative_humidity": 80.0},
        {"datetime": "2026-10-01T11:00", "temperature": 24.0, "relative_humidity": 60.0},
    ]
    resultado = analisar_umidade_temperatura(dados_falsos)

    assert resultado["temp_media"] == 22.0
    assert resultado["umid_media"] == 70.0


def test_dados_vazios():
    """Testa se o programa lida bem quando a API não retorna dados."""
    assert calcular_resumo_periodo([]) is None
    assert analisar_precipitacao([]) is None
    assert analisar_umidade_temperatura([]) is None