from flask import Blueprint, render_template, request

from outils.actus.generator import (
    get_games,
    generate_discord_markdown,
    generate_reddit_markdown
)


actus_bp = Blueprint(
    "actus",
    __name__
)


@actus_bp.route(
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

            result = generate_reddit_markdown(
                games
            )

        else:

            result = generate_discord_markdown(
                games
            )

    return render_template(
        "actus.html",
        result=result,
        app_ids=app_ids_text
    )