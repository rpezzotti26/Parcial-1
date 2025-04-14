from flask import Flask, request, jsonify
from flask_mail import Mail
from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT') or 587)
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', True)
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['CELERY_BROKER_URL'] = os.environ.get('REDIS_URL')
app.config['CELERY_RESULT_BACKEND'] = os.environ.get('REDIS_URL')

mail = Mail(app)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask

from tasks import send_async_email  # Importamos la tarea desde tasks.py

# Ejemplo de una ruta para agregar un libro (simulado)
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data.get('title', 'Libro Desconocido')
    send_async_email.delay(
        subject=f"Nuevo libro agregado: {title}",
        recipients=['usuario@example.com'],  # Reemplaza con el destinatario real
        body=f"El libro '{title}' ha sido agregado exitosamente."
    )
    return jsonify({'message': f'Libro "{title}" agregado y correo de confirmación en proceso de envío.'}), 201

# Ejemplo de una ruta para eliminar un libro (simulado)
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    # Simulación de obtener el título del libro (reemplaza con tu lógica real)
    title = f"Libro con ID {book_id}"
    send_async_email.delay(
        subject=f"Libro eliminado: {title}",
        recipients=['usuario@example.com'],  # Reemplaza con el destinatario real
        body=f"El libro '{title}' ha sido eliminado."
    )
    return jsonify({'message': f'Libro con ID {book_id} eliminado y correo de confirmación en proceso de envío.'}), 200

if __name__ == '__main__':
    app.run(debug=True)