from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from app.user_jwt import createToken

login_user = APIRouter(
    prefix='/v1/api'
)


class User(BaseModel):
    email: str
    password: str


@login_user.post('/login')
def login(user: User):
    if user.email == 'jcarlosgarcial@outlook.com' and user.password == '123456':
        token: str = createToken(user.model_dump())
        print(token)
        return JSONResponse(content=token)
