from sqlmodel import Session

from schemas.price_schema import Price, PriceCreate
from models.price import Price as PriceModel


class PriceDAO:
    def __init__(self, db: Session):
        self.db = db

    def add(self, price: PriceCreate) -> Price:
        new_price = PriceModel.model_validate(price)
        self.db.add(new_price)
        self.db.flush()

        return Price.model_validate(new_price)