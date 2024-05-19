from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from db.database import SessionLocal
from sqlalchemy.orm import Session
from models.models import ToDo
from schemas.todo_schemas import ToDoSchema, ToDoCreateSchema


def get_session():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


todo_router = APIRouter(prefix="")


@todo_router.get("/todo", response_model=List[ToDoSchema])
def get_all_todos(session: Session = Depends(get_session)):
    todos = session.query(ToDo).all()

    return todos


@todo_router.get("/todo/{todo_id: int}", response_model=ToDoSchema)
def get_todo_by_id(todo_id: int, session: Session = Depends(get_session)):
    todo = session.query(ToDo).get(todo_id)

    if not todo:
        raise HTTPException(
            status_code=404, detail=f"ToDo item with id {todo_id} not found"
        )

    return todo


@todo_router.delete(
    "/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.query(ToDo).get(todo_id)

    if todo:
        session.delete(todo)
        session.commit()

        return None

    raise HTTPException(
        status_code=404, detail=f"ToDo item with id {todo_id} not found"
    )


@todo_router.put("/todo/{todo_id}", response_model=ToDoSchema)
def update_todo(todo_id: int, task: str, session: Session = Depends(get_session)):
    todo = session.query(ToDo).get(todo_id)

    if todo:
        todo.task = task
        session.commit()

        return todo

    raise HTTPException(
        status_code=404, detail=f"ToDo item with id {todo_id} not found"
    )


@todo_router.post(
    "/todo", response_model=ToDoSchema, status_code=status.HTTP_201_CREATED
)
def create_todo(todo: ToDoCreateSchema, session: Session = Depends(get_session)):
    tododb = ToDo(task=todo.task)
    session.add(tododb)
    session.commit()
    session.refresh(tododb)

    return tododb
