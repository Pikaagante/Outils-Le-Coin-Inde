from PIL import Image
import cv2
import numpy as np


def apply_colors(input_path, output_path, colors=4):
    """
    Réduit le nombre de couleurs présentes dans une image.

    Paramètres :
        input_path : chemin vers l'image originale
        output_path : chemin où enregistrer l'image générée
        colors : nombre de couleurs finales souhaitées

    Le traitement utilise l'algorithme K-Means d'OpenCV
    pour regrouper les couleurs similaires.
    """
    
    # Ouvre l'image et la convertit en RGB pour avoir trois canaux : Rouge, Vert et Bleu.
    image = Image.open(input_path).convert("RGB")

    # On réduit temporairement l'image à 100x100 pixels.
    # Cela permet de réduire fortement le nombre de pixels
    # à analyser et donc d'accélérer le K-Means.
    size = 100

    small = image.resize((size, size),Image.Resampling.BILINEAR)

    # Convertit l'image PIL en tableau NumPy.
    array = np.array(small)

    # Transforme l'image en une simple liste de pixels.
    pixels = array.reshape((-1, 3)).astype(np.float32)

    # Définit les conditions d'arrêt de l'algorithme.
    criteria = (cv2.TERM_CRITERIA_EPS+ cv2.TERM_CRITERIA_MAX_ITER,30,1.0
    )

    # Regroupe les pixels en plusieurs groupes de couleurs.
    # "colors" correspond au nombre de groupes souhaités.
    _, labels, centers = cv2.kmeans(pixels,colors,None,criteria,10,cv2.KMEANS_PP_CENTERS
    )

    # Convertit les centres de couleurs en entiers compris entre 0 et 255.
    centers = np.uint8(centers)

    # Remplace chaque pixel par la couleur du groupe auquel il appartient.
    result = centers[
        labels.flatten()
    ]

    # Remet les pixels dans la forme originale de notre petite image 100x100.
    result = result.reshape(
        array.shape
    )

    # Convertit le tableau NumPy en image
    result = Image.fromarray(result)

    # Agrandit l'image pour lui redonner sa taille originale.
    result = result.resize(image.size,Image.Resampling.NEAREST)

    result.save(output_path)