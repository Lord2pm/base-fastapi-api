from fastapi import Depends, FastAPI, status, HTTPException
from sqlalchemy.orm import Session
from schemas import ToDoSchema, ToDoCreateSchema
from models import ToDo
from database import Base, engine, SessionLocal
from typing import List


app = FastAPI()
Base.metadata.create_all(engine)


def get_session():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


@app.get("/todo", response_model=List[ToDoSchema])
def get_all_todos(session: Session = Depends(get_session)):
    todos = session.query(ToDo).all()

    return todos


@app.get("/todo/{todo_id: int}", response_model=ToDoSchema)
def get_todo_by_id(todo_id: int, session: Session = Depends(get_session)):
    todo = session.query(ToDo).get(todo_id)

    if not todo:
        raise HTTPException(
            status_code=404, detail=f"ToDo item with id {todo_id} not found"
        )

    return todo


@app.delete(
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


@app.put("/todo/{todo_id}", response_model=ToDoSchema)
def update_todo(todo_id: int, task: str, session: Session = Depends(get_session)):
    todo = session.query(ToDo).get(todo_id)

    if todo:
        todo.task = task
        session.commit()

        return todo

    raise HTTPException(
        status_code=404, detail=f"ToDo item with id {todo_id} not found"
    )


@app.post("/todo", response_model=ToDoSchema, status_code=status.HTTP_201_CREATED)
def create_todo(todo: ToDoCreateSchema, session: Session = Depends(get_session)):
    tododb = ToDo(task=todo.task)
    session.add(tododb)
    session.commit()
    session.refresh(tododb)

    return tododb
