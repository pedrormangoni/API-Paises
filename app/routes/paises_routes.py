from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
from bson import ObjectId
from typing import List, Optional
import unicodedata

from fastapi.responses import JSONResponse
from app.models.paises import Pais
import os

def filtrar_input(texto: str) -> str:
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    return texto

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

@router.get("/paises/continente/{continente}")
async def buscar_paises_continente(continente: str, request: Request):
    collection = get_collection(request)
    texto_filtrado = filtrar_input(continente)
    continente = texto_filtrado.capitalize()
    try:
        paises = list(collection.find({"continente": {"$regex": continente, "$options": "i"}}, {'_id': 0}))
        if not paises:
            return JSONResponse(status_code=404, content={"detail": "Nenhum pais no continente"})
        return JSONResponse(status_code=200, content={"paises": paises})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Erro no servidor: {str(e)}"})

@router.get("/paises/linguas/{linguas}")
async def buscar_paises_por_lingua(linguas: str, request: Request):
    collection = get_collection(request)
    texto_filtrado = filtrar_input(linguas)
    linguas = texto_filtrado.capitalize()
    try:
        paises = list(collection.find({"linguas": {"$regex": linguas, "$options": "i"}}, {'_id': 0}))
        if not paises:
            return JSONResponse(status_code=404, content={"detail": "Nenhum país com essa linguagem"})
        return {"paises": paises, "detail": "Um ou mais país encontrado"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Erro no servidor: {str(e)}"})
    
@router.get("/paises/moeda/{moeda}")
async def buscar_paises_por_moeda(moeda: str, request: Request):
    collection = get_collection(request)
    texto_filtrado = filtrar_input(moeda)
    moeda = texto_filtrado.capitalize()
    try:
        paises = list(collection.find({"moeda": {"$regex": moeda , "$options": "i"}}, {'_id': 0}))
        if not paises:
            return JSONResponse(status_code=404, content={"detail": "Nenhum país com essa moeda"})
        
        return {"paises": paises, "detail": "Um ou mais país encontrado"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Erro no servidor: {str(e)}"})

@router.get("/paises/filtrar")
async def buscar_paises_filtrados(
    request: Request,
    continente: Optional[str] = Query(
        None, description="Nome do continente para filtrar."
    ),
    linguas: Optional[str] = Query(
        None, description="Língua(s) falada(s) no país."
    ),
    km2: Optional[float] = Query(
        None, gt=0, description="Área do país em km², deve ser um valor positivo."
    ),
    habitantes: Optional[int] = Query(
        None, gt=0, description="Número de habitantes, deve ser um valor inteiro positivo."
    ),
    longitude: Optional[float] = Query(
        None, description="Coordenada de longitude do país."
    ),
    latitude: Optional[float] = Query(
        None, description="Coordenada de latitude do país."
    ),
    clima: Optional[str] = Query(
        None, description="Tipo de clima predominante."
    ),
    fuso_horario: Optional[str] = Query(
        None, description="Fuso horário do país."
    )
):
    collection = get_collection(request)
    filtro = {}
    if continente:
        filtro["continente"] = continente
    if linguas:
        filtro["linguas"] = {"$in": linguas.split(',')} 
    if km2:
        filtro["km2"] = km2
    if habitantes:
        filtro["habitantes"] = habitantes
    if longitude:
        filtro["longitude"] = longitude
    if latitude:
        filtro["latitude"] = latitude
    if clima:
        filtro["clima"] = clima
    if fuso_horario:
        filtro["fuso_horario"] = fuso_horario
    if not filtro:
        return JSONResponse(
            status_code=400,
            content={"detail": "Forneça pelo menos um critério de busca."}
        )
    try:
        paises = list(collection.find(filtro, {'_id': 0}))
        if paises:
            return {"paises": paises, "detail": f"{len(paises)} país(es) encontrado(s)."}
        else:
            return JSONResponse(
                status_code=404, 
                content={"detail": "Nenhum país encontrado com os critérios fornecidos."}
            )
    except Exception as e:
        print(f"Erro ao buscar países: {e}")
        return JSONResponse(
            status_code=500, 
            content={"detail": "Erro interno no servidor."}
        )


    