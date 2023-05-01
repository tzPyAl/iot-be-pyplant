from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from app import models
#from app.database import engine
from app.routers import sensors, users, auth, readings


#models.Base.metadata.create_all(bind=engine)
app = FastAPI(debug=True)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sensors.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(readings.router)
