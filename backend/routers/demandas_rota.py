from typing import Literal

from fastapi import APIRouter, Query

from models import Demanda
from schemas import DemandaSchema

demandas_router = APIRouter(prefix="/demandas", tags=["Demandas"])

tipos = Literal["uniforme", "tendencia", "ciclica", "mista"]
nomes = [classe().nome for classe in Demanda.TIPOS.values()]

@demandas_router.get("/", response_model=DemandaSchema | list[str])
async def get_demandas(tipo: tipos | None = None, periodo: int = Query(8, ge=4, le=36)):
    if tipo is None:
        return nomes
    return Demanda.TIPOS[tipo](periodo=periodo)