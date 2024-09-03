from flask import Flask, render_template, request, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
from src.utils.ask_question_to_pdf import ask_question_to_pdf, read_pdf, split_text

app = Flask(__name__)
app.secret_key = 'jdjpew7fw'

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Assurez-vous que le dossier de téléchargement existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print("Aucun fichier trouvé dans la requête.")
        return "Aucun fichier sélectionné", 400

    file = request.files['file']
    
    if file.filename == '':
        print("Le nom de fichier est vide.")
        return "Nom de fichier vide", 400

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        print(f"Téléchargement du fichier : {filepath}")
        file.save(filepath)  # Sauvegarde le fichier sur le disque
        print(read_pdf(filepath))
        # Lecture du fichier PDF et traitement
        try:
            document = read_pdf(filepath)
            pdf_text = ' '.join(split_text(document))
            
            # Stocker le texte dans la session pour l'utiliser dans 'prompt'
            session['pdf_text'] = pdf_text
            print(f"Le texte extrait du PDF a été stocké en session. Longueur du texte : {len(pdf_text)} caractères.")
            return redirect(url_for('hello_world'))
        except Exception as e:
            print(f"Erreur lors de la lecture du PDF : {e}")
            return "Erreur lors de la lecture du PDF", 500
    else:
        print("Aucun fichier valide reçu.")
        return "Erreur lors du téléchargement du fichier", 400


@app.route('/prompt', methods=['POST'])
def prompt():
    message = request.form['prompt']
    
    # Récupérer le texte extrait du PDF depuis la session
    pdf_text = session.get('pdf_text', '')

    if pdf_text:
        print(f"Question reçue : {message}")
        answer = ask_question_to_pdf(message, pdf_text)
        print(f"Réponse générée : {answer}")
    else:
        print("Aucun PDF n'a été téléchargé ou le texte n'a pas pu être extrait.")
        answer = "Aucun PDF n'a été téléchargé ou le texte n'a pas pu être extrait."
    
    return {"answer": answer}


if __name__ == "__main__":
    app.run(debug=True)
