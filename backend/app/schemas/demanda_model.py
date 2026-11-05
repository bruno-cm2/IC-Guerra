from pydantic import BaseModel
from src import Demanda
from enum import Enum
from typing import TYPE_CHECKING

class DemandaModel(BaseModel):
    tipo: str
    minimo: int
    maximo: int
    n_periodos: int
    dados: list[int]
    referencias: list[int] | None = None
    amplitude: int

TIPOS = Demanda.TIPOS

if TYPE_CHECKING:
    class TiposEnum(str, Enum):
        pass
else: 
    TiposEnum = Enum("TiposEnum", {nome: nome for nome in TIPOS})
