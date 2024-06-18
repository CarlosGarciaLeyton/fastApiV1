from fastapi import APIRouter, HTTPException, Path, Request
from fastapi import Depends
from fastapi.security import HTTPBearer
from app.bd.database import SessionLocal, get_db
from app.user_jwt import validateToken
from sqlalchemy.orm import Session
from app.schemas.schemas import MovieSchema, Response, MovieSchema
from fastapi.encoders import jsonable_encoder

from app.bd import crud

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
    return Response(status="Ok", code="200", message="Pelicula creada correctamente", result=request).dict(
        exclude_none=True)


#Retornamos la respuesta con el schema de responde
@router.get("/")
async def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     dependencies=[Depends(BearerJWT())]):
    _movies = crud.get_movie(db, skip, limit)
    if not _movies: #opcion 1
        return Response(status="NoOk", code="200", message="Lista vacia", result=f"Lista vacia")

    else:
        return Response(status="Ok", code="200", message="Resultados obtenidos", result=jsonable_encoder(_movies))
    

@router.patch("/update")
async def update_movies(request: MovieSchema, db: Session = Depends(get_db)):
    try:
        _movie = crud.update_movies(db, movies_id=request.id, title=request.title, overview=request.overview,
                                    year=request.year, rating=request.rating, category=request.category)
        return Response(status="Ok", code="200", message="Resultados obtenidos", result=jsonable_encoder(_movie))
    except Exception as e:
        return Response(
            status="malo",
            code="304",
            message="eliminado fallado"
        )


@router.delete("/delete")
async def delete_movie(movies_id: int, db: Session = Depends(get_db)):
    try:
        _movie: object = await crud.remove_movies(db, movies_id=movies_id)
        return Response(status="Ok", code="200", message="Pelicula borrada", result=jsonable_encoder(_movie.__dict__))
    except Exception as e:
        return Response(
            status="malo",
            code="422",
            message="Fallo al eliminar"
        )
