from fastapi import APIRouter, HTTPException, Depends
from models import Usuario
from .dependencies import session, validar
from main import bcrypt_context, TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, REFRESH_TOKEN_DAYS
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])

def novo_token(id, duracao = timedelta(minutes=TOKEN_EXPIRE_MINUTES)):
    expiracao = datetime.now(timezone.utc) + duracao
    dict_info = {"sub": id, "exp": expiracao}
    encoded = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return encoded

def autenticar(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario or not bcrypt_context.verify(senha, usuario.senha):
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
    dados["senha"] = bcrypt_context.hash(dados["senha"])
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
    
@auth_router.post("/refresh")
async def refresh(token, usuario: Usuario = Depends(validar)):
    usuario = validar(token)
    novo_token = novo_token(usuario)