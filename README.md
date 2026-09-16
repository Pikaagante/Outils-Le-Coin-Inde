# Outils Le Coin Indé

Petit projet fait en quelques heures permettant de regrouper au même endroit différents outils que j'utilise pour gérer et créer du contenu pour mon serveur Discord **Le Coin Indé**.

L'objectif n'est pas de créer une grosse application, mais simplement d'avoir un petit espace local qui me permet de retrouver rapidement mes outils sans avoir plusieurs scripts séparés à lancer manuellement.

---

## Infos

Une petite application web locale développée avec **Python** et **Flask**.

Elle regroupe plusieurs outils utilisés pour la création de contenu et la gestion du serveur discord Le Coin Indé.

---

## Outils

### Actus

Le générateur d'actus permet de créer rapidement une publication à partir d'un ou plusieurs AppID Steam.

Il récupère automatiquement les informations du jeu depuis Steam et permet ensuite de générer un texte adapté à différents supports (**Discord** et **Reddit**).

---

### Images

La partie Images permet de transformer les covers de jeux afin de les utiliser pour différents contenus.

Filtres disponibles :

* **Couleurs**

  * Réduit le nombre de couleurs présentes dans l'image.

* **Déformation**

  * Déforme l'image avec différentes vagues et distorsions.

* **Mosaïque**

  * Découpe l'image en plusieurs morceaux et les réorganise.

* **Pixelisation hexagonale**

  * Transforme l'image en utilisant une grille d'hexagones.

Les paramètres des différents filtres peuvent être modifiés directement depuis l'interface.

---

### Quiz

La partie Quiz permet de gérer les jeux utilisés pour les quiz du serveur Discord.

Elle permet notamment de :

* rechercher un jeu
* filtrer les jeux par catégorie
* ajouter de nouveaux jeux
* ajouter un contexte à une question
* créer de nouvelles catégories

Les données sont stockées dans un fichier `JSON`.

---

### Indiecord

La partie Indiecord permet de gérer facilement les données utilisées par le bot Discord **Indiecord**.

Elle permet de :

* consulter les différentes catégories
* modifier les traductions
* modifier les raretés
* ajouter ou supprimer des entrées
* créer de nouvelles catégories
* sauvegarder les modifications

Les données sont stockées dans un fichier `.ods`.

---

## Installation

Le projet utilise **Python** et **Flask**.

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Puis lancer l'application :

```bash
python app.py
```

L'application sera accessible depuis le navigateur à l'adresse :

```text
http://127.0.0.1:5000/
```

---

## Création de l'exécutable

Le projet utilise **PyInstaller** pour créer une version exécutable.

Pour générer l'exécutable :

```bash
pyinstaller ImageIndie.spec
```

Le résultat sera généré dans le dossier `dist/`.

---