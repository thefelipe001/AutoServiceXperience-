const express = require('express');
const fetch = require('node-fetch');
const cors = require('cors');
const app = express();
const PORT = 3000;

app.set('view engine', 'ejs');
app.set('views', __dirname + '/views');
app.use(express.static('public'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors()); // Habilitar CORS

const API_URL = 'http://localhost:8000/api/estudiantes';

// Ruta principal: Listar estudiantes
app.get('/', async (req, res) => {
  try {
    const response = await fetch(API_URL);
    const estudiantes = await response.json();
    res.render('index', { estudiantes });
  } catch (error) {
    console.error('Error al consumir la API:', error.message);
    res.send('Error al cargar los estudiantes.');
  }
});

// Ruta para mostrar el formulario de agregar estudiante
app.get('/agregar', (req, res) => {
  res.render('agregar');
});



app.post('/agregar', async (req, res) => {
  const nuevoEstudiante = req.body;
  console.log('Datos del nuevo estudiante:', nuevoEstudiante); // Verificar datos recibidos

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(nuevoEstudiante),
    });

    const result = await response.json(); // Captura la respuesta de la API
    console.log('Respuesta de la API:', result); // Verificar respuesta de la API

    res.status(201).json({ message: 'Estudiante agregado correctamente.' });
  } catch (error) {
    console.error('Error al agregar estudiante:', error.message);
    res.status(500).json({ message: 'Error al agregar el estudiante.' });
  }
});






// Ruta para eliminar estudiante
app.post('/eliminar/:id', async (req, res) => {
  const { id } = req.params;
  try {
    await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    res.redirect('/?eliminado=true');

  } catch (error) {
    console.error('Error al eliminar estudiante:', error.message);
    res.send('Error al eliminar el estudiante.');
  }
});

app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
});


app.get('/editar/:id', async (req, res) => {
  const { id } = req.params;

  try {
    const response = await fetch(`${API_URL}/${id}`);
    const estudiante = await response.json();

    res.render('editar', { estudiante });
  } catch (error) {
    console.error('Error al cargar estudiante:', error.message);
    res.send('Error al cargar el estudiante.');
  }
});


app.put('/editar/:id', async (req, res) => {
  const { id } = req.params; // Captura el ID del parámetro de ruta
  const estudianteActualizado = req.body; // Captura los datos enviados

  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(estudianteActualizado),
    });

    const result = await response.json(); // Captura la respuesta de la API
    console.log('Respuesta de la API:', result); // Verificar respuesta de la API

    res.status(200).json({ message: 'Estudiante editado correctamente.' });
  } catch (error) {
    console.error('Error al editar estudiante:', error.message);
    res.status(500).json({ message: 'Error al editar el estudiante.' });
  }
});
