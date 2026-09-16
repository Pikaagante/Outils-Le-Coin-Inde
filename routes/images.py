from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    send_from_directory,
    current_app
)

import os
import uuid

from outils.images.colors import apply_colors
from outils.images.distortion import apply_distortion
from outils.images.mosaic import apply_mosaic
from outils.images.hex_pixelate import apply_hex_pixelate


images_bp = Blueprint(
    "images",
    __name__
)


# Page Images
@images_bp.route("/images")
def images():

    return render_template(
        "images.html"
    )


# Génération d'une image
@images_bp.route(
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


    upload_folder = current_app.config[
        "UPLOAD_FOLDER"
    ]

    output_folder = current_app.config[
        "OUTPUT_FOLDER"
    ]


    input_path = os.path.join(
        upload_folder,
        input_filename
    )


    output_path = os.path.join(
        output_folder,
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


# Accès aux images générées
@images_bp.route(
    "/outputs/<filename>"
)
def output_file(filename):

    return send_from_directory(
        current_app.config["OUTPUT_FOLDER"],
        filename
    )