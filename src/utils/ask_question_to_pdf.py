from io import StringIO
import os
import fitz
import openai
from dotenv import load_dotenv
from nltk.tokenize import sent_tokenize
from openai import OpenAI
from flask import session

client = OpenAI()

def gpt3_completion(question, texte):
    # Check if the session context exists
    if "context" not in session:
        # If it doesn't exist, initialize it with an empty string
        session["context"] = ""

    # Append the current conversation to the session context
    session["context"] += "User Question: " + question + "\n"
    session["context"] += "Course Text: " + texte + "\n"

    # Send the conversation to the GPT-3 API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": session["context"]}] + [{"role": "user", "content": question}]
    )

    # Update the session context with the AI's response
    session["context"] += "AI Response: " + response.choices[0].message.content + "\n"

    # Return the AI's response
    return response.choices[0].message.content


load_dotenv()

def open_file(filepath):
    with open(filepath, "r", encoding="utf-8") as infile:
        return infile.read()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")

def read_pdf(filename):
    context = ""

    # Open the PDF file
    with fitz.open(filename) as pdf_file:
        # Get the number of pages in the PDF file
        num_pages = pdf_file.page_count

        # Loop through each page in the PDF file
        for page_num in range(num_pages):
            # Get the current page
            page = pdf_file[page_num]

            # Get the text from the current page
            page_text = page.get_text().replace("\n", "")

            # Append the text to context
            context += page_text
    return context

def split_text(text, chunk_size=5000):
    chunks = []
    current_chunk = StringIO()
    current_size = 0
    sentences = sent_tokenize(text)
    for sentence in sentences:
        sentence_size = len(sentence)
        if sentence_size > chunk_size:
            while sentence_size > chunk_size:
                chunk = sentence[:chunk_size]
                chunks.append(chunk)
                sentence = sentence[chunk_size:]
                sentence_size -= chunk_size
                current_chunk = StringIO()
                current_size = 0
        if current_size + sentence_size < chunk_size:
            current_chunk.write(sentence)
            current_size += sentence_size
        else:
            chunks.append(current_chunk.getvalue())
            current_chunk = StringIO()
            current_chunk.write(sentence)
            current_size = sentence_size
    if current_chunk:
        chunks.append(current_chunk.getvalue())
    return chunks

def ask_question_to_pdf(question, texte):
    return gpt3_completion(question, texte)