from datetime import UTC, datetime, timedelta
from http import HTTPStatus

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config import (
    ALGORITHM,
    REFRESH_TOKEN_DAYS,
    SECRET_KEY,
    TOKEN_EXPIRE_MINUTES,
    pass_hash,
)
from models import Usuario, Moderador
from schemas import TeamSchema, AdmSchema

from .dependencies import session, validar

auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])

def novo_token(id, duracao = timedelta(minutes=int(TOKEN_EXPIRE_MINUTES))):
    expiracao = datetime.now(UTC) + duracao
    dict_info = {"sub": str(id), "exp": expiracao}
    encoded = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return encoded

def autenticar(login: str, senha: str, session: Session = Depends(session)):
    usuario = session.query(Usuario).filter(Usuario.login==login).first()
    if not usuario or not pass_hash.verify(senha, usuario.senha):
        return False
    return usuario


@auth_router.get("/")
async def home(): 
    """
    Rota padrão de autenticação
    """

@auth_router.post("/cadastrar", status_code=HTTPStatus.CREATED)
async def cadastrar(usuario_schema: AdmSchema, session: Session = Depends(session)):
    usuario = session.query(Moderador).filter(Moderador.login==usuario_schema.login).first()
    if usuario:
        raise HTTPException(HTTPStatus.CONFLICT, "Usuário já existe")
    dados = usuario_schema.model_dump()
    dados["senha"] = pass_hash.hash(dados["senha"])
    novo_usuario = Moderador(**dados)
    session.add(novo_usuario)
    session.commit()
    return {"mensagem": "Usuário cadastrado"}

@auth_router.post("/login")
async def login(login_schema: TeamSchema, session: Session = Depends(session)):
    usuario = autenticar(login_schema.login, login_schema.senha, session)
    if not usuario:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Credenciais inválidas")
    token = novo_token(usuario.id)
    refresh_token = novo_token(usuario.id, timedelta(days=REFRESH_TOKEN_DAYS))
    return {
        "access_token": token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }

@auth_router.post("/login_form")
async def login_form(dados_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(session)):
    usuario = autenticar(dados_form.username, dados_form.password, session)
    if not usuario:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Credenciais inválidas")
    token = novo_token(usuario.id)
    return {
        "access_token": token,
        "token_type": "Bearer"
    }
    
@auth_router.get("/refresh")
async def refresh(usuario: Usuario = Depends(validar)):
    token = novo_token(usuario.id)
    return {
        "access_token": token,
        "token_type": "Bearer"
    }