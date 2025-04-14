from flask import request
from flask_restful import Resource

# Simulación de una lista de libros (en memoria para este ejemplo sencillo)
BOOKS = [
    {'id': 1, 'title': 'El Señor de los Anillos', 'author': 'J.R.R. Tolkien'},
    {'id': 2, 'title': 'Cien años de soledad', 'author': 'Gabriel García Márquez'}
]

book_id_counter = len(BOOKS) + 1

class BookListResource(Resource):
    def get(self):
        return BOOKS, 200  # Devolvemos la lista de libros y un código de estado 200 (OK)

    def post(self):
        global book_id_counter
        data = request.get_json()
        if not data or 'title' not in data or 'author' not in data:
            return {'message': 'Debes proporcionar título y autor del libro'}, 400  # Bad Request
        new_book = {'id': book_id_counter, 'title': data['title'], 'author': data['author']}
        BOOKS.append(new_book)
        book_id_counter += 1
        return new_book, 201  # Created

class BookResource(Resource):
    def get(self, id):
        book = next((book for book in BOOKS if book['id'] == id), None)
        if book:
            return book, 200
        return {'message': 'Libro no encontrado'}, 404  # Not Found

    def put(self, id):
        data = request.get_json()
        book = next((book for book in BOOKS if book['id'] == id), None)
        if book:
            book.update(data)
            return book, 200
        return {'message': 'Libro no encontrado'}, 404

    def delete(self, id):
        global BOOKS
        BOOKS = [book for book in BOOKS if book['id'] != id]
        return {'message': 'Libro eliminado'}, 204  # No Content (eliminación exitosa)