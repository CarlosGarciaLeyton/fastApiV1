from fastapi import FastAPI
from fastapi.responses import HTMLResponse,JSONResponse
from pydantic import BaseModel
from bd.database import engine, Base
from routers.movie import routerMovie
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
