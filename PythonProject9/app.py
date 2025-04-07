# app.py
import os
from flask import Flask, render_template, request, redirect, url_for
from redis import Redis
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'your_secret_key')

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_DB = int(os.environ.get('REDIS_DB', 0))

db = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
BOOK_KEY_PREFIX = 'book:'

def get_next_book_id():
    return db.incr('next_book_id')

def save_book(book_id, title, author, genre):
    key = f"{BOOK_KEY_PREFIX}{book_id}"
    db.hmset(key, {'title': title, 'author': author, 'genre': genre})

def get_all_books():
    keys = db.keys(f"{BOOK_KEY_PREFIX}*")
    books = []
    for key in keys:
        book_data = db.hgetall(key)
        if book_data:
            book_id = key.decode('utf-8').split(':')[1]
            books.append({
                'id': book_id,
                'title': book_data.get(b'title').decode('utf-8'),
                'author': book_data.get(b'author').decode('utf-8'),
                'genre': book_data.get(b'genre').decode('utf-8')
            })
    return books

@app.route('/')
def index():
    books = get_all_books()
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        book_id = get_next_book_id()
        save_book(book_id, title, author, genre)
        return redirect(url_for('index'))
    return render_template('add_book.html')

if __name__ == '__main__':
    app.run(debug=True)