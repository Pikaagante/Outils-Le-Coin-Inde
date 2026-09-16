from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    current_app
)

import pandas as pd


indiecord_bp = Blueprint(
    "indiecord",
    __name__
)


# Lit le fichier Indiecord
def load_indiecord():

    fichier = pd.ExcelFile(
        current_app.config["ODS_FILE"],
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
        current_app.config["ODS_FILE"],
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


# Page Indiecord
@indiecord_bp.route("/indiecord")
def indiecord():

    feuilles = load_indiecord()

    return render_template(
        "indiecord.html",
        feuilles=feuilles
    )


# API : récupérer Indiecord
@indiecord_bp.route("/api/indiecord")
def indiecord_data():

    return jsonify(
        load_indiecord()
    )


# API : sauvegarder Indiecord
@indiecord_bp.route(
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
@indiecord_bp.route(
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