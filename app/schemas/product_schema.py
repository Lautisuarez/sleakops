from typing import Optional
from pydantic import BaseModel

class ProductBase(BaseModel):
    instance_type: Optional[str] = None
    database_engine: str
    memory: Optional[str] = None
    vcpu: int

class Product(ProductBase):
    sku: str

    model_config = {
        "from_attributes": True
    }
