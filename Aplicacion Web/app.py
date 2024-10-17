from flask import Flask,jsonify, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'EstudianteDB'

mysql = MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Estudiantes")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', estudiantes=data)

@app.route('/insert', methods=['POST'])
def insert():
    try:
        # Obtener los valores del formulario
        nombre = request.form['Nombre']
        apellido = request.form['Apellido']
        email = request.form['Correo']
        telefono = request.form['Celular']
        fecha_nacimiento = request.form['Fecha']
        direccion = request.form.get('Dirección', None)
        ciudad = request.form.get('Ciudad', None)
        codigo_postal = request.form.get('CódigoPostal', None)
        carrera = request.form.get('Carrera', None)
        semestre = int(request.form['Semestre'])
        promedio = float(request.form.get('Promedio', 0.0))

        # Validar que el promedio esté en el rango permitido (0 - 10)
        if not (0 <= promedio <= 10):
            raise ValueError("El promedio debe estar entre 0 y 10.")

        # Insertar en la base de datos
        cur = mysql.connection.cursor()
        cur.execute(
            """
            INSERT INTO estudiantes (
                nombre, apellido, email, telefono, fecha_nacimiento, 
                direccion, ciudad, codigo_postal, carrera, semestre, promedio
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, 
            (nombre, apellido, email, telefono, fecha_nacimiento, 
             direccion, ciudad, codigo_postal, carrera, semestre, promedio)
        )
        mysql.connection.commit()

        # Devolver mensaje de éxito
        return jsonify(message="Estudiante agregado con éxito"), 200

    except ValueError as ve:
        # Capturar errores de validación y devolver mensaje personalizado
        return jsonify(message=str(ve)), 400

    except Exception as e:
        # Manejar otros errores y hacer rollback
        mysql.connection.rollback()
        return jsonify(message="Error al insertar los datos. Intente nuevamente."), 500

    
@app.route('/delete/<string:id_data>', methods=['DELETE'])
def delete(id_data):
    try:
        # Eliminar el registro de la base de datos
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM estudiantes WHERE id=%s", (id_data,))
        mysql.connection.commit()

        # Respuesta exitosa en formato JSON
        return jsonify(message="Estudiante eliminado con éxito"), 200

    except Exception as e:
        # Manejar el error y devolver mensaje en formato JSON
        mysql.connection.rollback()
        return jsonify(message=f"Error al eliminar: {str(e)}"), 500



@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    try:
        # Obtener los datos del formulario
        nombre = request.form['name']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['phone']
        direccion = request.form['direccion']
        codigo_postal = request.form['codigo_postal']
        carrera = request.form['carrera']
        semestre = request.form['semestre']
        promedio = request.form['promedio']

        # Ejecutar la actualización en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE estudiantes 
            SET nombre=%s, apellido=%s, email=%s, telefono=%s, 
                direccion=%s, codigo_postal=%s, carrera=%s, semestre=%s, promedio=%s 
            WHERE id=%s
        """, (nombre, apellido, email, telefono, direccion, codigo_postal, carrera, semestre, promedio, id))
        mysql.connection.commit()

        return jsonify({'message': 'Estudiante actualizado con éxito.'}), 200

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500




if __name__ == "__main__":
    app.run(debug=True)