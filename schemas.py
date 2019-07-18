from typing import List
from pydantic.dataclasses import dataclass
from pydantic import BaseModel

class Loc(BaseModel):
    loc:str
    lat:float
    lon:float
    address:str
    city:str
    accuracy:str
