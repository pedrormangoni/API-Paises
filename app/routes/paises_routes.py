from fastapi import APIRouter, Request 
from bson import ObjectId
from typing import List

from fastapi.responses import JSONResponse
from app.models.paises import Pais
import os

router = APIRouter(prefix="", tags=['paises']) 

def get_collection(request):
    if os.getenv("TESTING") == "1":
        return request.app.db["paises_testes"]
    return request.app.db["paises"]

@router.get("/buscar_todos/")
async def buscar_todos_paises(request: Request):
    collection = get_collection(request)
    paises = list(collection.find())
    for pais in paises:
        pais["_id"] = str(pais["_id"])
    return {"paises": paises}

@router.post("/")
async def criar_pais(pais: Pais, request: Request):
    collection = get_collection(request)
    resultado = collection.insert_one(pais.model_dump())
    return str(resultado.inserted_id)

@router.put("/{pais_id}") 
async def atualizar_pais(pais_id: str, pais: Pais, request: Request):   
    collection = get_collection(request)
    try:
        _pais_id = ObjectId(pais_id)
    except Exception:
        return JSONResponse(status_code=422, content={"detail": "ID inválido"})
    result = collection.update_one({"_id": _pais_id}, {"$set": pais.model_dump()})
    if result.matched_count == 0:
        return JSONResponse(status_code=404, content={"detail": "Pais nao encontrado"})
    return {"paises_atualizados": result.modified_count}

@router.delete("/{pais_id}") 
async def deletar_pais(pais_id: str, request: Request):     
    collection = get_collection(request)
    try:
        object_id = ObjectId(pais_id)
    except Exception:
        return JSONResponse(status_code=422, content={"detail": "ID inválido"})
    
    resultado = collection.find_one({"_id": object_id})
    if not resultado:
        return JSONResponse(status_code=404, content={"detail": "Pais nao encontrado"})

    collection.delete_one({"_id": object_id})
    return {"mensagem": f"País deletado com sucesso: ID: {pais_id}, Nome: {resultado['nome']}"}

@router.get("/{pais_id}")
async def buscar_pais(pais_id: str, request: Request):
    collection = get_collection(request)
    try:
        _pais_id = ObjectId(pais_id)
    except Exception:
        return JSONResponse(status_code=422, content={"detail": "ID inválido"})
    
    pais = collection.find_one({"_id": _pais_id})
    if not pais:
        return JSONResponse(status_code=404, content={"detail": "Pais nao encontrado"})
    pais["_id"] = str(pais["_id"])
    return pais
