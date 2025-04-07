import pytest
from app.models.product import Product
from app.models.material import Material
from app.models.bom import BillOfMaterial
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base, engine, SessionLocal

client = TestClient(app)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    product = Product(name="Test Deduct Product", description="Test for deduction", quantity=10, price=20.0)
    mat1 = Material(name="Cloth", description="Basic cloth", quantity=10.0, unit="yards")
    mat2 = Material(name="Zipper", description="Standard zipper", quantity=5.0, unit="pcs")

    db.add_all([product, mat1, mat2])
    db.commit()

    bom1 = BillOfMaterial(product_id=product.id, material_id=mat1.id, quantity=2.0)
    bom2 = BillOfMaterial(product_id=product.id, material_id=mat2.id, quantity=1.0)

    db.add_all([bom1, bom2])
    db.commit()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)

def test_successful_inventory_deduction(db):
    response = client.post("/bom/deduct/?product_id=1&batch_size=2")
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_insufficient_inventory_deduction(db):
    response = client.post("/bom/deduct/?product_id=1&batch_size=10")
    assert response.status_code == 422
    assert "insufficient" in response.json()["detail"]
