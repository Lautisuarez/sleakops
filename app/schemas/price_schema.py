from pydantic import BaseModel

class PriceBase(BaseModel):
    price_code: str
    term_code: str
    unit: str
    description: str
    price_per_unit: float
    currency: str

class PriceCreate(PriceBase):
    pass

class Price(PriceBase):
    model_config = {
        "from_attributes": True
    }
