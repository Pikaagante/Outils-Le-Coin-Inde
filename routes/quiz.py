from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    current_app
)

import json


quiz_bp = Blueprint(
    "quiz",
    __name__
)


# Lit le fichier JSON
def load_quiz_data():

    with open(
        current_app.config["JSON_FILE"],
        "r",
        encoding="utf-8"
    ) as fichier:

        return json.load(fichier)


# Sauvegarde le fichier JSON
def save_quiz_data(data):

    with open(
        current_app.config["JSON_FILE"],
        "w",
        encoding="utf-8"
    ) as fichier:

        json.dump(
            data,
            fichier,
            ensure_ascii=False,
            indent=4
        )


# Page Quiz
@quiz_bp.route("/quiz")
def quiz():

    jeux = load_quiz_data()

    return render_template(
        "quiz.html",
        jeux=jeux
    )


# API : récupérer les jeux
@quiz_bp.route("/api/quiz")
def quiz_data():

    return jsonify(
        load_quiz_data()
    )


# API : ajouter un jeu
@quiz_bp.route(
    "/api/quiz/add",
    methods=["POST"]
)
def add_quiz_game():

    data = request.get_json()

    nom = data.get(
        "nom",
        ""
    ).strip()

    categorie = data.get(
        "categorie",
        ""
    ).strip()

    context = data.get(
        "context",
        ""
    ).strip()


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


    jeux[categorie].append(
        nouveau_jeu
    )

    save_quiz_data(jeux)


    return jsonify({
        "success": True,
        "jeu": nouveau_jeu
    })


# API : créer une catégorie
@quiz_bp.route(
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