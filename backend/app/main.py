from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # porta padrão do Vite (CRA usa 3000)
    allow_methods=["*"],
    allow_headers=["*"],
)

from routers import demandas_router

app.include_router(demandas_router)

@app.get("/")
async def home():
    return {"message": "Teste"}