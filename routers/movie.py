from fastapi import FastAPI, Body, Path, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional
from models.movie import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder

from fastapi import APIRouter
from user_jwt import validateToken
from sqlalchemy.orm import Session

routerMovie = APIRouter()

class BearerJWT ( HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data ['email'] != 'jcarlosgarcial@outlook.com':
            raise HTTPException(status_code=403, detail='Credenciales incorrectas')
        

class Movie(BaseModel):     
      id: Optional[int] = None
      title : str = Field (default='Pelic', min_length=5, max_length=200)
      overview: str = Field (default='descripcion peli', min_length=15, max_length=200)
      year: int = Field (default=2023)
      rating: float = Field (ge=1, le=0)
      category: str = Field(min_length=3, max_length=100, default='aca categoria')




@routerMovie.get('/movies', tags=['Movies'], dependencies=[Depends(BearerJWT())])  
def get_movies():
      db = Session()
      data = db.query(ModelMovie.all())
      return JSONResponse(content=jsonable_encoder(data))





