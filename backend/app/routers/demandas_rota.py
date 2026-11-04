from fastapi import APIRouter
from src.demandas import Demanda, DemandaUniforme, DemandaTendencia, DemandaCiclica
from enum import Enum
from src.utils import plot

demandas_router = APIRouter(prefix="/demandas", tags=["Demandas"])

TIPOS: dict[str, type[Demanda]] = {
    "Uniforme": DemandaUniforme,
    "Tendência": DemandaTendencia,
    "Cíclica": DemandaCiclica,
}

TiposEnum = Enum("TiposEnum", {nome: nome for nome in TIPOS}) # type: ignore[misc]

@demandas_router.get("/{tipo}")
async def gerar_demanda(tipo: TiposEnum): # type: ignore[valid-type]
    classe = TIPOS[tipo.value]()
    return classe.dados