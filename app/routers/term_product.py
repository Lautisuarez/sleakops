from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from db import get_session
from schemas.term_product_schema import TermProduct, TermProductCreate, TermProductDelete
from services.term_product_service import TermProductService


router = APIRouter(prefix='/terms/product')

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TermProduct)
def add_term_to_product(
    params: TermProductCreate,
    db: Session = Depends(get_session)
):
    service = TermProductService(db)
    return service.add(params)

@router.delete("/", response_model=TermProduct)
def remove_term_to_product(
    sku: str,
    term_code: str,
    db: Session = Depends(get_session)
):
    service = TermProductService(db)
    return service.delete(TermProductDelete(
        sku=sku,
        term_code=term_code
    ))
