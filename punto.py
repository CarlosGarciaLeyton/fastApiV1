
from fastapi import FastAPI
import uvicorn

import models.movie as model
from bd.database import engine
from routers.routes_movie import router as router_crud
from routers.users import login_user

model.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API FACIL",
    description="uso de crud con apis",
    version="1.0.0"
)


'''@app.get("/")
def hello_world():
    return {
        "msg": "Hola Mundo"
    }'''


app.include_router(router=login_user, tags=["LOGIN"], prefix="/movies")
app.include_router(router=router_crud, tags=["CRUD"], prefix="/movies")


if __name__ == "__main__":
    uvicorn.run("punto:app",
                host="localhost",
                reload=True)
