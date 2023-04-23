from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import sensors, users, auth, readings
from app.config import settings


models.Base.metadata.create_all(bind=engine)
app = FastAPI(debug=True)

app.include_router(sensors.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(readings.router)
