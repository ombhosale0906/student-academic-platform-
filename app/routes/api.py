from flask import Blueprint, request, jsonify
from app.services.library_service import LibraryService

api_bp = Blueprint("api", __name__)


@api_bp.route("/health", methods=["GET"])
def healthcheck():
    return jsonify({
        "status": "UP",
        "service": "Enterprise Smart Library Management Platform",
        "version": "1.0.0"
    }), 200


@api_bp.route("/users", methods=["POST"])
def register_user():
    data = request.get_json() or {}
    try:
        user = LibraryService.add_user(
            data.get("user_id"),
            data.get("name"),
            data.get("email"),
            data.get("role", "Student")
        )
        return jsonify({"message": "User registered successfully", "user": user}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = LibraryService.get_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


@api_bp.route("/books", methods=["GET"])
def list_books():
    query = request.args.get("q", "")
    books = LibraryService.search_books(query)
    return jsonify({"count": len(books), "books": books}), 200


@api_bp.route("/books", methods=["POST"])
def add_book():
    data = request.get_json() or {}
    try:
        book = LibraryService.add_book(
            data.get("book_id"),
            data.get("title"),
            data.get("author"),
            data.get("isbn"),
            int(data.get("total_copies", 1))
        )
        return jsonify({"message": "Book added successfully", "book": book}), 201
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/borrow", methods=["POST"])
def borrow_book():
    data = request.get_json() or {}
    try:
        loan = LibraryService.borrow_book(
            data.get("user_id"),
            data.get("book_id")
        )
        return jsonify({"message": "Book checked out successfully", "loan": loan}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/return", methods=["POST"])
def return_book():
    data = request.get_json() or {}
    try:
        loan = LibraryService.return_book(
            data.get("user_id"),
            data.get("book_id")
        )
        return jsonify({"message": "Book returned successfully", "loan": loan}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
