from pydantic import BaseModel, Field
from typing import Optional, List, Union

class Pais(BaseModel):
    nome: str
    continente: str
    habitantes: int = Field(gt=0)
    linguas: Union[str, List[str]]
    moeda: str
    km2: float = Field(gt=0)
    longitude: float
    latitude: float
    clima: Optional[str] = None
    fuso_horario: Optional[str] = None
    


    

