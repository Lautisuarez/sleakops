from sqlmodel import Relationship, SQLModel, Field

from models.term import Term


class Price(SQLModel, table=True):
    price_code: str = Field(primary_key=True)
    term_code: str = Field(foreign_key="term.term_code")
    unit: str
    description: str
    price_per_unit: float
    currency: str
    
    term: Term = Relationship(back_populates="prices")