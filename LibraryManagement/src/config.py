import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
BOOKS_FILE = os.path.join(DATA_DIR, "books.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
LOGS_FILE = os.path.join(DATA_DIR, "logs.txt")

BORROW_DAYS_LIMIT = 7 