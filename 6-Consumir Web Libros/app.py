from flask import Flask, render_template, jsonify, request, abort
import requests

app = Flask(__name__)

EXTERNAL_API_URL = "https://fakerestapi.azurewebsites.net/api/v1/Books"
local_books = []  # Lista local para CRUD

# Sincronizar la lista local con los libros obtenidos de la API externa
def sync_books():
    response = requests.get(EXTERNAL_API_URL)
    if response.status_code == 200:
        global local_books
        local_books = response.json()  # Guardamos los libros en la lista local
    else:
        print("Error fetching books from external API")

# Ruta principal para mostrar la vista HTML
@app.route('/')
def home():
    return render_template('index.html')

# Obtener todos los libros desde la lista local, ordenados por fecha de creación (descendente)
@app.route('/books', methods=['GET'])
def get_books():
    sorted_books = sorted(local_books, key=lambda x: x.get('publishDate', ''), reverse=True)
    return jsonify(sorted_books), 200

# Obtener un libro desde la lista local por ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in local_books if b['id'] == book_id), None)
    if book is None:
        abort(404, description="Book not found in local list")
    return jsonify(book), 200

# Agregar un libro a la lista local
@app.route('/books', methods=['POST'])
def add_book():
    if not request.is_json:
        abort(415, description="Content-Type must be application/json")
    data = request.get_json()
    new_book = {
        "id": local_books[-1]["id"] + 1 if local_books else 1,
        "title": data['title'],
        "description": data.get('description', ''),
        "pageCount": data.get('pageCount', 0),
        "excerpt": data.get('excerpt', ''),
        "publishDate": data.get('publishDate', '')
    }
    local_books.append(new_book)
    return jsonify(new_book), 201

# Actualizar un libro en la lista local
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    if not request.is_json:
        abort(415, description="Content-Type must be application/json")
    book = next((b for b in local_books if b['id'] == book_id), None)
    if book is None:
        abort(404, description="Book not found in local list")
    data = request.get_json()

    book['title'] = data.get('title', book['title'])
    book['description'] = data.get('description', book['description'])
    book['pageCount'] = data.get('pageCount', book['pageCount'])
    book['excerpt'] = data.get('excerpt', book['excerpt'])
    book['publishDate'] = data.get('publishDate', book['publishDate'])
    return jsonify(book), 200

# Eliminar un libro de la lista local
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = next((b for b in local_books if b['id'] == book_id), None)
    if book is None:
        abort(404, description="Book not found in local list")
    local_books.remove(book)
    return jsonify({"message": "Book deleted successfully"}), 200

if __name__ == '__main__':
    sync_books()  # Sincronizamos los libros al iniciar la aplicación
    app.run(debug=True)
