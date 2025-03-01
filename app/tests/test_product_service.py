import unittest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from daos.product_dao import ProductDAO
from services.product_service import ProductService
from schemas.product_schema import Product, ProductCreate
from exceptions import DatabaseException, NotFoundException

class TestProductService(unittest.TestCase):
    def setUp(self):
        self.db_session = Mock(spec=Session)
        self.mock_product_dao = Mock(spec=ProductDAO)
        self.service = ProductService(self.db_session)
        self.service.product_dao = self.mock_product_dao
    
    def mock_get_products(*args, **kwargs):
        all_products = [
            Product(sku="AAAAAAAAAAAAAAA", instance_type="db.ins.type", database_engine="PostgreSQL", memory="64Gib", vcpu=64),
            Product(sku="BBBBBBBBBBBBBBB", instance_type="db.ins.type2", database_engine="MySQL", memory="128Gib", vcpu=128),
        ]
        
        filtered_products = [
            p for p in all_products
            if all(kwargs.get(k) is None or getattr(p, k) == v for k, v in kwargs.items())
        ]
        
        return [filtered_products]

    def test_get_products_success(self):
        self.mock_product_dao.get_products.side_effect = self.mock_get_products()

        result = self.service.get_products()

        expected_products = [
            Product(sku="AAAAAAAAAAAAAAA", instance_type="db.ins.type", database_engine="PostgreSQL", memory="64Gib", vcpu=64),
            Product(sku="BBBBBBBBBBBBBBB", instance_type="db.ins.type2", database_engine="MySQL", memory="128Gib", vcpu=128),
        ]
        self.assertEqual(result, expected_products)
        self.mock_product_dao.get_products.assert_called_once()

    def test_get_products_exception(self):
        self.mock_product_dao.get_products.side_effect = Exception("DB error")

        with self.assertRaises(DatabaseException) as context:
            self.service.get_products()

        self.assertEqual(context.exception.status_code, 500)
        self.assertEqual(str(context.exception.message), "Error reading products.")
        self.mock_product_dao.get_products.assert_called_once()

    def test_create_product_success(self):
        product_data = ProductCreate(sku="AAAAAAAAAAAAAAA", instance_type="db.ins.type", database_engine="PostgreSQL", memory="64Gib", vcpu=64)
        mock_product = Product(sku="AAAAAAAAAAAAAAA", instance_type="db.ins.type", database_engine="PostgreSQL", memory="64Gib", vcpu=64)

        self.mock_product_dao.create_product.side_effect = lambda product: Product(**product.model_dump())
        
        result = self.service.create_product(product_data)
        
        self.assertIsInstance(result, Product)
        self.assertEqual(result.model_dump(), mock_product.model_dump())
        self.db_session.commit.assert_called_once()
        self.mock_product_dao.create_product.assert_called_once_with(product_data)

    def test_create_product_exception(self):
        product_data = ProductCreate(sku="AAAAAAAAAAAAAAA", instance_type="db.instance.type", database_engine="PostgreSQL", memory="16Gib", vcpu=32)
        
        self.mock_product_dao.create_product.side_effect = Exception("DB error")

        with self.assertRaises(DatabaseException) as context:
            self.service.create_product(product_data)

        self.assertEqual(context.exception.status_code, 500)
        self.assertEqual(str(context.exception.message), "Error creating product.")
        self.db_session.rollback.assert_called_once()
  
    def test_exists_product_success(self):
        self.mock_product_dao.get_product.side_effect = self.mock_get_products(sku="AAAAAAAAAAAAAAA")

        result = self.service.exists_product("AAAAAAAAAAAAAAA")
        self.assertTrue(result)
        self.mock_product_dao.get_product.assert_called_once_with("AAAAAAAAAAAAAAA")

    def test_exists_product_exception(self):
        self.mock_product_dao.get_product.return_value = None

        with self.assertRaises(NotFoundException) as context:
            self.service.exists_product("NON_EXISTING_SKU")

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(str(context.exception.message), "Product with SKU NON_EXISTING_SKU not found")
        self.mock_product_dao.get_product.assert_called_once_with("NON_EXISTING_SKU")
