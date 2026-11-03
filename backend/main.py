from fastapi import FastAPI
from src.demandas import *

app = FastAPI()

@app.get("/demanda")
def todas(n_periodos: int = 8):
    return {
        "uniforme":  DemandaUniforme(n_periodos=n_periodos).dados(),
        "tendencia": DemandaTendencia(n_periodos=n_periodos).dados(),
        "ciclica":   DemandaCiclica(n_periodos=n_periodos).dados(),
    }