# Envío de Correos Electrónicos Asíncrono con Flask y Celery

Este proyecto implementa el envío de correos electrónicos de forma asíncrona en una aplicación Flask utilizando Celery como gestor de tareas y Redis como broker de mensajes.

## Requisitos

* Python 3.x
* Pip (gestor de paquetes de Python)
* Redis instalado y en ejecución

## Instalación

1.  Clona este repositorio:
    ```bash
    git clone <URL_del_repositorio>
    cd tu_proyecto
    ```

2.  Crea un entorno virtual (opcional pero recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    venv\Scripts\activate  # En Windows
    ```

3.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4.  Configura las variables de entorno:
    Crea un archivo `.env` en la raíz del proyecto y añade la URL de Redis y la configuración del servidor SMTP (reemplaza con tus valores reales):

    ```
    REDIS_URL=redis://localhost:6379/0
    MAIL_SERVER=smtp.example.com
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=tu_correo@example.com
    MAIL_PASSWORD=tu_contraseña
    ```

    Estas variables son leídas en el archivo `app.py` para configurar Flask-Mail y Celery.

## Ejecución

1.  **Iniciar Redis:**
    Asegúrate de que el servidor de Redis esté en ejecución.

2.  **Iniciar el Worker de Celery:**
    Abre una terminal y ejecuta el worker de Celery desde la raíz del proyecto:
    ```bash
    celery -A app.celery worker -l info
    ```
    El worker ejecutará las tareas definidas en `tasks.py`, como la función `send_async_email`.

3.  **Iniciar la Aplicación Flask (Desarrollo):**
    Abre otra terminal y ejecuta la aplicación Flask:
    ```bash
    python app.py
    ```
    Las rutas de ejemplo en `app.py` (`/books` POST y `/books/<ID>` DELETE) utilizan `send_async_email.delay()` para encolar el envío de correos.

## Uso

Al acceder a las rutas `/books` (para agregar un libro) o `/books/<ID>` (para eliminar un libro), la aplicación Flask encolará una tarea para enviar un correo electrónico de confirmación utilizando Celery. El worker de Celery procesará esta tarea en segundo plano, enviando el correo configurado en `tasks.py`.

## Ejecución en Producción (Opcional)

Para ejecutar en un entorno de producción, puedes usar Gunicorn como servidor WSGI y Nginx como proxy inverso. Consulta la documentación de Gunicorn y Nginx para obtener instrucciones detalladas de configuración.

```bash
# Ejecutar con Gunicorn
gunicorn "app:app" -w 4 -b 0.0.0.0:8000