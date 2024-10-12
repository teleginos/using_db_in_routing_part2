from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from slugify import slugify
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session

from app.backend.db_depends import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas import CreateUser, UpdateUser

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/all_users")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalars(select(User).where(User.id == user_id)).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.get("/user_id/tasks")
def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()

    if tasks is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tasks not found for this user",
        )
    return tasks


@router.post("/create_users")
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(
        insert(User).values(
            username=create_user.username,
            firstname=create_user.firstname,
            lastname=create_user.lastname,
            age=create_user.age,
            slug=slugify(create_user.username),
        )
    )
    db.commit()
    return {"status": status.HTTP_201_CREATED, "transaction": "Successful"}


@router.put("/update_users")
async def update_user(
    db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UpdateUser
):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db.execute(
        update(User)
        .where(User.id == user_id)
        .values(
            firstname=update_user.firstname,
            lastname=update_user.lastname,
            age=update_user.age,
        )
    )
    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "User update is successful",
    }


@router.delete("/delete_users")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db.execute(delete(User).where(User.id == user_id))
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "User deletion is successful",
    }
