from fastapi import FastAPI
from routes import usuarios, login, grupos_viagem



app = FastAPI()

app.include_router(usuarios.router)
app.include_router(login.router)
app.include_router(grupos_viagem.router)

@app.get("/")
def home():
    return {"mensagem": "API funcionando"}