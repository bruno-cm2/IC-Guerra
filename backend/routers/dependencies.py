from http import HTTPStatus

from fastapi import Depends, HTTPException
from jwt import ExpiredSignatureError, InvalidTokenError, decode
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
        dict_info = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = dict_info.get("sub")
    except ExpiredSignatureError:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Login expirado")
    except InvalidTokenError:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Acesso negado")
    usuario = session.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Acesso negado")
    return usuario
