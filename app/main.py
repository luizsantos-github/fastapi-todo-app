from fastapi import FastAPI
from db import models
from db.database import engine
from routers import auth, todos

app = FastAPI()

# Create db if this does not exist
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)