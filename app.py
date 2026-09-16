from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import uuid
import webbrowser
import sys
import json
import pandas as pd

from outils.actus.generator import (
    get_games,
    generate_discord_markdown,
    generate_reddit_markdown
)

from outils.images.colors import apply_colors
from outils.images.distortion import apply_distortion
from outils.images.mosaic import apply_mosaic
from outils.images.hex_pixelate import apply_hex_pixelate


app = Flask(__name__)


# Dossiers
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")
JSON_FILE = os.path.join(BASE_DIR, "data", "jeux.json")
ODS_FILE = os.path.join(BASE_DIR, "data", "Indiecord.ods")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(JSON_FILE), exist_ok=True)


# Lit le fichier JSON
def load_quiz_data():

    with open(
        JSON_FILE,
        "r",
        encoding="utf-8"
    ) as fichier:

        return json.load(fichier)


# Sauvegarde le fichier JSON
def save_quiz_data(data):

    with open(
        JSON_FILE,
        "w",
        encoding="utf-8"
    ) as fichier:

        json.dump(
            data,
            fichier,
            ensure_ascii=False,
            indent=4
        )


# Lit le fichier Indiecord
def load_indiecord():

    fichier = pd.ExcelFile(
        ODS_FILE,
        engine="odf"
    )

    feuilles = {}

    for feuille in fichier.sheet_names:

        data = fichier.parse(
            feuille
        )

        data = data.fillna("")

        feuilles[feuille] = data.to_dict(
            orient="records"
        )

    return feuilles


# Sauvegarde le fichier Indiecord
def save_indiecord(data):

    with pd.ExcelWriter(
        ODS_FILE,
        engine="odf"
    ) as writer:

        for feuille, lignes in data.items():

            dataframe = pd.DataFrame(
                lignes,
                columns=[
                    "EN",
                    "FR",
                    "Rareté"
                ]
            )

            dataframe.to_excel(
                writer,
                sheet_name=feuille,
                index=False
            )


# Page d'accueil
@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# Page Actus
@app.route(
    "/actus",
    methods=["GET", "POST"]
)
def actus():

    result = ""
    app_ids_text = ""

    if request.method == "POST":

        app_ids_text = request.form.get(
            "app_ids",
            ""
        )

        app_ids = []

        for line in app_ids_text.splitlines():

            line = line.strip()

            if line.isdigit():
                app_ids.append(int(line))

        games = get_games(app_ids)

        format_type = request.form.get(
            "format",
            "discord"
        )

        if format_type == "reddit":
            result = generate_reddit_markdown(games)

        else:
            result = generate_discord_markdown(games)

    return render_template(
        "actus.html",
        result=result,
        app_ids=app_ids_text
    )


# Page Images
@app.route("/images")
def images():

    return render_template(
        "images.html"
    )


# Page Quiz
@app.route("/quiz")
def quiz():

    jeux = load_quiz_data()

    return render_template(
        "quiz.html",
        jeux=jeux
    )


# API : récupérer les jeux
@app.route("/api/quiz")
def quiz_data():

    return jsonify(
        load_quiz_data()
    )


# API : ajouter un jeu
@app.route(
    "/api/quiz/add",
    methods=["POST"]
)
def add_quiz_game():

    data = request.get_json()

    nom = data.get("nom", "").strip()
    categorie = data.get("categorie", "").strip()
    context = data.get("context", "").strip()

    if not nom:
        return jsonify({
            "success": False,
            "error": "Le nom du jeu est obligatoire."
        }), 400

    if not categorie:
        return jsonify({
            "success": False,
            "error": "La catégorie est obligatoire."
        }), 400

    jeux = load_quiz_data()

    if categorie not in jeux:
        return jsonify({
            "success": False,
            "error": "Cette catégorie n'existe pas."
        }), 400

    existe = any(
        jeu.get("nom", "").lower() == nom.lower()
        for jeu in jeux[categorie]
    )

    if existe:
        return jsonify({
            "success": False,
            "error": "Ce jeu existe déjà dans cette catégorie."
        }), 400

    nouveau_jeu = {
        "nom": nom
    }

    if context:
        nouveau_jeu["context"] = context

    jeux[categorie].append(nouveau_jeu)

    save_quiz_data(jeux)

    return jsonify({
        "success": True,
        "jeu": nouveau_jeu
    })


