from sqlmodel import Session, select

from schemas.term_product_schema import TermProduct, TermProductCreate, TermProductDelete
from models.term_product import TermProduct as TermProductModel


class TermProductDAO:
    def __init__(self, db: Session):
        self.db = db

    def add(self, term_product: TermProductCreate) -> TermProduct:
        new_term_product = TermProductModel.model_validate(term_product)
        self.db.add(new_term_product)
        self.db.flush()
        return TermProduct.model_validate(new_term_product)
    
    def delete(self, term_product: TermProductDelete) -> TermProduct:
        term_product_db = self.db.exec(
            select(TermProductModel)
            .where(TermProductModel.sku == term_product.sku, TermProductModel.term_code == term_product.term_code)
        ).first()
        self.db.delete(term_product_db)
        return TermProduct.model_validate(term_product_db)
