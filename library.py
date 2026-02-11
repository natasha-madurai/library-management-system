from datetime import datetime, timedelta
from database import get_connection

FINE_PER_DAY = 5

def issue_book(username, book_id):
    conn = get_connection()
    cur = conn.cursor()

    issue_date = datetime.now()
    due_date = issue_date + timedelta(days=7)

    cur.execute("""
    INSERT INTO issued_books (username, book_id, issue_date, due_date)
    VALUES (?, ?, ?, ?)
    """, (username, book_id, issue_date, due_date))

    cur.execute("UPDATE books SET available=0 WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

def calculate_fine(due_date, return_date):
    delay = (return_date - due_date).days
    return max(0, delay * FINE_PER_DAY)
def add_book(title, author):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO books (title, author, available) VALUES (?, ?, 1)",
        (title, author)
    )

    conn.commit()
    conn.close()
import pandas as pd

def get_issued_books():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM issued_books", conn)
    conn.close()
    return df
def return_book(issue_id):
    from datetime import datetime

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT due_date, book_id FROM issued_books WHERE id=?",
        (issue_id,)
    )
    record = cur.fetchone()

    if record:
        due_date = datetime.fromisoformat(record[0])
        return_date = datetime.now()
        fine = calculate_fine(due_date, return_date)

        cur.execute("""
        UPDATE issued_books
        SET return_date=?
        WHERE id=?
        """, (return_date, issue_id))

        cur.execute("UPDATE books SET available=1 WHERE id=?", (record[1],))

        conn.commit()
        conn.close()
        return fine

    conn.close()
    return None
