
# ==============================================================================
# BLOCO 1: IMPORTAÇÕES E BIBLIOTECAS EXTERNAS
# Objetivo: Trazer o módulo 'requests' para fazer chamadas HTTP via internet.
# ==============================================================================



import requests

BASE_URL_FORECAST = "https://api.open-meteo.com/v1/forecast"
#==========================================================================================

# BLOCO 2: CONSTANTES DE CONFIGURAÇÃO E LOCALIDADE
# Objetivo: Definir URL da Open-Meteo, coordenadas de São Paulo e fuso horário.

#===========================================================================================================
LATITUDE = -23.5505
LONGITUDE = -46.6333
TIMEZONE = "America/Sao_Paulo"

HOURLY_VARS = [
    "temperature_2m",
    "apparent_temperature",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
    "weather_code",
]
#===========================================================================================


# BLOCO 3: DEFINIÇÃO DAS VARIÁVEIS METEOROLÓGICAS OBRIGATÓRIAS
# Objetivo: Listar as 6 métricas climáticas exigidas pelo Tio Fazo no desafio

#============================================================================================
def fetch_open_meteo_data():
    """Busca dados da Open-Meteo com as variáveis obrigatórias."""
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": ",".join(HOURLY_VARS),
        "timezone": TIMEZONE,
        "past_days": 90,
        "forecast_days": 7,
    }
#===========================================================================================


#  4.2: Chamada HTTP e verificação de erros na resposta
#==============================================================================================================
    response = requests.get(BASE_URL_FORECAST, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()

 #========================================================================================================
# 4.3: Extração das listas paralelas retornadas pela API externa

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    apparent_temps = hourly.get("apparent_temperature", [])
    humidities = hourly.get("relative_humidity_2m", [])
    precipitations = hourly.get("precipitation", [])
    wind_speeds = hourly.get("wind_speed_10m", [])
    weather_codes = hourly.get("weather_code", [])
#==================================================================================================================

## 4.4: Junção das métricas em um registro único para cada hora
#========================================================================================================================

    records = []
    for i in range(len(times)):
        records.append({
            "datetime": times[i],
            "temperature": temps[i] if i < len(temps) else None,
            "apparent_temperature": apparent_temps[i] if i < len(apparent_temps) else None,
            "relative_humidity": humidities[i] if i < len(humidities) else None,
            "precipitation": precipitations[i] if i < len(precipitations) else None,
            "wind_speed": wind_speeds[i] if i < len(wind_speeds) else None,
            "weather_code": weather_codes[i] if i < len(weather_codes) else None,
        })

    return records