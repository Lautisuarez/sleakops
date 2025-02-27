from sqlmodel import Session

from daos.term_product_dao import TermProductDAO
from services.product_service import ProductService
from services.term_service import TermService
from schemas.term_product_schema import TermProduct, TermProductCreate, TermProductDelete


class TermProductService:
    def __init__(self, db: Session):
        self.term_product_dao = TermProductDAO(db)
        self.product_service = ProductService(db)
        self.term_service = TermService(db)
    
    def add(self, term_product: TermProductCreate) -> TermProduct:
        self.product_service.exists_product(term_product.sku)
        self.term_service.exists_term(term_product.term_code)
        return self.term_product_dao.add(term_product)
    
    def delete(self, term_product: TermProductDelete) -> TermProduct:
        self.product_service.exists_product(term_product.sku)
        self.term_service.exists_term(term_product.term_code)
        return self.term_product_dao.delete(term_product)

