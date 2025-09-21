# main_library.py
from library_system import *
import sys

def main():
    while True:
        print("\n=== Library Management System ===")
        print("1. Add Member")
        print("2. Add Book")
        print("3. List All Books")
        print("4. Search Books")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. Update Book Stock")
        print("8. Update Member Email")
        print("9. Delete Member")
        print("10. Delete Book")
        print("11. Show Member Borrowed Books")
        print("12. Top 5 Borrowed Books")
        print("13. Members with Overdue Books")
        print("14. Count Books Borrowed Per Member")
        print("0. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Member name: ")
            email = input("Member email: ")
            print(add_member(name, email))
        elif choice == "2":
            title = input("Book title: ")
            author = input("Author: ")
            category = input("Category: ")
            stock = int(input("Stock: "))
            print(add_book(title, author, category, stock))
        elif choice == "3":
            list_books()
        elif choice == "4":
            term = input("Enter search term: ")
            search_books(term)
        elif choice == "5":
            member_id = int(input("Member ID: "))
            book_id = int(input("Book ID: "))
            borrow_book(member_id, book_id)
        elif choice == "6":
            member_id = int(input("Member ID: "))
            book_id = int(input("Book ID: "))
            return_book(member_id, book_id)
        elif choice == "7":
            book_id = int(input("Book ID: "))
            new_stock = int(input("New stock: "))
            print(update_book_stock(book_id, new_stock))
        elif choice == "8":
            member_id = int(input("Member ID: "))
            new_email = input("New email: ")
            print(update_member_email(member_id, new_email))
        elif choice == "9":
            member_id = int(input("Member ID: "))
            print(delete_member(member_id))
        elif choice == "10":
            book_id = int(input("Book ID: "))
            print(delete_book(book_id))
        elif choice == "11":
            member_id = int(input("Member ID: "))
            member_borrowed_books(member_id)
        elif choice == "12":
            top_5_borrowed_books()
        elif choice == "13":
            members_with_overdue_books()
        elif choice == "14":
            count_books_borrowed_per_member()
        elif choice == "0":
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
