from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar("T")


class MovieSchema(BaseModel):
    id : Optional[int] = None
    title :Optional[str] = None
    overview : Optional[str] = None
    year : Optional[int] = None
    rating : Optional[float] = None
    category : Optional[str] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "ejemplo":
                {
                    "id": 0,
                    "title": "Toy Story 3",
                    "overview": "Buenas",
                    "year": "2024",
                    "rating": "1.0",
                    "category": "Accion"

                }
        }

class Response(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[T]
