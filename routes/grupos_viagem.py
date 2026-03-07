from fastapi import APIRouter, HTTPException, Depends
from database import conectar_db
from utils.auth import get_usuario_logado
router = APIRouter()
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer() 

@router.get("/grupos")
def listar_grupos():
    conexao = conectar_db()
    cursor = conexao.cursor(dictionary=True)
    sql = """
    SELECT g.id_grupo, g.nome_grupo, g.destino_principal, g.data_inicio, g.data_fim, u.nome AS criador
    FROM grupos_viagem g
    JOIN usuarios u ON g.criado_por = u.id_usuario
    """
    cursor.execute(sql)
    grupos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return grupos

@router.get("/grupos/{id_grupo}")
def buscar_grupo_por_id(id_grupo: int):
    conexao = conectar_db()
    cursor = conexao.cursor(dictionary=True)
    sql = """
    SELECT g.id_grupo, g.nome_grupo, g.destino_principal, g.data_inicio, g.data_fim, u.nome AS criador
    FROM grupos_viagem g
    JOIN usuarios u ON g.criado_por = u.id_usuario
    WHERE g.id_grupo = %s
    """
    cursor.execute(sql, (id_grupo,))
    grupo = cursor.fetchone()
    cursor.close()
    conexao.close()
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    return grupo

@router.get("/grupos/buscar")
def buscar_grupo_por_nome(nome: str = None):
    conexao = conectar_db()
    cursor = conexao.cursor(dictionary=True)
    sql = """
    SELECT g.id_grupo, g.nome_grupo, g.destino_principal, g.data_inicio, g.data_fim, u.nome AS criador
    FROM grupos_viagem g
    JOIN usuarios u ON g.criado_por = u.id_usuario
    """
    params = ()
    if nome:
        sql += " WHERE g.nome_grupo LIKE %s"
        params = (f"%{nome}%",)
    cursor.execute(sql, params)
    grupos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return grupos

@router.post("/grupos")
def criar_grupo(nome_grupo: str, destino_principal: str, usuario_id: int = Depends(get_usuario_logado)):
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO grupos_viagem(nome_grupo, destino_principal, criado_por) VALUES (%s, %s, %s)",
        (nome_grupo, destino_principal, usuario_id)
    )
    conexao.commit()
    cursor.close()
    conexao.close()
    return {"mensagem": "Grupo criado com sucesso", "usuario_id": usuario_id}

@router.put("/grupos/{id_grupo}")
def atualizar_grupo(id_grupo: int, nome_grupo: str, destino_principal: str):
    conexao = conectar_db()
    cursor = conexao.cursor()
    sql = """
    UPDATE grupos_viagem
    SET nome_grupo=%s, destino_principal=%s
    WHERE id_grupo=%s
    """
    cursor.execute(sql, (nome_grupo, destino_principal, id_grupo))
    conexao.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    cursor.close()
    conexao.close()
    return {"mensagem": "Grupo atualizado"}

@router.delete("/grupos/{id_grupo}")
def deletar_grupo(id_grupo: int):
    conexao = conectar_db()
    cursor = conexao.cursor()
    sql = "DELETE FROM grupos_viagem WHERE id_grupo=%s"
    cursor.execute(sql, (id_grupo,))
    conexao.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    cursor.close()
    conexao.close()
    return {"mensagem": "Grupo deletado"}