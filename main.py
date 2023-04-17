from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app import models
from app.database import engine
from app.routers import sensors, users, auth, readings

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='iot', user='tiho', password='1234', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connected!")
        break
    except Exception as error:
        print(error)
        time.sleep(2)

app.include_router(sensors.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(readings.router)
