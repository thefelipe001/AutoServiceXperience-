const API_URL = 'http://localhost:8000/api/estudiantes';

cargarEstudiantes();
document.getElementById('formEstudiante').addEventListener('submit', guardarEstudiante);

function cargarEstudiantes() {
  fetch(API_URL)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(estudiantes => {
      const tabla = document.getElementById('estudiantesTable');
      tabla.innerHTML = '';
      estudiantes.forEach(estudiante => {
        tabla.innerHTML += `
          <tr>
            <td>${estudiante.id}</td>
            <td>${estudiante.nombre}</td>
            <td>${estudiante.apellido}</td>
            <td>${estudiante.email}</td>
            <td>
              <button class="btn btn-warning" onclick="editarEstudiante(${estudiante.id})">Editar</button>
              <button class="btn btn-danger" onclick="eliminarEstudiante(${estudiante.id})">Eliminar</button>
            </td>
          </tr>`;
      });
    })
    .catch(error => console.error('Error:', error));
}

function guardarEstudiante(e) {
  e.preventDefault();
  const id = document.getElementById('idEstudiante').value;
  const nombre = document.getElementById('nombre').value;
  const apellido = document.getElementById('apellido').value;
  const email = document.getElementById('email').value;

  const metodo = id ? 'PUT' : 'POST';
  const url = id ? `${API_URL}/${id}` : API_URL;

  fetch(url, {
    method: metodo,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre, apellido, email })
  }).then(() => {
    cargarEstudiantes();
    document.getElementById('formEstudiante').reset();
  }).catch(error => console.error('Error:', error));
}

function editarEstudiante(id) {
  fetch(`${API_URL}/${id}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(estudiante => {
      document.getElementById('idEstudiante').value = estudiante.id;
      document.getElementById('nombre').value = estudiante.nombre;
      document.getElementById('apellido').value = estudiante.apellido;
      document.getElementById('email').value = estudiante.email;
    }).catch(error => console.error('Error:', error));
}

function eliminarEstudiante(id) {
  fetch(`${API_URL}/${id}`, { method: 'DELETE' })
    .then(() => cargarEstudiantes())
    .catch(error => console.error('Error:', error));
}
