from typing import List
from sqlalchemy.orm import Session

from daos.product_dao import ProductDAO
from schemas.product_schema import Product, ProductCreate

class ProductService:
    def __init__(self, db: Session):
        self.product_dao = ProductDAO(db)

    def get_products(
        self,
        database_engine: str = None,
        instance_type: str = None,
        vcpu: int = None,
        memory: str = None,
    ) -> List[Product]:
        return self.product_dao.get_products(database_engine, instance_type, vcpu, memory)

    def create_product(self, product: ProductCreate) -> Product:
        return self.product_dao.create_product(product)

    def exists_product(self, sku: str) -> bool:
        product = self.product_dao.get_product(sku)
        if not product:
            raise ValueError(f"Product with SKU {sku} not found")
        return True
