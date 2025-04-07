import pytest
from app.models.product import Product
from app.models.material import Material
from app.models.bom import BillOfMaterial
from app.models.inventory_log import InventoryChangeLog, ChangeType
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base, engine, SessionLocal

client = TestClient(app)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    product = Product(name="Logging Test Product", description="Test with log", quantity=10, price=20.0)
    mat = Material(name="Foam", description="Soft material", quantity=10.0, unit="sheets")
    db.add_all([product, mat])
    db.commit()

    bom = BillOfMaterial(product_id=product.id, material_id=mat.id, quantity=2.0)
    db.add(bom)
    db.commit()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)

def test_inventory_log_created_on_deduction(db):
    response = client.post("/bom/deduct/?product_id=1&batch_size=2")
    assert response.status_code == 200

    logs = db.query(InventoryChangeLog).all()
    assert len(logs) == 1
    log = logs[0]
    assert log.material.name == "Foam"
    assert log.change_type == ChangeType.DEDUCTION
    assert log.quantity == 4.0
    assert log.remaining == 6.0
    assert "batch" in log.note
