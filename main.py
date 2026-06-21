
from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers.auth import router as auth_router
from routers.members import router as members_router
from routers.dashboard import router as dashboard_router
from routers.subscriptions import router as subscription_router
from routers.payments import router as payments_router
from scheduler import scheduler



@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(title="Gym Management API",lifespan=lifespan)


app.include_router(auth_router,prefix="/auth",tags=["Authentication"])

app.include_router(dashboard_router,tags=["Dashboard"])

app.include_router(members_router,tags=["Members"])

app.include_router(subscription_router,tags=["Subscriptions"])

app.include_router(payments_router, tags=["Payments"])


@app.get("/")
def root():
    return {"message": "Gym Subscription API Running"}