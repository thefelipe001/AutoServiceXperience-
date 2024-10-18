from flask import Flask, jsonify, request, render_template, abort
from flask_cors import CORS

app = Flask(__name__)

# Habilitar CORS para todas las rutas
CORS(app)

# Datos simulados
estudiantes = [
    {"id": 1, "nombre": "Carlos", "apellido": "García", "email": "carlos@example.com", 
     "telefono": "809-123-4567", "fecha_nacimiento": "2000-05-21", 
     "carrera": "Ingeniería de Software", "semestre": 3, "promedio": 3.5}
]
next_id = 2

@app.route('/api/estudiantes', methods=['GET'])
def obtener_estudiantes():
    return jsonify(estudiantes)

@app.route('/api/estudiantes/<int:id>', methods=['GET'])
def obtener_estudiante(id):
    estudiante = next((e for e in estudiantes if e['id'] == id), None)
    if estudiante:
        return jsonify(estudiante)
    return abort(404, description=f"Estudiante con ID {id} no encontrado")

@app.route('/api/estudiantes', methods=['POST'])
def agregar_estudiante():
    global next_id
    data = request.json
    nuevo_estudiante = {
        "id": next_id,
        "nombre": data["nombre"],
        "apellido": data["apellido"],
        "email": data["email"]
    }
    estudiantes.append(nuevo_estudiante)
    next_id += 1
    return jsonify(nuevo_estudiante), 201

@app.route('/api/estudiantes/<int:id>', methods=['PUT'])
def actualizar_estudiante(id):
    estudiante = next((e for e in estudiantes if e['id'] == id), None)
    if not estudiante:
        return abort(404, description=f"Estudiante con ID {id} no encontrado")
    
    data = request.json
    estudiante.update(data)
    return jsonify(estudiante)

@app.route('/api/estudiantes/<int:id>', methods=['DELETE'])
def eliminar_estudiante(id):
    global estudiantes
    estudiantes = [e for e in estudiantes if e['id'] != id]
    return jsonify({"mensaje": f"Estudiante con ID {id} eliminado"}), 200

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
