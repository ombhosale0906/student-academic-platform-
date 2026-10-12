import pytest
from database.db import db
from app.services.library_service import LibraryService


def test_borrow_book_updates_stock():
    loan = LibraryService.borrow_book("U101", "B001")
    assert loan["status"] == "ACTIVE"
    assert db.books["B001"]["available_copies"] == 4
    assert db.users["U101"]["active_loans"] == 1


def test_return_book_restores_stock():
    LibraryService.borrow_book("U101", "B001")
    loan = LibraryService.return_book("U101", "B001")
    assert loan["status"] == "RETURNED"
    assert db.books["B001"]["available_copies"] == 5
    assert db.users["U101"]["active_loans"] == 0


def test_borrow_unknown_user_rejected():
    with pytest.raises(ValueError):
        LibraryService.borrow_book("U999", "B001")


def test_return_without_borrowing_rejected():
    with pytest.raises(ValueError):
        LibraryService.return_book("U101", "B001")
