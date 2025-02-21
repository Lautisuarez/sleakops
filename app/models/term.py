from datetime import datetime
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field

from models.term_attribute import TermAttribute
from models.product import Product


class Term(SQLModel, table=True):
    term_code: str = Field(primary_key=True)
    sku: str = Field(foreign_key="product.sku")
    term_attribute_id: Optional[int] = Field(default=None, foreign_key="term_attribute.id")
    type: str
    effective_date: datetime
    
    product: Product = Relationship(back_populates="terms")
    term_attribute: Optional[TermAttribute] = Relationship(back_populates="terms")
    prices: List["Price"] = Relationship(back_populates="term")
