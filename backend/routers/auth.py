from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.db import Usuario
from schemas import AdminSchema, TeamSchema, UserRequestSchema, UserSchema
from services.auth import cadastrar, autenticar, novo_token, novo_refresh

from .dependencies import session, validar

auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])


@auth_router.get("/")
async def home(): 
    """
    Rota padrão de autenticação
    """
    return {"mensagem": "Bem-vindo à Rota de Autenticação"}

@auth_router.post("/signup", status_code=HTTPStatus.CREATED)
async def signup(usuario: AdminSchema, session: Session = Depends(session)):
    try:
        cadastrar(usuario, session)
    except ValueError as e:
        if "Usuário já existe" in str(e):
            raise HTTPException(HTTPStatus.CONFLICT, "Usuário já existe")
        raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, "Erro ao cadastrar usuário")
    return {"message": "Usuário cadastrado"}

@auth_router.post("/create_team", status_code=HTTPStatus.CREATED)
async def signup_team(usuario: TeamSchema, id_sessao: int, session: Session = Depends(session)):
    usuario.id_sessao = id_sessao
    try:
        cadastrar(usuario, session)
    except ValueError as e:
        if "Usuário já existe" in str(e):
            raise HTTPException(HTTPStatus.CONFLICT, "Equipe já existe")
        raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, "Erro ao cadastrar usuário")
    return {"message": "Usuário cadastrado"}

@auth_router.post("/signin", status_code=HTTPStatus.ACCEPTED)
async def signin(login_request: UserSchema, session: Session = Depends(session)):
    usuario = autenticar(login_request, session)
    if not usuario:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Credenciais inválidas")
    return {
        "access_token": novo_token(usuario.id),
        "refresh_token": novo_refresh(usuario.id),
        "token_type": "Bearer"
    }
    
@auth_router.get("/refresh")
async def refresh(usuario = Depends(validar)):
    token = novo_token(usuario.id)
    return {
        "access_token": token,
        "token_type": "Bearer"
    }

@auth_router.get("/me", response_model=UserRequestSchema)
async def me(usuario = Depends(validar)):
    return usuario