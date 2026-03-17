from fastapi import APIRouter, HTTPException, Depends
from database import conectar_db
from utils.auth import get_usuario_logado

router = APIRouter()

@router.get("/roteiros")
def listar_roteiros():
    conexao = conectar_db()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id_roteiro, id_grupo, titulo, descricao, data_criacao from roteiros")
    roteiros = cursor.fetchall()
    cursor.close()
    conexao.close()
    return roteiros

@router.get("/roteiros/{id_roteiro}")
def buscar_roteiro(id_roteiro: int):
    conexao = conectar_db()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id_roteiro, id_grupo, titulo, descricao, data_criacao from roteiros WHERE id_roteiro=%s", (id_roteiro,))
    roteiro = cursor.fetchone()
    cursor.close()
    conexao.close()
    if roteiro is None:
        raise HTTPException(status_code=404, detail="Roteiro não encontrado")
    return roteiro

@router.post("/roteiros")
def criar_roteiro(id_grupo: int, titulo: str, descricao: str, usuario_id: int = Depends(get_usuario_logado)):
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute("SELECT 1 FROM grupos_viagem WHERE id_grupo=%s", (id_grupo,))
    if cursor.fetchone() is None:
        cursor.close()
        conexao.close()
        raise HTTPException(status_code=404, detail="Grupo não existe")

    cursor.execute(
        "SELECT 1 FROM grupo_membros WHERE id_grupo=%s AND id_usuario=%s",
        (id_grupo, usuario_id)
    )
    if cursor.fetchone() is None:
        cursor.close()
        conexao.close()
        raise HTTPException(status_code=403, detail="Usuário não pertence ao grupo")
    
    cursor.execute(
        "INSERT INTO roteiros (id_grupo, titulo, descricao) VALUES (%s, %s, %s)",
        (id_grupo, titulo, descricao)
    )

    conexao.commit()
    cursor.close()
    conexao.close()

    return {"mensagem": "Roteiro criado com sucesso"}

@router.put("/roteiros/{id_roteiro}")
def atualizar_roteiro(id_roteiro: int, titulo: str, descricao: str, usuario_id: int = Depends(get_usuario_logado)):
    conexao = conectar_db()
    cursor = conexao.cursor()

    cursor.execute("SELECT id_grupo FROM roteiros WHERE id_roteiro=%s", (id_roteiro,))
    resultado = cursor.fetchone()

    if resultado is None:
        cursor.close()
        conexao.close()
        raise HTTPException(404, "Roteiro não encontrado")
    id_grupo = resultado[0]

    cursor.execute(
        "SELECT 1 FROM grupo_membros WHERE id_grupo=%s AND id_usuario=%s",
        (id_grupo, usuario_id)
    )
    if cursor.fetchone() is None:
        cursor.close()
        conexao.close()
        raise HTTPException(403, "Sem permissão")

    cursor.execute(
        "UPDATE roteiros SET titulo=%s, descricao=%s WHERE id_roteiro=%s",
        (titulo, descricao, id_roteiro)
    )

    conexao.commit()
    cursor.close()
    conexao.close()
    return {"mensagem": "Roteiro atualizado"}

@router.delete("/roteiros/{id_roteiro}")
def deletar_roteiro(id_roteiro: int, usuario_id: int = Depends(get_usuario_logado)):
    conexao = conectar_db()
    cursor = conexao.cursor()

    cursor.execute("SELECT id_grupo FROM roteiros WHERE id_roteiro=%s", (id_roteiro,))
    resultado = cursor.fetchone()

    if resultado is None:
        cursor.close()
        conexao.close()
        raise HTTPException(status_code=404, detail="Roteiro não encontrado")
    id_grupo = resultado[0]

    cursor.execute(
        "SELECT 1 FROM grupo_membros WHERE id_grupo=%s AND id_usuario=%s",
        (id_grupo, usuario_id)
    )
    if cursor.fetchone() is None:
        cursor.close()
        conexao.close()
        raise HTTPException(status_code=403, detail="Sem permissão")

    cursor.execute("DELETE FROM roteiros WHERE id_roteiro=%s", (id_roteiro,))
    conexao.commit()
    cursor.close()
    conexao.close()
    return {"mensagem": "Roteiro deletado com sucesso"}