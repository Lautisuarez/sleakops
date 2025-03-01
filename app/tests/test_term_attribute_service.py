from datetime import datetime
import unittest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from daos.term_attribute_dao import TermAttributeDAO
from services.term_attribute_service import TermAttributeService
from schemas.term_attribute_schema import TermAttribute, TermAttributeCreate
from exceptions import DatabaseException

class TestTermAttribureService(unittest.TestCase):
    def setUp(self):
        self.db_session = Mock(spec=Session)
        self.mock_term_attribute_dao = Mock(spec=TermAttributeDAO)
        self.service = TermAttributeService(self.db_session)
        self.service.term_attribute_dao = self.mock_term_attribute_dao
    
    def test_get_or_create_term_attribute_existing(self):
        term_attr_data = TermAttributeCreate(
            lease_contract_length="1yr",
            purchase_option="All Upfront",
            offering_class="standard"
        )
        mock_term_attr = TermAttribute(id=1, **term_attr_data.model_dump())

        self.mock_term_attribute_dao.get.side_effect = lambda lease_contract_length, purchase_option, offering_class: (
            TermAttribute(id=1, **term_attr_data.model_dump())
            if lease_contract_length == term_attr_data.lease_contract_length
            and purchase_option == term_attr_data.purchase_option
            and offering_class == term_attr_data.offering_class
            else None
        )

        result = self.service.get_or_create_term_attribute(term_attr_data)

        self.assertIsInstance(result, TermAttribute)
        self.assertEqual(result.model_dump(), mock_term_attr.model_dump())
        self.mock_term_attribute_dao.get.assert_called_once_with("1yr", "All Upfront", "standard")

    def test_get_or_create_term_attribute_success(self):
        term_attr_data = TermAttributeCreate(
            lease_contract_length="3yr",
            purchase_option="Partial Upfront",
            offering_class="standard"
        )
        mock_term_attr = TermAttribute(id=1, **term_attr_data.model_dump())

        self.mock_term_attribute_dao.get.return_value = None
        self.mock_term_attribute_dao.add.side_effect = lambda term_attr: TermAttribute(id=1, **term_attr.model_dump())

        result = self.service.get_or_create_term_attribute(term_attr_data)

        self.assertIsInstance(result, TermAttribute)
        self.assertEqual(result.model_dump(), mock_term_attr.model_dump())
        self.mock_term_attribute_dao.get.assert_called_once_with("3yr", "Partial Upfront", "standard")
        self.mock_term_attribute_dao.add.assert_called_once_with(term_attr_data)
        self.db_session.commit.assert_called_once()

    def test_get_or_create_term_attribute_db_exception(self):
        term_attr_data = TermAttributeCreate(
            lease_contract_length="3yr",
            purchase_option="All Upfront",
            offering_class="standard"
        )

        self.mock_term_attribute_dao.get.return_value = None
        self.mock_term_attribute_dao.add.side_effect = Exception("DB Error")

        with self.assertRaises(DatabaseException) as context:
            self.service.get_or_create_term_attribute(term_attr_data)

        self.assertEqual(context.exception.status_code, 500)
        self.assertEqual(context.exception.message, "Error creating term attribute.")
        self.db_session.rollback.assert_called_once()