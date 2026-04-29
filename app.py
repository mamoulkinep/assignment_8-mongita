from flask import Flask, render_template, request, redirect, url_for
from mongita import MongitaClientDisk
import os

app = Flask(__name__)

# ------------------------------------------
# Mongita Setup (local embedded NoSQL DB)
# ------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
client = MongitaClientDisk(os.path.join(BASE_DIR, "mongita_data"))

db = client.bookstore

# These names match the seed.py you are currently using
categories_col = db.category
books_col = db.book


# ------------------------------------------
# Helper Functions
# ------------------------------------------
def get_categories():
    categories = list(categories_col.find())
    return sorted(categories, key=lambda c: c["categoryName"])


def get_next_book_id():
    books = list(books_col.find())

    if not books:
        return 1

    return max(book["bookId"] for book in books) + 1


def get_category_name(category_id):
    category = categories_col.find_one({"categoryId": category_id})
    if category:
        return category["categoryName"]
    return ""


# ------------------------------------------
# HOME PAGE
# ------------------------------------------
@app.route("/", methods=["GET"])
def home():
    categories = get_categories()
    return render_template("index.html", categories=categories)


# ------------------------------------------
# READ ALL BOOKS PAGE
# ------------------------------------------
@app.route("/read", methods=["GET"])
def read():
    categories = get_categories()
    books = list(books_col.find())
    books = sorted(books, key=lambda b: b["bookId"])
    return render_template("read.html", categories=categories, books=books)


# ------------------------------------------
# CREATE BOOK FORM
# ------------------------------------------
@app.route("/create", methods=["GET"])
def create():
    categories = get_categories()
    return render_template("create.html", categories=categories)


# ------------------------------------------
# CREATE BOOK POST
# ------------------------------------------
@app.route("/create_post", methods=["POST"])
def create_post():
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    isbn = request.form.get("isbn", "").strip()
    price = request.form.get("price", type=float)
    image = request.form.get("image", "").strip()
    category_id = request.form.get("categoryId", type=int)
    read_now = request.form.get("readNow", type=int)

    new_book = {
        "bookId": get_next_book_id(),
        "categoryId": category_id,
        "categoryName": get_category_name(category_id),
        "title": title,
        "author": author,
        "isbn": isbn,
        "price": price,
        "image": image,
        "readNow": read_now
    }

    books_col.insert_one(new_book)
    return redirect(url_for("read"))


# ------------------------------------------
# EDIT BOOK FORM
# ------------------------------------------
@app.route("/edit/<int:id>", methods=["GET"])
def edit(id):
    categories = get_categories()
    book = books_col.find_one({"bookId": id})

    if not book:
        return render_template("error.html", categories=categories, error="Book not found"), 404

    return render_template("edit.html", categories=categories, book=book)


# ------------------------------------------
# EDIT BOOK POST
# ------------------------------------------
@app.route("/edit_post/<int:id>", methods=["POST"])
def edit_post(id):
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    isbn = request.form.get("isbn", "").strip()
    price = request.form.get("price", type=float)
    image = request.form.get("image", "").strip()
    category_id = request.form.get("categoryId", type=int)
    read_now = request.form.get("readNow", type=int)

    updated_book = {
        "categoryId": category_id,
        "categoryName": get_category_name(category_id),
        "title": title,
        "author": author,
        "isbn": isbn,
        "price": price,
        "image": image,
        "readNow": read_now
    }

    books_col.update_one({"bookId": id}, {"$set": updated_book})
    return redirect(url_for("read"))


# ------------------------------------------
# DELETE BOOK
# ------------------------------------------
@app.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    books_col.delete_one({"bookId": id})
    return redirect(url_for("read"))


# ------------------------------------------
# CATEGORY PAGE
# /category?categoryId=1
# ------------------------------------------
@app.route("/category", methods=["GET"])
def category():
    category_id = request.args.get("categoryId", type=int)

    categories = get_categories()
    selected_category = categories_col.find_one({"categoryId": category_id})

    books = list(books_col.find({"categoryId": category_id}))
    books = sorted(books, key=lambda b: b["title"])

    return render_template(
        "category.html",
        categories=categories,
        selectedCategory=selected_category,
        books=books,
        searchTerm=None,
        nothingFound=False
    )


# ------------------------------------------
# SEARCH
# ------------------------------------------
@app.route("/search", methods=["POST"])
def search():
    term = request.form.get("search", "").strip()

    categories = get_categories()
    all_books = list(books_col.find())

    books = [
        book for book in all_books
        if term.lower() in book["title"].lower()
    ]
    books = sorted(books, key=lambda b: b["title"])

    return render_template(
        "category.html",
        categories=categories,
        selectedCategory=None,
        books=books,
        searchTerm=term,
        nothingFound=(len(books) == 0)
    )


# ------------------------------------------
# BOOK DETAIL PAGE
# /book?bookId=3
# ------------------------------------------
@app.route("/book", methods=["GET"])
def book_detail():
    book_id = request.args.get("bookId", type=int)

    categories = get_categories()
    book = books_col.find_one({"bookId": book_id})

    if not book:
        return render_template("error.html", categories=categories, error="Book not found"), 404

    return render_template(
        "book_detail.html",
        book=book,
        categories=categories
    )


# Old route kept only so the starter website does not break if a link still points here
@app.route("/add-book", methods=["GET"])
def add_book():
    return redirect(url_for("create"))


# ------------------------------------------
# ERRORS
# ------------------------------------------
@app.errorhandler(Exception)
def handle_error(e):
    categories = []
    try:
        categories = get_categories()
    except Exception:
        pass
    return render_template("error.html", categories=categories, error=e), 500


# ------------------------------------------
# RUN APP
# ------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
