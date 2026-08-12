from fastapi import FastAPI, APIRouter
from app.api.v1.endpoints import books, notes, users, auth

app = FastAPI(root_path="/api/v1")

# app.include_router(books.router, prefix="/v1")
app.include_router(books.router)
app.include_router(notes.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/about")
async def about():
    return {"message": "About"}