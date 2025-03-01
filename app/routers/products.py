from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session

from db import get_session
from services.product_service import ProductService
from schemas.product_schema import Product

router = APIRouter(prefix='/products')

@router.get("/", response_model=List[Product])
def get_products(
    database_engine: str = None,
    instance_type: str = None,
    vcpu: int = None,
    memory: str = None,
    db: Session = Depends(get_session)
):
    service = ProductService(db)
    return service.get_products(database_engine, instance_type, vcpu, memory)


