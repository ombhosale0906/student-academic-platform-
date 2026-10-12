class User:
    """User entity with role and borrowing information."""

    def __init__(self, user_id, name, email, role="Student",
                 active_loans=0):
        if not all([user_id, name, email]):
            raise ValueError("User ID, name and email are required.")

        if role not in ("Student", "Faculty"):
            raise ValueError("Role must be Student or Faculty.")

        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.active_loans = active_loans
