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
            fileTitle.textContent = `Cours : ${fileName}`;

            // Soumettre le formulaire automatiquement
            uploadForm.submit();
        }
    });
});

const appendHumanMessage = (message) => {
    const humanMessageElement = document.createElement("div");
    humanMessageElement.classList.add("message", "message-human");
    humanMessageElement.innerHTML = message;
    messagesContainer.appendChild(humanMessageElement);
};

const typeAIMessage = (message) => {
    return new Promise((resolve) => {
        const aiMessageElement = document.createElement("div");
        aiMessageElement.classList.add("message", "message-ai");
        messagesContainer.appendChild(aiMessageElement);

        const words = message.split(' '); // Split the message into words
        let index = 0;
        const typingSpeed = 200; // Time in milliseconds between words (adjust as needed)

        const typeNextWord = () => {
            if (index < words.length) {
                aiMessageElement.innerHTML += (index > 0 ? ' ' : '') + words[index];
                index++;
                setTimeout(typeNextWord, typingSpeed);
            } else {
                resolve();
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

    // Show the loader
    loaderContainer.classList.remove("hidden");

    // Fetch the AI message and type it out word by word
    const response = await fetch(url, {
        method: "POST",
        body: data,
    });
    const result = await response.text(); // Fetch the text directly

    // Type out the AI message word by word
    await typeAIMessage(result);

    // Hide the loader after typing is done
    loaderContainer.classList.add("hidden");
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
