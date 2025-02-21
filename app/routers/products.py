from typing import List
from fastapi import APIRouter, Depends
from dependencies.products import get_products_service
from services.product_service import ProductService
from schemas.product_schema import Product

router = APIRouter()

@router.get("/", response_model=List[Product])
def get_products(
    database_engine: str = None,
    instance_type: str = None,
    vcpu: int = None,
    memory: str = None,
    service: ProductService = Depends(get_products_service),
):
    try:
        return service.get_products(database_engine, instance_type, vcpu, memory)
    except Exception as e:
        return {"error": str(e)}
