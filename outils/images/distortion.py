from PIL import Image
import cv2
import numpy as np


def apply_distortion(input_path, output_path, distortion=0.4):
    """
    Applique une déformation ondulée à une image.

    Paramètres :
        input_path : chemin vers l'image originale
        output_path : chemin où enregistrer l'image générée
        distortion : intensité de la déformation
    """

    # Ouvre l'image avec Pillow et la convertit en RGB.
    image = Image.open(input_path).convert("RGB")

    # Convertit l'image en tableau NumPy.
    array = np.array(image)

    # Récupère la hauteur et la largeur de l'image.
    height, width = array.shape[:2]

    # Crée deux tableaux contenant les coordonnées de chaque pixel de l'image.
    x, y = np.meshgrid(
        np.arange(width),
        np.arange(height)
    )

    # Transforme la valeur de distortion en une valeur plus importante pour la déformation.
    amount = distortion * 100

    # Modifie la position horizontale de chaque pixel.
    new_x = (x+ np.sin(y / 35)* amount
    )

    # Même principe que pour X, mais cette fois sur l'axe vertical
    new_y = (y+ np.sin(x / 45)* amount
    )

    # Empêche les coordonnées X de sortir de l'image.
    new_x = np.clip(new_x,0,width - 1).astype(np.float32)

    # Même chose pour les coordonnées Y.
    new_y = np.clip(new_y,0,height - 1).astype(np.float32)

    # Remappe les pixels de l'image en utilisant les nouvelles coordonnées calculées.
    result = cv2.remap(array,new_x,new_y,interpolation=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)

    Image.fromarray(result).save(output_path)