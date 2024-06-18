from sqlalchemy.orm import Session  #La sesion de la BD
from app.models.movie import Movie  #El modelo ORM de nuestra BD
from app.schemas.schemas import MovieSchema  #El esquema del JSON


#creamos la funcion para obtener todas las peliculas
def get_movie(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Movie).offset(skip).limit(limit).all()


#query busca segun el modelo
#skip es el salto o pasos que hace
#limit es la cantidad total de resultados que trae
#la funcion all trae todos los resultados


def get_movies_by_id(db: Session, movies_id: int):
    return db.query(Movie).filter(Movie.id == movies_id).first()


#query busca segun el modelo
#Se hace filtro por el id
#se obtiene el primer resultado

def create_movie(db: Session, movie: MovieSchema):
    _movie = Movie(
        title=movie.title,
        overview=movie.overview,
        year=movie.year,
        rating=movie.rating,
        category=movie.category
    )
    db.add(_movie)
    db.commit()
    db.refresh(_movie)
    return _movie


#Creamos y le damos propiedades
#asignamos cada valor correspondiente del JSON al Modelo
#guardamos en la BD

def remove_movies(db: Session, movies_id: int):
    _movies = get_movies_by_id(db=db, movies_id=movies_id)
    db.delete(_movies)
    db.commit()
    db.refresh(_movies)
    return _movies


#Para eliminar filtramos por el Id
#Eliminamos

def update_movies(db: Session, movies_id: int, title: str, overview: str, year: int, rating: float, category: str):
    _movies = get_movies_by_id(db=db, movies_id=movies_id)
    _movies.title = title
    _movies.overview = overview
    _movies.year = year
    _movies.rating = rating
    _movies.category = category
    db.commit()
    db.refresh(_movies)
    return _movies
#filtramos por id
#reasignamos los valores de la entidad del modelo
#guardamos el cambio en la BD
