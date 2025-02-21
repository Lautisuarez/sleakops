from db import get_session
from services.product_service import ProductService


def get_products_service():
    db = get_session()
    return ProductService(db)