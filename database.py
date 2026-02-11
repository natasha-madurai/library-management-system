import sqlite3

def get_connection():
    return sqlite3.connect("library.db", check_same_thread=False)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        available INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS issued_books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        book_id INTEGER,
        issue_date TEXT,
        due_date TEXT,
        return_date TEXT
    )
    """)

    conn.commit()
    conn.close()
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def insert_default_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO users VALUES (?, ?, ?)",
        ("admin", hash_password("admin123"), "admin")
    )
    cur.execute(
        "INSERT OR IGNORE INTO users VALUES (?, ?, ?)",
        ("student", hash_password("student123"), "user")
    )

    conn.commit()
    conn.close()
