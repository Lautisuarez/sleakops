from sqlmodel import Session
from exceptions import DatabaseException
from daos.term_attribute_dao import TermAttributeDAO
from schemas.term_attribute_schema import TermAttribute, TermAttributeCreate


class TermAttributeService:
    def __init__(self, db: Session):
        self.db = db
        self.term_attribute_dao = TermAttributeDAO(db)

    def get_or_create_term_attribute(self, term_attribute: TermAttributeCreate) -> TermAttribute:
        term_attribute_db = self.term_attribute_dao.get(
            term_attribute.lease_contract_length,
            term_attribute.purchase_option,
            term_attribute.offering_class
        )
        if term_attribute_db:
            return term_attribute_db
        
        try:
            new_term_attribute = self.term_attribute_dao.add(term_attribute)
            self.db.commit()
            return new_term_attribute
        except Exception as err:
            self.db.rollback()
            print(f"Error creating term attribute: {err}")
            raise DatabaseException(status_code=500, message="Error creating term attribute.")