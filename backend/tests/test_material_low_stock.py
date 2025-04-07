import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base, engine, SessionLocal
from app.models.material import Material

client = TestClient(app)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    db.add_all([
        Material(name="Enough Stock", quantity=20.0, unit="yards", reorder_point=10.0),
        Material(name="Low Stock Item", quantity=3.0, unit="yards", reorder_point=10.0),
        Material(name="Zero Stock", quantity=0.0, unit="meters", reorder_point=1.0)
    ])
    db.commit()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)

def test_low_stock_endpoint_returns_only_low_stock(db):
    response = client.get("/materials/low_stock/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    names = [m["name"] for m in data]
    
    assert "Low Stock Item" in names
    assert "Zero Stock" in names
    assert "Enough Stock" not in names
