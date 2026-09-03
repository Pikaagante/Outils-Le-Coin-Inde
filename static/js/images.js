document.addEventListener("DOMContentLoaded", () => {

const imageInput = document.getElementById("image-input");
const selectButton = document.getElementById("select-image");

const previewContainer = document.getElementById("preview-container");
const imagePreview = document.getElementById("image-preview");
const imageName = document.getElementById("image-name");

const options = document.getElementById("options");
const filter = document.getElementById("filter");

const generateButton = document.getElementById("generate-button");

const resultContainer = document.getElementById("result-container");
const resultImage = document.getElementById("result-image");
const downloadButton = document.getElementById("download-button");

let selectedFile = null;

selectButton.addEventListener("click", () => {
    imageInput.click();
});

imageInput.addEventListener("change", () => {
    if (imageInput.files.length === 0) {
        return;
    }
    const file = imageInput.files[0];
    // Vérification du format
    if (!file.type.startsWith("image/")) {
        alert("Veuillez sélectionner une image.");
        imageInput.value = "";
        return;
    }

    // Sauvegarder l'image
    selectedFile = file;

    // Nom du fichier
    imageName.textContent = file.name;

    // Aperçu
    imagePreview.src = URL.createObjectURL(file);

    // Afficher les options
    previewContainer.style.display = "block";
    options.style.display = "block";

    // Cacher l'ancien résultat
    resultContainer.style.display = "none";
});

// Changement de filtre
filter.addEventListener("change", () => {
    const filterType = filter.value;

    // Cacher toutes les options
    document
        .querySelectorAll(".filter-options")
        .forEach((element) => {
            element.style.display = "none";
        });

    // Afficher les options correspondantes
    const selectedOptions = document.getElementById(
        filterType + "-options"
    );
    if (selectedOptions) {
        selectedOptions.style.display = "block";
    }
});

// Valeur pour la distortion
const distortionInput = document.getElementById("distortion");
const distortionValue = document.getElementById("distortion-value");

distortionInput.addEventListener("input", () => {
    distortionValue.textContent =
        distortionInput.value;
});


// Genere l'image
generateButton.addEventListener("click", async () => {
    if (!selectedFile) {
        alert("Sélectionne d'abord une image.");
        return;
    }

    const formData = new FormData();
    formData.append(
        "image",
        selectedFile
    );
    formData.append(
        "filter",
        filter.value
    );
    formData.append(
        "colors",
        document.getElementById("colors").value
    );
    formData.append(
        "distortion",
        document.getElementById("distortion").value
    );
    formData.append(
        "grid",
        document.getElementById("grid").value
    );
    formData.append(
        "hex_size",
        document.getElementById("hex-size").value
    );

    // Bouton chargement
    generateButton.disabled = true;
    generateButton.textContent =
        "Génération...";


    try {
        const response = await fetch(
            "/images/generate",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        // Erreur
        if (!data.success) {

            throw new Error(
                data.error ||
                "Une erreur est survenue."
            );

        }

        // Resultat
        resultImage.src =
            data.image;

        downloadButton.href =
            data.download;

        resultContainer.style.display =
            "block";

        resultContainer.scrollIntoView({
            behavior: "smooth"
        });
    } catch (error) {
        console.error("Erreur :",error);
        alert("Erreur : " + error.message );

    } finally {
        generateButton.disabled = false;
        generateButton.textContent ="Générer l'image";}
});
});
