from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Payment System", lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "ok"}