import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base, engine, SessionLocal
from app.models.material import Material
from app.models.inventory_log import InventoryChangeLog, ChangeType

client = TestClient(app)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    material = Material(name="Restock Test", description="Material to restock", quantity=5.0, unit="rolls")
    db.add(material)
    db.commit()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)

def test_successful_restock_creates_log(db):
    payload = {
        "material_id": 1,
        "quantity": 10.5,
        "note": "Supplier delivery"
    }

    response = client.post("/materials/restock/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "restocked by 10.5" in data["message"]

    logs = db.query(InventoryChangeLog).all()
    assert len(logs) == 1
    log = logs[0]
    assert log.change_type == ChangeType.RESTOCK
    assert log.quantity == 10.5
    assert log.remaining == 15.5
    assert "Supplier" in log.note

def test_restock_with_invalid_material_id(db):
    payload = {
        "material_id": 999,
        "quantity": 5,
        "note": "Should fail"
    }

    response = client.post("/materials/restock/", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Material not found"
