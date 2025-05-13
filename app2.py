import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from library_database import Library
from library_classes import Member, Manager

# Initialize the library system
library = Library()
manager = Manager(0, 'Manager', 'manager_password')

# Initialize the Tkinter root window
root = tk.Tk()
root.title("Library Management System")
root.geometry("600x600")

# Load the background image and store the reference
background_image = Image.open("background.jpg")
background_image = background_image.resize((600, 600), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

# Create a canvas for the main menu (initially hidden)
canvas = tk.Canvas(root, width=600, height=600)

# --- LOGIN SYSTEM ---
current_user = None

def login():
    global current_user
    username = entry_username.get()
    password = entry_password.get()
    
    if username == "Manager" and password == "manager_password":
        current_user = manager
        login_frame.destroy()  # Remove the login frame
        show_main_menu()
    else:
        c = library.conn.cursor()
        c.execute("SELECT member_id FROM members WHERE name = ? AND password = ?", (username, password))
        member = c.fetchone()
        if member:
            current_user = Member(member[0], username, password)
            login_frame.destroy()  # Remove the login frame
            show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password")

def show_login_window():
    global entry_username, entry_password, login_frame
    login_frame = tk.Frame(root)
    login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    tk.Label(login_frame, text="Username").pack()
    entry_username = tk.Entry(login_frame)
    entry_username.pack()
    
    tk.Label(login_frame, text="Password").pack()
    entry_password = tk.Entry(login_frame, show="*")
    entry_password.pack()
    
    tk.Button(login_frame, text="Login", command=login, bg="#000080", fg="white").pack()

def show_main_menu():
    canvas.pack(fill="both", expand=True)
    canvas.background = background_photo  # Store reference
    canvas.create_image(0, 0, image=background_photo, anchor="nw")

    label_main_menu = tk.Label(canvas, text=f"Welcome, {current_user.name}", font=("Helvetica", 16, "bold"))
    canvas.create_window(300, 50, window=label_main_menu)
    
    buttons = [("Search Books", search_books_window), ("Show All Books", show_all_books), ("Borrow Book", borrow_book_window), ("Return Book", return_book_window)]
    
    if isinstance(current_user, Manager):
        buttons.extend([("Insert Member", insert_member_window), ("Delete Member", delete_member_window), ("Show All Members", show_all_members)])
    
    for idx, (text, command) in enumerate(buttons):
        button = tk.Button(canvas, text=text, command=command, width=20, height=2, bg="#000080", fg="white")
        canvas.create_window(300, 100 + (idx * 60), window=button)

# Placeholder functions for other features
def search_books_window():
    def search_books():
        title = entry_book_title.get()
        books = library.search_books(title)
        if books:
            result = "\n".join([f'Book ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Borrowed By: {book[3] if book[3] else "Not borrowed"}' for book in books])
        else:
            result = "No books found."
        messagebox.showinfo("Search Results", result)
        window.destroy()

    window = tk.Toplevel(root)
    window.title("Search Books")
    window.geometry("300x150")
    
    label_book_title = tk.Label(window, text="Book Title")
    label_book_title.pack()
    entry_book_title = tk.Entry(window)
    entry_book_title.pack()
    
    button_search_books = tk.Button(window, text="Search Books", command=search_books, bg="#000080", fg="white")
    button_search_books.pack()

def show_all_books():
    books = library.get_all_books()
    if books:
        result = "\n".join([f'Book ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Borrowed By: {book[3] if book[3] else "Not borrowed"}' for book in books])
    else:
        result = "No books found."
    messagebox.showinfo("All Books", result)

def borrow_book_window():
    def borrow_book():
        book_id = int(entry_book_id.get())
        member_name = entry_member_name.get()

        # Retrieve member ID based on name
        c = library.conn.cursor()
        c.execute('SELECT member_id FROM members WHERE name = ?', (member_name,))
        member = c.fetchone()
        if member:
            member_id = member[0]

            # Check if the book exists
            c.execute('SELECT book_id FROM books WHERE book_id = ?', (book_id,))
            book = c.fetchone()
            if not book:
                messagebox.showinfo("Error", f'Book with ID {book_id} does not exist.')
                return

            # Check if the book is already borrowed
            c.execute('SELECT borrowed_by FROM books WHERE book_id = ?', (book_id,))
            borrowed_by = c.fetchone()[0]

            if borrowed_by:
                c.execute('SELECT name FROM members WHERE member_id = ?', (borrowed_by,))
                borrower_name = c.fetchone()[0]
                messagebox.showinfo("Unavailable", f'The book is already borrowed by {borrower_name}. It is currently unavailable.')
            else:
                library.borrow_book(book_id, member_id)
                messagebox.showinfo("Success", f"Book with ID {book_id} borrowed by member {member_name}.")
        else:
            messagebox.showinfo("Error", f'Member with name {member_name} does not exist.')
        window.destroy()

    window = tk.Toplevel(root)
    window.title("Borrow Book")
    window.geometry("300x200")
    
    label_book_id = tk.Label(window, text="Book ID")
    label_book_id.pack()
    entry_book_id = tk.Entry(window)
    entry_book_id.pack()
    
    label_member_name = tk.Label(window, text="Member Name")
    label_member_name.pack()
    entry_member_name = tk.Entry(window)
    entry_member_name.pack()
    
    button_borrow_book = tk.Button(window, text="Borrow Book", command=borrow_book, bg="#000080", fg="white")
    button_borrow_book.pack()

def return_book_window():
    def return_book():
        book_id = int(entry_book_id.get())

        # Check if the book exists
        c = library.conn.cursor()
        c.execute('SELECT book_id FROM books WHERE book_id = ?', (book_id,))
        book = c.fetchone()
        if not book:
            messagebox.showinfo("Error", f'Book with ID {book_id} does not exist.')
            return
        
        library.return_book(book_id)
        messagebox.showinfo("Success", f"Book with ID {book_id} has been returned.")
        window.destroy()

    window = tk.Toplevel(root)
    window.title("Return Book")
    window.geometry("300x150")
    
    label_book_id = tk.Label(window, text="Book ID")
    label_book_id.pack()
    entry_book_id = tk.Entry(window)
    entry_book_id.pack()
    
    button_return_book = tk.Button(window, text="Return Book", command=return_book, bg="#000080", fg="white")
    button_return_book.pack()

def insert_member_window():
    def insert_member():
        name = entry_member_name.get()
        password = entry_member_password.get()
        member = Member(None, name, password)
        manager.add_member(library, member)
        messagebox.showinfo("Success", f"Member {name} added.")
        window.destroy()

    window = tk.Toplevel(root)
    window.title("Insert Member")
    window.geometry("300x200")
    
    label_member_name = tk.Label(window, text="Member Name")
    label_member_name.pack()
    entry_member_name = tk.Entry(window)
    entry_member_name.pack()
    
    label_member_password = tk.Label(window, text="Member Password")
    label_member_password.pack()
    entry_member_password = tk.Entry(window, show="*")
    entry_member_password.pack()
    
    button_insert_member = tk.Button(window, text="Insert Member", command=insert_member, bg="#000080", fg="white")
    button_insert_member.pack()

def delete_member_window():
    def delete_member():
        member_id = int(entry_member_id.get())
        manager.delete_member(library, member_id)
        messagebox.showinfo("Success", f"Member with ID {member_id} deleted.")
        window.destroy()

    window = tk.Toplevel(root)
    window.title("Delete Member")
    window.geometry("300x150")
    
    label_member_id = tk.Label(window, text="Member ID")
    label_member_id.pack()
    entry_member_id = tk.Entry(window)
    entry_member_id.pack()
    
    button_delete_member = tk.Button(window, text="Delete Member", command=delete_member, bg="#000080", fg="white")
    button_delete_member.pack()


def show_all_members():
    members = library.get_all_members()
    if members:
        result = "\n".join([f'Member ID: {member[0]}, Name: {member[1]}' for member in members])
    else:
        result = "No members found."
    messagebox.showinfo("All Members", result)

# Show login window on startup
show_login_window()
root.mainloop()
