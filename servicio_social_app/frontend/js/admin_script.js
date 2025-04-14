document.addEventListener('DOMContentLoaded', function() {
    const createEventForm = document.getElementById('create-event-form');
    const adminEventList = document.getElementById('admin-event-list');

    function loadAdminEvents() {
        fetch('/events')
            .then(response => response.json())
            .then(data => {
                adminEventList.innerHTML = '';
                data.events.forEach(event => {
                    const listItem = document.createElement('li');
                    listItem.innerHTML = `${event.nombre} (ID: <span class="math-inline">\{event\.id\}\) <button onclick\="editEvent\(</span>{event.id})">Editar</button> <button onclick="deleteEvent(${event.id})">Eliminar</button>`;
                    adminEventList.appendChild(listItem);
                });
            });
    }

    loadAdminEvents();

    createEventForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(createEventForm);
        const eventData = {};
        formData.forEach((value, key) => eventData[key] = value);

        fetch('/events', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(eventData)
        })
        .then(response => response.json())
        .then(data => {
            alert('Evento creado exitosamente!');
            createEventForm.reset();
            loadAdminEvents();
        });
    });

    window.deleteEvent = function(id) {
        fetch(`/events/${id}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.status === 204) {
                alert('Evento eliminado!');
                loadAdminEvents();
            } else {
                alert('Error al eliminar el evento.');
            }
        });
    };

    window.editEvent = function(id) {
        // Implementar lógica para cargar el formulario de edición con los datos del evento
        alert(`Función de edición para el evento con ID ${id} (a implementar)`);
    };
});