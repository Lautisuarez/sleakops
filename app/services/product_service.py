from typing import List
from sqlalchemy.orm import Session

from daos.product_dao import ProductDAO
from schemas.product_schema import Product

class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.product_dao = ProductDAO(self.db)

    def get_products(
        self,
        database_engine: str = None,
        instance_type: str = None,
        vcpu: int = None,
        memory: str = None,
    ) -> List[Product]:
        return self.product_dao.get_products(database_engine, instance_type, vcpu, memory)
