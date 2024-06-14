from fastapi import APIRouter, HTTPException, Path, Request
from fastapi import Depends
from fastapi.security import HTTPBearer
from bd.database import SessionLocal, get_db
from user_jwt import validateToken
from sqlalchemy.orm import Session
from schemas.schemas import MovieSchema, Response, MovieSchema

from bd import crud

#Creamos un router, que es un conjunto de rutas agrupadas
router = APIRouter(
     prefix='/v1/api'
)


#Cabe mencionar que vamos a usar constantemente dos parametros
#"request" el cual es la entrada y sera acorde con el esquema "mostrar en SWAGGER"
#Y "DB" que es de tipo sesion y de la cual depende la conexion de nuestra bd


#Clase que genera el token para ser consumido por las apis
class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data['email'] != 'jcarlosgarcial@outlook.com':
            raise HTTPException(status_code=403, detail='Credenciales incorrectas')
  
#Se usaran las funciones que creamos en el archivo crud.py       

#Creamos la ruta con la que se crearan
@router.post("/create")
async def create_movie_service(request: MovieSchema, db: Session = Depends(get_db)):
    crud.create_movie(db, movie=request)
    print(request)
    return Response(status="Ok", code="200", message="Pelicula creada correctamente", result=request).dict(
        exclude_none=True)


#Retornamos la respuesta con el schema de responde


@router.get("/")
async def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), dependencies=[Depends(BearerJWT())]):
    _movies = crud.get_movie(db, skip, limit)
    return Response(status="Ok", code="200", message="Resultados obtenidos", result=_movies)


@router.patch("/update")
async def update_movies(request: MovieSchema, db: Session = Depends(get_db)):
    try:
        _movie = crud.update_movies(db, movies_id=request.id, title=request.title, overview=request.overview,
                                    year=request.year, rating=request.rating, category=request.category)
        return Response(status="Ok", code="200", message="Resultados obtenidos", result=_movie)
    except Exception as e:
        return Response(
            status="malo",
            code="",
            message="eliminado fallado"
        )


@router.delete("/delete")
async def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    try:
        _movie = crud.remove_movies(db, _movie=movie_id)
        return Response(status="Ok", code="200", message="Pelicula borrada correctamente", result=_movie)
    except Exception as e:
        return Response(
            status="malo",
            code="",
            message="eliminado fallado"
        )
