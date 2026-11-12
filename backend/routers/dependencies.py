import jwt
from fastapi import Depends, HTTPException
from jwt import InvalidTokenError
from sqlalchemy.orm import Session, sessionmaker

from config import ALGORITHM, SECRET_KEY, outh2_schema
from models import Usuario, db


def session():
    sessao = sessionmaker(bind=db)()
    try:
        yield sessao
    finally:
        sessao.close()


def validar(token: str = Depends(outh2_schema), session: Session = Depends(session)):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = dict_info.get("sub")
    except InvalidTokenError:
        raise HTTPException(401, "Acesso negado")
    usuario = session.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(401, "Acesso inválido")
    return usuario
