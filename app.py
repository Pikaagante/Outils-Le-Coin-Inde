from flask import Flask
import os
import sys
import webbrowser

from routes.actus import actus_bp
from routes.images import images_bp
from routes.quiz import quiz_bp
from routes.indiecord import indiecord_bp


app = Flask(__name__)


# Dossiers
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.config["BASE_DIR"] = BASE_DIR
app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "uploads")
app.config["OUTPUT_FOLDER"] = os.path.join(BASE_DIR, "outputs")
app.config["JSON_FILE"] = os.path.join(
    BASE_DIR,
    "data",
    "jeux.json"
)
app.config["ODS_FILE"] = os.path.join(
    BASE_DIR,
    "data",
    "Indiecord.ods"
)


os.makedirs(
    app.config["UPLOAD_FOLDER"],
    exist_ok=True
)

os.makedirs(
    app.config["OUTPUT_FOLDER"],
    exist_ok=True
)

os.makedirs(
    os.path.dirname(app.config["JSON_FILE"]),
    exist_ok=True
)


# Routes
app.register_blueprint(actus_bp)
app.register_blueprint(images_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(indiecord_bp)


# Accueil
@app.route("/")
def index():

    from flask import render_template

    return render_template(
        "index.html"
    )


if __name__ == "__main__":

    webbrowser.open(
        "http://127.0.0.1:5000/"
    )

    app.run(
        host="127.0.0.1",
        port=5000
    )