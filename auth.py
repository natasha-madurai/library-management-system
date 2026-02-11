import hashlib
from database import get_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    conn = get_connection()
    cur = conn.cursor()

    hashed = hash_password(password)

    cur.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, hashed)
    )
    user = cur.fetchone()
    conn.close()
    return user
