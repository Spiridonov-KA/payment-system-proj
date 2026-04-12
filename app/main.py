from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db
from app.routes import router as payment_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Payment System", version="0.3.0", lifespan=lifespan)
app.include_router(payment_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}