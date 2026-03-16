# router for users both clients and freelancers
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app import models, schemas, utils, oauth
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])
limiter = Limiter(key_func=get_remote_address)

@router.post("/", response_model=schemas.UserResponse)
@limiter.limit("5/minute")
def create_user(request: Request, user: schemas.UserCreation, db: Session = Depends(get_db)):
    #check if user already exist
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = utils.hash_password(user.password)
    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        password_hash=hashed_pw,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=list[schemas.UserResponse])
@limiter.limit("5/minute")
def get_users(request: Request, db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.get("/{user_id}",response_model=schemas.UserResponse)
@limiter.limit("3/minute")
def get_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/delete/{user_id}")
@limiter.limit("3/minute")
def delete_user(request: Request, email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first() 
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    #then delete
    db.delete(user)
    db.commit()
    return {"message": "User Account Deleted"}
