from pydantic import BaseModel
from src import Demanda
from enum import Enum

class DemandaModel(BaseModel):
    tipo: str
    minimo: int
    maximo: int
    n_periodos: int
    dados: list[int]
    referencias: list[int]
    amplitude: int

TIPOS = Demanda.TIPOS
TiposEnum = Enum("TiposEnum", {nome: nome for nome in TIPOS})
