from fastapi import APIRouter
from schemas import TiposEnum, TIPOS, DemandaModel

demandas_router = APIRouter(prefix="/demandas", tags=["Demandas"])

@demandas_router.get("/tipos", response_model=list[str])
def listar_tipos():
    return [t.value for t in TiposEnum]

@demandas_router.get("/{tipo}", response_model= DemandaModel)
def gerar_demanda(tipo: TiposEnum):
    classe = TIPOS[tipo.value]()
    return classe