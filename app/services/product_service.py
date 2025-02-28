from typing import List
from sqlalchemy.orm import Session

from exceptions import DatabaseException, NotFoundException
from daos.product_dao import ProductDAO
from schemas.product_schema import Product, ProductCreate

class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.product_dao = ProductDAO(db)

    def get_products(
        self,
        database_engine: str = None,
        instance_type: str = None,
        vcpu: int = None,
        memory: str = None,
    ) -> List[Product]:
        try:
            return self.product_dao.get_products(database_engine, instance_type, vcpu, memory)
        except Exception as err:
            print(f"Error reading products: {err}")
            raise DatabaseException(status_code=500, message="Error reading products.")

    def create_product(self, product: ProductCreate) -> Product:
        try:
            product = self.product_dao.create_product(product)
            self.db.commit()
            return product
        except Exception as err:
            self.db.rollback()
            print(f"Error creating product: {err}")
            raise DatabaseException(status_code=500, message="Error creating product.")

    def exists_product(self, sku: str) -> bool:
        product = self.product_dao.get_product(sku)
        if not product:
            raise NotFoundException(status_code=404, message=f"Product with SKU {sku} not found")
        return True
