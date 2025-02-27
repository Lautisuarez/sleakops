from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from db import get_session
from schemas.term_product_schema import TermProduct, TermProductCreate, TermProductDelete
from services.term_product_service import TermProductService


router = APIRouter(prefix='/terms/product')

@router.post("/", response_model=TermProduct)
def add_term_to_product(
    params: TermProductCreate,
    db: Session = Depends(get_session)
):
    try:
        service = TermProductService(db)
        term_product = service.add(params)
        db.commit()
        return term_product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/", response_model=TermProduct)
def remove_term_to_product(
    params: TermProductDelete,
    db: Session = Depends(get_session)
):
    try:
        service = TermProductService(db)
        term_product = service.delete(params)
        db.commit()
        return term_product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))