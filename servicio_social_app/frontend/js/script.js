document.addEventListener('DOMContentLoaded', function() {
    fetch('/events')
        .then(response => response.json())
        .then(data => {
            const eventList = document.getElementById('event-list');
            data.events.forEach(event => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `
                    ${event.nombre} - ${event.fecha} ${event.hora} en <span class="math-inline">\{event\.lugar\} \(</span>{event.tipo})
                    <a href="event_details.html?id=${event.id}">Ver Detalles</a>
                `;
                eventList.appendChild(listItem);
            });
        });
});