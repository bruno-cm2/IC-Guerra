from fastapi import FastAPI

app = FastAPI()

from routers.demandas_rota import demandas_router

app.include_router(demandas_router)

@app.get("/")
async def home():
    return {"message": "Teste"}