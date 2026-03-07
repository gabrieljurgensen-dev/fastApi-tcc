from fastapi import APIRouter, HTTPException
from database import conectar_db
from utils.security import verificar_senha, criar_token

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
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if not verificar_senha(senha, usuario["senha_hash"]):
        cursor.close()
        conexao.close()
        raise HTTPException(status_code=401, detail="Senha incorreta")
    usuario_id = usuario["id_usuario"]
    token = criar_token(usuario_id)
    cursor.close()
    conexao.close()
    return {
        "mensagem": "Login realizado com sucesso",
        "usuario_id": usuario_id,
        "token": token
    }