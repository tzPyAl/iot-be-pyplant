from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List


class User(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class Sensor(BaseModel):
    name: str

class SensorResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    owner: UserResponse
    class Config:
        orm_mode = True

class ReadingSchema(BaseModel):
    id: int
    reading: str
    name: str
    sensor: SensorResponse
    created_at: datetime
    class Config:
        orm_mode = True

class ReadingGet(BaseModel):
    id: int
    reading: str
    name: str
    sensor: SensorResponse
    created_at: datetime
    class Config:
        orm_mode = True

class ReadingPost(BaseModel):
    name: str
    reading: str
    sensor_id: int

class SensorResponseSingle(BaseModel):
    id: int
    name: str
    created_at: datetime
    owner: UserResponse
    readings: List[ReadingSchema] = []
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
