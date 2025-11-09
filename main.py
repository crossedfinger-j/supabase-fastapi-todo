from fastapi import FastAPI
from app.routers import auth, todos, categories, priorities

app = FastAPI()

app.include_router(auth.router, tags=["Authentication"])
app.include_router(todos.router)
app.include_router(categories.router)
app.include_router(priorities.router)

@app.get("/")
def read_root():
    return {"Hello": "Supabase FastAPI"}