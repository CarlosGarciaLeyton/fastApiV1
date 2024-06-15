
from fastapi import FastAPI
import uvicorn

import app.models.movie as model
from app.bd.database import engine
from app.routers.routes_movie import router as router_crud
from app.routers.users import login_user

model.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API CRUD",
    description="uso de crud con apis",
    version="1.0.0"
)


app.include_router(router=login_user, tags=["LOGIN"], prefix="/movies")
app.include_router(router=router_crud, tags=["CRUD"], prefix="/movies")


if __name__ == "__main__":
    uvicorn.run("main:app",
                host="localhost",
                reload=True)
