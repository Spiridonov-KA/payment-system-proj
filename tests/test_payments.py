import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base, SessionLocal, get_db
from app.config import NOTIFICATION_FILE

client = TestClient(app)

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    with SessionLocal() as db:
        from app.models import Payment
        db.query(Payment).delete()
        db.commit()
    if os.path.exists(NOTIFICATION_FILE):
        os.remove(NOTIFICATION_FILE)

def test_create_payment():
    resp = client.post("/payments/", json={"user_id": "user_1", "amount": 500.0})
    assert resp.status_code == 200
    data = resp.json()
    assert data["user_id"] == "user_1"
    assert data["status"] in ["success", "failed"]
    assert os.path.exists(NOTIFICATION_FILE)

def test_get_payment_by_id():
    create_resp = client.post("/payments/", json={"user_id": "user_2", "amount": 300.0})
    pid = create_resp.json()["id"]

    get_resp = client.get(f"/payments/{pid}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == pid

def test_get_not_found():
    resp = client.get("/payments/99999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Payment not found"