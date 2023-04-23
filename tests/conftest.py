from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oath2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}/{settings.DATABASE_NAME}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "hello@gmail.com",
                 "password": "test1234"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "hello2@gmail.com",
                 "password": "test1234"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client

@pytest.fixture
def test_sensors(test_user, session):
    session.add_all([models.Sensors(name="1st title", user_id=test_user['id']),
                    models.Sensors(name="2nd title", user_id=test_user['id']), 
                    models.Sensors(name="3rd title", user_id=test_user['id'])])
    session.commit()

    sensors = session.query(models.Sensors).all()
    return sensors

@pytest.fixture
def test_readings(test_sensors, session):
    for sensor in test_sensors:
        session.add_all([models.Readings(name="dht11", reading="21.21", sensor_id=sensor.id, user_id=sensor.user_id),
                        models.Readings(name="dht11", reading="21.21", sensor_id=sensor.id, user_id=sensor.user_id), 
                        models.Readings(name="sht21", reading="21.21", sensor_id=sensor.id, user_id=sensor.user_id)])
    session.commit()

    readings = session.query(models.Readings).all()
    print(f"OVDJE {readings}")
    return readings
