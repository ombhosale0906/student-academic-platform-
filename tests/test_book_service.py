import pytest
from app.services.library_service import LibraryService


def test_get_existing_book():
    book = LibraryService.get_book("B001")
    assert book["title"] == "Cloud Native DevOps Architecture"


def test_search_books():
    books = LibraryService.search_books("Cloud Native")
    assert len(books) == 1
    assert books[0]["book_id"] == "B001"


def test_add_book():
    book = LibraryService.add_book(
        "B003", "Python Basics", "A. Author", "ISBN003", 2
    )
    assert book["available_copies"] == 2


def test_duplicate_book_rejected():
    with pytest.raises(ValueError):
        LibraryService.add_book(
            "B001", "Duplicate Book", "A. Author", "ISBN999", 1
        )
