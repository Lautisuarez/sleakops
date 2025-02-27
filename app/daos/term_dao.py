from sqlmodel import Session, select

from models.term import Term as TermModel
from models.price import Price as PriceModel
from models.term_attribute import TermAttribute as TermAttributeModel
from models.term import Term as TermModel

from schemas.term_schema import TermCreate
from schemas.term_schema import Term

class TermDAO:
    def __init__(self, db: Session):
        self.db = db

    def add_term(self, term: TermCreate) -> Term:
        term_attribute = None
        if term.term_attribute is not None:
            term_attribute: TermAttributeModel = self.db.merge(TermAttributeModel.model_validate(term.term_attribute))

        term_instance = TermModel(
            term_code=term.term_code,
            type=term.type,
            effective_date=term.effective_date,
            term_attribute=term_attribute,
            prices=[PriceModel.model_validate(price) for price in term.prices]
        )

        self.db.add(term_instance)
        self.db.flush()

        return Term.model_validate(term_instance)

    def get_term(self, term_code: str) -> Term:
        term = self.db.exec(
            select(TermModel).where(TermModel.term_code == term_code)
        ).first()
        return Term.model_validate(term) if term else None
