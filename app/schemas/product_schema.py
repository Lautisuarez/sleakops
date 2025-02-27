from typing import List, Optional
from pydantic import BaseModel

from schemas.term_schema import Term

class ProductBase(BaseModel):
    sku: str
    instance_type: Optional[str] = None
    database_engine: str
    memory: Optional[str] = None
    vcpu: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    terms: List[Term] = []

    model_config = {
        "from_attributes": True
    }
