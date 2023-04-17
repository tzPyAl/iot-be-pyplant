from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import Optional
from app import models, schemas, oath2
from app.database import get_db

router = APIRouter(prefix="/readings", tags=['Readings'])

@router.get("/{reading_id}", response_model=schemas.ReadingSchema)
def get_reading(reading_id: int, 
               db: Session = Depends(get_db), 
               current_user: int = Depends(oath2.get_current_user)):
    reading = db.query(models.Readings).filter(models.Readings.id == reading_id).first()
    if not reading:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    sensor_owner = db.query(models.Sensors).filter(models.Sensors.id == reading.sensor_id).first()
    if sensor_owner.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform required action.")
    return reading

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ReadingSchema)
def create_reading(payload: schemas.ReadingPost, 
                  db: Session = Depends(get_db), 
                  current_user: int = Depends(oath2.get_current_user)):
    new_reading = models.Readings(**payload.dict())
    db.add(new_reading)
    db.commit()
    db.refresh(new_reading)
    return new_reading
