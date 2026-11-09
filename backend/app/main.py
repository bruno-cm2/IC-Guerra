from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routers import demandas_router

app = FastAPI()

app.include_router(demandas_router, prefix="/api")

DIST = Path(__file__).parent / "dist"

app.mount("/assets", StaticFiles(directory=DIST / "assets"), name="assets")

@app.get("/{caminho:path}")
async def spa(caminho: str):
    arquivo = DIST / caminho
    if caminho and arquivo.is_file():
        return FileResponse(arquivo)
    return FileResponse(DIST / "index.html")