from PIL import Image, ImageDraw
import numpy as np


def apply_hex_pixelate(input_path,output_path,hex_size=12):
    """
    Transforme une image en une mosaïque d'hexagones.

    Paramètres :
        input_path : chemin vers l'image originale
        output_path : chemin où enregistrer l'image générée
        hex_size : taille des hexagones

    """
    
    # Ouvre l'image avec Pillow et la convertit en RGB.
    img = Image.open(
        input_path
    ).convert("RGB")

    # Convertit l'image en tableau NumPy.
    img_np = np.array(img)

    # Récupère la hauteur et la largeur de l'image.
    h, w = img_np.shape[:2]

    # Crée une nouvelle image vide avec les mêmes dimensions que l'image originale.
    output = Image.new(
        "RGB",
        (w, h)
    )

    # Crée un objet permettant de dessiner sur l'image.
    draw = ImageDraw.Draw(output)

    # Calcule la distance horizontale/verticale entre deux hexagones.
    dx = int(hex_size * 3 / 4)
    dy = int(hex_size * (3 ** 0.5) / 2)

    # Parcourt l'image ligne par ligne.
    for y in range(0, h, dy):
        # Parcourt l'image colonne par colonne.
        for x in range(0, w, dx):

            # Position horizontale du centre de l'hexagone.
            cx = x

            # Position verticale du centre.
            cy = y + (
                # Une colonne sur deux est légèrement décalée
                dx // 2
                if (x // dx) % 2 == 1
                else 0
            )

            # Vérifie que le centre de l'hexagone se trouve bien dans l'image.
            if cy >= h or cx >= w:
                continue

            # Récupère la couleur du pixel situé au centre de l'hexagone.
            r, g, b = img_np[cy % h,cx % w]

            # Calcule les 6 points nécessaires pour dessiner un hexagone régulier.
            polygon = [
                (
                    cx + hex_size * np.cos(np.pi / 3 * i),
                    cy + hex_size *np.sin(np.pi / 3 * i)
                )
                for i in range(6)
            ]

            # Dessine l'hexagone avec la couleur récupérée au centre.
            draw.polygon(polygon,fill=(r, g, b))

    output.save(output_path)