from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, Date, Numeric, Boolean,
    TIMESTAMP, CheckConstraint, DateTime, Float, ARRAY, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from typing import Set

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(String)
    status = Column(String)
    timezone = Column(DateTime(timezone=True), server_default=func.now())


class PasswordResetOTP(Base):
    __tablename__ = "password_reset_otps"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    otp = Column(String)
    expires_at = Column(DateTime, nullable=False)
    
class VerifyOTP(Base):
    __tablename__ = "verify_otps"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    otp = Column(String)
    expires_at = Column(DateTime, nullable=False)
