from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse
from user_jwt import createToken, validateToken

login_user = APIRouter()

class User (BaseModel):
    email: str
    password: str


@login_user.post('/login', tags=['autentificacion'])  
def login(user: User):
    if user.email == 'jcarlosgarcial@outlook.com' and user.password == '123':
        token: str = createToken(user.dict())
        print (token)
        return JSONResponse(content=token)
      





