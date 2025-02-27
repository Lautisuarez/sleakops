from sqlmodel import Session, select

from models.term_attribute import TermAttribute as TermAttributeModel
from schemas.term_attribute_schema import TermAttributeCreate, TermAttribute


class TermAttributeDAO:
    def __init__(self, db: Session):
        self.db = db

    def get(self, lease_contract_length: str, purchase_option: str, offering_class: str) -> TermAttribute:
        term_attribute = self.db.exec(
            select(TermAttributeModel).where(
                TermAttributeModel.lease_contract_length == lease_contract_length,
                TermAttributeModel.purchase_option == purchase_option,
                TermAttributeModel.offering_class == offering_class
            )
        ).first()
        return TermAttribute.model_validate(term_attribute) if term_attribute else None

    def add(self, term_attribute: TermAttributeCreate) -> TermAttribute:
        term_attribute = TermAttributeModel.model_validate(term_attribute)
        self.db.add(term_attribute)
        self.db.flush()
        return TermAttribute.model_validate(term_attribute)

