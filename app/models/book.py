class Book:
    """Book entity for the library platform."""

    def __init__(self, book_id, title, author, isbn,
                 total_copies=1, available_copies=None):
        if not all([book_id, title, author, isbn]):
            raise ValueError("Book ID, title, author and ISBN are required.")

        if total_copies < 1:
            raise ValueError("Total copies must be at least 1.")

        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.total_copies = total_copies
        self.available_copies = (
            total_copies if available_copies is None
            else available_copies
        )
