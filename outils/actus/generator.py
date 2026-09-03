import requests
from datetime import datetime
import html

def get_french_date():
    """
    Retourne la date actuelle en français.
    """
    
    # Liste des jours de la semaine
    days = [
        "lundi", "mardi", "mercredi", "jeudi",
        "vendredi", "samedi", "dimanche"
    ]

    # Liste des mois
    months = [
        "janvier", "février", "mars", "avril",
        "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"
    ]

    # Récupère la date et l'heure actuelles
    now = datetime.now()

    # weekday() retourne un nombre de 0 à 6
    return f"{days[now.weekday()]} {now.day} {months[now.month - 1]} {now.year}"


def get_game_details(app_id: int):
    """
    Récupère les informations principales d'un jeu depuis Steam.

    Paramètre :
        app_id : identifiant Steam du jeu

    Retourne :
        Un dictionnaire contenant le nom, la description et l'URL.
        Retourne None si le jeu n'est pas trouvé.
    """

    # URL de l'API Steam permettant de récupérer les informations du jeu correspondant à l'AppID.
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&l=french"

    # Envoie une requête à Steam
    r = requests.get(url)

    # Force l'encodage UTF-8 pour éviter les problèmes avec les accents et caractères français.
    r.encoding = "utf-8"

    # Convertit la réponse JSON de Steam en dictionnaire Python
    data = r.json()

    # Vérifie sur la récupération à réussi
    if str(app_id) not in data or not data[str(app_id)]["success"]:
        return None

    # Donnée du jeu
    game_data = data[str(app_id)]["data"]

    # Récupère le nom du jeu
    name = game_data.get(
        "name",
        "Nom inconnu"
    )

    # Récupère la description du jeu
    short_desc = html.unescape(
        game_data.get(
            "short_description",
            "Pas de description."
        )
    )

    # Le lien vers la page Steam du jeu.
    steam_url = f"https://store.steampowered.com/app/{app_id}/"

    return {
        "name": name,
        "description": short_desc,
        "url": steam_url
    }


def get_game_tags(app_id: int, limit=4):
    """
    Récupère les tags d'un jeu depuis sa page Steam.

    Paramètres :
        app_id : identifiant Steam du jeu
        limit : nombre maximum de tags à récupérer

    Exemple :
        Action · Aventure · Indépendant · RPG
    """
    
    # URL de la page Steam du jeu
    url = f"https://store.steampowered.com/app/{app_id}"

    # Envoie une requête à Steam
    r = requests.get(url)

    if r.status_code != 200:
        return []

    # Liste qui contiendra les tags trouvés
    page_html = r.text
    tags = []
    tag_marker = 'class="app_tag"'
    parts = page_html.split(tag_marker)

    # Parcourt toutes les parties trouvées
    for part in parts[1:]:
        try:
            # Récupère le texte situé entre les balises HTML
            tag = part.split(">")[1].split("<")[0].strip()
            # Vérifie que le tag existe et qu'il n'a pas déjà été ajouté à la liste
            if tag and tag not in tags:
                tags.append(tag)
        except:
            pass
    return tags[:limit]


def get_games(app_ids):
    """
    Récupère les informations de plusieurs jeux Steam.

    Paramètre :
        app_ids : liste d'AppID Steam

    Retourne :
        Une liste contenant les informations de chaque jeu trouvé.
    """
    
    # Liste qui contiendra tous les jeux
    games = []

    # Parcourt chaque AppID fourni
    for app_id in app_ids:
        # Récupère les informations principales du jeu
        details = get_game_details(app_id)

        # Si le jeu n'existe pas ou si Steam a renvoyé une erreur, on passe simplement au jeu suivant.
        if not details:
            continue

        # Récupère les tags du jeu
        tags = get_game_tags(app_id)

        # Ajoute le jeu dans notre liste
        games.append({
            "name": details["name"],
            "description": details["description"],
            "url": details["url"],
            "tags": tags
        })

    # Retourne tous les jeux récupérés
    return games


def generate_discord_markdown(games):
    """
    Génère une publication au format Markdown pour Discord.

    Paramètre :
        games : liste des jeux récupérés avec get_games()

    Retourne :
        Le texte complet prêt à être copié sur Discord.
    """
    
    # Récupère la date actuelle en français
    today = get_french_date()

    md = []

    # Titre de la publication
    md.append("# :newspaper: ACTU INDÉ")

    # Ajoute la date et le nombre de jeux
    md.append(
        f":calendar_spiral: **{today} · {len(games)} sorties à surveiller**"
    )

    # Ligne de séparation
    md.append("━━━━━━━━━━━━━━━━━━━━━━\n")

    # Parcourt chaque jeu
    for game in games:
        # Ajoute le nom du jeu en titre
        md.append(
            f"## {game['name']}"
        )

        # Transforme les tags en :
        #
        # `Action` · `RPG` · `Indépendant`
        #
        tag_line = " · ".join(
            [f"`{tag}`" for tag in game["tags"]]
        )

        # Si des tags ont été trouvés, on les ajoute
        if tag_line:
            md.append(tag_line + "\n")
        # Sinon, on indique qu'aucun tag n'a été trouvé
        else:
            md.append("`Tags indisponibles`\n")
        # Ajoute la description du jeu
        md.append(
            game["description"] + "\n"
        )
        # Ajoute le lien Steam
        md.append(
            f":link: {game['url']}\n"
        )

        md.append(
            "━━━━━━━━━━━━━━━━━━━━━━\n"
        )

    return "\n".join(md)


def generate_reddit_markdown(games):
    """
    Génère une publication au format Markdown pour Reddit.

    Paramètre :
        games : liste des jeux récupérés avec get_games()

    Retourne :
        Le texte complet prêt à être copié sur Reddit.
    """
    
    md = []

    # Titre
    md.append(
        "Aujourd'hui dans les nouveautés :\n"
    )

    # Ajoute une liste contenant uniquement
    # les noms des jeux
    for game in games:

        md.append(
            f"- {game['name']}"
        )

    # Ajoute une nouvelle section
    md.append(
        "\nDécouvrez les jeux :\n"
    )

    # Parcourt chaque jeu pour créer sa présentation complète
    for game in games:

        md.append("---\n")

        # Nom du jeu sous forme de titre
        md.append(
            f"## {game['name']}\n"
        )

        # Vérifie si le jeu possède des tags
        if game["tags"]:

            tags = " · ".join(
                [f"`{tag}`" for tag in game["tags"]]
            )
            
            # Ajoute les tags
            md.append(tags + "\n")

        # Ajoute la description
        md.append(
            game["description"] + "\n"
        )

        # Ajoute le lien vers Steam
        md.append(
            f"[🔗 Voir sur Steam]({game['url']})\n"
        )

    return "\n".join(md)