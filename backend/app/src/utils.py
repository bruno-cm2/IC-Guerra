import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import unicodedata

def plot(demanda, amplitude: int = 12000, titulo: str = "") -> Figure:
  
  dados = demanda.dados
  
  with plt.style.context("ggplot"):
    fig, ax = plt.subplots()
    ax.plot(range(1, len(dados) + 1), dados)
    ax.set_ylim(demanda.centro - amplitude / 2, demanda.centro + amplitude / 2)
    ax.set_xlabel("Trimestre")
    ax.set_ylabel("Demanda")
    ax.set_title(f"Demanda {titulo}")

  return fig

def normalize(string : str):
  return unicodedata.normalize('NFD', string).encode('ascii', 'ignore').decode('ascii')