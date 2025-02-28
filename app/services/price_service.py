from sqlmodel import Session

from exceptions import DatabaseException
from schemas.price_schema import Price, PriceCreate
from daos.price_dao import PriceDAO


class PriceService:
    def __init__(self, db: Session):
        self.db = db
        self.price_dao = PriceDAO(db)

    def add(self, price: PriceCreate) -> Price:
        try:
            price = self.price_dao.add(price)
            self.db.commit()
            return price
        except Exception as err:
            self.db.rollback()
            print(f"Error creating price: {err}")
            raise DatabaseException(status_code=500, message="Error creating price.")

