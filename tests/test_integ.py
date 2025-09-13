from fastapi.testclient import TestClient
from main import app
import os
os.environ["TESTING"] = "1"

def test_buscar_pais_existente():
    with TestClient(app) as client:
        novo_pais = {
            "nome": "None",
            "localizacao": "None",
            "habitantes": 1,
            "linguas": "None",
            "capital": "None",
            "moeda": "None"
        }
        create_response = client.post("/", json=novo_pais)
        assert create_response.status_code in (200, 201)

        pais_id = create_response.json()

        response = client.get(f"/{pais_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "None"
        assert data["capital"] == "None"

def test_criar_e_buscar_pais():
    with TestClient(app) as client:
        novo_pais = {
            "nome": "Teste",
            "localizacao": "Teste",
            "habitantes": 123456,
            "linguas": "Teste",
            "capital": "Teste",
            "moeda": "Teste"
        }
        response = client.post("/", json=novo_pais)
        assert response.status_code == 200 or response.status_code == 201
        data = response.json()

        response = client.get("/buscar_todos/")
        assert response.status_code == 200
        paises = response.json()["paises"]
        assert any(p["nome"] == "Teste" for p in paises)

def test_atualizar_e_deletar_pais():
    with TestClient(app) as client:
        novo_pais = {
            "nome": "Update",
            "localizacao": "Update",
            "habitantes": 654321,
            "linguas": "Update",
            "capital": "Update",
            "moeda": "Update"
        }
        response = client.post("/", json=novo_pais)
        assert response.status_code == 200 or response.status_code == 201
        pais_id = response.json()

        pais_atualizado = {
            "nome": "Updated",
            "localizacao": "Updated",
            "habitantes": 654322,
            "linguas": "Updated",
            "capital": "Updated",
            "moeda": "Updated"
        }
        response = client.put(f"/{pais_id}", json=pais_atualizado)
        assert response.status_code == 200
        assert response.json()["paises_atualizados"] == 1

        response = client.delete(f"/{pais_id}")
        assert response.status_code == 200
        assert f"País deletado com sucesso: ID: {pais_id}, Nome: Updated" in response.json()["mensagem"]
    
def test_buscar_pais_inexistente():
    with TestClient(app) as client:
        response = client.get("/000000000000000000000000")
        assert response.status_code == 404
        assert response.json()["detail"] == "Pais nao encontrado"

def test_deletar_pais_inexistente():
    with TestClient(app) as client:
        response = client.delete("/000000000000000000000000")
        assert response.status_code == 404
        assert response.json()["detail"] == "Pais nao encontrado"

def test_atualizar_pais_inexistente():
    with TestClient(app) as client:
        pais_atualizado = {
            "nome": "NonExistent",
            "localizacao": "Nowhere",
            "habitantes": 1,
            "linguas": ["None"],  
            "capital": "None",
            "moeda": "None"
        }

        response = client.put("/000000000000000000000000", json=pais_atualizado)
        assert response.status_code == 404
        assert response.json()["detail"] == "Pais nao encontrado"

def test_buscar_todos_paises_vazio():
    with TestClient(app) as client:
        app.db["paises_testes"].delete_many({})
        response = client.get("/buscar_todos/")
        assert response.status_code == 200
        assert response.json()["paises"] == []

def test_criar_pais_valido():
    with TestClient(app) as client:
        novo_pais = {
            "nome": "None",
            "localizacao": "None",
            "habitantes": 123456,
            "linguas": "None",
            "capital": "None",
            "moeda": "None"
        }
        response = client.post("/", json=novo_pais)
        assert response.status_code in (200, 201)
        data = response.json()

def test_criar_pais_invalido():
    with TestClient(app) as client:
        novo_pais = {
            "nome": "None",
            "localizacao": "None",
            "habitantes": -1,
            "linguas": "None",
            "capital": "None",
            "moeda": "None"
        }
        response = client.post("/", json=novo_pais)
        assert response.status_code == 422
        data = response.json()

def test_buscar_pais_id_invalido():
    with TestClient(app) as client:
        response = client.get("/123")
        assert response.status_code == 422
        assert response.json()["detail"] == "ID inválido"

def test_deletar_pais_existente(): 
    with TestClient(app) as client:
        novo_pais = {
            "nome": "None",
            "localizacao": "None",
            "habitantes": 1,
            "linguas": "None",
            "capital": "None",
            "moeda": "None"
        }
        create_response = client.post("/", json=novo_pais)
        assert create_response.status_code in (200, 201)

        pais_id = create_response.json()

        response = client.delete(f"/{pais_id}")
        assert response.status_code == 200
        data = response.json()

def test_deletar_pais_id_invalido():
    with TestClient(app) as client:
        response = client.delete("/123")
        assert response.status_code == 422
        assert response.json()["detail"] == "ID inválido"

def test_atualizar_id_invalido():
    with TestClient(app) as client:
        pais_atualizado = {
            "nome": "NonExistent",
            "localizacao": "Nowhere",
            "habitantes": 1,
            "linguas": ["None"],  
            "capital": "None",
            "moeda": "None"
        }

        response = client.put("/123", json=pais_atualizado)
        assert response.status_code == 422
        assert response.json()["detail"] == "ID inválido"

def test_deletar_pais_ja_deletado():
    with TestClient(app) as client:
        novo_pais = {
            "nome": "None",
            "localizacao": "None",
            "habitantes": 1,
            "linguas": "None",
            "capital": "None",
            "moeda": "None"
        }
        create_response = client.post("/", json=novo_pais)
        assert create_response.status_code in (200, 201)
        pais_id = create_response.json()

        response = client.delete(f"/{pais_id}")
        assert response.status_code == 200

        response = client.delete(f"/{pais_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Pais nao encontrado"

def test_criar_pais_com_tipo_de_dado_incorreto():
    with TestClient(app) as client:
        novo_pais = {
            "nome": "None",
            "localizacao": "None",
            "habitantes": "texto", 
            "linguas": "None",
            "capital": "None",
            "moeda": "None"
        }
        response = client.post("/", json=novo_pais)
        assert response.status_code == 422

def test_criar_pais_com_campos_ausentes():
    with TestClient(app) as client:
        novo_pais = {
            "nome": "None",
            "localizacao": "None",
            "habitantes": 1,
            "linguas": "None",
            "capital": "None"
        }
        response = client.post("/", json=novo_pais)
        assert response.status_code == 422

def test_conexao_banco_dados():
    with TestClient(app) as client:
        response = client.get("/buscar_todos/")
        assert response.status_code == 200
        assert "paises" in response.json()