from PIL import Image
import random


def apply_mosaic(input_path, output_path, grid=12):
    """
    Découpe une image en plusieurs morceaux puis
    mélange aléatoirement leur position.

    Paramètres :
        input_path : chemin vers l'image originale
        output_path : chemin où enregistrer l'image générée
        grid : nombre de cases horizontales et verticales
    """
    # Ouvre l'image et la convertit en RGB.
    image = Image.open(input_path).convert("RGB")

    # Récupère la largeur et la hauteur de l'image.
    width, height = image.size

    # Calcule la largeur/hauteur de chaque morceau.
    tile_width = width // grid
    tile_height = height // grid

    tiles = []

    # Parcourt chaque ligne de la grille.
    for y in range(grid):
        # Parcourt chaque colonne de la grille.
        for x in range(grid):
            # Position gauche du morceau.
            left = x * tile_width
            # Position haute du morceau.
            top = y * tile_height
            # Position droite du morceau.
            right = (
                (x + 1) * tile_width
                if x < grid - 1
                else width
            )
            # Position basse du morceau.
            bottom = (
                (y + 1) * tile_height
                if y < grid - 1
                else height
            )
            # Découpe le morceau de l'image.
            tile = image.crop((left, top, right, bottom))
            # Ajoute le morceau à notre liste.
            tiles.append(tile)

    # Mélange aléatoirement tous les morceaux.
    random.shuffle(tiles)

    # Crée une nouvelle image vide avec les mêmes dimensions que l'originale.
    result = Image.new(
        "RGB",
        image.size
    )

    index = 0

    # Parcourt à nouveau chaque ligne de la grille.
    for y in range(grid):
        # Parcourt chaque colonne.
        for x in range(grid):
            # Place le morceau correspondant dans l'image finale.
            result.paste(
                tiles[index],
                (
                    x * tile_width,
                    y * tile_height
                )
            )

            index += 1

    result.save(output_path)