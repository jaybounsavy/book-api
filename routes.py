from flask import Blueprint, jsonify, request
from models.book import Book
from typing import List, Optional

# Create Blueprint for book routes
book_bp = Blueprint('books', __name__, url_prefix='/api/books')

# In-memory storage for books (minimum 5 book objects as requested)
books_data: List[Book] = [
    Book(1, "To Kill a Mockingbird", "Harper Lee", 1960, "English", 336),
    Book(2, "1984", "George Orwell", 1949, "English", 328),
    Book(3, "Pride and Prejudice", "Jane Austen", 1813, "English", 279),
    Book(4, "The Great Gatsby", "F. Scott Fitzgerald", 1925, "English", 180),
    Book(5, "One Hundred Years of Solitude", "Gabriel García Márquez", 1967, "Spanish", 417),
    Book(6, "The Catcher in the Rye", "J.D. Salinger", 1951, "English", 277),
    Book(7, "Don Quixote", "Miguel de Cervantes", 1605, "Spanish", 863)
]

def find_book_by_id(book_id: int) -> Optional[Book]:
    """Helper function to find a book by its ID"""
    return next((book for book in books_data if book.id == book_id), None)

def get_next_book_id() -> int:
    """Helper function to get the next available book ID"""
    return max(book.id for book in books_data) + 1 if books_data else 1

@book_bp.route('/', methods=['GET'])
def get_all_books():
    """Get all books"""
    try:
        return jsonify({
            "status": "success",
            "data": [book.to_dict() for book in books_data],
            "total": len(books_data)
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            "status": "error",
            "message": "Failed to fetch books"
        }), 500

@book_bp.route('/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id: int):
    """Get a book by its ID"""
    try:
        book = find_book_by_id(book_id)
        if book:
            return jsonify({
                "status": "success",
                "data": book.to_dict()
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": f"Book with ID {book_id} not found"
            }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Failed to fetch book"
        }), 500

@book_bp.route('/', methods=['POST'])
def create_book():
    """Create a new book"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'author', 'language']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    "status": "error",
                    "message": f"Missing required field: {field}"
                }), 400
        
        # Create new book with auto-generated ID
        new_book = Book(
            id=get_next_book_id(),
            title=data['title'],
            author=data['author'],
            language=data['language'],
            isbn=data.get('isbn'),
            published_year=data.get('published_year'),
            genre=data.get('genre')
        )
        
        books_data.append(new_book)
        
        return jsonify({
            "status": "success",
            "message": "Book created successfully",
            "data": new_book.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Failed to create book"
        }), 500

@book_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id: int):
    """Update a book by its ID"""
    try:
        book = find_book_by_id(book_id)
        if not book:
            return jsonify({
                "status": "error",
                "message": f"Book with ID {book_id} not found"
            }), 404
        
        data = request.get_json()
        
        # Update book fields if provided in request
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'language' in data:
            book.language = data['language']
        if 'isbn' in data:
            book.isbn = data['isbn']
        if 'published_year' in data:
            book.published_year = data['published_year']
        if 'genre' in data:
            book.genre = data['genre']
        
        return jsonify({
            "status": "success",
            "message": "Book updated successfully",
            "data": book.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Failed to update book"
        }), 500

@book_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id: int):
    """Delete a book by its ID"""
    try:
        book = find_book_by_id(book_id)
        if not book:
            return jsonify({
                "status": "error",
                "message": f"Book with ID {book_id} not found"
            }), 404
        
        books_data.remove(book)
        
        return jsonify({
            "status": "success",
            "message": f"Book with ID {book_id} deleted successfully"
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Failed to delete book"
        }), 500

@book_bp.route('/search', methods=['GET'])
def search_book():
    """Search books by title, author, or language"""
    try:
        query = request.args.get('q', '').lower().strip()
        
        if not query:
            return jsonify({
                "status": "error",
                "message": "Search query parameter 'q' is required"
            }), 400
        
        # Search in title, author, and language fields
        matching_books = []
        for book in books_data:
            if (query in book.title.lower() or 
                query in book.author.lower() or 
                query in book.language.lower()):
                matching_books.append(book)
        
        return jsonify({
            "status": "success",
            "data": [book.to_dict() for book in matching_books],
            "total": len(matching_books),
            "query": query
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Failed to search books"
        }), 500