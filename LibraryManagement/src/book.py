from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, year, isbn):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn
        self.is_borrowed = False
        self.borrowed_by = None
        self.borrow_date = None
        self.due_date = None

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "isbn": self.isbn,
            "is_borrowed": self.is_borrowed,
            "borrowed_by": self.borrowed_by,
            "borrow_date": self.borrow_date.isoformat() if self.borrow_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None
        }

    @classmethod
    def from_dict(cls, data):
        book = cls(data["title"], data["author"], data["year"], data["isbn"])
        book.is_borrowed = data["is_borrowed"]
        book.borrowed_by = data.get("borrowed_by")
        book.borrow_date = datetime.fromisoformat(data["borrow_date"]) if data.get("borrow_date") else None
        book.due_date = datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None
        return book