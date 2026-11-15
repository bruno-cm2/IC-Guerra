from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

db = create_engine("sqlite:///banco.db")


class Base(DeclarativeBase):
    pass

class Usuario(Base):
    __tablename__ = "usuarios"

    id:    Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str]
    tipo:  Mapped[str]

    __mapper_args__ = {"polymorphic_on": "tipo"}

class Moderador(Usuario):
    __tablename__ = "moderadores"

    id:      Mapped[int] = mapped_column(ForeignKey("usuarios.id"), primary_key=True)
    nome:    Mapped[str]
    sessoes: Mapped[list["Sessao"]] = relationship()

    __mapper_args__ = {"polymorphic_identity": "moderador"}


class Sessao(Base):
    __tablename__ = "sessoes"

    id:              Mapped[int] = mapped_column(primary_key=True)
    id_moderador:    Mapped[int] = mapped_column(ForeignKey("moderadores.id"))
    demandas:        Mapped[list["Demanda"]] = relationship(back_populates="sessao", cascade="all, delete-orphan")
    rodadas:         Mapped[list["Rodada"]] = relationship(back_populates="sessao", cascade="all, delete-orphan", order_by="Rodada.num_rodada")
    rodada_atual:    Mapped[int]
    equipes:         Mapped[list["Equipe"]] = relationship(back_populates="sessao", cascade="all, delete-orphan")


class Demanda(Base):
    __tablename__ = "demandas"

    id_sessao: Mapped[int] = mapped_column(ForeignKey("sessoes.id"), primary_key=True)
    id:        Mapped[int] = mapped_column(primary_key=True)
    tipo:      Mapped[str]
    minimo:    Mapped[int]
    maximo:    Mapped[int]
    sessao:    Mapped["Sessao"] = relationship(back_populates="demandas")


class Rodada(Base):
    __tablename__ = "rodadas"

    id_sessao:     Mapped[int] = mapped_column(ForeignKey("sessoes.id"), primary_key=True)
    num_rodada:    Mapped[int] = mapped_column(primary_key=True)
    valor_demanda: Mapped[int]
    sessao:        Mapped["Sessao"] = relationship(back_populates="rodadas")


class Equipe(Usuario):
    __tablename__ = "equipes"

    id:        Mapped[int] = mapped_column(ForeignKey("usuarios.id"), primary_key=True)
    id_sessao: Mapped[int] = mapped_column(ForeignKey("sessoes.id"))
    sessao:    Mapped["Sessao"] = relationship(back_populates="equipes")
    alunos:    Mapped[list["Aluno"]] = relationship(back_populates="equipe")

    __mapper_args__ = {"polymorphic_identity": "equipe"}


class Aluno(Base):
    __tablename__ = "alunos"

    matricula: Mapped[str] = mapped_column(String(11),primary_key=True)
    nome:      Mapped[str | None]
    id_equipe: Mapped[int] = mapped_column(ForeignKey("equipes.id"))
    equipe:    Mapped["Equipe"] = relationship(back_populates="alunos")