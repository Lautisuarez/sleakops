from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from schemas.price_schema import Price, PriceCreate
from schemas.term_attribute_schema import TermAttribute, TermAttributeCreate

class TermBase(BaseModel):
    term_code: str
    type: str
    effective_date: datetime

class TermCreate(TermBase):
    term_attribute: Optional[TermAttributeCreate] = None
    prices: List[PriceCreate] = []

class Term(TermBase):
    term_attribute: Optional[TermAttribute] = None
    prices: List[Price] = []

    model_config = {
        "from_attributes": True
    }
