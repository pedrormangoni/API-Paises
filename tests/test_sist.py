from fastapi.testclient import TestClient
from main import app
import os
os.environ["TESTING"] = "1"

def test_fluxo_completo_pais():
    """
    Testa o fluxo completo de um pais na API:
    1. Cria um novo pais
    2. Busca o pais criado para verificar se ele existe
    3. Atualiza os dados do pais
    4. Busca o pais atualizado para verificar a modificação
    5. Deleta o pais
    6. Tenta buscar o pais novamente para confirmar que foi deletado
    """
    with TestClient(app) as client:
        # 1. Cria um novo pais
        novo_pais = {
            "nome": "Brazil",
            "localizacao": "South America",
            "habitantes": 212000000,
            "linguas": "Portuguese",
            "capital": "Brasília",
            "moeda": "Real"
        }
        response = client.post("/", json=novo_pais)
        assert response.status_code == 200 or response.status_code == 201
        pais_id = response.json()
        print(f"País criado com ID: {pais_id}")

        # 2. Busca o pais criado para verificar
        response = client.get(f"/{pais_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Brazil"

        # 3. Atualiza o pais
        pais_atualizado = {
            "nome": "Brasil",
            "localizacao": "América do Sul",
            "habitantes": 212000000,
            "linguas": "Portugues",
            "capital": "Brasília",
            "moeda": "Real"
        }
        response = client.put(f"/{pais_id}", json=pais_atualizado)
        assert response.status_code == 200
        assert response.json()["paises_atualizados"] == 1

        # 4. Busca o pais atualizado para verificar
        response = client.get(f"/{pais_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Brasil"
        assert data["linguas"] == "Portugues"

        # 5. Deleta o pais
        response = client.delete(f"/{pais_id}")
        assert response.status_code == 200
        assert f"País deletado com sucesso: ID: {pais_id}, Nome: Brasil" in response.json()["mensagem"]

        # 6. Tenta buscar o pais para confirmar a exclusão
        response = client.get(f"/{pais_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Pais nao encontrado"
