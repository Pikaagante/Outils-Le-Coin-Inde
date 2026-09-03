# Outils Le Coin Indé

Petit projet fait en quelques heures permettant de regrouper au même endroit différents outils que j'utilise pour gérer et créer du contenu pour mon serveur Discord Le Coin Indé.

L'objectif n'est pas de créer une grosse application, mais simplement d'avoir un petit espace local qui me permet de retrouver rapidement mes outils sans avoir plusieurs scripts séparés à lancer manuellement.

---

## Infos

Une petite application web locale développée avec Python et Flask.

Elle regroupe plusieurs outils utilisés pour la création de contenu du serveur, notamment :

- génération d'actualités à partir d'AppID Steam
- modification et transformation de covers de jeux

---

## Outils

### Actus

Le générateur d'actus permet de créer rapidement une publication à partir d'un ou plusieurs AppID Steam.
Il récupère automatiquement les informations du jeu depuis Steam et permet ensuite de générer un texte adapté à différents supports (Discord et Reddit).

---

### Images

La partie Images permet de transformer les covers de jeux afin de les utiliser pour différents contenus.

Filtres disponibles :

- Couleurs
  - Réduit le nombre de couleurs présentes dans l'image.

- Déformation
  - Déforme l'image avec différentes vagues et distorsions.

- Mosaïque
  - Découpe l'image en plusieurs morceaux et les réorganise.

- Pixelisation hexagonale
  - Transforme l'image en utilisant une grille d'hexagones.

Les paramètres des différents filtres peuvent être modifiés directement depuis l'interface.

