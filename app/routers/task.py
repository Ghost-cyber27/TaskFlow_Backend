from operator import and_
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app import models, schemas, oauth
from app.database import get_db
from slowapi import Limiter
from slowapi.util import get_remote_address
from datetime import date, datetime

router = APIRouter(prefix="/tasks", tags=["Tasks"])
limiter = Limiter(key_func=get_remote_address)

@router.post("/", response_model=schemas.TaskResponse)
@limiter.limit("10/minute")
def create_task(
    request: Request,
    task: schemas.TaskCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth.get_current_user)
    ):
    db_task = models.Task(
        user_id= current_user.id,
        title=task.title,
        description = task.description,
        status=task.status,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/me", response_model=list[schemas.TaskResponse])
def get_my_task(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth.get_current_user)
):
    tasks = (
        db.query(models.Task)
        .filter(models.Task.user_id == current_user.id)
        .all()
    )
    for t in tasks:
        t.title = t.title or ""
        t.description = t.description or ""
        t.status = t.status or ""
    return tasks

@router.get("/{task_id}", response_model=schemas.TaskResponse)
@limiter.limit("20/minute")
def get_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(request: Request,task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(stauts_code=404, detail="Task not found")
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.status is not None:
        task.status = task_update.status
    
    db.commit()
    db.refresh(task)
    return task

@router.put("/{task_id}/{status}", response_model=schemas.TaskResponse)
def update_task(request: Request,task_id: int, status: str, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    task.status = status
    db.commit()
    db.refresh(task)
    return task
    
@router.delete("/{task_id}", status_code=204)
@limiter.limit("10/minute")
def delete_task(request: Request,task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return
