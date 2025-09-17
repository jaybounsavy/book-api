from dataclasses import dataclass
from typing import Optional

@dataclass
class Book:
    """Book model class representing a book entity"""
    id: int
    title: str
    author: str
    language: str
    isbn: Optional[str] = None
    published_year: Optional[int] = None
    genre: Optional[str] = None
    
    def to_dict(self):
        """Convert Book instance to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'language': self.language,
            'isbn': self.isbn,
            'published_year': self.published_year,
            'genre': self.genre
        }
        
    @classmethod
    def from_dict(cls, data):
        """Create Book instance from dictionary"""
        return cls(
            id=data.get('id'),
            title=data.get('title'),
            author=data.get('author'),
            language=data.get('language'),
            isbn=data.get('isbn'),
            published_year=data.get('published_year'),
            genre=data.get('genre')
        )