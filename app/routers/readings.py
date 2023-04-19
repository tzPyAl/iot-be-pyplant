from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import Optional
from app import models, schemas, oath2
from app.database import get_db

router = APIRouter(prefix="/readings", tags=['Readings'])

@router.get("/")
def get_all_readings_from_connected_user(db: Session = Depends(get_db), 
                current_user: int = Depends(oath2.get_current_user),
                limit: int = 10,
                offset: int = 0,
                name: Optional[str] = ""):
    readings = db.query(models.Readings).filter(models.Readings.user_id == current_user.id).filter(models.Readings.name.contains(name)).limit(limit).offset(offset).all()
    if not readings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return readings

@router.get("/{reading_id}", response_model=schemas.ReadingSchema)
def get_reading(reading_id: int, 
               db: Session = Depends(get_db), 
               current_user: int = Depends(oath2.get_current_user)):
    reading = db.query(models.Readings).filter(models.Readings.id == reading_id).first()
    if not reading:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if reading.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform required action.")
    return reading

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ReadingSchema)
def create_reading(payload: schemas.ReadingPost, 
                  db: Session = Depends(get_db), 
                  current_user: int = Depends(oath2.get_current_user)):
    new_reading = models.Readings(user_id=current_user.id, **payload.dict())
    db.add(new_reading)
    db.commit()
    db.refresh(new_reading)
    return new_reading

@router.post("/add_bulk", status_code=status.HTTP_201_CREATED)
def create_readings_in_bulk(
    readings_in: schemas.ReadingIn, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(oath2.get_current_user)):
    n = 0
    for reading in readings_in.readings:
        reading_dict = models.Readings(user_id=current_user.id, 
                                       sensor_id=reading.sensor_id, 
                                       name=reading.name, 
                                       reading=reading.reading)   
        db.add(reading_dict)
        db.commit()
        n += 1
    payload = db.query(models.Readings).order_by(models.Readings.id.desc()).limit(n).all()
    return payload