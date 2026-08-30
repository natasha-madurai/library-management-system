from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


# MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="library_db"
    )


# Home page
@app.route("/")
def index():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM books ORDER BY id DESC")

    books = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("index.html", books=books)


# Add book
@app.route("/add", methods=["POST"])
def add_book():

    title = request.form["title"]
    author = request.form["author"]
    isbn = request.form["isbn"]
    category = request.form["category"]

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO books (title, author, isbn, category)
        VALUES (%s, %s, %s, %s)
        """,
        (title, author, isbn, category)
    )

    db.commit()

    cursor.close()
    db.close()

    return redirect("/")


# Edit page
@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        title = request.form["title"]
        author = request.form["author"]
        isbn = request.form["isbn"]
        category = request.form["category"]

        cursor.execute(
            """
            UPDATE books
            SET title=%s, author=%s, isbn=%s, category=%s
            WHERE id=%s
            """,
            (title, author, isbn, category, book_id)
        )

        db.commit()

        cursor.close()
        db.close()

        return redirect("/")

    cursor.execute(
        "SELECT * FROM books WHERE id=%s",
        (book_id,)
    )

    book = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template("edit.html", book=book)


# Delete book
@app.route("/delete/<int:book_id>")
def delete_book(book_id):

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM books WHERE id=%s",
        (book_id,)
    )

    db.commit()

    cursor.close()
    db.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)