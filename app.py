import streamlit as st
import sqlite3
from datetime import date

# ---------------- DATABASE SETUP ----------------
conn = sqlite3.connect("library.db", check_same_thread=False)
c = conn.cursor()

# Users table
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    password TEXT,
    role TEXT
)
""")

# Books table
c.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    available INTEGER
)
""")

# Issued books table
c.execute("""
CREATE TABLE IF NOT EXISTS issued (
    username TEXT,
    book_id INTEGER,
    issue_date TEXT
)
""")

# Reset users (IMPORTANT)
c.execute("DELETE FROM users")
c.execute("INSERT INTO users VALUES ('admin','admin123','admin')")
c.execute("INSERT INTO users VALUES ('student','student123','user')")
conn.commit()

# ---------------- LOGIN ----------------
st.title("📚 Library Management System")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        c.execute(
            "SELECT role FROM users WHERE username=? AND password=?",
            (username, password)
        )
        result = c.fetchone()

        if result:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = result[0]
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid username or password ❌")

# ---------------- DASHBOARD ----------------
else:
    st.success(f"Welcome {st.session_state.username} ({st.session_state.role})")

    # -------- ADMIN --------
    if st.session_state.role == "admin":
        st.subheader("👨‍💼 Admin Dashboard")

        st.markdown("### ➕ Add Book")
        title = st.text_input("Book Title")
        author = st.text_input("Author Name")

        if st.button("Add Book"):
            c.execute(
                "INSERT INTO books (title, author, available) VALUES (?,?,1)",
                (title, author)
            )
            conn.commit()
            st.success("Book added successfully ✅")

        st.markdown("### 📖 All Books")
        books = c.execute("SELECT * FROM books").fetchall()
        st.table(books)

    # -------- USER --------
    else:
        st.subheader("👩‍🎓 User Dashboard")

        st.markdown("### 📚 Available Books")
        books = c.execute(
            "SELECT id, title, author FROM books WHERE available=1"
        ).fetchall()

        for b in books:
            if st.button(f"Issue {b[1]} by {b[2]}"):
                c.execute(
                    "INSERT INTO issued VALUES (?,?,?)",
                    (st.session_state.username, b[0], str(date.today()))
                )
                c.execute(
                    "UPDATE books SET available=0 WHERE id=?",
                    (b[0],)
                )
                conn.commit()
                st.success("Book issued ✅")
                st.rerun()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
