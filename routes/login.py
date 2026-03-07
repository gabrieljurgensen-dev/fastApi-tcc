from fastapi import APIRouter
from database import conectar_db
from utils.security import verificar_senha

router = APIRouter()

@router.post("/login")
def login(email: str, senha: str):

    conexao = conectar_db()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
    usuario = cursor.fetchone()

    if not usuario:
        cursor.close()
        conexao.close()
        return {"erro": "Usuário não encontrado"}

    if not verificar_senha(senha, usuario["senha_hash"]):
        cursor.close()
        conexao.close()
        return {"erro": "Senha incorreta"}

    cursor.close()
    conexao.close()

    return {"mensagem": "Login realizado com sucesso"}