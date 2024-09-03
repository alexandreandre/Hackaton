from flask import Flask
from flask import render_template
from flask import request
from src.utils.ask_question_to_pdf import ask_question_to_pdf

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route('/prompt', methods=['POST'])
def prompt():
    message = request.form['prompt']
    return{"answer" : ask_question_to_pdf(message)}

# @app.route("/")
# def hello_world():
#     print("aaa")