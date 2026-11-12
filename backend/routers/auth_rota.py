from datetime import UTC, datetime, timedelta

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
from models import Usuario
from schemas import LoginSchema, UsuarioSchema

from .dependencies import session, validar

auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])

def novo_token(id, duracao = timedelta(minutes=int(TOKEN_EXPIRE_MINUTES))):
    expiracao = datetime.now(UTC) + duracao
    dict_info = {"sub": str(id), "exp": expiracao}
    encoded = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return encoded

def autenticar(email: str, senha: str, session: Session = Depends(session)):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario or not pass_hash.verify(senha, usuario.senha):
        return False
    return usuario


@auth_router.get("/")
async def home(): 
    """
    Rota padrão de autenticação
    """

@auth_router.post("/cadastrar")
async def cadastrar(usuario_schema: UsuarioSchema, session: Session = Depends(session)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        raise HTTPException(400, "Usuário já existe")
    dados = usuario_schema.model_dump()
    dados["senha"] = pass_hash.hash(dados["senha"])
    novo_usuario = Usuario(**dados)
    session.add(novo_usuario)
    session.commit()
    return {"mensagem": "Usuário cadastrado"}

@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(session)):
    usuario = autenticar(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(400, "Credenciais inválidas")
    token = novo_token(usuario.id)
    token_permanente = novo_token(usuario.id, timedelta(days=REFRESH_TOKEN_DAYS))
    return {
        "access_token": token,
        "refresh_token": token_permanente,
        "token_type": "Bearer"
    }

@auth_router.post("/login_form")
async def login_form(dados_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(session)):
    usuario = autenticar(dados_form.username, dados_form.password, session)
    if not usuario:
        raise HTTPException(400, "Credenciais inválidas")
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