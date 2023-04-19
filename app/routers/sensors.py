from typing import List, Optional
from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, oath2
from app.database import get_db

router = APIRouter(prefix="/sensors", tags=['Sensors'])

@router.get("/", response_model=List[schemas.SensorResponse])
def get_sensors(db: Session = Depends(get_db),
                current_user: int = Depends(oath2.get_current_user),
                limit: int = 10,
                offset: int = 0,
                name: Optional[str] = ""):
    sensors = db.query(models.Sensors).filter(models.Sensors.user_id == current_user.id).filter(models.Sensors.name.contains(name)).limit(limit).offset(offset).all()
    if not sensors:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return sensors

@router.get("/{id}", response_model=schemas.SensorResponseSingle)
def get_sensor(id: int, 
               db: Session = Depends(get_db), 
               current_user: int = Depends(oath2.get_current_user),
               reading_name: Optional[str] = ""):
    sensor = db.query(models.Sensors).filter(models.Sensors.id==id).first()
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if sensor.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform required action.")
    readings = db.query(models.Readings).filter(models.Readings.sensor_id == sensor.id)
    if reading_name:
        readings = readings.filter(models.Readings.name.contains(reading_name))
        if not readings.all():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    sensor.readings = readings.all()
    return sensor

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.SensorResponse)
def create_sensor(payload: schemas.Sensor, 
                  db: Session = Depends(get_db), 
                  current_user: int = Depends(oath2.get_current_user)):
    new_sensor = models.Sensors(user_id=current_user.id, **payload.dict())
    db.add(new_sensor)
    db.commit()
    db.refresh(new_sensor)
    return new_sensor

@router.put("/{id}", response_model=schemas.SensorResponseSingle)
def update_sensor(id: int, 
                  payload: schemas.Sensor, 
                  db: Session = Depends(get_db),
                  current_user: int = Depends(oath2.get_current_user)):
    _query = db.query(models.Sensors).filter(models.Sensors.id==id)
    if not _query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sensor with id: {id} does not exists.")
    if _query.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform required action.")
    _query.update(payload.dict(), synchronize_session=False)
    db.commit()
    return _query.first()

@router.delete("/{id}")
def delete_sensor(id: int, 
                  db: Session = Depends(get_db),
                  current_user: int = Depends(oath2.get_current_user)):
    _query = db.query(models.Sensors).filter(models.Sensors.id==id)
    if not _query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sensor with id: {id} does not exists.")
    if _query.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform required action.")
    _query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
