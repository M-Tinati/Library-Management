import os
from library import Library
from user import UserManager
from config import BOOKS_FILE, USERS_FILE, LOGS_FILE
from logger import Logger

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    logger = Logger(LOGS_FILE)
    user_manager = UserManager(USERS_FILE)
    library = Library(BOOKS_FILE, logger)
    current_user = None

    while True:
        clear_screen()
        if not current_user:
            print("=== Library ===")
            print("1. login")
            print("2. sign up")
            print("3. exit")
            choice = input("choose the number (1-3): ")

            if choice == "1":
                username = input("username: ")
                password = input("password: ")
                success, result = user_manager.login(username, password)
                if success:
                    current_user = result
                    logger.log(f"user {username} login done")
                    print(f"welcome {username}!")
                else:
                    print(result)
                input("press ENTER for next step ...")

            elif choice == "2":
                username = input("username: ")
                password = input("password: ")
                role = "admin" if input("are you admin (y/n): ").lower() == 'y' else "member"
                success, message = user_manager.register(username, password, role)
                print(message)
                if success:
                    logger.log(f"new user {username} with {role} login")
                input("press ENTER for next step ...")

            elif choice == "3":
                print("come back again, bye")
                break

            else:
                print("error")
                input("press ENTER for next step ...")

        else:
            clear_screen()
            print(f"=== Library Management System - User: {current_user.username} ({current_user.role}) ===")
            print("1. Add Book" if current_user.role == "admin" else "1. Search Book")
            print("2. Remove Book" if current_user.role == "admin" else "2. Borrow Book")
            print("3. Search Book" if current_user.role == "admin" else "3. Return Book")
            print("4. Borrow Book" if current_user.role == "admin" else "4. Show All Books")
            print("5. Return Book" if current_user.role == "admin" else "5. View Borrow History")
            print("6. Show All Books" if current_user.role == "admin" else "6. Logout")
            print("7. View Borrow History" if current_user.role == "admin" else "7. Logout")
            print("8. Logout" if current_user.role == "admin" else "")

            choice = input("Enter your choice: ")

            if choice == "1" and current_user.role == "admin":
                title = input("Book Title: ")
                author = input("Book Author: ")
                year = input("Year of Publication: ")
                isbn = input("ISBN: ")
                success, message = library.add_book(title, author, year, isbn, current_user)
                print(message)
                user_manager.save_users()

            elif (choice == "1" and current_user.role == "member") or (choice == "3" and current_user.role == "admin"):
                query = input("Title, Author, or Year for search: ")
                results = library.search_book(query)
                if results:
                    print("\nSearch Results:")
                    for book in results:
                        status = f"Borrowed by {book.borrowed_by}, Due: {book.due_date.strftime('%Y-%m-%d')}" if book.is_borrowed else "Available"
                        print(f"Title: {book.title}, Author: {book.author}, Year: {book.year}, ISBN: {book.isbn}, Status: {status}")
                else:
                    print("No books found.")
                logger.log(f"User {current_user.username} performed a search with query '{query}'.")

            elif choice == "2" and current_user.role == "admin":
                isbn = input("ISBN of the book to remove: ")
                success, message = library.remove_book(isbn, current_user)
                print(message)
                user_manager.save_users()

            elif (choice == "2" and current_user.role == "member") or (choice == "4" and current_user.role == "admin"):
                isbn = input("ISBN of the book to borrow: ")
                success, message = library.borrow_book(isbn, current_user)
                print(message)
                user_manager.save_users()

            elif (choice == "3" and current_user.role == "member") or (choice == "5" and current_user.role == "admin"):
                isbn = input("ISBN of the book to return: ")
                success, message = library.return_book(isbn, current_user)
                print(message)
                user_manager.save_users()

            elif (choice == "4" and current_user.role == "member") or (choice == "6" and current_user.role == "admin"):
                books = library.list_books()
                if books:
                    print("\nBook List:")
                    for book in books:
                        status = f"Borrowed by {book.borrowed_by}, Due: {book.due_date.strftime('%Y-%m-%d')}" if book.is_borrowed else "Available"
                        print(f"Title: {book.title}, Author: {book.author}, Year: {book.year}, ISBN: {book.isbn}, Status: {status}")
                else:
                    print("No books available in the library.")
                logger.log(f"User {current_user.username} viewed the book list.")

            elif (choice == "5" and current_user.role == "member") or (choice == "7" and current_user.role == "admin"):
                history = library.get_user_borrow_history(current_user)
                if history:
                    print("\nBorrow History:")
                    for entry in history:
                        print(f"Title: {entry['title']}, ISBN: {entry['isbn']}, Borrow Date: {entry['borrow_date']}, Due: {entry['due_date']}")
                else:
                    print("You have not borrowed any books.")
                logger.log(f"User {current_user.username} viewed their borrow history.")

            elif (choice == "6" and current_user.role == "member") or (choice == "8" and current_user.role == "admin"):
                logger.log(f"User {current_user.username} logged out.")
                current_user = None

            else:
                print("Invalid choice.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
