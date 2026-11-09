from fastapi import APIRouter, Query
from schemas import DemandaModel
from typing import Literal
from src import Demanda

demandas_router = APIRouter(prefix="/demandas")

tipos = Literal["uniforme", "tendencia", "ciclica", "mista"]
nomes = [classe().nome for classe in Demanda.TIPOS.values()]

@demandas_router.get("", response_model=DemandaModel | list[str])
def get_demandas(tipo: tipos | None = None, periodo: int = Query(8, ge=4, le=36)):
    if tipo is None:
        return nomes
    return Demanda.TIPOS[tipo](periodo=periodo)