from datetime import datetime
import unittest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from daos.term_dao import TermDAO
from schemas.term_schema import Term, TermCreate
from services.term_service import TermService
from exceptions import DatabaseException, NotFoundException

class TestTermService(unittest.TestCase):
    def setUp(self):
        self.db_session = Mock(spec=Session)
        self.mock_term_dao = Mock(spec=TermDAO)
        self.service = TermService(self.db_session)
        self.service.term_dao = self.mock_term_dao
    
    def test_get_or_create_term_existing(self):
        term_data = TermCreate(
            term_code="11111111111",
            type="OnDemand",
            effective_date=datetime.now(),
            term_attribute=None
        )
        mock_term = Term(**term_data.model_dump())

        self.mock_term_dao.get_term.side_effect = lambda term_code: (
            Term(**term_data.model_dump()) if term_code == term_data.term_code else None
        )

        result = self.service.get_or_create_term(term_data)

        self.assertIsInstance(result, Term)
        self.assertEqual(result.model_dump(), mock_term.model_dump())
        self.mock_term_dao.get_term.assert_called_once_with(term_code="11111111111")


    def test_get_or_create_term_success(self):
        new_term_data = TermCreate(
            term_code="11111111111", 
            type="OnDemand", 
            effective_date=datetime.now(), 
            term_attribute=None
        )
        mock_term = Term(**new_term_data.model_dump())

        self.mock_term_dao.get_term.return_value = None
        self.mock_term_dao.add_term.side_effect = lambda term: Term(**term.model_dump())

        result = self.service.get_or_create_term(new_term_data)

        self.assertEqual(result, mock_term)
        self.mock_term_dao.get_term.assert_called_once_with(term_code="11111111111")
        self.mock_term_dao.add_term.assert_called_once_with(new_term_data)
        self.db_session.commit.assert_called_once()

    def test_get_or_create_term_database_exception(self):
        new_term_data = TermCreate(
            term_code="11111111111", 
            type="OnDemand", 
            effective_date=datetime.now(), 
            term_attribute=None
        )

        self.mock_term_dao.get_term.return_value = None
        self.mock_term_dao.add_term.side_effect = Exception("DB error")

        with self.assertRaises(DatabaseException) as context:
            self.service.get_or_create_term(new_term_data)

        self.assertEqual(context.exception.status_code, 500)
        self.assertEqual(context.exception.message, "Error creating term.")
        self.mock_term_dao.get_term.assert_called_once_with(term_code="11111111111")
        self.mock_term_dao.add_term.assert_called_once_with(new_term_data)
        self.db_session.rollback.assert_called_once()

    def test_exists_term_success(self):
        term = Term(
            term_code="11111111111",
            type="OnDemand",
            effective_date=datetime.now(),
            term_attribute=None
        )
        self.mock_term_dao.get_term.return_value = term

        result = self.service.exists_term("11111111111")

        self.assertEqual(result, term)
        self.mock_term_dao.get_term.assert_called_once_with("11111111111")

    def test_exists_term_not_found(self):
        self.mock_term_dao.get_term.return_value = None

        with self.assertRaises(NotFoundException) as context:
            self.service.exists_term("NON_TERM_CODE")

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(str(context.exception.message), "Term with code NON_TERM_CODE not found")
        self.mock_term_dao.get_term.assert_called_once_with("NON_TERM_CODE")