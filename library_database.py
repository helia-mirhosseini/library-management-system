import sqlite3
from library_classes import Book, Member

class Library:
    def __init__(self, db_name='library.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
        self.add_sample_data()
        
    
        
    def create_tables(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS members (
                member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                borrowed_by INTEGER,
                FOREIGN KEY (borrowed_by) REFERENCES members(member_id)
            )
        ''')
        self.conn.commit()
        

    def add_sample_data(self):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM members')
        if c.fetchone()[0] == 0:  # Check if there are no members
            # Insert sample member data
            members = [
                ("Helia Mirhosseini", "13820620"),
                ("Mohamad Mashhadi", "13830424"),
                ("Ilia Mirhosseini", "13840424"),
            ]
            c.executemany('INSERT INTO members (name, password) VALUES (?, ?)', members)

        c.execute('SELECT COUNT(*) FROM books')
        if c.fetchone()[0] == 0:  # Check if there are no books
            # Insert sample book data
            books = [
                ("Harry Potter and the Philosopher's Stone", "J.K. Rowling"),
                ("To Kill a Mockingbird", "Harper Lee"),
                ("1984", "George Orwell"),
                ("Pride and Prejudice", "Jane Austen"),
                ("The Great Gatsby", "F. Scott Fitzgerald"),
            ]
            c.executemany('INSERT INTO books (title, author) VALUES (?, ?)', books)

        self.conn.commit()

    def insert_member(self, member):
        c = self.conn.cursor()
        c.execute('INSERT INTO members (name, password) VALUES (?, ?)', (member.name, member.password))
        self.conn.commit()
        print(f'Member {member.name} added.')

    def delete_member(self, member_id):
        c = self.conn.cursor()
        c.execute('DELETE FROM members WHERE member_id = ?', (member_id,))
        self.conn.commit()
        print(f'Member with ID {member_id} deleted.')

    def search_books(self, title):
        c = self.conn.cursor()
        c.execute('''
            SELECT books.book_id, books.title, books.author, members.name
            FROM books
            LEFT JOIN members ON books.borrowed_by = members.member_id
            WHERE books.title LIKE ?
        ''', ('%' + title + '%',))
        rows = c.fetchall()
        return rows

    def search_members(self, name):
        c = self.conn.cursor()
        c.execute('''
            SELECT members.member_id, members.name, members.password, books.book_id, books.title, books.author
            FROM members
            LEFT JOIN books ON members.member_id = books.borrowed_by
            WHERE members.name LIKE ?
        ''', ('%' + name + '%',))
        rows = c.fetchall()
        return rows

    def get_all_members(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM members')
        rows = c.fetchall()
        return rows

    def get_all_books(self):
        c = self.conn.cursor()
        c.execute('''
            SELECT books.book_id, books.title, books.author, members.name
            FROM books
            LEFT JOIN members ON books.borrowed_by = members.member_id
        ''')
        rows = c.fetchall()
        return rows

    def insert_book(self, book):
        c = self.conn.cursor()
        c.execute('INSERT INTO books (title, author) VALUES (?, ?)', (book.title, book.author))
        self.conn.commit()
        print(f'Book "{book.title}" added.')

    def delete_book(self, book_id):
        c = self.conn.cursor()
        c.execute('DELETE FROM books WHERE book_id = ?', (book_id,))
        self.conn.commit()
        print(f'Book with ID {book_id} deleted.')

    def borrow_book(self, book_id, member_id):
        c = self.conn.cursor()
        
        # Check if the book exists
        c.execute('SELECT book_id FROM books WHERE book_id = ?', (book_id,))
        book = c.fetchone()
        if not book:
            print(f'Book with ID {book_id} does not exist.')
            return

        # Check if the book is already borrowed
        c.execute('SELECT borrowed_by FROM books WHERE book_id = ?', (book_id,))
        borrowed_by = c.fetchone()[0]
        
        if borrowed_by:
            c.execute('SELECT name FROM members WHERE member_id = ?', (borrowed_by,))
            borrower_name = c.fetchone()[0]
            print(f'The book is already borrowed by {borrower_name}. It is currently unavailable.')
        else:
            # Retrieve member name
            c.execute('SELECT name FROM members WHERE member_id = ?', (member_id,))
            member = c.fetchone()
            member_name = member[0] if member else "Unknown"

            # Retrieve book title
            c.execute('SELECT title FROM books WHERE book_id = ?', (book_id,))
            book = c.fetchone()
            book_title = book[0] if book else "Unknown"

            # Update the borrowed_by field
            c.execute('UPDATE books SET borrowed_by = ? WHERE book_id = ?', (member_id, book_id))
            self.conn.commit()

            print(f'Book "{book_title}" borrowed by member "{member_name}".')
            
    def return_book(self, book_id):
        c = self.conn.cursor()

        # Check if the book exists
        c.execute('SELECT book_id FROM books WHERE book_id = ?', (book_id,))
        book = c.fetchone()
        if not book:
            print(f'Book with ID {book_id} does not exist.')
            return

        # Retrieve book title
        c.execute('SELECT title FROM books WHERE book_id = ?', (book_id,))
        book = c.fetchone()
        book_title = book[0] if book else "Unknown"

        # Update the borrowed_by field to None
        c.execute('UPDATE books SET borrowed_by = NULL WHERE book_id = ?', (book_id,))
        self.conn.commit()

        print(f'Book "{book_title}" has been returned.')