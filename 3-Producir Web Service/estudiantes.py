import connexion
from flask import jsonify, request, abort

# Datos simulados
ESTUDIANTES = {
    1: {
        "id": 1,
        "nombre": "Carlos",
        "apellido": "García",
        "email": "carlos@example.com",
        "telefono": "809-123-4567",
        "fecha_nacimiento": "2000-05-21",
        "carrera": "Ingeniería de Software",
        "semestre": 3,
        "promedio": 3.5
    }
}
NEXT_ID = max(ESTUDIANTES.keys()) + 1 if ESTUDIANTES else 1

def get_all():
    """Obtener todos los estudiantes."""
    return jsonify(list(ESTUDIANTES.values())), 200

def get_one(id):
    """Obtener un estudiante por ID."""
    estudiante = ESTUDIANTES.get(id)
    if estudiante:
        return jsonify(estudiante), 200
    else:
        abort(404, description=f"Estudiante con ID {id} no encontrado")

def add():
    """Agregar un nuevo estudiante."""
    global NEXT_ID
    data = request.get_json()
    
    # Validar campos obligatorios
    if not all(key in data for key in ["nombre", "apellido", "email"]):
        abort(400, description="Faltan datos necesarios para crear el estudiante")

    nuevo_estudiante = {
        "id": NEXT_ID,
        "nombre": data["nombre"],
        "apellido": data["apellido"],
        "email": data["email"],
        "telefono": data.get("telefono", ""),
        "fecha_nacimiento": data.get("fecha_nacimiento", ""),
        "carrera": data.get("carrera", ""),
        "semestre": data.get("semestre", 1),
        "promedio": data.get("promedio", 0.0)
    }

    ESTUDIANTES[NEXT_ID] = nuevo_estudiante
    NEXT_ID += 1

    return jsonify(nuevo_estudiante), 201

def delete(id):
    """Eliminar un estudiante por ID."""
    if id in ESTUDIANTES:
        del ESTUDIANTES[id]
        return jsonify({"mensaje": f"Estudiante con ID {id} eliminado"}), 200
    else:
        abort(404, description=f"Estudiante con ID {id} no encontrado")

def update(id):
    """Actualizar los datos de un estudiante por ID."""
    if id not in ESTUDIANTES:
        abort(404, description=f"Estudiante con ID {id} no encontrado")

    data = request.get_json()

    # Validar que los campos necesarios están presentes
    if not all(key in data for key in ["nombre", "apellido", "email"]):
        abort(400, description="Faltan datos necesarios para actualizar el estudiante")

    # Actualizar los datos del estudiante
    estudiante = ESTUDIANTES[id]
    estudiante["nombre"] = data.get("nombre", estudiante["nombre"])
    estudiante["apellido"] = data.get("apellido", estudiante["apellido"])
    estudiante["email"] = data.get("email", estudiante["email"])
    estudiante["telefono"] = data.get("telefono", estudiante["telefono"])
    estudiante["fecha_nacimiento"] = data.get("fecha_nacimiento", estudiante["fecha_nacimiento"])
    estudiante["carrera"] = data.get("carrera", estudiante["carrera"])
    estudiante["semestre"] = data.get("semestre", estudiante["semestre"])
    estudiante["promedio"] = data.get("promedio", estudiante["promedio"])

    return jsonify(estudiante), 200



# Crear la aplicación Flask + Connexion
app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")

if __name__ == "__main__":
    app.run(port=8000, debug=True)


