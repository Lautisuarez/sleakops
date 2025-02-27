from pydantic import BaseModel

class TermProductBase(BaseModel):
    sku: str
    term_code: str

class TermProductCreate(TermProductBase):
    pass

class TermProductDelete(TermProductBase):
    pass

class TermProduct(TermProductBase):
    pass

    model_config = {
        "from_attributes": True
    }