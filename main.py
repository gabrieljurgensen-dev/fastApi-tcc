from fastapi import FastAPI
from routes import usuarios
from routes import login

app = FastAPI()

app.include_router(usuarios.router)
app.include_router(login.router)

@app.get("/")
def home():
    return {"mensagem": "API funcionando"}