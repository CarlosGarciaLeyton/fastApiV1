import movies
from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from fastapi.security import HTTPBearer
from app.models.movie import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from app.user_jwt import validateToken
from sqlalchemy.orm import Session


routerMovie = APIRouter(
    prefix='/v1/api'
)


class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data['email'] != 'jcarlosgarcial@outlook.com':
            raise HTTPException(status_code=403, detail='Credenciales incorrectas')


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default='Pelic', min_length=5, max_length=200)
    overview: str = Field(default='descripcion peli', min_length=15, max_length=200)
    year: int = Field(default=2023)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=3, max_length=100, default='aca categoria')


@routerMovie.get('/movies', tags=['Movies'], dependencies=[Depends(BearerJWT())])
def get_movies():
    db = Session()
    data = db.query(ModelMovie).all()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    return JSONResponse(content=jsonable_encoder(data))


@routerMovie.get('/movies/{id}', tags=['Movies'], status_code=200, dependencies=[Depends(BearerJWT())])
def get_movies(id: int = Path(ge=1, le=100)):
    db = Session()
    print (db)
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))


@routerMovie.get('/movies/', tags=['Movies'], dependencies=[Depends(BearerJWT())])
def get_movies_by_category(category: str = Query(min_length=3, max_length=15)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.category == category).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(data))


@routerMovie.post('/movies', tags=['Movies'], status_code=201)
def create_movie(movie: Movie):
    db = Session()
    newMovie = ModelMovie(**movie.dict())
    db.add(newMovie)
    db.commit()
    return JSONResponse(status_code=201, content={'message': 'Se agrego la nueva pelicula','movie': [movie.model_dump() for m in movies]})


@routerMovie.put('/movies/{id}', tags=['Movies'], status_code=200, dependencies=[Depends(BearerJWT())])
def update_movie(id: int, movie: Movie):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    print('entro')
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no disponible'})
    data.title = movie.title
    data.overview = movie.overview
    data.year = movie.year
    data.rating = movie.rating
    data.category = movie.category
    db.commit()
    return JSONResponse(content={'message': 'Pelicula modificada'})


@routerMovie.delete('/movies/{id}', tags=['Movies'], status_code=200, dependencies=[Depends(BearerJWT())])
def delete_movie(id: int):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no disponible'})
    db.delete(data)
    db.commit()
    return JSONResponse(content={'message': 'Pelicula eliminada', 'data': jsonable_encoder(data)})
