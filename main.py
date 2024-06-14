from fastapi import FastAPI
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from bd.database import engine, Base
from routers.moviessss import routerMovie
from routers.users import login_user
import uvicorn
import os

app = FastAPI(
    title='api facil',
    description='api de prueba con sqlite',
    version='0.0.1'
)

app.include_router(login_user)
app.include_router(routerMovie)


Base.metadata.create_all(bind=engine)


'''if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run ("main:app", host="127.0.0.1", port=port)'''

