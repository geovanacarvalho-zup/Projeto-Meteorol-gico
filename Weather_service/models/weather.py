# é um molde nessa caixa tem que ter o  espaço pra colocar a temperatura , a chuva o vento e a data , mas é so o molde vazio 4


from pydantic import BaseModel
from typing import Optional


class WeatherData(BaseModel):
    datetime: str
    temperature: Optional[float] = None
    apparent_temperature: Optional[float] = None
    relative_humidity: Optional[float] = None
    precipitation: Optional[float] = None
    wind_speed: Optional[float] = None
    weather_code: Optional[int] = None
    data_type: str
    collected_at: str


class WeatherStats(BaseModel):
    metric: str
    start_date: str
    end_date: str
    count: int
    mean: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None