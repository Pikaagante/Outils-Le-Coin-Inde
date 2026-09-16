let quizData = {};
let categorieActuelle = "toutes";

const recherche = document.getElementById("recherche");
const filtre = document.getElementById("filtre-categorie");
const liste = document.getElementById("liste-jeux");


// Charge les données
async function chargerQuiz() {

    const response = await fetch("/api/quiz");

    quizData = await response.json();

    remplirCategories();
    afficherJeux();
}


// Remplit les catégories
function remplirCategories() {

    filtre.innerHTML = `
        <option value="toutes">
            Toutes les catégories
        </option>
    `;

    const selectCategorie = document.getElementById(
        "categorie-jeu"
    );

    selectCategorie.innerHTML = "";

    for (const categorie of Object.keys(quizData)) {

        const optionFiltre = document.createElement("option");

        optionFiltre.value = categorie;
        optionFiltre.textContent = categorie;

        filtre.appendChild(optionFiltre);


        const optionAjout = document.createElement("option");

        optionAjout.value = categorie;
        optionAjout.textContent = categorie;

        selectCategorie.appendChild(optionAjout);
    }
}


// Affiche les jeux
function afficherJeux() {

    const rechercheTexte = recherche.value
        .trim()
        .toLowerCase();

    liste.innerHTML = "";

    let nombreJeux = 0;

    for (const [categorie, jeux] of Object.entries(quizData)) {

        if (
            categorieActuelle !== "toutes"
            && categorie !== categorieActuelle
        ) {
            continue;
        }

        for (const jeu of jeux) {

            if (
                rechercheTexte
                && !jeu.nom.toLowerCase().includes(rechercheTexte)
            ) {
                continue;
            }

            nombreJeux++;

            const element = document.createElement("div");

            element.className = "quiz-game";

            element.innerHTML = `
                <div class="quiz-game-info">

                    <strong>${jeu.nom}</strong>

                    <span class="quiz-game-category">
                        ${categorie}
                    </span>

                    ${jeu.context
                        ? `<span class="quiz-game-context">
                            ${jeu.context}
                        </span>`
                        : ""
                    }

                </div>
            `;

            liste.appendChild(element);
        }
    }

    document.getElementById(
        "nombre-jeux"
    ).textContent =
        nombreJeux + (nombreJeux > 1 ? " jeux" : " jeu");


    if (!nombreJeux) {

        liste.innerHTML = `
            <p class="quiz-empty">
                Aucun jeu trouvé.
            </p>
        `;
    }
}


// Recherche
recherche.addEventListener(
    "input",
    afficherJeux
);


// Filtre
filtre.addEventListener(
    "change",
    function () {

        categorieActuelle = this.value;

        afficherJeux();
    }
);


// Ajouter un jeu
document
    .getElementById("form-ajout-jeu")
    .addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const nom = document
                .getElementById("nom-jeu")
                .value
                .trim();

            const categorie = document
                .getElementById("categorie-jeu")
                .value;

            const context = document
                .getElementById("context-jeu")
                .value
                .trim();

            const response = await fetch(
                "/api/quiz/add",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        nom,
                        categorie,
                        context
                    })
                }
            );

            const result = await response.json();

            if (!result.success) {

                alert(result.error);

                return;
            }

            alert("Jeu ajouté !");

            document
                .getElementById("form-ajout-jeu")
                .reset();

            await chargerQuiz();
        }
    );


// Créer une catégorie
document
    .getElementById("form-ajout-categorie")
    .addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const categorie = document
                .getElementById("nom-categorie")
                .value
                .trim();

            const response = await fetch(
                "/api/quiz/category",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        categorie
                    })
                }
            );

            const result = await response.json();

            if (!result.success) {

                alert(result.error);

                return;
            }

            alert("Catégorie créée !");

            document
                .getElementById("form-ajout-categorie")
                .reset();

            await chargerQuiz();
        }
    );


// Initialisation
chargerQuiz();