import sqlite3
from typing import List, Dict, Optional

DB_NAME = "weather.db"


def init_db():
    """Cria a tabela SQLite com todas as colunas necessárias."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weather_data (
                datetime TEXT PRIMARY KEY,
                temperature REAL,
                apparent_temperature REAL,
                relative_humidity REAL,
                precipitation REAL,
                wind_speed REAL,
                weather_code INTEGER,
                collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def save_weather_records(records: List[Dict]):
    """Salva os registros evitando duplicidade pelo datetime."""
    init_db()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.executemany(
            """
            INSERT OR REPLACE INTO weather_data 
            (datetime, temperature, apparent_temperature, relative_humidity, precipitation, wind_speed, weather_code)
            VALUES (:datetime, :temperature, :apparent_temperature, :relative_humidity, :precipitation, :wind_speed, :weather_code)
            """,
            records,
        )
        conn.commit()


def get_records_by_range(start_date: str, end_date: str) -> List[Dict]:
    """Busca registros entre duas datas (YYYY-MM-DD)."""
    init_db()
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM weather_data
            WHERE date(datetime) >= date(?) AND date(datetime) <= date(?)
            ORDER BY datetime ASC
            """,
            (start_date, end_date),
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_latest_record() -> Optional[Dict]:
    """Retorna o registro meteorológico mais recente disponível."""
    init_db()
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM weather_data
            ORDER BY datetime DESC
            LIMIT 1
            """
        )
        row = cursor.fetchone()
        return dict(row) if row else None