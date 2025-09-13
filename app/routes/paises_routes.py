from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
from bson import ObjectId
from typing import List, Optional

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

@router.get("/paises/localizacao/{localizacao}")
async def buscar_paises_localizacao(localizacao: str, request: Request):
    collection = get_collection(request)
    try:
        paises = list(collection.find({"localizacao": localizacao}, {'_id': 0}))
        if not paises:
            return JSONResponse(status_code=404, content={"detail": "Nenhum pais na localizacao"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Erro no servidor: {str(e)}"})

@router.get("/paises/linguas/{linguas}")
async def buscar_paises_por_lingua(linguas: str, request: Request):
    collection = get_collection(request)
    try:
        paises = list(collection.find({"linguas": linguas}, {'_id': 0}))
        if not paises:
            return JSONResponse(status_code=404, content={"detail": "Nenhum país com essa linguagem"})
        return {"paises": paises, "detail": "Um ou mais país encontrado"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Erro no servidor: {str(e)}"})
    
@router.get("/paises/moeda/{moeda}")
async def buscar_paises_por_moeda(moeda: str, request: Request):
    collection = get_collection(request)
    try:
        paises = list(collection.find({"moeda": moeda}, {'_id': 0}))
        if not paises:
            return JSONResponse(status_code=404, content={"detail": "Nenhum país com essa moeda"})
        
        return {"paises": paises, "detail": "Um ou mais país encontrado"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Erro no servidor: {str(e)}"})

@router.get("/paises/filtrar")
async def buscar_paises_filtrados(
    request: Request,
    localizacao: Optional[str] = Query(None),
    linguas: Optional[str] = Query(None)
):
    collection = get_collection(request)
    filtro = {}
    if localizacao:
        filtro["localizacao"] = localizacao
    if linguas:
        filtro["linguas"] = linguas
    if not filtro:
        return JSONResponse(
            status_code=400,
            content={"detail": "Forneça pelo menos um critério de busca (localizacao ou linguas)."}
        )
    try:
        paises = list(collection.find(filtro, {'_id': 0}))
        if not paises:
            return JSONResponse(status_code=404, content={"detail": "Nenhum país encontrado com os critérios fornecidos."})     
        return {"paises": paises, "detail": "Um ou mais países encontrados."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Erro no servidor: {str(e)}"})


    