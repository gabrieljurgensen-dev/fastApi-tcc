from fastapi import APIRouter, HTTPException, Depends
from database import conectar_db
from utils.auth import get_usuario_logado

router = APIRouter()


@router.get("/chat")
def listar_chat(usuario_id: int = Depends(get_usuario_logado)):
    conexao = conectar_db()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_chat, id_grupo, pergunta, resposta, data_interacao
        FROM chat_ia
        WHERE id_usuario = %s
        ORDER BY data_interacao DESC
        LIMIT 50
    """, (usuario_id,))

    dados = cursor.fetchall()

    cursor.close()
    conexao.close()
    return dados


@router.post("/chat")
def criar_chat(
    pergunta: str,
    resposta: str,
    id_grupo: int = None,
    usuario_id: int = Depends(get_usuario_logado)
):
    if not pergunta.strip():
        raise HTTPException(status_code=400, detail="Pergunta vazia")

    conexao = conectar_db()
    cursor = conexao.cursor()

    if id_grupo:
        cursor.execute(
            "SELECT 1 FROM grupo_membros WHERE id_grupo=%s AND id_usuario=%s",
            (id_grupo, usuario_id)
        )
        if cursor.fetchone() is None:
            cursor.close()
            conexao.close()
            raise HTTPException(status_code=403, detail="Você não pertence ao grupo")

    cursor.execute("""
        INSERT INTO chat_ia (id_usuario, id_grupo, pergunta, resposta)
        VALUES (%s, %s, %s, %s)
    """, (usuario_id, id_grupo, pergunta, resposta))

    conexao.commit()
    cursor.close()
    conexao.close()

    return {"mensagem": "Conversa salva"}