from typing import List
from models.product import Product as ProductModel
from schemas.product_schema import Product
from sqlmodel import select, Session

class ProductDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_products(
        self,
        database_engine: str = None,
        instance_type: str = None,
        vcpu: int = None,
        memory: str = None,
    ) -> List[Product]:
        query = select(ProductModel)

        if database_engine:
            query = query.where(ProductModel.database_engine == database_engine)
        if instance_type:
            query = query.where(ProductModel.instance_type == instance_type)
        if vcpu:
            query = query.where(ProductModel.vcpu == vcpu)
        if memory:
            query = query.where(ProductModel.memory == memory)

        products = self.db.exec(query).all()
        return products

