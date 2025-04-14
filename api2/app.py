from flask import Flask
from flask_restful import Api
from resources import BookResource, BookListResource

app = Flask(__name__)
api = Api(app)

# Definimos las rutas de nuestra API y los recursos que las manejarán
api.add_resource(BookListResource, '/books')      # Para obtener la lista y agregar libros
api.add_resource(BookResource, '/books/<int:id>') # Para obtener, actualizar y eliminar un libro específico

if __name__ == '__main__':
    app.run(debug=True)

    from flask import Flask, render_template, request, redirect, url_for
    import requests
    import os
    from dotenv import load_dotenv

    load_dotenv()

    app = Flask(__name__)
    API_BASE_URL = os.environ.get('API_BASE_URL', 'http://127.0.0.1:5000')  # URL base de tu API


    def get_all_books():
        try:
            response = requests.get(f"{API_BASE_URL}/books")
            response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")
            return []


    def get_book(book_id):
        try:
            response = requests.get(f"{API_BASE_URL}/books/{book_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")
            return None


    def add_book(title, author):
        try:
            response = requests.post(f"{API_BASE_URL}/books", json={'title': title, 'author': author})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")
            return None


    def update_book(book_id, title=None, author=None):
        data = {}
        if title:
            data['title'] = title
        if author:
            data['author'] = author
        try:
            response = requests.put(f"{API_BASE_URL}/books/{book_id}", json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")
            return None


    def delete_book(book_id):
        try:
            response = requests.delete(f"{API_BASE_URL}/books/{book_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")
            return False


    # Ejemplo de rutas Flask (tendrás que adaptarlas a tu aplicación)
    @app.route('/')
    def index():
        books = get_all_books()
        return render_template('index.html', books=books)


    @app.route('/add', methods=['GET', 'POST'])
    def add():
        if request.method == 'POST':
            title = request.form['title']
            author = request.form['author']
            add_book(title, author)
            return redirect(url_for('index'))
        return render_template('add.html')


    @app.route('/edit/<int:id>', methods=['GET', 'POST'])
    def edit(id):
        book = get_book(id)
        if request.method == 'POST':
            title = request.form['title']
            author = request.form['author']
            update_book(id, title, author)
            return redirect(url_for('index'))
        return render_template('edit.html', book=book)


    @app.route('/delete/<int:id>')
    def delete(id):
        delete_book(id)
        return redirect(url_for('index'))


    if __name__ == '__main__':
        app.run(debug=True)