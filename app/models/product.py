from typing import List
from sqlmodel import SQLModel, Field, Relationship

from models.term_product import TermProduct


class Product(SQLModel, table=True):
    sku: str = Field(primary_key=True)
    instance_type: str
    database_engine: str
    memory: str
    vcpu: int
    
    terms: List["Term"] = Relationship(back_populates="products", link_model=TermProduct)

