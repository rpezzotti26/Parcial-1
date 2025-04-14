document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const eventId = parseInt(urlParams.get('id'));
    const detailsDiv = document.getElementById('event-details');
    const registerBtn = document.getElementById('register-btn');

    fetch(`/events/${eventId}`)
        .then(response => response.json())
        .then(data => {
            const event = data;
            detailsDiv.innerHTML = `
                <h2><span class="math-inline">\{event\.nombre\}</h2\>
 <p>{event.descripcion}</p>
<p>Fecha: ${event.fecha}</p>
<p>Hora: ${event.hora}</p>
<p>Lugar: ${event.lugar}</p>
<p>Tipo: ${event.tipo}</p>
\`;
});

registerBtn.addEventListener('click', function() {
        fetch(`/events/${eventId}/register`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        });
    });
});