from fastapi import APIRouter, Body, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from app import models, schemas, utils, oauth
from app.database import get_db
from datetime import datetime, timedelta
import random
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix="/auth", tags=["Authentication"])
limiter = Limiter(key_func=get_remote_address)

@router.post("/signup", response_model=schemas.UserResponse)
@limiter.limit("3/minute")
def signup(request: Request, user: schemas.UserCreation, db: Session = Depends(get_db)):
    #check for existing user
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = utils.hash_password(user.password)
    new_user = models.User(
        full_name=user.full_name,
        email=user.email,
        password_hash=hashed_pw,
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print("Successful")
    return new_user

@router.post("/login")
#@limiter.limit("5/minute")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #request.username and request.password come from form data
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    
    if not utils.verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    
    #create JWT Token
    access_token = oauth.create_access_token(data={"user_id": user.id})
    refresh_token = oauth.create_refresh_token(data={"user_id": user.id})
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token,
        "token_type": "bearer"
        }

@router.post("/refresh")
@limiter.limit("3/minute")
def refresh_token(request: Request, refresh_token: str = Body(...), db: Session = Depends(get_db)):
    payload = oauth.verify_access_token(refresh_token, "refresh")
    user = db.query(models.User).filter(models.User,id == payload.get("user_id")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_access_token = oauth.create_access_token(data={"user_id": user.id})
    return {"access_token": new_access_token,"token_type": "bearer"}


@router.get("/me", response_model=schemas.UserResponse)
@limiter.limit("20/minute")
def get_logged_in_user(request: Request, current_user: models.User = Depends(oauth.get_current_user)):
    return current_user

@router.post("/forgot-password")
@limiter.limit("3/minute")
def forgot_password(request: Request, data: schemas.ForgotPasswordSchema, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate OTP
    otp = str(random.randint(100000, 999999))
    expires = datetime.utcnow() + timedelta(minutes=10)

    reset_entry = models.PasswordResetOTP(
        email=data.email,
        otp=otp,
        expires_at=expires
    )

    db.add(reset_entry)
    db.commit()

    # TODO → send OTP to email using FastAPI Mail / SMTP
    print("OTP:", otp)  

    return {"OTP": otp}

@router.post("/reset-password")
@limiter.limit("3/minute")
def reset_password(
    request: Request, 
    data: schemas.ResetPasswordSchema,
    db: Session = Depends(get_db)
):
    record = db.query(models.PasswordResetOTP).filter(
        models.PasswordResetOTP.email == data.email,
        models.PasswordResetOTP.otp == data.otp
    ).first()

    if not record:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")

    user = db.query(models.User).filter(models.User.email == data.email).first()

    user.password_hash = utils.hash_password(data.new_password)

    # Delete OTP so it can't be reused
    db.delete(record)
    db.commit()
    db.refresh(user)

    return {"message": "Password reset successful"}