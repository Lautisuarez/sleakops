from typing import Optional
from pydantic import BaseModel

class TermAttributeBase(BaseModel):
    lease_contract_length: str
    purchase_option: str
    offering_class: str

class TermAttributeCreate(TermAttributeBase):
    pass

class TermAttribute(TermAttributeBase):
    id: int

    model_config = {
        "from_attributes": True
    }
