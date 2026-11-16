from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    login: str
    
class TeamSchema(UserSchema):

    senha: str

class AdmSchema(UserSchema):
    
    nome: str
    senha: str

class DemandaSchema(BaseModel):
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

