let indiecordData = {};
let feuilleActuelle = "";

const select = document.getElementById("feuille-select");
const tbody = document.getElementById("indiecord-body");
const message = document.getElementById("indiecord-message");


async function chargerIndiecord() {

    const response = await fetch("/api/indiecord");

    indiecordData = await response.json();

    remplirFeuilles();

}


function remplirFeuilles() {

    select.innerHTML = "";

    Object.keys(indiecordData).forEach(feuille => {

        const option = document.createElement("option");

        option.value = feuille;
        option.textContent = feuille;

        select.appendChild(option);

    });

    if (Object.keys(indiecordData).length > 0) {

        feuilleActuelle = Object.keys(indiecordData)[0];

        select.value = feuilleActuelle;

        afficherFeuille();

    }

}


function afficherFeuille() {

    tbody.innerHTML = "";

    const lignes = indiecordData[feuilleActuelle] || [];

    lignes.forEach((ligne, index) => {

        ajouterLigne(
            ligne.EN || "",
            ligne.FR || "",
            ligne.Rareté || "",
            index
        );

    });

}


function ajouterLigne(
    en = "",
    fr = "",
    rarete = "",
    index = null
) {

    const tr = document.createElement("tr");

    tr.innerHTML = `
        <td>
            <input type="text" value="${en}">
        </td>

        <td>
            <input type="text" value="${fr}">
        </td>

        <td>
            <select>
                <option value="">---</option>
                <option value="C" ${rarete === "C" ? "selected" : ""}>C</option>
                <option value="R" ${rarete === "R" ? "selected" : ""}>R</option>
                <option value="E" ${rarete === "E" ? "selected" : ""}>E</option>
                <option value="L" ${rarete === "L" ? "selected" : ""}>L</option>
            </select>
        </td>

        <td>
            <button class="supprimer-ligne">
                Supprimer
            </button>
        </td>
    `;

    tr.querySelector(".supprimer-ligne").addEventListener(
        "click",
        () => tr.remove()
    );

    tbody.appendChild(tr);
}


function recupererTableau() {

    const lignes = [];

    tbody.querySelectorAll("tr").forEach(tr => {

        const inputs = tr.querySelectorAll("input");
        const rarete = tr.querySelector("select");

        lignes.push({
            EN: inputs[0].value,
            FR: inputs[1].value,
            Rareté: rarete.value
        });

    });

    return lignes;
}


async function sauvegarder() {

    indiecordData[feuilleActuelle] = recupererTableau();

    const response = await fetch(
        "/api/indiecord/save",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(indiecordData)
        }
    );

    const result = await response.json();

    if (result.success) {

        afficherMessage("Sauvegarde effectuée.");

    } else {

        afficherMessage(
            "Erreur : " + result.error
        );

    }

}


async function nouvelleFeuille() {

    const nom = prompt("Nom de la nouvelle page :");

    if (!nom) {
        return;
    }

    const response = await fetch(
        "/api/indiecord/sheet",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                nom: nom
            })
        }
    );

    const result = await response.json();

    if (!result.success) {

        afficherMessage(
            "Erreur : " + result.error
        );

        return;
    }

    await chargerIndiecord();

    select.value = nom;

    feuilleActuelle = nom;

    afficherFeuille();

    afficherMessage("Page créée.");

}


function afficherMessage(texte) {

    message.textContent = texte;

    setTimeout(() => {
        message.textContent = "";
    }, 3000);

}


select.addEventListener(
    "change",
    () => {

        feuilleActuelle = select.value;

        afficherFeuille();

    }
);


document.getElementById(
    "ajouter-ligne"
).addEventListener(
    "click",
    () => ajouterLigne()
);


document.getElementById(
    "sauvegarder"
).addEventListener(
    "click",
    sauvegarder
);


document.getElementById(
    "nouvelle-feuille"
).addEventListener(
    "click",
    nouvelleFeuille
);


chargerIndiecord();
