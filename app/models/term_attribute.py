from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field


class TermAttribute(SQLModel, table=True):
    __tablename__ = "term_attribute"
    id: Optional[int] = Field(default=None, primary_key=True)
    lease_contract_length: str
    purchase_option: str
    offering_class: str
    
    terms: List["Term"] = Relationship(back_populates="term_attribute")
