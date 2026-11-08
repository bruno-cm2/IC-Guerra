import random
from abc import ABC, abstractmethod
from typing import ClassVar
from .utils import normalize

class Intervalo:
  def __init__(self, minimo: int | None = None, maximo: int | None = None, amplitude: int | None = None):

    minimo = minimo if minimo is not None else 30000
    maximo = maximo if maximo is not None else 50000

    self.amplitude = amplitude if amplitude is not None else random.randint(
        0, maximo - minimo)
    self.minimo = random.randint(minimo, maximo - self.amplitude)
    self.maximo = self.minimo + self.amplitude
    self.centro = (self.minimo + self.maximo) / 2

  def __str__(self):
    return (
        f"Intervalo: [{self.minimo}, {self.maximo}]\n"
        f"Amplitude: {self.amplitude}\n"
        f"Centro: {self.centro:g}"
    )
 
    
class Demanda(ABC, Intervalo):
  TIPOS: ClassVar[dict[str, type["Demanda"]]] = {}
  nome: ClassVar[str]
  
  def __init_subclass__(cls, **kwargs):
    super().__init_subclass__(**kwargs)
    if getattr(cls, "nome", None) is None:
      raise TypeError(f"{cls.__name__} deve definir o atributo 'nome'")
    cls.tipo = normalize(cls.nome.lower())

    Demanda.TIPOS[cls.tipo] = cls

  def __init__(self, minimo: int | None = None, maximo: int | None = None, amplitude: int | None = None, n_periodos: int=8):
    super().__init__(minimo, maximo, amplitude)
    self.n_periodos = n_periodos
    
  @property
  @abstractmethod
  def dados(self) -> list[int]:
    "Método dados() a ser implementado"


class DemandaUniforme(Demanda):
  
  nome = "Uniforme"
  
  def __init__(self, minimo: int | None = None, maximo: int | None = None, n_periodos: int=8):
    amplitude = random.randint(2000, min(
        5000, maximo - minimo) if minimo is not None and maximo is not None else 5000)
    super().__init__(minimo, maximo, amplitude, n_periodos)
  
  @property
  def dados(self) -> list[int]:
    return [random.randint(self.minimo, self.maximo) for _ in range(self.n_periodos)]

  def __str__(self):
    return (
        f"Demanda uniforme:\n"
        f"{super().__str__()}\n"
        f"Número de períodos: {self.n_periodos}"
    )


class DemandaTendencia(Demanda):

  nome = "Tendência"

  def __init__(self, minimo: int | None = None, maximo: int | None = None, n_periodos: int=8):
    amplitude = random.randint(5000, min(
        15000, maximo - minimo) if minimo is not None and maximo is not None else 15000)
    super().__init__(minimo, maximo, amplitude, n_periodos)
    self.inicial = self.minimo/2
    self.incremento = (self.minimo - self.inicial) / self.n_periodos

  @property
  def dados(self) -> list[int]:
    return [
        random.randint(
            int(self.inicial + self.incremento * (i-1)),
            int(self.inicial + self.incremento * i))
        for i in range(1, self.n_periodos + 1)
    ]

  def __str__(self):
    return (
        f"Demanda com tendência:\n"
        f"{super().__str__()}\n"
        f"Inicial: {self.inicial:g}\n"
        f"Incremento: {self.incremento:g}"
    )


class DemandaCiclica(Demanda):

  nome = "Cíclica"

  def __init__(self, minimo: int | None = None, maximo: int | None = None, n_periodos: int=8):
    amplitude = random.randint(5000, min(
        10000, maximo - minimo) if minimo is not None and maximo is not None else 10000)
    super().__init__(minimo, maximo, amplitude, n_periodos)
    referencias_centro = [(i+1) * (self.amplitude // 4) +
                          self.minimo for i in range(3)]
    self.referencias = [self.minimo, *referencias_centro, self.maximo]

  def __ciclo(self, lista: list[int]):
    n = len(lista) - 1
    i, direcao = random.randrange(n), random.choice([-1, 1])
    while True:
      yield lista[i], lista[i + 1]
      if not 0 <= i + direcao < n:
        direcao = -direcao
      i += direcao

  @property
  def dados(self):
    geradores = self.__ciclo(self.referencias)
    return [random.randint(*next(geradores)) for _ in range(1, self.n_periodos + 1)]

  def __str__(self):
    return (
      f"Demanda cíclica:\n"
      f"{super().__str__()}\n"
      f"Referências: {self.referencias}"
    )
