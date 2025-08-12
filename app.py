from flask import Flask, render_template, request, jsonify
import os
import fitz  # PyMuPDF
import nltk

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

pdf_text_store = ""  # Store extracted text globally for now
sentences_store = []  # Store sentences of the PDF text

# Download punkt tokenizer if not already present
nltk.download('punkt')

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def split_text_into_sentences(text):
    return nltk.sent_tokenize(text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global pdf_text_store, sentences_store
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Extract and store PDF text and sentences
    pdf_text_store = extract_text_from_pdf(file_path)
    sentences_store = split_text_into_sentences(pdf_text_store)

    return jsonify({'message': f"File '{file.filename}' uploaded and processed successfully!"})

@app.route('/ask', methods=['POST'])
def ask_question():
    global sentences_store
    question = request.json.get('question', '').lower()

    if not sentences_store:
        return jsonify({'answer': "No PDF uploaded yet."})

    keywords = question.split()

    # Find sentences containing any keyword
    matches = [sentence for sentence in sentences_store if any(k in sentence.lower() for k in keywords)]

    if matches:
        # Return top 3 matching sentences joined as answer
        return jsonify({'answer': " ".join(matches[:3])})
    else:
        return jsonify({'answer': "Sorry, I couldn't find anything related to that question."})

if __name__ == '__main__':
    app.run(debug=True)
