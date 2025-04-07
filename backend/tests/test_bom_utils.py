from app.models.product import Product
from app.models.material import Material
from app.models.bom import BillOfMaterial
from app.utils.bom import calculate_materials_for_batch

def test_calculate_materials_for_batch(db):
    product = Product(name="Test Product", description="A test product", quantity=100, price=10.0)
    material1 = Material(name="Fabric", description="Test fabric", quantity=100, unit="yards")
    material2 = Material(name="Thread", description="Test thread", quantity=50, unit="spools")
    db.add_all([product, material1, material2])
    db.commit()

    bom1 = BillOfMaterial(product_id=product.id, material_id=material1.id, quantity=0.5)
    bom2 = BillOfMaterial(product_id=product.id, material_id=material2.id, quantity=0.2)
    db.add_all([bom1, bom2])
    db.commit()

    result = calculate_materials_for_batch(db, product_id=product.id, batch_size=10)
    assert result["product_id"] == product.id
    assert result["batch_size"] == 10
    assert result["materials_needed"]["Fabric"] == 5.0
    assert result["materials_needed"]["Thread"] == 2.0

def test_calculate_with_zero_batch(db):
    product = Product(name="Zero Batch Product", description="Should return zero quantities", quantity=10, price=5.0)
    material = Material(name="Glue", description="Used sparingly", quantity=5, unit="bottles")
    db.add_all([product, material])
    db.commit()

    bom = BillOfMaterial(product_id=product.id, material_id=material.id, quantity=1.0)
    db.add(bom)
    db.commit()

    result = calculate_materials_for_batch(db, product_id=product.id, batch_size=0)
    assert result["batch_size"] == 0
    assert result["materials_needed"]["Glue"] == 0.0

def test_calculate_with_no_bom_entries(db):
    product = Product(name="Product With No BoM", description="No materials linked", quantity=1, price=1.0)
    db.add(product)
    db.commit()

    result = calculate_materials_for_batch(db, product_id=product.id, batch_size=5)
    assert result["product_id"] == product.id
    assert result["materials_needed"] == {}

def test_calculate_with_invalid_product_id(db):
    result = calculate_materials_for_batch(db, product_id=9999, batch_size=10)
    assert result["product_id"] == 9999
    assert result["materials_needed"] == {}

def test_quantity_type_validation(db):
    product = Product(name="Type Validation Product", description="Validation", quantity=10, price=5.0)
    material = Material(name="Labels", description="Testing type coercion", quantity=200, unit="pcs")
    db.add_all([product, material])
    db.commit()

    bom = BillOfMaterial(product_id=product.id, material_id=material.id, quantity="2.5")  # intentionally a string
    db.add(bom)
    db.commit()

    result = calculate_materials_for_batch(db, product_id=product.id, batch_size=4)
    assert result["materials_needed"]["Labels"] == 10.0

def test_large_batch_performance(db):
    product = Product(name="High Volume Product", description="Stress test", quantity=5000, price=50.0)
    material = Material(name="Bulk Fabric", description="Mass usage", quantity=10000, unit="yards")
    db.add_all([product, material])
    db.commit()

    bom = BillOfMaterial(product_id=product.id, material_id=material.id, quantity=1.75)
    db.add(bom)
    db.commit()

    result = calculate_materials_for_batch(db, product_id=product.id, batch_size=10000)
    assert result["materials_needed"]["Bulk Fabric"] == 17500.0

def test_availability_all_sufficient(db):
    product = Product(name="Sufficient Product", description="Enough stock", quantity=10, price=1.0)
    material = Material(name="Ink", description="Plenty available", quantity=50, unit="bottles")
    db.add_all([product, material])
    db.commit()

    bom = BillOfMaterial(product_id=product.id, material_id=material.id, quantity=2.0)
    db.add(bom)
    db.commit()

    result = calculate_materials_for_batch(db, product_id=product.id, batch_size=5, check_availability=True)
    assert result["materials"]["Ink"]["status"] == "ok"
    assert result["insufficient"] == {}

def test_availability_some_insufficient(db):
    product = Product(name="Insufficient Product", description="Shortage test", quantity=5, price=3.0)
    material = Material(name="Dye", description="Limited stock", quantity=3, unit="liters")
    db.add_all([product, material])
    db.commit()

    bom = BillOfMaterial(product_id=product.id, material_id=material.id, quantity=2.0)
    db.add(bom)
    db.commit()

    result = calculate_materials_for_batch(db, product_id=product.id, batch_size=2, check_availability=True)
    assert result["materials"]["Dye"]["status"] == "insufficient"
    assert "Dye" in result["insufficient"]
    assert result["insufficient"]["Dye"]["required"] == 4.0
    assert result["insufficient"]["Dye"]["available"] == 3
