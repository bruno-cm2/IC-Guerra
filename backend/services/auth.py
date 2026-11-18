from datetime import datetime, timedelta, timezone

import jwt

from config import ACCESS_TOKEN_MINUTES, ALGORITHM, REFRESH_TOKEN_DAYS, SECRET_KEY, pass_hash
from models.db import Usuario
from schemas import AdminSchema, TeamSchema, UserSchema

def cadastrar(usuario: AdminSchema | TeamSchema, session):
    if session.query(Usuario).filter(Usuario.login==usuario.login).first():
        raise ValueError("Usuário já existe")
    usuario.senha = pass_hash.hash(usuario.senha)
    session.add(Usuario(self=usuario))
    session.commit()

def autenticar(login: UserSchema, session):
    usuario = session.query(Usuario).filter(Usuario.login==login.login).first()
    if not usuario or not pass_hash.verify(login.senha, usuario.senha):
        return False
    return usuario

def novo_token(id: int, exp: timedelta = timedelta(minutes=ACCESS_TOKEN_MINUTES)):
    expiracao = datetime.now(timezone.utc) + exp
    dict_info = {"sub": str(id), "exp": expiracao}
    encoded = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return encoded

def novo_refresh(id: int, exp: timedelta = timedelta(days=REFRESH_TOKEN_DAYS)):
    expiracao = datetime.now(timezone.utc) + exp
    dict_info = {"sub": str(id), "exp": expiracao}
    encoded = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return encoded

    