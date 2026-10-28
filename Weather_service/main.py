from fastapi import FastAPI
from api.routes import router as weather_router

app = FastAPI(
    title="Weather Service API",
    description="Backend para coleta e consulta de dados meteorológicos de São Paulo",
    version="1.0.0"
)

app.include_router(weather_router, tags=["Weather"])


@app.get("/")
def root():
    return {"message": "API Weather Service está online!"}