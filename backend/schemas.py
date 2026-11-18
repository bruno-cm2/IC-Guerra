from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str | None = None
    login: str
    senha: str
    tipo: str

class AdminSchema(UserSchema):

    login: EmailStr
    tipo: str = "moderador"


class TeamSchema(UserSchema):

    id_sessao: int
    tipo: str = "equipe"


class UserRequestSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login: str
    tipo: str
    nome: str | None = None        # só Moderador tem
    id_sessao: int | None = None   # só Equipe tem


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

