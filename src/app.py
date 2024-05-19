from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import Base, engine
from routes.todo_routes import todo_router


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["http://127.0.0.1:3000"])
Base.metadata.create_all(engine)

app.include_router(todo_router)
