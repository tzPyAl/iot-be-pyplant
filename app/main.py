from fastapi import FastAPI
from . import models
from .database import engine
from .routers import sensors, users, auth, readings
from .config import settings


models.Base.metadata.create_all(bind=engine)
app = FastAPI(debug=True)

app.include_router(sensors.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(readings.router)
