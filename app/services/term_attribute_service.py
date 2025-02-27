from sqlmodel import Session
from daos.term_attribute_dao import TermAttributeDAO
from schemas.term_attribute_schema import TermAttribute, TermAttributeCreate


class TermAttributeService:
    def __init__(self, db: Session):
        self.term_attribute_dao = TermAttributeDAO(db)

    def get_or_create_term_attribute(self, term_attribute: TermAttributeCreate) -> TermAttribute:
        term_attribute_db = self.term_attribute_dao.get(
            term_attribute.lease_contract_length,
            term_attribute.purchase_option,
            term_attribute.offering_class
        )
        return term_attribute_db if term_attribute_db else self.term_attribute_dao.add(term_attribute)