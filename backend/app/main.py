from fastapi import FastAPI
from app.api import inventory
from app.api import product
from app.api import material
from app.api import location
from app.api import bom_deduct  # ✅ New import
from app.api import material_restock
from app.api import material_low_stock
from app.api import inventory_log
from app.api import production_order
from app.api import production_order_deduct
from app.api import production_audit_log

app = FastAPI(title="Craft Inventory System")

app.include_router(inventory.router)
app.include_router(product.router)
app.include_router(material.router)
app.include_router(location.router)
app.include_router(bom_deduct.router)  # ✅ New route
app.include_router(material_restock.router)
app.include_router(material_low_stock.router)
app.include_router(inventory_log.router)
app.include_router(production_order.router)
app.include_router(production_order_deduct.router)
app.include_router(production_audit_log.router)