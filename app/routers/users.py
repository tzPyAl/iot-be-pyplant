from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.utils import hash_password

router = APIRouter(prefix='/users', tags=['Users'])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(payload: schemas.User, db: Session = Depends(get_db)):
    payload.password = hash_password(payload.password)
    new_user = models.Users(**payload.dict()) # this will unpact dict in name=payload.name
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exists.")
    return user

@router.delete('/{id}')
def delete_user(id: int, db: Session = Depends(get_db)):
    _query = db.query(models.Users).filter(models.Users.id==id)
    if not _query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exists.")
    _query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)