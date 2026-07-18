from fastapi import FastAPI, APIRouter
from .api.v1.endpoints import books, notes

app = FastAPI()

app.include_router(books.router, prefix="/api")
app.include_router(notes.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/about")
async def about():
    return {"message": "About"}