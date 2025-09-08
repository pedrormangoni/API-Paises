from fastapi import APIRouter, Request 
from bson import ObjectId
from typing import List
from models.paises import Pais

router = APIRouter(prefix="", tags=['paises']) 

# Rota para testar a conexão com o banco de dados
@router.get("/testar_conexao")
async def testar_conexao(request: Request):
    try:
        colecoes = request.app.db.list_collection_names()
        return {"status": "conectado", "colecoes": colecoes}
    except Exception as e:
        return {"status": "erro", "detalhe": str(e)}

# Rota para buscar todas os paises cadastrados
@router.get("/buscar_todos/")
async def buscar_todos_paises(request: Request):
    collection = request.app.db["paises"]
    paises = list(collection.find())
    for pais in paises:
        pais["_id"] = str(pais["_id"])
    return {"paises": paises}

# Rota para inserir um novo pais
@router.post("/")
async def criar_pais(pais: Pais, request: Request):
     # Obtém a coleção 'paises' do banco de dados
     collection = request.app.db["paises"]
       # Insere o pais recebida no banco
     resultado = collection.insert_one(pais.model_dump())
    # Retorna apenas o id gerado
     return str(resultado.inserted_id)

@router.put("/{pais_id}") 
async def atualizar_pais(pais_id: str, pais: Pais, request: Request):   
      # Obtém a coleção 'paises' do banco de dados   
      paises_collection = request.app.db.paises   
      # Converte o id recebido para o tipo ObjectId do MongoDB   
      _pais_id = ObjectId(pais_id)   
      # Atualiza o pais com os novos dados   
      result = paises_collection.update_one({"_id": _pais_id}, {"$set": pais.model_dump()})   
      # Retorna quantos paises foram atualizadas   
      return {"series_atualizadas": result.modified_count}

@router.delete("/{pais_id}") 
async def deletar_pais(pais_id: str, request: Request):     
      paises_collection = request.app.db.paises  

      _pais_id = ObjectId(pais_id)

      resultado = paises_collection.find_one({"_id": _pais_id})

      nome = resultado["nome"] if resultado else "não encontrado"
      
      return {"mensagem": f"Pais deletado com sucesso: ID: {pais_id}, Nome: {nome}"}



