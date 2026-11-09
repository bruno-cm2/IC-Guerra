from pydantic import BaseModel, ConfigDict
class DemandaModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    nome: str
    tipo: str
    minimo: int
    maximo: int
    amplitude: int
    periodo: int
    dados: list[int]
    referencias: list[int] | None = None
    peso: float | None = None