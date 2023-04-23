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
    id: Optional[int]
    name: str
    #created_at: Optional[datetime]
    class Config:
        orm_mode = True

class SensorResponse(Sensor):
    owner: UserResponse
    class Config:
        orm_mode = True

class ReadingPost(BaseModel):
    name: str
    reading: str
    sensor_id: int
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

class SensorResponseSingle(Sensor):
    readings: List[ReadingSchema] = []
    class Config:
        orm_mode = True

class Reading(BaseModel):
    name: str
    reading: float
    sensor_id: int
    user_id: Optional[int]

class ReadingIn(BaseModel):
    readings: List[Reading]

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
