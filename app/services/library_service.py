from datetime import datetime, timezone
from database.db import db


class LibraryService:
    """Business logic for the library management platform."""

    @staticmethod
    def add_user(user_id, name, email, role="Student"):
        if not user_id or not name or not email:
            raise ValueError("User ID, name and email are required.")
        if user_id in db.users:
            raise ValueError(f"User '{user_id}' already exists.")

        user = {
            "user_id": user_id,
            "name": name,
            "email": email,
            "role": role,
            "active_loans": 0
        }
        db.users[user_id] = user
        return user

    @staticmethod
    def get_user(user_id):
        return db.users.get(user_id)

    @staticmethod
    def delete_user(user_id):
        user = db.users.get(user_id)
        if not user:
            raise ValueError("User not found.")
        if user["active_loans"] > 0:
            raise ValueError("Cannot delete a user with active loans.")
        del db.users[user_id]
        return True

    @staticmethod
    def add_book(book_id, title, author, isbn, total_copies=1):
        if not all([book_id, title, author, isbn]):
            raise ValueError("All book fields are required.")
        if book_id in db.books:
            raise ValueError(f"Book '{book_id}' already exists.")
        if total_copies < 1:
            raise ValueError("Total copies must be at least 1.")

        book = {
            "book_id": book_id,
            "title": title,
            "author": author,
            "isbn": isbn,
            "total_copies": total_copies,
            "available_copies": total_copies
        }
        db.books[book_id] = book
        return book

    @staticmethod
    def get_book(book_id):
        return db.books.get(book_id)

    @staticmethod
    def search_books(query=""):
        query = query.lower().strip()
        if not query:
            return list(db.books.values())

        return [
            book for book in db.books.values()
            if query in book["title"].lower()
            or query in book["author"].lower()
            or query in book["isbn"].lower()
        ]

    @staticmethod
    def borrow_book(user_id, book_id):
        user = db.users.get(user_id)
        book = db.books.get(book_id)

        if not user:
            raise ValueError("User not found.")
        if not book:
            raise ValueError("Book not found.")

        quota = 5 if user["role"] == "Faculty" else 3
        if user["active_loans"] >= quota:
            raise ValueError("Borrowing limit reached.")
        if book["available_copies"] < 1:
            raise ValueError("No copies available.")

        book["available_copies"] -= 1
        user["active_loans"] += 1

        loan = {
            "loan_id": f"L-{len(db.loans) + 1:04d}",
            "user_id": user_id,
            "book_id": book_id,
            "borrowed_at": datetime.now(timezone.utc).isoformat(),
            "status": "ACTIVE"
        }
        db.loans.append(loan)
        return loan

    @staticmethod
    def return_book(user_id, book_id):
        user = db.users.get(user_id)
        book = db.books.get(book_id)

        if not user:
            raise ValueError("User not found.")
        if not book:
            raise ValueError("Book not found.")

        loan = next(
            (
                item for item in db.loans
                if item["user_id"] == user_id
                and item["book_id"] == book_id
                and item["status"] == "ACTIVE"
            ),
            None
        )

        if not loan:
            raise ValueError("No active loan found for this user and book.")

        loan["status"] = "RETURNED"
        loan["returned_at"] = datetime.now(timezone.utc).isoformat()
        book["available_copies"] += 1
        user["active_loans"] -= 1
        return loan
