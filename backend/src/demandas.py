import random
import math
from operator import add
from abc import ABC, abstractmethod
from typing import ClassVar
from .utils import normalize

class Intervalo:
  def __init__(self, minimo: int, maximo: int, amplitude: int):

    limite = maximo - minimo
    self.amplitude = random.randint(0, limite) if amplitude is None else min(amplitude, limite)
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

  def __init__(self, periodo: int | None = 8, minimo: int | None = 30000, maximo: int | None = 50000, amplitude: int = 20000):
    if periodo is None: periodo = 8
    if periodo < 4: periodo = 4
    elif periodo > 36: periodo = 36
    if minimo is None: minimo = 30000
    if maximo is None: maximo = 50000
    super().__init__(minimo, maximo, amplitude)
    self.periodo = periodo
    
  @property
  @abstractmethod
  def dados(self) -> list[int]:
    "Get dados a ser implementado"


class DemandaUniforme(Demanda):
  
  nome = "Uniforme"
  
  def __init__(self, periodo: int | None = None, minimo: int | None = None, maximo: int | None = None, amplitude: int | None = None):
    amplitude = random.randint(2000, 5000) if amplitude is None else amplitude
    super().__init__(periodo, minimo, maximo, amplitude)
  
  @property
  def dados(self) -> list[int]:
    return [random.randint(self.minimo, self.maximo) for _ in range(self.periodo)]

  def __str__(self):
    return (
        f"Demanda uniforme:\n"
        f"{super().__str__()}\n"
        f"Número de períodos: {self.periodo}"
    )


class DemandaTendencia(Demanda):

  nome = "Tendência"

  def __init__(self, periodo: int | None = None, minimo: int | None = None, maximo: int | None = None, amplitude: int | None = None):
    amplitude = random.randint(5000,15000) if amplitude is None else amplitude
    super().__init__(periodo, minimo, maximo, amplitude)
    self.inicial = self.minimo
    self.incremento = (self.maximo - self.inicial)/2 / self.periodo

  @property
  def dados(self) -> list[int]:
    return [
        random.randint(
            int(self.inicial + self.incremento * (i-1)),
            int(self.inicial + self.incremento * i))
        for i in range(1, self.periodo + 1)
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

  def __init__(self, periodo: int | None = None, minimo: int | None = None, maximo: int | None = None, amplitude: int | None = None):
    amplitude = random.randint(5000, 10000) if amplitude is None else amplitude
    super().__init__(periodo, minimo, maximo, amplitude)
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
  def dados(self) -> list[int]:
    geradores = self.__ciclo(self.referencias)
    return [random.randint(*next(geradores)) for _ in range(1, self.periodo + 1)]

  def __str__(self):
    return (
      f"Demanda cíclica:\n"
      f"{super().__str__()}\n"
      f"Referências: {self.referencias}"
    )

class DemandaMista(Demanda):
  nome = "Mista"
  def __init__(self, periodo: int | None = None, peso: float = 0.5, minimo: int | None = None, maximo: int | None = None, amplitude: int | None = None):
    amplitude = random.randint(10000, 18000) if amplitude is None else amplitude
    super().__init__(periodo, minimo, maximo, amplitude)
    self.peso = peso
    self.tendencia = DemandaTendencia(periodo, math.ceil(self.minimo*peso), math.floor(self.maximo*self.peso), int(amplitude*self.peso))
    self.ciclica = DemandaCiclica(periodo, math.ceil(self.minimo*(1-self.peso)), math.floor(self.maximo*(1-self.peso)), int(amplitude*(1-self.peso)))

  @property
  def dados(self) -> list[int]:
    dadosTendencia = self.tendencia.dados
    dadosCiclica = self.ciclica.dados
    return list(map(add, dadosCiclica, dadosTendencia))
    
      
