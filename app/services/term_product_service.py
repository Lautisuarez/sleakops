from sqlmodel import Session

from exceptions import DatabaseException
from daos.term_product_dao import TermProductDAO
from services.product_service import ProductService
from services.term_service import TermService
from schemas.term_product_schema import TermProduct, TermProductCreate, TermProductDelete


class TermProductService:
    def __init__(self, db: Session):
        self.db = db
        self.term_product_dao = TermProductDAO(db)
        self.product_service = ProductService(db)
        self.term_service = TermService(db)
    
    def add(self, term_product: TermProductCreate) -> TermProduct:
        self.product_service.exists_product(term_product.sku)
        self.term_service.exists_term(term_product.term_code)

        try:
            term_product = self.term_product_dao.add(term_product)
            self.db.commit()
        except Exception as err:
            self.db.rollback()
            print(f"Error creating term to product: {err}")
            raise DatabaseException(status_code=500, message="An unexpected error ocurred creating term to product.")
        
        return term_product
    
    def delete(self, term_product: TermProductDelete) -> TermProduct:
        self.product_service.exists_product(term_product.sku)
        self.term_service.exists_term(term_product.term_code)
        
        try:
            term_product = self.term_product_dao.delete(term_product)
            self.db.commit()
        except Exception as err:
            self.db.rollback()
            print(f"Error deleting term from product: {err}")
            raise DatabaseException(status_code=500, message="An unexpected error ocurred deleting term from product.")

        return term_product


