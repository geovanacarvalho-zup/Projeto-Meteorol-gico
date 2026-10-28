import requests

BASE_URL_FORECAST = "https://api.open-meteo.com/v1/forecast"
BASE_URL_ARCHIVE = "https://archive-api.open-meteo.com/v1/archive"

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


def fetch_open_meteo_data():
    """Busca previsão para os próximos 7 dias e histórico recente."""
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": ",".join(HOURLY_VARS),
        "timezone": TIMEZONE,
        "past_days": 90,  # Garante os 3 meses anteriores
        "forecast_days": 7,  # Garante os 7 dias seguintes
    }

    response = requests.get(BASE_URL_FORECAST, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    apparent_temps = hourly.get("apparent_temperature", [])
    humidities = hourly.get("relative_humidity_2m", [])
    precipitations = hourly.get("precipitation", [])
    wind_speeds = hourly.get("wind_speed_10m", [])
    weather_codes = hourly.get("weather_code", [])

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