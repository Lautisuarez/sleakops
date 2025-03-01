from datetime import datetime
import unittest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from daos.term_product_dao import TermProductDAO
from services.product_service import ProductService
from services.term_product_service import TermProductService
from services.term_service import TermService
from schemas.term_product_schema import TermProduct, TermProductCreate, TermProductDelete
from exceptions import DatabaseException

class TestTermProductService(unittest.TestCase):
    def setUp(self):
        self.db_session = Mock(spec=Session)
        self.mock_term_product_dao = Mock(spec=TermProductDAO)
        self.mock_product_service = Mock(spec=ProductService(self.db_session))
        self.mock_term_service = Mock(spec=TermService(self.db_session))
        self.service = TermProductService(self.db_session)
        self.service.term_product_dao = self.mock_term_product_dao
        self.service.product_service = self.mock_product_service
        self.service.term_service = self.mock_term_service

    def test_add_term_product_success(self):
        term_product_data = TermProductCreate(sku="AAAAAAAAAAAAAAA", term_code="11111111111")
        mock_term_product = TermProduct(**term_product_data.model_dump())

        self.mock_product_service.exists_product.return_value = True
        self.mock_term_service.exists_term.return_value = True
        self.mock_term_product_dao.add.return_value = mock_term_product

        result = self.service.add(term_product_data)

        self.assertIsInstance(result, TermProduct)
        self.assertEqual(result.model_dump(), mock_term_product.model_dump())

        self.mock_product_service.exists_product.assert_called_once_with("AAAAAAAAAAAAAAA")
        self.mock_term_service.exists_term.assert_called_once_with("11111111111")
        self.mock_term_product_dao.add.assert_called_once_with(term_product_data)
        self.db_session.commit.assert_called_once()

    def test_add_term_product_db_exception(self):
        term_product_data = TermProductCreate(sku="AAAAAAAAAAAAAAA", term_code="11111111111")

        self.mock_product_service.exists_product.return_value = True
        self.mock_term_service.exists_term.return_value = True
        self.mock_term_product_dao.add.side_effect = Exception("DB Error")

        with self.assertRaises(DatabaseException) as context:
            self.service.add(term_product_data)

        self.assertEqual(context.exception.status_code, 500)
        self.assertEqual(context.exception.message, "An unexpected error ocurred creating term to product.")

        self.db_session.rollback.assert_called_once()
    
    def test_delete_term_product_success(self):
        term_product_data = TermProductDelete(sku="AAAAAAAAAAAAAAA", term_code="11111111111")
        mock_term_product = TermProduct(**term_product_data.model_dump())

        self.mock_product_service.exists_product.return_value = True
        self.mock_term_service.exists_term.return_value = True
        self.mock_term_product_dao.delete.return_value = mock_term_product

        result = self.service.delete(term_product_data)

        self.assertIsInstance(result, TermProduct)
        self.assertEqual(result.model_dump(), mock_term_product.model_dump())

        self.mock_product_service.exists_product.assert_called_once_with("AAAAAAAAAAAAAAA")
        self.mock_term_service.exists_term.assert_called_once_with("11111111111")
        self.mock_term_product_dao.delete.assert_called_once_with(term_product_data)
        self.db_session.commit.assert_called_once()

    def test_delete_term_product_db_exception(self):
        term_product_data = TermProductDelete(sku="AAAAAAAAAAAAAAA", term_code="11111111111")

        self.mock_product_service.exists_product.return_value = True
        self.mock_term_service.exists_term.return_value = True
        self.mock_term_product_dao.delete.side_effect = Exception("DB Error")

        with self.assertRaises(DatabaseException) as context:
            self.service.delete(term_product_data)

        self.assertEqual(context.exception.status_code, 500)
        self.assertEqual(context.exception.message, "An unexpected error ocurred deleting term from product.")

        self.db_session.rollback.assert_called_once()
