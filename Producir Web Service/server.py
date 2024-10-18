from flask import render_template
from flask_cors import CORS  # Importar CORS
import connexion

app = connexion.App(__name__, specification_dir="./")

# Habilitar CORS para todas las rutas
CORS(app.app)  

app.add_api("swagger.yml")

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(port=8000)
