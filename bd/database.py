import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#sqliteName = '../movies.sqlite'
#base_dir = os.path.dirname(os.path.realpath(__file__))
#datebaseUrl = f"sqlite:///{os.path.join(base_dir, sqliteName)}"

#RUTA DE LA BD
DATABASE_URL = "sqlite:///movies.sqlite"

#CREA EL MOTOR Y SE ESPECIFICA QUE ES SQLITE
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

#SE CREAN PARAMETROS PARA LAS SESSIONES
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

#MAPEADOR DE ORM
Base = declarative_base()

#FUNCION PARA EL USO DE LA BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
