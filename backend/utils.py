import unicodedata

def normalize(string : str) -> str:
  return unicodedata.normalize('NFD', string).encode('ascii', 'ignore').decode('ascii')