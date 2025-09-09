from pydantic import BaseModel, Field
from typing import Optional, List, Union

class Pais(BaseModel):
    nome: str
    localizacao: str
    habitantes: int = Field(gt=0)
    linguas: Union[str, List[str]]
    capital: str
    moeda: str
    pontos_turisticos: Optional[List[str]] = None
    culinaria: Optional[List[str]] = None
    clima: Optional[str] = None
    idh: Optional[float] = None
    avaliacao: Optional[float] = None

    

