from sqlmodel import Session
from services.term_attribute_service import TermAttributeService
from services.product_service import ProductService
from schemas.term_schema import Term, TermCreate
from daos.term_dao import TermDAO


class TermService:
    def __init__(self, db: Session):
        self.term_dao = TermDAO(db)
        self.product_service = ProductService(db)
        self.term_attribute_service = TermAttributeService(db)

    def get_or_create_term(self, term: TermCreate) -> Term:
        term_db = self.term_dao.get_term(term_code=term.term_code)
        if term_db: 
            return term_db
        if term.term_attribute is not None:
            term.term_attribute = self.term_attribute_service.get_or_create_term_attribute(term.term_attribute)
        return self.term_dao.add_term(term)
    
    def exists_term(self, term_code: str) -> Term:
        term = self.term_dao.get_term(term_code)
        if not term:
            raise ValueError(f"Term with code {term_code} not found")
        return term
