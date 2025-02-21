from typing import List
from sqlmodel import Relationship, SQLModel, Field


class TermAttribute(SQLModel, table=True):
    __tablename__ = "term_attribute"
    id: int = Field(primary_key=True)
    lease_contract_length: str
    purchase_option: str
    offering_class: str
    
    terms: List["Term"] = Relationship(back_populates="term_attribute")
