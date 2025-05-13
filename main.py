from library_database import Library
from library_classes import Book, Member, Manager

def main():
    library = Library()
    manager = Manager(0, 'Manager', 'manager_password')

    while True:
        print("\n1. Insert Member")
        print("2. Delete Member")
        print("3. Search Books")
        print("4. Search Members")
        print("5. Insert Book")
        print("6. Delete Book")
        print("7. Show All Members")
        print("8. Show All Books")
        print("9. Borrow Book")
        print("10. Return Book")
        print("11. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter Member Name: ")
            password = input("Enter Member Password: ")
            member = Member(None, name, password)
            manager.add_member(library, member)
        elif choice == '2':
            member_id = int(input("Enter Member ID to delete: "))
            manager.delete_member(library, member_id)
        elif choice == '3':
            title = input("Enter Book Title to search: ")
            books = library.search_books(title)
            if books:
                for book in books:
                    print(f'Book ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Borrowed By: {book[3] if book[3] else "Not borrowed"}')
            else:
                print("No books found.")
        elif choice == '4':
            name = input("Enter Member Name to search: ")
            members = library.search_members(name)
            if members:
                for member in members:
                    member_id, member_name, password, book_id, book_title, book_author = member
                    print(f'Member ID: {member_id}, Name: {member_name}, Password: {password}')
                    if book_id:
                        print(f'   Borrowed Book ID: {book_id}, Title: {book_title}, Author: {book_author}')
            else:
                print("No members found.")
        elif choice == '5':
            title = input("Enter Book Title: ")
            author = input("Enter Book Author: ")
            book = Book(None, title, author, None)
            manager.add_book(library, book)
        elif choice == '6':
            book_id = int(input("Enter Book ID to delete: "))
            manager.delete_book(library, book_id)
        elif choice == '7':
            members = library.get_all_members()
            if members:
                for member in members:
                    print(f'Member ID: {member[0]}, Name: {member[1]}, Password: {member[2]}')
            else:
                print("No members found.")
        elif choice == '8':
            books = library.get_all_books()
            if books:
                for book in books:
                    print(f'Book ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Borrowed By: {book[3] if book[3] else "Not borrowed"}')
            else:
                print("No books found.")
        elif choice == '9':
            book_id = int(input("Enter Book ID to borrow: "))
            member_name = input("Enter Member Name who is borrowing the book: ")
            
            # Retrieve member ID based on name
            members = library.search_members(member_name)
            if members:
                member_id = members[0][0]  # Assuming the first match is the correct one
                library.borrow_book(book_id, member_id)
                
            else:
                print(f'Member with name {member_name} does not exist.')
        elif choice == '10':
            book_id = int(input("Enter Book ID to return: "))
            library.return_book(book_id)
            
        elif choice == '11':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
