import pytest 
from pydantic import ValidationError
from app.models.paises import Pais
import os
os.environ["TESTING"] = "1"

def test_criar_pais_valido():
    pais = Pais(
        nome="Brasil",
        localizacao="South America",
        habitantes=211000000,
        linguas="Portuguese",
        capital="Brasília",
        moeda="Real",
        pontos_turisticos=["Cristo Redentor", "Praia de Copacabana"],
        culinaria=["Feijoada", "Churrasco"],
        clima="Tropical",
        idh=0.759,
        avaliacao=4.5
    )
    assert pais.nome == "Brasil"
    assert pais.habitantes > 0
    assert pais.idh == 0.759
    assert pais.moeda == "Real"

@pytest.mark.parametrize("habitantes", [0, -1, -100])
def test_criar_pais_invalido_habitantes(habitantes):
    with pytest.raises(ValueError):
        Pais(
            nome="País Inválido",
            localizacao="Unknown",
            habitantes=habitantes,  # Validando informacao do model -> habitantes: int = Field(gt=0)
            linguas="Unknown",
            capital="Unknown",
            moeda="Unknown"
        )

def test_criar_pais_informacao_invalida():
    with pytest.raises(ValueError):
        Pais(
            nome="Inválido",
            localizacao=2,
            habitantes="1",
            linguas=2,
            capital=3,
            moeda=4
        )

def test_criar_apenas_obrigatorios():
    novo_pais = Pais(
        nome="Apenas dados obrigatorios",
        localizacao="testes",
        habitantes=1,
        linguas="testes",
        capital="testes",
        moeda="testes"
    )   
    assert novo_pais.nome == "Apenas dados obrigatorios"
    assert novo_pais.pontos_turisticos is None

@pytest.mark.parametrize("campo", ["nome", "localizacao", "habitantes", "linguas", "capital", "moeda"])
def test_criar_sem_campo_obrigatorio(campo):
    novo_pais = {
        "nome": "Argentina",
        "localizacao": "América do Sul",
        "habitantes": 45_000_000,
        "linguas": "Espanhol",
        "capital": "Buenos Aires",
        "moeda": "Peso"
    } 
    novo_pais.pop(campo)
    with pytest.raises(ValidationError):
        Pais(**novo_pais)
