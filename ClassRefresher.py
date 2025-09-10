"""
Library Management System - Python Classes Exercise

This project demonstrates:
- Class creation and initialization
- Instance methods, class methods, static methods
- Properties and property decorators
- Inheritance and method overriding
- Abstract base classes
- Special methods (__str__, __repr__, __eq__, etc.)
- Composition and aggregation
- Class variables vs instance variables
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional
import json


class Person(ABC):
    """Abstract base class for all people in the library system"""
    
    # TODO: Add class variable to track total number of people created
    total_people = 0
    
    def __init__(self, name: str, email: str, phone: str):
        # TODO: Initialize instance attributes
        self._name = name
        self._email = email
        self._phone = phone
        self._id = self._generate_id()
        
        # TODO: Increment class variable when new person is created
        Person.total_people += 1
    
    @property
    def name(self) -> str:
        # TODO: Create getter for name (make it read-only)
        return self._name
    
    @property
    def email(self) -> str:
        # TODO: Create getter for email
        return self._email
    
    @email.setter
    def email(self, value: str) -> None:
        # TODO: Create setter for email with validation
        if "@" not in value:
            raise ValueError("Invalid email format")
        self._email = value
    
    @property
    def phone(self) -> str:
        # TODO: Create getter for phone
        return self._phone
    
    @phone.setter  
    def phone(self, value: str) -> None:
        # TODO: Create setter for phone with validation
        if len(value) < 10:
            raise ValueError("Phone number must be at least 10 digits")
        self._phone = value
    
    @classmethod
    def get_total_people(cls) -> int:
        # TODO: Return total number of people created
        return cls.total_people
    
    @staticmethod
    def validate_email(email: str) -> bool:
        # TODO: Static method to validate email format
        return "@" in email and "." in email
    
    def _generate_id(self) -> str:
        # TODO: Generate unique ID (private method)
        return f"{self.__class__.__name__[:3].upper()}{Person.total_people + 1:04d}"
    
    @abstractmethod
    def get_permissions(self) -> List[str]:
        # TODO: Abstract method that must be implemented by subclasses
        pass
    
    def __str__(self) -> str:
        # TODO: String representation for users
        return f"{self.name} ({self._id})"
    
    def __repr__(self) -> str:
        # TODO: Developer-friendly representation
        return f"{self.__class__.__name__}(name='{self.name}', email='{self.email}')"
    
    def __eq__(self, other) -> bool:
        # TODO: Compare persons by ID
        if not isinstance(other, Person):
            return False
        return self._id == other._id


class Member(Person):
    """Library member who can borrow books"""
    
    def __init__(self, name: str, email: str, phone: str, membership_type: str = "basic"):
        # TODO: Call parent constructor
        super().__init__(name, email, phone)
        self._membership_type = membership_type
        self._borrowed_books = []
        self._membership_date = datetime.now()
    
    @property
    def membership_type(self) -> str:
        # TODO: Getter for membership type
        return self._membership_type
    
    @membership_type.setter
    def membership_type(self, value: str) -> None:
        # TODO: Setter with validation for membership type
        valid_types = ["basic", "premium", "student"]
        if value not in valid_types:
            raise ValueError(f"Invalid membership type. Must be one of: {valid_types}")
        self._membership_type = value
    
    @property
    def borrowed_books(self) -> List:
        # TODO: Return copy of borrowed books list (read-only)
        return self._borrowed_books.copy()
    
    def get_permissions(self) -> List[str]:
        # TODO: Implement abstract method - return member permissions
        base_permissions = ["borrow_books", "reserve_books", "access_catalog"]
        if self._membership_type == "premium":
            base_permissions.extend(["priority_reservations", "extended_borrowing"])
        return base_permissions
    
    def borrow_book(self, book) -> bool:
        # TODO: Add book to borrowed books if allowed
        max_books = {"basic": 3, "premium": 10, "student": 5}
        if len(self._borrowed_books) >= max_books[self._membership_type]:
            return False
        
        self._borrowed_books.append(book)
        return True
    
    def return_book(self, book) -> bool:
        # TODO: Remove book from borrowed books
        if book in self._borrowed_books:
            self._borrowed_books.remove(book)
            return True
        return False
    
    @classmethod
    def create_student_member(cls, name: str, email: str, phone: str):
        # TODO: Class method to create student member with discount
        return cls(name, email, phone, "student")
    
    def get_membership_duration(self) -> int:
        # TODO: Return membership duration in days
        return (datetime.now() - self._membership_date).days


class Librarian(Person):
    """Librarian who manages the library system"""
    
    def __init__(self, name: str, email: str, phone: str, employee_id: str, department: str = "General"):
        # TODO: Call parent constructor and add librarian-specific attributes
        super().__init__(name, email, phone)
        self._employee_id = employee_id
        self._department = department
        self._hire_date = datetime.now()
    
    @property
    def employee_id(self) -> str:
        # TODO: Getter for employee ID (read-only)
        return self._employee_id
    
    @property
    def department(self) -> str:
        # TODO: Getter for department
        return self._department
    
    @department.setter
    def department(self, value: str) -> None:
        # TODO: Setter for department
        self._department = value
    
    def get_permissions(self) -> List[str]:
        # TODO: Implement abstract method - return librarian permissions
        return [
            "manage_books", "manage_members", "issue_fines", 
            "access_reports", "manage_reservations", "override_limits"
        ]
    
    def add_book_to_catalog(self, book) -> bool:
        # TODO: Method to add book (placeholder for now)
        print(f"Librarian {self.name} added book: {book}")
        return True
    
    def issue_fine(self, member: Member, amount: float, reason: str) -> None:
        # TODO: Issue fine to member
        print(f"Fine of ${amount} issued to {member.name} for: {reason}")


class Book:
    """Represents a book in the library"""
    
    # TODO: Class variable to track total books created
    total_books = 0
    
    def __init__(self, title: str, author: str, isbn: str, publication_year: int, genre: str):
        # TODO: Initialize book attributes
        self._title = title
        self._author = author
        self._isbn = isbn
        self._publication_year = publication_year
        self._genre = genre
        self._is_available = True
        self._borrower = None
        self._due_date = None
        
        Book.total_books += 1
    
    @property
    def title(self) -> str:
        # TODO: Getter for title
        return self._title
    
    @property
    def author(self) -> str:
        # TODO: Getter for author
        return self._author
    
    @property
    def isbn(self) -> str:
        # TODO: Getter for ISBN (read-only)
        return self._isbn
    
    @property
    def is_available(self) -> bool:
        # TODO: Getter for availability status
        return self._is_available
    
    @property
    def borrower(self) -> Optional[Member]:
        # TODO: Getter for current borrower
        return self._borrower
    
    @property
    def due_date(self) -> Optional[datetime]:
        # TODO: Getter for due date
        return self._due_date
    
    def borrow(self, member: Member, days: int = 14) -> bool:
        # TODO: Mark book as borrowed if available
        if not self._is_available:
            return False
        
        self._is_available = False
        self._borrower = member
        self._due_date = datetime.now() + timedelta(days=days)
        return True
    
    def return_book(self) -> bool:
        # TODO: Mark book as returned
        if self._is_available:
            return False
        
        self._is_available = True
        self._borrower = None
        self._due_date = None
        return True
    
    def is_overdue(self) -> bool:
        # TODO: Check if book is overdue
        if self._is_available or not self._due_date:
            return False
        return datetime.now() > self._due_date
    
    @classmethod
    def from_json(cls, json_data: str):
        # TODO: Create book instance from JSON string
        data = json.loads(json_data)
        return cls(
            data['title'], 
            data['author'], 
            data['isbn'], 
            data['publication_year'], 
            data['genre']
        )
    
    @staticmethod
    def is_valid_isbn(isbn: str) -> bool:
        # TODO: Validate ISBN format (simplified)
        return len(isbn.replace('-', '').replace(' ', '')) in [10, 13]
    
    def to_dict(self) -> dict:
        # TODO: Convert book to dictionary
        return {
            'title': self._title,
            'author': self._author,
            'isbn': self._isbn,
            'publication_year': self._publication_year,
            'genre': self._genre,
            'is_available': self._is_available,
            'borrower': self._borrower.name if self._borrower else None,
            'due_date': self._due_date.isoformat() if self._due_date else None
        }
    
    def __str__(self) -> str:
        # TODO: String representation for users
        status = "Available" if self._is_available else f"Borrowed by {self._borrower.name}"
        return f"'{self._title}' by {self._author} - {status}"
    
    def __repr__(self) -> str:
        # TODO: Developer representation
        return f"Book(title='{self._title}', author='{self._author}', isbn='{self._isbn}')"
    
    def __eq__(self, other) -> bool:
        # TODO: Compare books by ISBN
        if not isinstance(other, Book):
            return False
        return self._isbn == other._isbn
    
    def __lt__(self, other) -> bool:
        # TODO: Compare books by title for sorting
        if not isinstance(other, Book):
            return NotImplemented
        return self._title < other._title


class Library:
    """Main library class that manages books and members"""
    
    def __init__(self, name: str, address: str):
        # TODO: Initialize library attributes
        self._name = name
        self._address = address
        self._books = []
        self._members = []
        self._librarians = []
    
    @property
    def name(self) -> str:
        # TODO: Getter for library name
        return self._name
    
    @property
    def books_count(self) -> int:
        # TODO: Return total number of books
        return len(self._books)
    
    @property
    def members_count(self) -> int:
        # TODO: Return total number of members
        return len(self._members)
    
    @property
    def available_books_count(self) -> int:
        # TODO: Return number of available books
        return sum(1 for book in self._books if book.is_available)
    
    def add_book(self, book: Book) -> bool:
        # TODO: Add book to library if not already exists
        if book in self._books:
            return False
        self._books.append(book)
        return True
    
    def remove_book(self, isbn: str) -> bool:
        # TODO: Remove book by ISBN
        for book in self._books:
            if book.isbn == isbn:
                if not book.is_available:
                    return False  # Can't remove borrowed book
                self._books.remove(book)
                return True
        return False
    
    def add_member(self, member: Member) -> bool:
        # TODO: Add member to library
        if member in self._members:
            return False
        self._members.append(member)
        return True
    
    def find_book_by_isbn(self, isbn: str) -> Optional[Book]:
        # TODO: Find book by ISBN
        for book in self._books:
            if book.isbn == isbn:
                return book
        return None
    
    def find_books_by_author(self, author: str) -> List[Book]:
        # TODO: Find all books by author
        return [book for book in self._books if author.lower() in book.author.lower()]
    
    def find_member_by_email(self, email: str) -> Optional[Member]:
        # TODO: Find member by email
        for member in self._members:
            if member.email == email:
                return member
        return None
    
    def get_overdue_books(self) -> List[Book]:
        # TODO: Return list of overdue books
        return [book for book in self._books if book.is_overdue()]
    
    def get_member_borrowed_books(self, member: Member) -> List[Book]:
        # TODO: Get all books borrowed by a specific member
        return [book for book in self._books if book.borrower == member]
    
    @classmethod
    def create_default_library(cls):
        # TODO: Class method to create library with default settings
        return cls("City Public Library", "123 Main Street")
    
    def generate_report(self) -> dict:
        # TODO: Generate library statistics report
        return {
            "library_name": self._name,
            "total_books": self.books_count,
            "available_books": self.available_books_count,
            "borrowed_books": self.books_count - self.available_books_count,
            "total_members": self.members_count,
            "overdue_books": len(self.get_overdue_books())
        }
    
    def __len__(self) -> int:
        # TODO: Return total number of books when len() is called
        return len(self._books)
    
    def __contains__(self, item) -> bool:
        # TODO: Support 'in' operator for books and members
        if isinstance(item, Book):
            return item in self._books
        elif isinstance(item, Member):
            return item in self._members
        return False
    
    def __str__(self) -> str:
        # TODO: String representation
        return f"{self._name} - {self.books_count} books, {self.members_count} members"


# TODO: Create a demonstration function that shows all the concepts
def demonstrate_library_system():
    """
    Demonstration function to test all implemented features
    Add your test code here to verify everything works correctly
    """
    
    # TODO: Create library instance
    library = Library.create_default_library()
    
    # TODO: Create some books using different methods
    book1 = Book("Python Programming", "John Smith", "978-0123456789", 2023, "Programming")
    
    book_json = '{"title": "Data Structures", "author": "Jane Doe", "isbn": "978-9876543210", "publication_year": 2022, "genre": "Computer Science"}'
    book2 = Book.from_json(book_json)
    
    # TODO: Create members using different methods
    member1 = Member("Alice Johnson", "alice@email.com", "1234567890", "premium")
    member2 = Member.create_student_member("Bob Wilson", "bob@student.edu", "0987654321")
    
    # TODO: Create librarian
    librarian = Librarian("Carol Admin", "carol@library.gov", "5555555555", "EMP001", "IT")
    
    # TODO: Add books and members to library
    library.add_book(book1)
    library.add_book(book2)
    library.add_member(member1)
    library.add_member(member2)
    
    # TODO: Demonstrate borrowing and returning
    book1.borrow(member1)
    member1.borrow_book(book1)
    
    # TODO: Print various information using different methods and properties
    print(f"Library: {library}")
    print(f"Total people created: {Person.get_total_people()}")
    print(f"Member permissions: {member1.get_permissions()}")
    print(f"Librarian permissions: {librarian.get_permissions()}")
    print(f"Book status: {book1}")
    print(f"Library report: {library.generate_report()}")
    
    # TODO: Test property setters and validation
    try:
        member1.email = "invalid_email"
    except ValueError as e:
        print(f"Email validation works: {e}")
    
    # TODO: Test static methods
    print(f"Valid ISBN: {Book.is_valid_isbn('978-0123456789')}")
    print(f"Valid email: {Person.validate_email('test@example.com')}")


if __name__ == "__main__":
    demonstrate_library_system()