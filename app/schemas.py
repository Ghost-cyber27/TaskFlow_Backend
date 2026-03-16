from datetime import datetime, date
from typing import Optional, List, Set
from pydantic import BaseModel, EmailStr, ConfigDict

# Shared user fields
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    
# For user creation (registration)
class UserCreation(UserBase):
    password: str 
    
class ChangePassword(BaseModel):
    old_password: str
    new_password: str
    
class ResetPasswordSchema(BaseModel):
    email: str
    otp: str
    new_password: str
    
class ForgotPasswordSchema(BaseModel):
    email: str
    
# for user response(to avoid exposing password)
class UserResponse(UserBase):
    id: int
    email: EmailStr
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True) 
       
class TaskCreate(BaseModel):
    title: str
    description: str
    status: str
    
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    status: str

    model_config = ConfigDict(from_attributes=True)