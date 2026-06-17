
from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.members import router as members_router

from database.db import engine
from database.models import Base

app = FastAPI(title="Gym Management API")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router,prefix="/auth",tags=["Authentication"])

app.include_router(members_router,prefix="/members",tags=["Members"])


@app.get("/")
def root():
    return {"message": "Gym Subscription API Running"}