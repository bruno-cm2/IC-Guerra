from fastapi import APIRouter
from schemas import TiposEnum, TIPOS, DemandaModel

demandas_router = APIRouter(prefix="/demandas", tags=["Demandas"])

@demandas_router.get("/{tipo}", response_model= DemandaModel)
def gerar_demanda(tipo: TiposEnum): #type: ignore[valid-type]
    classe = TIPOS[tipo.value]()
    return classe.dados()