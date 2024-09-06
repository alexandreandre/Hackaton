const promptForm = document.getElementById("prompt-form");
const submitButton = document.getElementById("submit-button");
const questionButton = document.getElementById("question-button");
const messagesContainer = document.getElementById("messages-container");
const loaderContainer = document.getElementById("loader-container");
document.addEventListener('DOMContentLoaded', () => {
// Sélectionner le formulaire et le champ de fichier
const uploadForm = document.getElementById("upload-form");
const fileInput = document.getElementById("file");
const fileTitle = document.getElementById("file-title");

// Ajouter un écouteur d'événement pour le changement du fichier
fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
        // Obtenir le nom du fichier
        const fileName = fileInput.files[0].name;

        // Mettre à jour le contenu du div avec le titre du fichier
        fileTitle.textContent = 'Cours : ${fileName}';

        // Soumettre le formulaire automatiquement
        uploadForm.submit();
    }
});
});
document.addEventListener('DOMContentLoaded', () => {
    const darkModeButton = document.getElementById('dark-mode-button');
    const body = document.body;

    // Vérifier si l'utilisateur a déjà activé le dark mode
    if (localStorage.getItem('darkMode') === 'enabled') {
        body.classList.add('dark-mode');
        darkModeButton.textContent = "Mode clair"; // Mode sombre activé, afficher "Mode clair"
        darkModeButton.classList.add('dark-mode');
    } else {
        darkModeButton.textContent = "Mode sombre"; // Mode clair activé
    }

    // Bascule entre le mode clair et sombre
    darkModeButton.addEventListener('click', () => {
        if (body.classList.contains('dark-mode')) {
            body.classList.remove('dark-mode');
            darkModeButton.textContent = "Mode sombre"; // Revenir au mode clair
            darkModeButton.classList.remove('dark-mode');
            localStorage.setItem('darkMode', 'disabled');
        } else {
            body.classList.add('dark-mode');
            darkModeButton.textContent = "Mode clair"; // Activer le mode sombre
            darkModeButton.classList.add('dark-mode');
            localStorage.setItem('darkMode', 'enabled');
        }
    });
});

// Fonction pour faire défiler automatiquement vers le bas
const scrollToBottom = () => {
    const messagesContainer = document.getElementById("messages-container");
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
};
let stopTyping = false; // Variable pour gérer l'état d'arrêt

const stopButton = document.getElementById("stop-button");
stopButton.addEventListener("click", () => {
    stopTyping = true; // Arrêter l'affichage des mots de l'IA
    stopButton.classList.add("hidden"); // Masquer le bouton "Arrêter" une fois cliqué
});

// Appelle cette fonction à chaque fois qu'un message est ajouté
const appendHumanMessage = (message) => {
    const humanMessageElement = document.createElement("div");
    humanMessageElement.classList.add("message", "message-human");
    humanMessageElement.innerHTML = message;
    messagesContainer.appendChild(humanMessageElement);
    scrollToBottom(); // Faire défiler vers le bas après l'ajout
};

const typeAIMessage = (message) => {
    return new Promise((resolve) => {
        const aiMessageElement = document.createElement("div");
        aiMessageElement.classList.add("message", "message-ai");
        messagesContainer.appendChild(aiMessageElement);

        const words = message.split(' ');
        let index = 0;
        const typingSpeed = 200; // Vitesse entre chaque mot

        const typeNextWord = () => {
            if (stopTyping) {
                // Si le bouton "Arrêter" est cliqué, on arrête d'afficher le message de l'IA
                aiMessageElement.innerHTML += '... (interrompu)';
                resolve(); // Fin de la promesse
                stopTyping = false; // Réinitialiser pour la prochaine fois
                return;
            }

            if (index < words.length) {
                aiMessageElement.innerHTML += (index > 0 ? ' ' : '') + words[index];
                index++;
                scrollToBottom(); // Faire défiler vers le bas pendant la frappe
                setTimeout(typeNextWord, typingSpeed);
            } else {
                resolve(); // Fin de l'affichage des mots
            }
        };

        typeNextWord();
    });
};


const handlePrompt = async (event) => {
    event.preventDefault();
    const data = new FormData(event.target);
    promptForm.reset();

    let url = "/prompt";
    if (questionButton.dataset.question !== undefined) {
        url = "/answer";
        data.append("question", questionButton.dataset.question);
        delete questionButton.dataset.question;
        questionButton.classList.remove("hidden");
        submitButton.innerHTML = "Message";
    }

    appendHumanMessage(data.get("prompt"));

    // Afficher le loader, le bouton "Arrêter", et masquer les boutons inutiles
    loaderContainer.classList.remove("hidden");
    stopButton.classList.remove("hidden");
    submitButton.classList.add("hidden");
    questionButton.classList.add("hidden");

    // Fetch la réponse de l'IA
    const response = await fetch(url, {
        method: "POST",
        body: data,
    });
    const result = await response.text();

    // Affichage du message de l'IA, mot par mot
    await typeAIMessage(result);

    // Masquer le loader et le bouton "Arrêter", et réafficher les boutons une fois l'IA terminée
    loaderContainer.classList.add("hidden");
    stopButton.classList.add("hidden");
    submitButton.classList.remove("hidden");
    questionButton.classList.remove("hidden");
};


promptForm.addEventListener("submit", handlePrompt);

const handleQuestionClick = async () => {
    appendHumanMessage("Pose-moi une question!");

    const response = await fetch("/question", {
        method: "GET",
    });
    const result = await response.json();
    const question = result.answer;

    questionButton.dataset.question = question;
    questionButton.classList.add("hidden");
    submitButton.innerHTML = "Répondre à la question";

    appendHumanMessage(question);
};

// Sélectionner le formulaire et le champ de fichier
const uploadForm = document.getElementById("upload-form");
const fileInput = document.getElementById("file");

// Ajouter un écouteur d'événement pour le changement du fichier
fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
        // Soumettre le formulaire automatiquement
        uploadForm.submit();
    }
});


questionButton.addEventListener("click", handleQuestionClick);
