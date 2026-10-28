from typing import List, Dict

# PERCORRE A LISTA DE TEMPRATURA , FAZ SOMA E DIVIDE PELA QUANTIDADE PRA ACHAR A MEDIA 

def calcular_resumo_periodo(dados: List[Dict]):
    """1. Resumo meteorológico: temperatura média, mínima e máxima."""
    temps = [d["temperature"] for d in dados if d.get("temperature") is not None]
    if not temps:
        return None
    return {
        "media": round(sum(temps) / len(temps), 2),
        "min": min(temps),
        "max": max(temps),
        "total": len(temps)
    }

# ANALISAR PRECIPITAÇÃO > AGRUPA AS CHUVAS DE HORA EM HORA POR DIA E IDENTIFICA O DIA COM MAIOR CHUVA E O TOTAL ACUMULADO

def analisar_precipitacao(dados: List[Dict]):
    """2. Análise de precipitação: dias com maior chuva e acumulado total."""
    acumulado_por_dia = {}
    for d in dados:
        dia = d["datetime"].split("T")[0]
        chuva = d.get("precipitation") or 0.0
        acumulado_por_dia[dia] = acumulado_por_dia.get(dia, 0.0) + chuva

    if not acumulado_por_dia:
        return None

    dia_mais_chuvoso = max(acumulado_por_dia, key=acumulado_por_dia.get)
    total_acumulado = sum(acumulado_por_dia.values())

    return {
        "total_acumulado_mm": round(total_acumulado, 2),
        "dia_mais_chuvoso": dia_mais_chuvoso,
        "chuva_no_dia_mm": round(acumulado_por_dia[dia_mais_chuvoso], 2)
    }

# ANALISAR UMIDADE DA TEMPERATURA > FAZ A MEDIA DE TEMPERATURA E UMIDADE RELATIVA

def analisar_umidade_temperatura(dados: List[Dict]):
    """3. Análise de umidade e temperatura: médias e comparativo."""
    temps = [d["temperature"] for d in dados if d.get("temperature") is not None]
    umids = [d["relative_humidity"] for d in dados if d.get("relative_humidity") is not None]

    if not temps or not umids:
        return None

    return {
        "temp_media": round(sum(temps) / len(temps), 2),
        "umid_media": round(sum(umids) / len(umids), 2)
    }

# ANALISAR EXTREMOS DE PREVISÃO > AGRUPA AS TEMPRATURAS POR DIA E IDENTIFICA O DIA MAIS QUENTE E O MAIS FRIO

def analisar_extremos_previsao(dados: List[Dict]):
    """4. Análise de previsão: dias previstos com maiores e menores temperaturas."""
    temp_por_dia = {}
    for d in dados:
        dia = d["datetime"].split("T")[0]
        temp = d.get("temperature")
        if temp is not None:
            if dia not in temp_por_dia:
                temp_por_dia[dia] = []
            temp_por_dia[dia].append(temp)

    if not temp_por_dia:
        return None

    medias_diarias = {dia: sum(valores) / len(valores) for dia, valores in temp_por_dia.items()}
    dia_mais_quente = max(medias_diarias, key=medias_diarias.get)
    dia_mais_frio = min(medias_diarias, key=medias_diarias.get)

    return {
        "dia_mais_quente": dia_mais_quente,
        "media_quente": round(medias_diarias[dia_mais_quente], 2),
        "dia_mais_frio": dia_mais_frio,
        "media_frio": round(medias_diarias[dia_mais_frio], 2)
    }