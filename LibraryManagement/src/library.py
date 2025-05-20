import json
import os
from datetime import datetime, timedelta
from book import Book
from config import BOOKS_FILE, BORROW_DAYS_LIMIT
from logger import Logger

class Library:
    def __init__(self, data_file, logger):
        self.data_file = data_file
        self.logger = logger
        self.books = []
        self.load_books()

    def load_books(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                self.books = [Book.from_dict(book) for book in data]
        else:
            self.books = []

    def save_books(self):
        with open(self.data_file, 'w') as file:
            json.dump([book.to_dict() for book in self.books], file, indent=4)

    def add_book(self, title, author, year, isbn, user):
        if user.role != "admin":
            return False, "Only admin can add books."
        for book in self.books:
            if book.isbn == isbn:
                return False, "A book with this ISBN already exists."
        book = Book(title, author, year, isbn)
        self.books.append(book)
        self.save_books()
        self.logger.log(f"User {user.username} added the book '{title}' (ISBN: {isbn}).")
        return True, "Book successfully added."

    def remove_book(self, isbn, user):
        if user.role != "admin":
            return False, "Only admin can remove books."
        for i, book in enumerate(self.books):
            if book.isbn == isbn:
                if not book.is_borrowed:
                    self.books.pop(i)
                    self.save_books()
                    self.logger.log(f"User {user.username} removed the book '{book.title}' (ISBN: {isbn}).")
                    return True, "Book successfully removed."
                else:
                    return False, "Book is currently borrowed and cannot be removed."
        return False, "Book with this ISBN was not found."

    def search_book(self, query):
        query = query.lower()
        results = [
            book for book in self.books
            if query in book.title.lower() or query in book.author.lower() or query == str(book.year)
        ]
        return results

    def borrow_book(self, isbn, user):
        for book in self.books:
            if book.isbn == isbn:
                if not book.is_borrowed:
                    book.is_borrowed = True
                    book.borrowed_by = user.username
                    book.borrow_date = datetime.now()
                    book.due_date = book.borrow_date + timedelta(days=BORROW_DAYS_LIMIT)
                    user.borrow_history.append({
                        "isbn": isbn,
                        "title": book.title,
                        "borrow_date": book.borrow_date.isoformat(),
                        "due_date": book.due_date.isoformat()
                    })
                    self.save_books()
                    self.logger.log(f"User {user.username} borrowed the book '{book.title}' (ISBN: {isbn}).")
                    return True, f"Book successfully borrowed. Due date: {book.due_date.strftime('%Y-%m-%d')}"
                else:
                    return False, "Book has already been borrowed."
        return False, "Book with this ISBN was not found."

    def return_book(self, isbn, user):
        for book in self.books:
            if book.isbn == isbn:
                if book.is_borrowed and book.borrowed_by == user.username:
                    book.is_borrowed = False
                    book.borrowed_by = None
                    book.borrow_date = None
                    book.due_date = None
                    self.save_books()
                    self.logger.log(f"User {user.username} returned the book '{book.title}' (ISBN: {isbn}).")
                    return True, "Book successfully returned."
                else:
                    return False, "This book was not borrowed by you."
        return False, "Book with this ISBN was not found."

    def list_books(self):
        return self.books

    def get_user_borrow_history(self, user):
        return user.borrow_history
