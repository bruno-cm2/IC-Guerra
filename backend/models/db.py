from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

db = create_engine("sqlite:///banco.db")


class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str | None] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    senha: Mapped[str] = mapped_column(String)
    ativo: Mapped[bool | None] = mapped_column(default=True)
    admin: Mapped[bool | None] = mapped_column(default=False)
