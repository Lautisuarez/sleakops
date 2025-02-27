from sqlmodel import Session

from schemas.price_schema import Price, PriceCreate
from daos.price_dao import PriceDAO


class PriceService:
    def __init__(self, db: Session):
        self.price_dao = PriceDAO(db)

    def add(self, price: PriceCreate) -> Price:
        return self.price_dao.add(price)

