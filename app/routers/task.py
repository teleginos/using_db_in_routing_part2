from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from slugify import slugify
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session

from app.backend.db_depends import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas import CreateTask, UpdateTask

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all_task")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalars(select(Task).where(Task.id == task_id)).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    return task


@router.post("/create")
async def create_task(
    db: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int
):

    user = db.scalars(select(User).where(User.id == user_id)).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db.execute(
        insert(Task).values(
            title=create_task.title,
            content=create_task.content,
            priority=create_task.priority,
            user_id=user_id,
            slug=slugify(create_task.title),
        )
    )

    db.commit()
    return {"status": status.HTTP_201_CREATED, "transaction": "Successful"}


@router.put("/update")
async def update_task(
    db: Annotated[Session, Depends(get_db)], task_id: int, update_task: UpdateTask
):
    task = db.scalars(select(Task).where(Task.id == task_id))

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    db.execute(
        update(Task)
        .where(Task.id == task_id)
        .values(
            title=create_task.title,
            content=create_task.content,
            priority=create_task.priority,
            slug=slugify(create_task.title),
        )
    )


@router.delete("/delete")
async def delete_tasks(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalars(select(Task).where(Task.id == task_id))

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Task deletion is successful",
    }
