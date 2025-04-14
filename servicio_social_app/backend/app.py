from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# --- Simulación de Base de Datos en Memoria ---
EVENTS = [
    {'id': 1, 'nombre': 'Limpieza de Parque', 'descripcion': 'Ayuda a limpiar el parque local', 'fecha': '2025-05-15', 'hora': '09:00', 'lugar': 'Parque Central', 'tipo': 'Voluntariado'},
    {'id': 2, 'nombre': 'Tutoría de Matemáticas', 'descripcion': 'Ayuda a estudiantes con matemáticas', 'fecha': '2025-05-20', 'hora': '14:00', 'lugar': 'Biblioteca Universitaria', 'tipo': 'Apoyo Académico'}
]
event_id_counter = len(EVENTS) + 1

REGISTRATIONS = [] # [{'estudiante_id': '...', 'evento_id': 1}]

# --- Recursos de la API ---

class EventList(Resource):
    def get(self):
        return jsonify({'events': EVENTS})

    def post(self):
        global event_id_counter
        data = request.get_json()
        new_event = {
            'id': event_id_counter,
            'nombre': data.get('nombre'),
            'descripcion': data.get('descripcion'),
            'fecha': data.get('fecha'),
            'hora': data.get('hora'),
            'lugar': data.get('lugar'),
            'tipo': data.get('tipo')
        }
        EVENTS.append(new_event)
        event_id_counter += 1
        return jsonify(new_event), 201

class Event(Resource):
    def get(self, id):
        event = next((e for e in EVENTS if e['id'] == id), None)
        if event:
            return jsonify(event)
        return {'message': 'Evento no encontrado'}, 404

    def put(self, id):
        data = request.get_json()
        event = next((e for e in EVENTS if e['id'] == id), None)
        if event:
            event.update(data)
            return jsonify(event)
        return {'message': 'Evento no encontrado'}, 404

    def delete(self, id):
        global EVENTS
        EVENTS = [e for e in EVENTS if e['id'] != id]
        return {'message': 'Evento eliminado'}, 204

class EventRegistration(Resource):
    def post(self, id):
        student_id = 'usuario_simulado' # Simulación de estudiante
        if any(reg['estudiante_id'] == student_id and reg['evento_id'] == id for reg in REGISTRATIONS):
            return {'message': 'Ya estás registrado en este evento'}, 409
        REGISTRATIONS.append({'estudiante_id': student_id, 'evento_id': id})
        return {'message': 'Registrado exitosamente'}, 201

api.add_resource(EventList, '/events')
api.add_resource(Event, '/events/<int:id>')
api.add_resource(EventRegistration, '/events/<int:id>/register')

if __name__ == '__main__':
    app.run(debug=True)