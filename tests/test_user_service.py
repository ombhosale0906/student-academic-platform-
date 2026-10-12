import pytest
from app.services.library_service import LibraryService


def test_get_existing_user():
    user = LibraryService.get_user("U101")
    assert user["name"] == "Alice Johnson"


def test_add_user():
    user = LibraryService.add_user(
        "U103", "Test Student", "test@example.com"
    )
    assert user["user_id"] == "U103"
    assert user["role"] == "Student"


def test_duplicate_user_rejected():
    with pytest.raises(ValueError):
        LibraryService.add_user(
            "U101", "Another Alice", "another@example.com"
        )


def test_delete_user():
    LibraryService.add_user("U103", "Test", "test@example.com")
    assert LibraryService.delete_user("U103") is True
    assert LibraryService.get_user("U103") is None
