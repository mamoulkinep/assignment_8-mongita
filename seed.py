from mongita import MongitaClientDisk
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
client = MongitaClientDisk(os.path.join(BASE_DIR, "mongita_data"))

db = client.bookstore

categories_col = db.category
books_col = db.book

# Reset collections
categories_col.delete_many({})
books_col.delete_many({})

# -----------------------------
# CATEGORIES
# -----------------------------
categories_col.insert_many([
    {"categoryId": 1, "categoryName": "Fiction", "categoryImage": "fiction-category.jpg"},
    {"categoryId": 2, "categoryName": "Science Fiction", "categoryImage": "science-fiction-category.jpg"},
    {"categoryId": 3, "categoryName": "History", "categoryImage": "history-category.jpg"},
    {"categoryId": 4, "categoryName": "Business", "categoryImage": "business-category.jpg"}
])

# -----------------------------
# BOOKS
# -----------------------------
books_col.insert_many([
    {
        "bookId": 1,
        "categoryId": 1,
        "categoryName": "Fiction",
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "isbn": "9780446310789",
        "price": 11.07,
        "image": "to-kill-a-mockingbird.jpg",
        "readNow": 1
    },
    {
        "bookId": 2,
        "categoryId": 1,
        "categoryName": "Fiction",
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "isbn": "9780743273565",
        "price": 6.23,
        "image": "the-great-gatsby.jpg",
        "readNow": 0
    },
    {
        "bookId": 3,
        "categoryId": 1,
        "categoryName": "Fiction",
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "isbn": "9780141439518",
        "price": 5.29,
        "image": "pride-and-prejudice.jpg",
        "readNow": 1
    },
    {
        "bookId": 4,
        "categoryId": 2,
        "categoryName": "Science Fiction",
        "title": "Dune",
        "author": "Frank Herbert",
        "isbn": "9780441172719",
        "price": 7.50,
        "image": "dune.jpg",
        "readNow": 1
    },
    {
        "bookId": 5,
        "categoryId": 2,
        "categoryName": "Science Fiction",
        "title": "Ender's Game",
        "author": "Orson Scott Card",
        "isbn": "9780812550702",
        "price": 11.90,
        "image": "enders-game.jpg",
        "readNow": 0
    },
    {
        "bookId": 6,
        "categoryId": 2,
        "categoryName": "Science Fiction",
        "title": "Neuromancer",
        "author": "William Gibson",
        "isbn": "9780441012039",
        "price": 14.56,
        "image": "neuromancer.jpg",
        "readNow": 0
    },
    {
        "bookId": 7,
        "categoryId": 3,
        "categoryName": "History",
        "title": "Sapiens: A Brief History of Humankind",
        "author": "Yuval Noah Harari",
        "isbn": "9780062316097",
        "price": 21.96,
        "image": "sapiens.jpg",
        "readNow": 1
    },
    {
        "bookId": 8,
        "categoryId": 3,
        "categoryName": "History",
        "title": "Guns, Germs, and Steel",
        "author": "Jared Diamond",
        "isbn": "9780393354324",
        "price": 13.57,
        "image": "guns-germs-and-steel.jpg",
        "readNow": 0
    },
    {
        "bookId": 9,
        "categoryId": 3,
        "categoryName": "History",
        "title": "The Silk Roads",
        "author": "Peter Frankopan",
        "isbn": "9781101912379",
        "price": 12.49,
        "image": "the-silk-roads.jpg",
        "readNow": 0
    },
    {
        "bookId": 10,
        "categoryId": 4,
        "categoryName": "Business",
        "title": "The Lean Startup",
        "author": "Eric Ries",
        "isbn": "9780307887894",
        "price": 16.09,
        "image": "the-lean-startup.jpg",
        "readNow": 1
    },
    {
        "bookId": 11,
        "categoryId": 4,
        "categoryName": "Business",
        "title": "Good to Great",
        "author": "Jim Collins",
        "isbn": "9780066620992",
        "price": 19.99,
        "image": "good-to-great.jpg",
        "readNow": 0
    },
    {
        "bookId": 12,
        "categoryId": 4,
        "categoryName": "Business",
        "title": "Atomic Habits",
        "author": "James Clear",
        "isbn": "9780735211292",
        "price": 18.00,
        "image": "atomic-habits.jpg",
        "readNow": 1
    }
])


def clean_for_json(collection):
    clean_docs = []

    for doc in collection.find():
        doc = dict(doc)
        doc.pop("_id", None)
        clean_docs.append(doc)

    return clean_docs


with open("categories.json", "w", encoding="utf-8") as f:
    json.dump(clean_for_json(categories_col), f, indent=2, ensure_ascii=False)

with open("books.json", "w", encoding="utf-8") as f:
    json.dump(clean_for_json(books_col), f, indent=2, ensure_ascii=False)

print("Bookstore Mongita DB created.")
