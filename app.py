from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import uuid

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
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

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
    # Variables utilisées par la page
    result = ""
    app_ids_text = ""

    # Vérifie si le formulaire a été envoyé
    if request.method == "POST":
        app_ids_text = request.form.get(
            "app_ids",
            ""
        )

        # Récupère les AppID
        app_ids = []

        # Récupération des AppID
        for line in app_ids_text.splitlines():

            line = line.strip()

            # Vérifie que la ligne contient uniquement des chiffres
            if line.isdigit():
                app_ids.append(int(line))

        # Récupération des jeux Steam
        games = get_games(app_ids)

        # Format demandé
        format_type = request.form.get(
            "format",
            "discord"
        )

        # Génère le format Reddit
        if format_type == "reddit":
            result = generate_reddit_markdown(games)
        # Sinon, génère le format Discord
        else:
            result = generate_discord_markdown(games)

    # Affiche la page avec le résultat
    return render_template("actus.html",result=result,app_ids=app_ids_text)

# Page Images
@app.route("/images")
def images():

    return render_template(
        "images.html"
    )

# Route qui reçoit l'image et génère le résultat
@app.route(
    "/images/generate",
    methods=["POST"]
)
def generate_image():

    # Vérifier qu'une image a été envoyée
    if "image" not in request.files:

        return jsonify({
            "success": False,
            "error": "Aucune image envoyée."
        }), 400

    # Récupère l'image envoyée
    file = request.files["image"]

    # Vérifie qu'un fichier a bien été sélectionné
    if file.filename == "":
        return jsonify({
            "success": False,
            "error": "Aucune image sélectionnée."
        }), 400

    # Récupère le filtre choisi
    filter_type = request.form.get("filter","colors")

    # Récupère l'extension du fichier
    extension = os.path.splitext(file.filename)[1].lower()

    # Extensions autorisées
    allowed_extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    ]

    # Vérifie que l'extension est autorisée
    if extension not in allowed_extensions:
        return jsonify({
            "success": False,
            "error": "Format d'image non supporté."
        }), 400

    unique_id = uuid.uuid4().hex

    # Nom du fichier original temporaire
    input_filename = (unique_id+ extension)

    # Nom du fichier généré
    output_filename = (unique_id+ "_result.png")
    # Chemin du fichier original
    input_path = os.path.join(UPLOAD_FOLDER,input_filename)
    # Chemin du résultat
    output_path = os.path.join(OUTPUT_FOLDER,output_filename)


    # Sauvegarde temporaire
    file.save(
        input_path
    )


    try:
        # Vérifie si le filtre Couleurs est choisi
        if filter_type == "colors":
            # Récupère le nombre de couleurs
            colors = int(request.form.get("colors",4))
            # Limite la valeur entre 2 et 20
            colors = max(2,min(colors, 20))
            apply_colors(input_path,output_path,colors)
            
        # Vérifie si le filtre Déformation est choisi
        elif filter_type == "distortion":
            # Récupère l'intensité
            distortion = float(request.form.get("distortion",0.4))
            # Limite la valeur entre 0.1 et 1
            distortion = max(0.1,min(distortion, 1))
            apply_distortion(input_path,output_path,distortion)
            
        # Vérifie si le filtre Mosaïque est choisi
        elif filter_type == "mosaic":
            # Récupère la taille de la grille
            grid = int(request.form.get("grid",12))
            # Limite la valeur entre 3 et 30
            grid = max(3,min(grid, 30))
            apply_mosaic(input_path,output_path,grid)

        # Vérifie si le filtre Hexagones est choisi
        elif filter_type == "hex":
            # Récupère la taille des hexagones
            hex_size = int(request.form.get("hex_size",12))
            # Limite la valeur entre 4 et 50
            hex_size = max(4,min(hex_size, 50))
            apply_hex_pixelate(input_path,output_path,hex_size)
            
        # Si le filtre n'existe pas
        else:
            return jsonify({
                "success": False,
                "error": "Filtre inconnu."
            }), 400

        # Renvoie les chemins du résultat
        return jsonify({
            "success": True,
            "image": (
                "/outputs/"
                + output_filename
            ),
            "download": (
                "/outputs/"
                + output_filename
            )
        })

    # Gestion des erreurs
    except Exception as e:
        print("Erreur génération :",e)

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
    app.run(
        debug=True
    )