import streamlit as st
import json

# File to store books
BOOKS_FILE = "books_data.json"

# Load books from file
def load_books():
    try:
        with open(BOOKS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save books to file
def save_books(books):
    with open(BOOKS_FILE, "w") as file:
        json.dump(books, file, indent=4)

# Initialize books
books = load_books()

# Streamlit UI
st.title("📚 Personal Library Manager")

# Sidebar for navigation
menu = st.sidebar.radio("Navigation", ["Add Book", "View Books", "Search Books", "Update Book", "Remove Book", "Reading Progress"])

if menu == "Add Book":
    st.header("📖 Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    year = st.number_input("Publication Year", min_value=0, format="%d")
    read = st.checkbox("Have you read this book?")
    
    if st.button("Add Book"):
        if title and author and genre:
            books.append({"title": title, "author": author, "genre": genre, "year": year, "read": read})
            save_books(books)
            st.success("Book added successfully!")
        else:
            st.error("Please fill in all required fields.")

elif menu == "View Books":
    st.header("📚 Your Book Collection")
    if books:
        st.table(books)
    else:
        st.info("No books in the collection yet.")

elif menu == "Search Books":
    st.header("🔍 Search for a Book")
    query = st.text_input("Enter book title or author name")
    
    if st.button("Search"):
        results = [book for book in books if query.lower() in book["title"].lower() or query.lower() in book["author"].lower()]
        if results:
            st.table(results)
        else:
            st.warning("No matching books found.")

elif menu == "Update Book":
    st.header("✏️ Update Book Details")
    book_titles = [book["title"] for book in books]
    selected_book = st.selectbox("Select a book to update", book_titles)
    
    if selected_book:
        book = next(book for book in books if book["title"] == selected_book)
        
        new_title = st.text_input("New Title", book["title"])
        new_author = st.text_input("New Author", book["author"])
        new_genre = st.text_input("New Genre", book["genre"])
        new_year = st.number_input("New Year", min_value=0, value=int(book["year"]), format="%d")
        new_read = st.checkbox("Have you read this book?", book["read"])
        
        if st.button("Update Book"):
            book.update({"title": new_title, "author": new_author, "genre": new_genre, "year": new_year, "read": new_read})
            save_books(books)
            st.success("Book updated successfully!")

elif menu == "Remove Book":
    st.header("🗑️ Remove a Book")
    book_titles = [book["title"] for book in books]
    selected_book = st.selectbox("Select a book to remove", book_titles)
    
    if st.button("Remove Book"):
        books = [book for book in books if book["title"] != selected_book]
        save_books(books)
        st.success("Book removed successfully!")

elif menu == "Reading Progress":
    st.header("📊 Reading Progress")
    total_books = len(books)
    read_books = sum(1 for book in books if book["read"])
    progress = (read_books / total_books * 100) if total_books else 0
    
    st.write(f"Total Books: {total_books}")
    st.write(f"Books Read: {read_books}")
    st.progress(progress / 100)
    st.write(f"Reading Completion: {progress:.2f}%")