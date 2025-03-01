import unittest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from daos.price_dao import PriceDAO
from services.price_service import PriceService
from schemas.price_schema import Price, PriceCreate
from exceptions import DatabaseException

class TestPriceService(unittest.TestCase):
    def setUp(self):
        self.db_session = Mock(spec=Session)
        self.mock_price_dao = Mock(spec=PriceDAO)
        self.service = PriceService(self.db_session)
        self.service.price_dao = self.mock_price_dao

    def test_create_price_success(self):
        price_data = PriceCreate(
            price_code="AAAAAAAAAAAAAAA", 
            term_code="11111111111",
            unit="Hrs",
            description="$21 per RDS",
            price_per_unit=21.0,
            currency="USD"
        )
        mock_price = Price(**price_data.model_dump())

        self.mock_price_dao.add.side_effect = lambda price: Price(**price.model_dump())
        
        result = self.service.add(price_data)
        
        self.assertIsInstance(result, Price)
        self.assertEqual(result.model_dump(), mock_price.model_dump())
        self.db_session.commit.assert_called_once()
        self.mock_price_dao.add.assert_called_once_with(price_data)

    def test_create_product_exception(self):
        price_data = PriceCreate(
            price_code="AAAAAAAAAAAAAAA", 
            term_code="11111111111",
            unit="Hrs",
            description="$21 per RDS",
            price_per_unit=21.0,
            currency="USD"
        )
        self.mock_price_dao.add.side_effect = Exception("DB error")

        with self.assertRaises(DatabaseException) as context:
            self.service.add(price_data)

        self.assertEqual(context.exception.status_code, 500)
        self.assertEqual(str(context.exception.message), "Error creating price.")
        self.db_session.rollback.assert_called_once()
  