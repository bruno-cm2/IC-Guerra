from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, outh2_schema
from models import Usuario, db
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError

def session():
    try:
        sessao = sessionmaker(bind=db)()
        yield sessao
    finally: 
        sessao.close()

def validar(token: str = Depends(outh2_schema), session: Session = Depends(session)):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id = dict_info.get("sub")
    except JWTError:
        raise HTTPException(401, "Acesso negado")
    usuario = session.query(Usuario).filter(Usuario.id == id)
    if not usuario:
        raise HTTPException(401, "Acesso inválido")
    return usuario

    