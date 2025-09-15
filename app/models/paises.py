from pydantic import BaseModel, Field
from typing import List, Union

class Pais(BaseModel):
    nome: str
    continente: str
    habitantes: int = Field(gt=0)
    linguas: Union[str, List[str]]
    moeda: str
    km2: float = Field(gt=0)
    longitude: float
    latitude: float
    climas: Union[str, List[str]] = None
    fusos_horarios: Union[str, List[str]] = None
    


    

