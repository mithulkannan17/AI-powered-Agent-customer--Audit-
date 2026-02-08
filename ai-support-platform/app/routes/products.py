from fastapi import APIRouter
from app.core.database import get_database
from app.models.product import Product
from typing import List

router = APIRouter()

@router.post("/", response_model=Product)
async def create_product(product: Product):
    db = get_database()
    result = await db.products.insert_one(product.dict(by_alias=True))
    product.id = str(result.inserted_id)
    return product

@router.get("/", response_model=List[Product])
async def list_products():
    db = get_database()
    products = []
    async for p in db.products.find():
        p["_id"] = str(p["_id"])
        products.append(p)
    return products
