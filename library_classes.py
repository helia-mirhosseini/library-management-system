class Book:
    def __init__(self, book_id, title, author, borrowed_by=None):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.borrowed_by = borrowed_by

    def __str__(self):
        return f'Book ID: {self.book_id}, Title: {self.title}, Author: {self.author}, Borrowed By: {self.borrowed_by}'

class Person:
    def __init__(self, person_id, name, password):
        self.person_id = person_id
        self.name = name
        self.password = password

    def __str__(self):
        return f'Person ID: {self.person_id}, Name: {self.name}, Password: {self.password}'

class Member(Person):
    def __init__(self, person_id, name, password):
        super().__init__(person_id, name, password)

class Manager(Person):
    def __init__(self, person_id, name, password):
        super().__init__(person_id, name, password)

    def add_member(self, library, member):
        library.insert_member(member)

    def delete_member(self, library, member_id):
        library.delete_member(member_id)

    def add_book(self, library, book):
        library.insert_book(book)

    def delete_book(self, library, book_id):
        library.delete_book(book_id)