# API : créer une catégorie
@app.route(
    "/api/quiz/category",
    methods=["POST"]
)
def add_quiz_category():

    data = request.get_json()

    categorie = data.get(
        "categorie",
        ""
    ).strip()

    if not categorie:
        return jsonify({
            "success": False,
            "error": "Le nom de la catégorie est obligatoire."
        }), 400

    jeux = load_quiz_data()

    if categorie in jeux:
        return jsonify({
            "success": False,
            "error": "Cette catégorie existe déjà."
        }), 400

    jeux[categorie] = []

    save_quiz_data(jeux)

    return jsonify({
        "success": True,
        "categorie": categorie
    })


# Page Indiecord
@app.route("/indiecord")
def indiecord():

    feuilles = load_indiecord()

    return render_template(
        "indiecord.html",
        feuilles=feuilles
    )


# API : récupérer Indiecord
@app.route("/api/indiecord")
def indiecord_data():

    return jsonify(
        load_indiecord()
    )


# API : sauvegarder Indiecord
@app.route(
    "/api/indiecord/save",
    methods=["POST"]
)
def save_indiecord_data():

    data = request.get_json()

    try:

        save_indiecord(data)

        return jsonify({
            "success": True
        })

    except Exception as e:

        print(
            "Erreur sauvegarde Indiecord :",
            e
        )

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# API : créer une feuille
@app.route(
    "/api/indiecord/sheet",
    methods=["POST"]
)
def add_indiecord_sheet():

    data = request.get_json()

    nom = data.get(
        "nom",
        ""
    ).strip()

    if not nom:
        return jsonify({
            "success": False,
            "error": "Le nom de la page est obligatoire."
        }), 400

    feuilles = load_indiecord()

    if nom in feuilles:
        return jsonify({
            "success": False,
            "error": "Cette page existe déjà."
        }), 400

    feuilles[nom] = []

    save_indiecord(feuilles)

    return jsonify({
        "success": True,
        "nom": nom
    })


# Route qui reçoit l'image et génère le résultat
@app.route(
    "/images/generate",
    methods=["POST"]
)
def generate_image():

    if "image" not in request.files:

        return jsonify({
            "success": False,
            "error": "Aucune image envoyée."
        }), 400

    file = request.files["image"]

    if file.filename == "":

        return jsonify({
            "success": False,
            "error": "Aucune image sélectionnée."
        }), 400

    filter_type = request.form.get(
        "filter",
        "colors"
    )

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    allowed_extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    ]

    if extension not in allowed_extensions:

        return jsonify({
            "success": False,
            "error": "Format d'image non supporté."
        }), 400

    unique_id = uuid.uuid4().hex

    input_filename = (
        unique_id
        + extension
    )

    output_filename = (
        unique_id
        + "_result.png"
    )

    input_path = os.path.join(
        UPLOAD_FOLDER,
        input_filename
    )

    output_path = os.path.join(
        OUTPUT_FOLDER,
        output_filename
    )

    file.save(input_path)

    try:

        if filter_type == "colors":

            colors = int(
                request.form.get(
                    "colors",
                    4
                )
            )

            colors = max(
                2,
                min(colors, 20)
            )

            apply_colors(
                input_path,
                output_path,
                colors
            )

        elif filter_type == "distortion":

            distortion = float(
                request.form.get(
                    "distortion",
                    0.4
                )
            )

            distortion = max(
                0.1,
                min(distortion, 1)
            )

            apply_distortion(
                input_path,
                output_path,
                distortion
            )

        elif filter_type == "mosaic":

            grid = int(
                request.form.get(
                    "grid",
                    12
                )
            )

            grid = max(
                3,
                min(grid, 30)
            )

            apply_mosaic(
                input_path,
                output_path,
                grid
            )

        elif filter_type == "hex":

            hex_size = int(
                request.form.get(
                    "hex_size",
                    12
                )
            )

            hex_size = max(
                4,
                min(hex_size, 50)
            )

            apply_hex_pixelate(
                input_path,
                output_path,
                hex_size
            )

        else:

            return jsonify({
                "success": False,
                "error": "Filtre inconnu."
            }), 400

        return jsonify({
            "success": True,
            "image": "/outputs/" + output_filename,
            "download": "/outputs/" + output_filename
        })

    except Exception as e:

        print(
            "Erreur génération :",
            e
        )

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# Permet d'accéder aux images générées
@app.route(
    "/outputs/<filename>"
)
def output_file(filename):

    return send_from_directory(
        OUTPUT_FOLDER,
        filename
    )


if __name__ == "__main__":

    webbrowser.open(
        "http://127.0.0.1:5000/"
    )

    app.run(
        host="127.0.0.1",
        port=5000
    )